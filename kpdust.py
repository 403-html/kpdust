#!/usr/bin/env python3
import pykeepass
import os
import sys
import getpass
import argparse
from tabulate import tabulate

def human_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0 or unit == 'GB':
            break
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} {unit}"

def analyze_kdbx(file_path, password, show_count=10, min_size=0):
    try:
        kp = pykeepass.PyKeePass(file_path, password=password)
        entries = kp.entries
        
        entry_data = []
        for entry in entries:
            attachments_size = 0
            attachment_names = []
            
            if entry.attachments:
                for attachment in entry.attachments:
                    size = len(attachment.data)
                    attachments_size += size
                    attachment_names.append(f"{attachment.filename} ({human_size(size)})")
            
            if attachments_size > min_size:
                entry_data.append({
                    'title': entry.title,
                    'group': entry.group.name if entry.group else "Root",
                    'attachments_size': attachments_size,
                    'attachment_count': len(entry.attachments) if entry.attachments else 0,
                    'attachment_names': attachment_names
                })
        
        entry_data.sort(key=lambda x: x['attachments_size'], reverse=True)
        
        table_data = []
        for entry in entry_data[:show_count]:
            table_data.append([
                human_size(entry['attachments_size']),
                f"{entry['attachment_count']}",
                entry['title'],
                entry['group'],
                ", ".join(entry['attachment_names'])
            ])
        
        total_db_size = os.path.getsize(file_path)
        total_attachments_size = sum(entry['attachments_size'] for entry in entry_data)
        
        print(f"KeePass DB: {os.path.basename(file_path)} ({human_size(total_db_size)})")
        print(f"Total entries with attachments: {len(entry_data)}")
        print(f"Total attachment size: {human_size(total_attachments_size)}")
        
        if table_data:
            headers = ["Size", "Count", "Entry", "Group", "Attachments"]
            print("\n" + tabulate(table_data, headers=headers, tablefmt="simple"))
        else:
            print("\nNo attachments found.")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Analyze storage usage in KeePass KDBX files")
    parser.add_argument("file", help="Path to the KDBX file")
    parser.add_argument("-n", "--entries", type=int, default=10, 
                      help="Number of entries to show (default: 10)")
    parser.add_argument("-m", "--min-size", type=str, default="0",
                      help="Minimum attachment size to display (e.g. '100KB', default: 0)")
    parser.add_argument("-p", "--password", help="Master password (omit to be prompted)")
    
    args = parser.parse_args()
    
    min_size = args.min_size
    if min_size[-2:].upper() == 'KB':
        min_bytes = int(min_size[:-2]) * 1024
    elif min_size[-2:].upper() == 'MB':
        min_bytes = int(min_size[:-2]) * 1024 * 1024
    elif min_size[-2:].upper() == 'GB':
        min_bytes = int(min_size[:-2]) * 1024 * 1024 * 1024
    else:
        min_bytes = int(min_size)
    
    password = args.password
    if not password:
        password = getpass.getpass("Enter master password: ")
    
    if not analyze_kdbx(args.file, password, args.entries, min_bytes):
        sys.exit(1)

if __name__ == "__main__":
    main()