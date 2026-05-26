import re

def fix_labels(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace empty labels with "Hidden Label"
    content = re.sub(r'st\.selectbox\(\s*\"\"', 'st.selectbox("Hidden Label"', content)
    content = re.sub(r'st\.text_input\(\s*\"\"', 'st.text_input("Hidden Label"', content)
    content = re.sub(r'st\.text_area\(\s*\"\"', 'st.text_area("Hidden Label"', content)
    content = re.sub(r'st\.radio\(\s*\"\"', 'st.radio("Hidden Label"', content)
    content = re.sub(r'st\.file_uploader\(\s*\"\"', 'st.file_uploader("Hidden Label"', content)
    content = re.sub(r'st\.select_slider\(\s*\"\"', 'st.select_slider("Hidden Label"', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_labels('app.py')
    fix_labels('AI-Career-Suite-main/app.py')
