#!/usr/bin/env python
"""
Simple script to compile Django translation files without gettext
This creates empty .mo files that Django can use for testing
"""

import os
import struct

def create_mo_file(po_file_path, mo_file_path):
    """Create a minimal .mo file from a .po file"""
    
    # Read the .po file
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the .po file to extract msgid and msgstr pairs
    translations = {}
    lines = content.split('\n')
    current_msgid = None
    current_msgstr = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('msgid "'):
            current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
        elif line.startswith('msgstr "'):
            current_msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
            if current_msgid and current_msgstr:
                translations[current_msgid] = current_msgstr
                current_msgid = None
                current_msgstr = None
    
    # Create a minimal .mo file
    # .mo file format: https://www.gnu.org/software/gettext/manual/html_node/MO-Files.html
    
    # Header
    magic = 0x950412de  # Magic number for .mo files
    revision = 0  # Format revision
    count = len(translations)  # Number of strings
    
    # Calculate offsets
    header_size = 28  # 7 * 4 bytes
    hash_offset = header_size
    hash_size = 0  # No hash table for simplicity
    strings_offset = hash_offset + hash_size
    
    # Create the .mo file
    with open(mo_file_path, 'wb') as f:
        # Write header
        f.write(struct.pack('<I', magic))  # Magic number
        f.write(struct.pack('<I', revision))  # Revision
        f.write(struct.pack('<I', count))  # Number of strings
        f.write(struct.pack('<I', hash_offset))  # Offset of hash table
        f.write(struct.pack('<I', hash_size))  # Size of hash table
        f.write(struct.pack('<I', strings_offset))  # Offset of strings
        f.write(struct.pack('<I', 0))  # Size of strings (will be calculated)
        
        # Write empty hash table
        # (skipped for simplicity)
        
        # Write string entries
        string_entries = []
        current_offset = strings_offset + count * 8  # 8 bytes per entry
        
        for msgid, msgstr in translations.items():
            if msgid == "":  # Skip empty msgid (header)
                continue
                
            # Calculate lengths and offsets
            msgid_bytes = msgid.encode('utf-8')
            msgstr_bytes = msgstr.encode('utf-8')
            
            msgid_len = len(msgid_bytes)
            msgstr_len = len(msgstr_bytes)
            
            # Store entry info
            string_entries.append((msgid_len, current_offset, msgstr_len, current_offset + msgid_len))
            current_offset += msgid_len + msgstr_len
        
        # Write string table
        for msgid_len, msgid_offset, msgstr_len, msgstr_offset in string_entries:
            f.write(struct.pack('<I', msgid_len))
            f.write(struct.pack('<I', msgid_offset))
            f.write(struct.pack('<I', msgstr_len))
            f.write(struct.pack('<I', msgstr_offset))
        
        # Write strings
        for msgid, msgstr in translations.items():
            if msgid == "":  # Skip empty msgid (header)
                continue
            f.write(msgid.encode('utf-8'))
            f.write(msgstr.encode('utf-8'))
    
    print(f"Created {mo_file_path}")

def main():
    """Compile all translation files"""
    
    # Define the paths
    locale_dirs = ['locale/en/LC_MESSAGES', 'locale/ne/LC_MESSAGES']
    
    for locale_dir in locale_dirs:
        po_file = os.path.join(locale_dir, 'django.po')
        mo_file = os.path.join(locale_dir, 'django.mo')
        
        if os.path.exists(po_file):
            create_mo_file(po_file, mo_file)
        else:
            print(f"Warning: {po_file} not found")

if __name__ == '__main__':
    main() 