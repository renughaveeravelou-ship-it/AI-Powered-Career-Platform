import os
import emoji

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find all emojis in the text.
    emojis_list = [c["emoji"] for c in emoji.emoji_list(content)]
    
    # Now we replace each emoji + space, or space + emoji, or just emoji
    # We sort by length descending to replace longer emoji sequences first (e.g. ones with ZWJ)
    for emj in sorted(set(emojis_list), key=len, reverse=True):
        content = content.replace(emj + '', '')
        content = content.replace(''+ emj, '')
        content = content.replace(emj, '')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for root, dirs, files in os.walk('.'):
    if '.git'in root or '.venv'in root or 'venv'in root or '.streamlit'in root:
        continue
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            clean_file(filepath)
            print(f"Cleaned {filepath}")
