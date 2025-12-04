import re
import os

path = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\templates\core\home.html"

if not os.path.exists(path):
    print(f"File not found: {path}")
    exit(1)

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Function to condense whitespace in the captured group
def repl(match):
    # match.group(0) is the whole tag
    # match.group(1) is the content inside quotes
    text = match.group(1)
    # Replace newlines and multiple spaces with a single space
    clean_text = ' '.join(text.split())
    return f'{{% trans "{clean_text}" %}}'

# Regex to find {% trans "..." %} tags, allowing for multi-line content inside quotes
# We use non-greedy match for the content inside quotes
pattern = r'\{% trans "([^"]+)" %\}'

new_content = re.sub(pattern, repl, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed home.html")
