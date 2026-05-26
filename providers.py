"""
providers.py — All AI API Providers
Supports: OpenRouter, NVIDIA Build, OpenAI, Anthropic, Google Gemini, Groq, Mistral, DeepSeek,
          Together AI, xAI Grok, Perplexity, Cohere, HuggingFace, Ollama, LM Studio
"""

import requests

# ─────────────────────────────────────────────────────────
# PROVIDER DEFINITIONS
# ─────────────────────────────────────────────────────────

PROVIDERS = {

    # ═══════════════════════════════════════════
    # OPENROUTER  (aggregates ALL providers)
    # ═══════════════════════════════════════════
    "OpenRouter": {
        "description": "Access 200+ models via one API key — Free & Paid",
        "get_key_url": "https://openrouter.ai/keys",
        "free_tier": "20 req/min · 200 req/day — No credit card",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-or-v1-...",
        "free_models": {
            "Auto Router ★ BEST — Never 404":                   "openrouter/free",
            "Llama 3.3 70B — Most Reliable":                    "meta-llama/llama-3.3-70b-instruct:free",
            "OpenAI GPT-OSS 120B — OpenAI Free":                "openai/gpt-oss-120b:free",
            "Qwen3 Coder 480B — Best for Tech":                 "qwen/qwen3-coder:free",
            "Qwen3 Next 80B — Latest Qwen":                     "qwen/qwen3-next-80b-a3b-instruct:free",
            "NVIDIA Nemotron 30B — MoE Powerful":               "nvidia/nemotron-3-nano-30b-a3b:free",
            "NVIDIA Nemotron 9B — Fast":                        "nvidia/nemotron-nano-9b-v2:free",
            "Gemma 3 27B — Best Google Free":                   "google/gemma-3-27b-it:free",
            "Gemma 3 12B — Google Balanced":                    "google/gemma-3-12b-it:free",
            "Mistral Small 3.1 24B — Fast":                     "mistralai/mistral-small-3.1-24b-instruct:free",
            "OpenAI GPT-OSS 20B — Light":                      "openai/gpt-oss-20b:free",
            "Llama 3.2 3B — Ultra Fast":                        "meta-llama/llama-3.2-3b-instruct:free",
            "StepFun Step 3.5 Flash — 256K Context":            "stepfun/step-3.5-flash:free",
            "Z.AI GLM 4.5 Air — Agent Model":                   "z-ai/glm-4.5-air:free",
            "Arcee Trinity Large — 400B MoE":                   "arcee-ai/trinity-large-preview:free",
            "Arcee Trinity Mini — Efficient":                   "arcee-ai/trinity-mini:free",
            "Solar Pro 3 — Upstage 102B":                       "upstage/solar-pro-3:free",
        },
        "paid_models": {
            "Claude 3.5 Sonnet — Best Overall":                  "anthropic/claude-3.5-sonnet",
            "Claude 3.5 Haiku — Fastest Claude":                 "anthropic/claude-3.5-haiku",
            "GPT-4o — Top Tier OpenAI":                         "openai/gpt-4o",
            "GPT-4o Mini — Fast & Cheap":                       "openai/gpt-4o-mini",
            "Gemini 2.0 Flash — Fast Google":                   "google/gemini-2.0-flash-001",
            "DeepSeek R1 — Best Reasoning":                     "deepseek/deepseek-r1",
            "DeepSeek Chat — Low Cost":                         "deepseek/deepseek-chat",
            "Mistral Large — Powerful":                          "mistralai/mistral-large",
            "Qwen3 235B — Best Open Source":                    "qwen/qwen3-235b-a22b",
        },
        "headers_extra": {
            "HTTP-Referer": "https://ai-career-suite.streamlit.app",
            "X-Title": "AI Career Suite"
        }
    },

    # ═══════════════════════════════════════════
    # NVIDIA BUILD  (NIM — Free API credits)
    # ═══════════════════════════════════════════
    "NVIDIA Build": {
        "description": "NVIDIA NIM — Gemma 4, Llama, Nemotron. 1000 free credits!",
        "get_key_url": "https://build.nvidia.com/explore/discover",
        "free_tier": "1000 free API credits on signup — No credit card",
        "endpoint": "https://integrate.api.nvidia.com/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "nvapi-...",
        "free_models": {
            "Gemma 4 31B IT ★ NEW — Google Frontier":           "google/gemma-4-31b-it",
            "Llama 3.3 70B — Meta's Best Open":                 "meta/llama-3.3-70b-instruct",
            "Llama 3.1 8B — Ultra Fast":                        "meta/llama-3.1-8b-instruct",
            "Llama 3.2 3B — Lightweight & Fast":                "meta/llama-3.2-3b-instruct",
            "Llama 3.2 11B Vision — Fast Multimodal":           "meta/llama-3.2-11b-vision-instruct",
            "Llama 3.2 90B Vision — Frontier Vision":           "meta/llama-3.2-90b-vision-instruct",
            "Nemotron 70B — NVIDIA Flagship Reward":            "nvidia/llama-3.1-nemotron-70b-instruct",
            "Phi-3 Mini 128K — Microsoft Small Model":          "microsoft/phi-3-mini-128k-instruct",
            "Mistral 7B — Fast & Light European":               "mistralai/mistral-7b-instruct-v0.3",
            "Mixtral 8x22B — Massive MoE":                      "mistralai/mixtral-8x22b-instruct-v0.1",
            "DeepSeek R1 — Elite Reasoning Model":              "deepseek-ai/deepseek-r1",
            "CodeGemma 7B — Google Coding Model":               "google/codegemma-1.1-7b",
            "Qwen 2.5 72B — Alibaba Frontier":                  "qwen/qwen2.5-72b-instruct",
        },
        "paid_models": {},
        "headers_extra": {}
    },

    # ═══════════════════════════════════════════
    # OPENAI  (GPT models)
    # ═══════════════════════════════════════════
    "OpenAI": {
        "description": "Official OpenAI API — GPT-4o, GPT-4o Mini",
        "get_key_url": "https://platform.openai.com/api-keys",
        "free_tier": "No free tier — ~$5 free credits for new accounts",
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-proj-...",
        "free_models": {},
        "paid_models": {
            "GPT-4o — Most Capable (~$2.5/$10 per M)":          "gpt-4o",
            "GPT-4o Mini — Fast & Cheap (~$0.15/$0.6 per M)":   "gpt-4o-mini",
            "GPT-4 Turbo — Reliable (~$10/$30 per M)":          "gpt-4-turbo",
            "o1 Mini — Reasoning Model (~$1.1/$4.4 per M)":     "o1-mini",
            "GPT-3.5 Turbo — Budget (~$0.5/$1.5 per M)":        "gpt-3.5-turbo",
        },
    },

    # ═══════════════════════════════════════════
    # ANTHROPIC  (Claude models)
    # ═══════════════════════════════════════════
    "Anthropic (Claude)": {
        "description": "Official Claude API — Best for writing & analysis",
        "get_key_url": "https://console.anthropic.com/",
        "free_tier": "No free tier — pay per use",
        "endpoint": "https://api.anthropic.com/v1/messages",
        "type": "anthropic",
        "placeholder": "sk-ant-api03-...",
        "free_models": {},
        "paid_models": {
            "Claude 3.5 Sonnet — Best Overall (~$3/$15 per M)":  "claude-3-5-sonnet-20241022",
            "Claude 3.5 Haiku — Fastest (~$0.8/$4 per M)":      "claude-3-5-haiku-20241022",
            "Claude 3 Opus — Most Powerful (~$15/$75 per M)":    "claude-3-opus-20240229",
            "Claude 3 Haiku — Budget (~$0.25/$1.25 per M)":      "claude-3-haiku-20240307",
        },
    },

    # ═══════════════════════════════════════════
    # GOOGLE GEMINI
    # ═══════════════════════════════════════════
    "Google Gemini": {
        "description": "Official Gemini API — Free tier available!",
        "get_key_url": "https://aistudio.google.com/app/apikey",
        "free_tier": "Free: 15 req/min · 1M tokens/day — No credit card",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
        "type": "gemini",
        "placeholder": "AIza...",
        "free_models": {
            "Gemini 2.0 Flash — FREE Fast & Smart":              "gemini-2.0-flash",
            "Gemini 1.5 Flash — FREE Reliable":                  "gemini-1.5-flash",
            "Gemini 1.5 Flash 8B — FREE Ultra Fast":             "gemini-1.5-flash-8b",
        },
        "paid_models": {
            "Gemini 1.5 Pro — Long Context (~$1.25/$5 per M)":  "gemini-1.5-pro",
            "Gemini 2.0 Flash Thinking — Reasoning":             "gemini-2.0-flash-thinking-exp",
        },
    },

    # ═══════════════════════════════════════════
    # GROQ  (Ultra-fast inference, free tier)
    # ═══════════════════════════════════════════
    "Groq": {
        "description": "Ultra-fast inference — 10x faster than others, Free tier!",
        "get_key_url": "https://console.groq.com/keys",
        "free_tier": "Free: 30 req/min · 14,400 req/day — No credit card",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "gsk_...",
        "free_models": {
            "Llama 3.3 70B — FREE Best Quality":                 "llama-3.3-70b-versatile",
            "Llama 3.1 8B — FREE Ultra Fast":                    "llama-3.1-8b-instant",
            "Gemma2 9B — FREE Google Model":                     "gemma2-9b-it",
            "Mixtral 8x7B — FREE MoE Model":                     "mixtral-8x7b-32768",
            "Llama 3.2 90B Vision — FREE Multimodal":            "llama-3.2-90b-vision-preview",
            "Llama 3.2 11B Vision — FREE Fast Vision":           "llama-3.2-11b-vision-preview",
            "DeepSeek R1 — FREE Reasoning":                      "deepseek-r1-distill-llama-70b",
        },
        "paid_models": {
            "Llama 3.1 70B — Paid Higher Limits":                "llama-3.1-70b-versatile",
        },
    },

    # ═══════════════════════════════════════════
    # DEEPSEEK  (Best value, dirt cheap)
    # ═══════════════════════════════════════════
    "DeepSeek": {
        "description": "Best value AI — R1 reasoning & V3 chat, very cheap",
        "get_key_url": "https://platform.deepseek.com/api_keys",
        "free_tier": "~$5 free credits for new accounts",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "sk-...",
        "free_models": {},
        "paid_models": {
            "DeepSeek R1 — Best Reasoning (~$0.55/$2.19 per M)": "deepseek-reasoner",
            "DeepSeek V3 — Great Chat (~$0.27/$1.1 per M)":      "deepseek-chat",
        },
    },

    # ═══════════════════════════════════════════
    # MISTRAL AI  (European AI, free tier)
    # ═══════════════════════════════════════════
    "Mistral AI": {
        "description": "European AI — Fast models, free trial available",
        "get_key_url": "https://console.mistral.ai/api-keys/",
        "free_tier": "Free trial credits available",
        "endpoint": "https://api.mistral.ai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "...",
        "free_models": {},
        "paid_models": {
            "Mistral Large — Most Powerful (~$2/$6 per M)":       "mistral-large-latest",
            "Mistral Small — Fast (~$0.1/$0.3 per M)":           "mistral-small-latest",
            "Mistral Nemo — Lightweight (~$0.15/$0.15 per M)":   "open-mistral-nemo",
            "Codestral — Best for Code (~$0.3/$0.9 per M)":      "codestral-latest",
        },
    },

    # ═══════════════════════════════════════════
    # TOGETHER AI  (Open source models, cheap)
    # ═══════════════════════════════════════════
    "Together AI": {
        "description": "Run open-source models — $25 free credits!",
        "get_key_url": "https://api.together.xyz/settings/api-keys",
        "free_tier": "$25 free credits on signup — No credit card",
        "endpoint": "https://api.together.xyz/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "...",
        "free_models": {},
        "paid_models": {
            "Llama 3.3 70B — Best Quality (~$0.88 per M)":       "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            "Llama 3.2 3B — Ultra Cheap (~$0.06 per M)":         "meta-llama/Llama-3.2-3B-Instruct-Turbo",
            "Qwen 2.5 72B — Great (~$1.2 per M)":               "Qwen/Qwen2.5-72B-Instruct-Turbo",
            "DeepSeek R1 — Reasoning (~$2.19 per M)":            "deepseek-ai/DeepSeek-R1",
            "Mixtral 8x7B — Fast MoE (~$0.6 per M)":             "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "Gemma 2 27B — Google (~$0.8 per M)":               "google/gemma-2-27b-it",
        },
    },

    # ═══════════════════════════════════════════
    # PERPLEXITY  (with web search!)
    # ═══════════════════════════════════════════
    "Perplexity": {
        "description": "AI with real-time web search built in!",
        "get_key_url": "https://www.perplexity.ai/settings/api",
        "free_tier": "No free tier — pay per use (~$5 min)",
        "endpoint": "https://api.perplexity.ai/chat/completions",
        "type": "openai_compat",
        "placeholder": "pplx-...",
        "free_models": {},
        "paid_models": {
            "Sonar Pro — Best with Web Search (~$3/$15 per M)":  "sonar-pro",
            "Sonar — Fast with Web Search (~$1/$1 per M)":       "sonar",
            "Sonar Reasoning — Think + Search (~$1/$5 per M)":   "sonar-reasoning",
        },
    },

    # ═══════════════════════════════════════════
    # XAI GROK  (Elon's AI)
    # ═══════════════════════════════════════════
    "xAI Grok": {
        "description": "xAI's Grok — Real-time X/Twitter knowledge",
        "get_key_url": "https://console.x.ai/",
        "free_tier": "$25 free credits on signup",
        "endpoint": "https://api.x.ai/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "xai-...",
        "free_models": {},
        "paid_models": {
            "Grok 3 — Most Capable (~$3/$15 per M)":             "grok-3",
            "Grok 3 Mini — Fast Reasoning (~$0.3/$0.5 per M)":   "grok-3-mini",
            "Grok 2 — Stable (~$2/$10 per M)":                   "grok-2-1212",
        },
    },

    # ═══════════════════════════════════════════
    # COHERE  (Enterprise RAG, free tier)
    # ═══════════════════════════════════════════
    "Cohere": {
        "description": "Enterprise AI — Best for RAG & document analysis, Free!",
        "get_key_url": "https://dashboard.cohere.com/api-keys",
        "free_tier": "Free trial — 20 req/min · 1000 req/month",
        "endpoint": "https://api.cohere.ai/v2/chat",
        "type": "cohere",
        "placeholder": "...",
        "free_models": {
            "Command R — FREE Best for RAG":                     "command-r",
            "Command R7B — FREE Fast":                           "command-r7b-12-2024",
        },
        "paid_models": {
            "Command R+ — Best Quality (~$2.5/$10 per M)":       "command-r-plus",
            "Command Light — Ultra Fast (~$0.3/$0.6 per M)":     "command-light",
        },
    },

    # ═══════════════════════════════════════════
    # HUGGING FACE  (Open source, free)
    # ═══════════════════════════════════════════
    "Hugging Face": {
        "description": "Open source models — Serverless Inference API, Free!",
        "get_key_url": "https://huggingface.co/settings/tokens",
        "free_tier": "Free Inference API — Limited but no credit card",
        "endpoint": "https://api-inference.huggingface.co/models",
        "type": "huggingface",
        "placeholder": "hf_...",
        "free_models": {
            "Llama 3.1 8B — FREE Fast Meta Model":               "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "Gemma 2 9B — FREE Google Model":                    "google/gemma-2-9b-it",
            "Qwen 2.5 7B — FREE Qwen Model":                    "Qwen/Qwen2.5-7B-Instruct",
            "Mistral 7B — FREE Classic":                         "mistralai/Mistral-7B-Instruct-v0.3",
            "Phi 3.5 Mini — FREE Microsoft":                     "microsoft/Phi-3.5-mini-instruct",
        },
        "paid_models": {},
    },

    # ═══════════════════════════════════════════
    # OLLAMA  (Local LLM — runs on YOUR machine)
    # ═══════════════════════════════════════════
    "Ollama (Local)": {
        "description": "Run ANY model locally on your own machine — 100% private, 100% free, no internet needed",
        "get_key_url": "https://ollama.com/download",
        "free_tier": "Completely FREE — runs on your CPU/GPU, no API key needed",
        "endpoint": "http://localhost:11434/api/chat",
        "type": "ollama",
        "placeholder": "no key needed — leave blank",
        "local_only": True,
        "free_models": {
            "llama3.2 — Meta Llama 3.2 3B (2GB)":               "llama3.2",
            "llama3.1 — Meta Llama 3.1 8B (5GB)":               "llama3.1",
            "llama3.3 — Meta Llama 3.3 70B (43GB, needs 64GB RAM)": "llama3.3",
            "deepseek-r1:7b — DeepSeek R1 7B (4GB)":            "deepseek-r1:7b",
            "deepseek-r1:14b — DeepSeek R1 14B (9GB)":          "deepseek-r1:14b",
            "qwen2.5:7b — Qwen 2.5 7B (5GB)":                   "qwen2.5:7b",
            "qwen2.5:14b — Qwen 2.5 14B (9GB)":                 "qwen2.5:14b",
            "gemma3:4b — Google Gemma 3 4B (3GB)":              "gemma3:4b",
            "gemma3:12b — Google Gemma 3 12B (8GB)":            "gemma3:12b",
            "mistral — Mistral 7B (4GB)":                        "mistral",
            "mistral-nemo — Mistral Nemo 12B (7GB)":             "mistral-nemo",
            "phi4 — Microsoft Phi 4 14B (9GB)":                  "phi4",
            "phi3.5 — Microsoft Phi 3.5 3B (2GB, very fast)":   "phi3.5",
            "mixtral — Mixtral 8x7B MoE (26GB)":                "mixtral",
            "Custom model — type your own model name below":     "__custom__",
        },
        "paid_models": {},
    },

    # ═══════════════════════════════════════════
    # LM STUDIO  (Local GGUF — drag & drop any model)
    # ═══════════════════════════════════════════
    "LM Studio (Local)": {
        "description": "Load any GGUF model file locally — drag & drop interface, OpenAI-compatible server",
        "get_key_url": "https://lmstudio.ai/",
        "free_tier": "Completely FREE — use any GGUF from HuggingFace, no API key needed",
        "endpoint": "http://localhost:1234/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "lm-studio (no key needed — leave blank or type anything)",
        "local_only": True,
        "free_models": {
            "Currently Loaded Model — whatever is active in LM Studio": "local-model",
        },
        "paid_models": {},
        "headers_extra": {},
    },

    # ═══════════════════════════════════════════
    # LLAMA.CPP SERVER  (Advanced — run GGUF directly)
    # ═══════════════════════════════════════════
    "llama.cpp Server (Local)": {
        "description": "Advanced: run GGUF files directly with llama.cpp server — full control",
        "get_key_url": "https://github.com/ggerganov/llama.cpp",
        "free_tier": "Completely FREE — any GGUF model, maximum control",
        "endpoint": "http://localhost:8080/v1/chat/completions",
        "type": "openai_compat",
        "placeholder": "no key needed — leave blank",
        "local_only": True,
        "free_models": {
            "Active GGUF Model — whatever model you launched the server with": "gpt-3.5-turbo",
        },
        "paid_models": {},
        "headers_extra": {},
    },
}


def get_all_models_for_provider(provider_name: str):
    """Return (free_models_dict, paid_models_dict) for a provider."""
    p = PROVIDERS.get(provider_name, {})
    return p.get("free_models", {}), p.get("paid_models", {})


def call_api(provider_name: str, api_key: str, model_id: str,
             prompt: str, temperature: float = 0.7, max_tokens: int = 2500) -> str:
    """Universal API caller — handles all provider formats."""
    p = PROVIDERS[provider_name]
    ptype = p["type"]

    # ── OpenAI-Compatible (OpenRouter, NVIDIA, Groq, DeepSeek, Mistral, Together, Perplexity, xAI) ──
    if ptype == "openai_compat":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        # Extra headers for OpenRouter
        if "headers_extra"in p:
            headers.update(p["headers_extra"])

        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["choices"][0]["message"]["content"].strip()

    # ── Anthropic Claude ──
    elif ptype == "anthropic":
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_id,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["content"][0]["text"].strip()

    # ── Google Gemini ──
    elif ptype == "gemini":
        url = f"{p['endpoint']}/{model_id}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperature},
        }
        r = requests.post(url, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # ── Cohere ──
    elif ptype == "cohere":
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        r = requests.post(p["endpoint"], headers=headers, json=payload, timeout=90)
        _check_errors(r, provider_name)
        return r.json()["message"]["content"][0]["text"].strip()

    # ── Hugging Face Inference API ──
    elif ptype == "huggingface":
        url = f"{p['endpoint']}/{model_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": temperature, "return_full_text": False},
        }
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        _check_errors(r, provider_name)
        result = r.json()
        if isinstance(result, list):
            return result[0].get("generated_text", "").strip()
        return str(result)

    # ── Ollama Local Server ──
    elif ptype == "ollama":
        return _call_ollama(p["endpoint"], model_id, prompt, temperature, max_tokens)

    raise ValueError(f"Unknown provider type: {ptype}")


def _call_ollama(endpoint: str, model_id: str, prompt: str,
                 temperature: float, max_tokens: int) -> str:
    """Call Ollama local server — handles streaming and non-streaming."""
    # Test if Ollama is running first
    try:
        requests.get("http://localhost:11434/api/tags", timeout=3)
    except requests.exceptions.ConnectionError:
        raise ValueError(
            "Ollama is not running on your machine!\n\n"
            "To start Ollama:\n"
            "① Download Ollama from ollama.com/download\n"
            "② Install it (Mac/Windows/Linux)\n"
            "③ Open Terminal → run: ollama serve\n"
            "④ Pull a model: ollama pull llama3.2\n"
            "⑤ Come back and try again!\n\n"
            "Note: This only works when running the app LOCALLY (not on Streamlit Cloud)"
        )
    except Exception:
        pass

    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        }
    }
    try:
        r = requests.post(endpoint, json=payload, timeout=300)
    except requests.exceptions.ConnectionError:
        raise ValueError(
            "Cannot connect to Ollama at localhost:11434\n"
            "Make sure Ollama is running: open Terminal and run 'ollama serve'"
        )

    if r.status_code == 404:
        raise ValueError(
            f"Model '{model_id}'not found in Ollama.\n\n"
            f"Pull it first — open Terminal and run:\n"
            f" ollama pull {model_id}\n\n"
            f"See all available models at: ollama.com/library"
        )
    if r.status_code != 200:
        raise ValueError(f"Ollama error {r.status_code}: {r.text[:200]}")

    data = r.json()
    # Ollama /api/chat response format
    return data.get("message", {}).get("content", "").strip()


def _check_errors(r, provider_name: str):
    """Unified error handler — clear actionable messages for every error type."""
    if r.status_code == 200:
        return

    # Try to extract error message from response body
    raw_msg = ""
    try:
        err = r.json()
        raw_msg = (
            err.get("error", {}).get("message", "")
            or err.get("message", "")
            or err.get("detail", "")
            or str(err)
        )
    except Exception:
        raw_msg = r.text[:300]

    p = PROVIDERS.get(provider_name, {})
    key_url = p.get("get_key_url", "")

    if r.status_code == 401:
        raise ValueError(
            f"Invalid API key for {provider_name}.\n\n"
            "Most likely causes:\n"
            "• You copied the key with extra spaces — paste it again carefully\n"
            "• The key was deleted or reset in your provider dashboard\n"
            "• You're using the wrong key for this provider\n\n"
            f"Get/check your key at: {key_url}"
        )

    elif r.status_code == 402:
        raise ValueError(
            f"No credits remaining for {provider_name}.\n\n"
            "Options:\n"
            "• Switch to a FREE provider — OpenRouter, Groq, NVIDIA Build, or Google Gemini\n"
            "• Add more credits at your provider dashboard\n\n"
            f"Add credits at: {key_url}"
        )

    elif r.status_code == 403:
        raise ValueError(
            f"Access forbidden (403) on {provider_name}.\n\n"
            "This usually means:\n"
            "• Your API key doesn't have permission for this model\n"
            "• Free tier doesn't allow this model — switch to a free model\n"
            "• For OpenRouter: enable 'Allow free model usage'at openrouter.ai/settings/privacy"
        )

    elif r.status_code == 404:
        raise ValueError(
            f"Model not found (404) on {provider_name}.\n\n"
            "This model was removed or renamed.\n\n"
            "Fix: Switch to a different model in the sidebar.\n"
            "If using OpenRouter → use 'Auto Free Router'— it NEVER gives 404 errors!"
        )

    elif r.status_code == 429:
        free_tier = p.get("free_tier", "")
        if provider_name == "OpenRouter":
            raise ValueError(
                "OpenRouter rate limit hit (free tier: 20 req/min · 200 req/day).\n\n"
                "Quick fixes — pick one:\n"
                "① Wait 60 seconds and try again\n"
                "② Switch model to 'Auto Free Router'(spreads load automatically)\n"
                "③ Switch provider to Groq (30 req/min free, much higher limits)\n"
                "④ Switch provider to NVIDIA Build (1000 free credits!)\n"
                "⑤ Switch provider to Google Gemini (1 million tokens/day free!)\n\n"
                "Best practice: use Groq for speed, NVIDIA for quality, OpenRouter as backup"
            )
        else:
            raise ValueError(
                f"Rate limit hit on {provider_name}.\n"
                f"Limit: {free_tier}\n\n"
                "Quick fixes:\n"
                "① Wait 60 seconds and retry\n"
                "② Switch to a different model in sidebar\n"
                "③ Switch to Groq, NVIDIA Build, or Google Gemini (all have generous free limits)"
            )

    elif r.status_code == 500:
        raise ValueError(
            f"{provider_name} server error (500) — their servers are having issues.\n\n"
            "This is not your fault. Try:\n"
            "• Wait 30 seconds and retry\n"
            "• Switch to a different provider (Groq is almost always up)"
        )

    elif r.status_code == 503:
        if provider_name == "Hugging Face":
            raise ValueError(
                "Model is loading on Hugging Face (503 — cold start).\n\n"
                "This is normal! The model needs ~30 seconds to wake up.\n"
                "Wait 30 seconds → click the button again → it will work!"
            )
        raise ValueError(
            f"{provider_name} is temporarily unavailable (503).\n"
            "Wait 30 seconds and try again, or switch to Groq."
        )

    else:
        raise ValueError(
            f"API error {r.status_code} from {provider_name}.\n"
            f"Details: {raw_msg[:200]}\n\n"
            "Try switching to a different model or provider."
        )