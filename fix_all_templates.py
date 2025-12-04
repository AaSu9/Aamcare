import os
import re

templates_dir = r"c:\Users\Dell\Desktop\Hackathon\Aamcare vaccine updated\core\templates\core"

def fix_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    modified = False
    
    # Replace custom_trans with i18n
    if 'load custom_trans' in content:
        content = content.replace('{% load custom_trans %}', '{% load i18n %}')
        modified = True
        print(f"  - Replaced custom_trans with i18n")
    
    # Check if template uses trans but doesn't have load i18n
    if '{% trans ' in content and '{% load i18n %}' not in content:
        # Insert after extends or at beginning
        extends_match = re.search(r"(\{% extends '[^']+' %\})\s*", content)
        if extends_match:
            insert_pos = extends_match.end()
            content = content[:insert_pos] + "\n{% load i18n %}\n" + content[insert_pos:]
        else:
            content = "{% load i18n %}\n" + content
        modified = True
        print(f"  - Added load i18n")
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process all templates
fixed_count = 0
for filename in os.listdir(templates_dir):
    if filename.endswith('.html'):
        filepath = os.path.join(templates_dir, filename)
        print(f"Processing: {filename}")
        if fix_template(filepath):
            fixed_count += 1
            print(f"  Fixed!")
        else:
            print(f"  No changes needed")

print(f"\nTotal files fixed: {fixed_count}")
