import os
import emoji

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We will use emoji.replace_emoji directly, which is the most robust way.
    # It removes all emoji sequences.
    cleaned_content = emoji.replace_emoji(content, replace='')
    
    # We may be left with multiple spaces or spaces at the start of quotes.
    # We can clean up spaces at the start of string literals:
    # e.g., "Follow-Up"-> "Follow-Up"
    cleaned_content = cleaned_content.replace('\"', '\"').replace('\'', '\'')
    
    if content != cleaned_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Removed emojis from {filepath}")

for root, dirs, files in os.walk('.'):
    if '.git'in root or '.venv'in root or 'venv'in root or '.streamlit'in root:
        continue
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            clean_file(filepath)
