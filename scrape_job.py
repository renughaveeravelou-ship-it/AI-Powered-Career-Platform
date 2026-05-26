import requests
from bs4 import BeautifulSoup
import re

def fetch_job_description(url: str) -> dict:
    """
    Fetches job details from a URL and returns a dict with title, company, and text.
    Optimized for LinkedIn, Greenhouse, Lever, and major career portals.
    """
    res = {"title": "", "company": "", "text": "Failed to extract text."}
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # ── 1. Scrape Title ──
        og_title = soup.find('meta', property='og:title')
        h1_tag = soup.find('h1')
        t_str = ""
        
        if og_title and og_title.get('content'):
            t_str = og_title.get('content')
        elif h1_tag:
            t_str = h1_tag.get_text(strip=True)
        elif soup.title:
            t_str = soup.title.string

        if t_str:
            # Clean title (Remove common suffixes)
            res["title"] = t_str.split('|')[0].split('-')[0].split('at ')[0].split('Job ')[0].strip()

        # ── 2. Scrape Company ──
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            res["company"] = og_site.get('content').replace("LinkedIn", "").strip()
        
        # Fallback heuristic for company
        if not res["company"] or res["company"].lower() == "linkedin":
            if t_str and 'at 'in t_str.lower():
                res["company"] = t_str.lower().split('at ')[1].split('|')[0].split('-')[0].strip().title()
            elif soup.title and 'hiring 'in soup.title.string.lower():
                res["company"] = soup.title.string.lower().split('hiring ')[0].strip().title()

        # ── 3. Scrape Job Description Text (Heuristic) ──
        # Try to find specific JD containers first
        jd_container = None
        for selector in ['div.description', 'div.job-description', 'section.description', 'div.content', 'div.details', 'div#job-details']:
            found = soup.select_one(selector)
            if found:
                jd_container = found
                break

        if jd_container:
            text_source = jd_container
        else:
            # Fallback: Remove noise and get body
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "button"]):
                element.extract()
            text_source = soup

        text = text_source.get_text(separator='', strip=True)
        text = re.sub(r'\s+', '', text)
        
        # Remove common "Apply Now", "Sign In", etc. noise
        noise_patterns = [r'Apply Now', r'Sign In', r'Join LinkedIn', r'Privacy Policy', r'Cookie Policy']
        for p in noise_patterns:
            text = re.sub(p, '', text, flags=re.IGNORECASE)

        if len(text) > 10000:
            text = text[:10000]
        
        res["text"] = text.strip()
        return res

    except Exception as e:
        res["text"] = f"Error: {str(e)}"
        return res
