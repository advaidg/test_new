import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import sys

def copy_file(file_name, source_dir, dest_dir):
    try:
        file_name = file_name.strip().replace(",", "")
        source_path = os.path.join(source_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            print(f"Copied {file_name} to {dest_dir}")
        else:
            print(f"File {file_name} not found in {source_dir}")
    except Exception as e:
        print(f"Error copying {file_name}: {e}")

def copy_files(source_dir, dest_dir, filename_list, num_workers=8):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    try:
        with open(filename_list, 'r', encoding='utf-8') as f:
            files = f.readlines()
    except FileNotFoundError:
        print(f"File {filename_list} not found.")
        return
    except Exception as e:
        print(f"Error reading file list: {e}")
        return

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for file_name in files:
            executor.submit(copy_file, file_name, source_dir, dest_dir)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py <source_dir> <dest_dir> <filename_list>")
        sys.exit(1)

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    filename_list = sys.argv[3]

    copy_files(source_dir, dest_dir, filename_list, num_workers=8)
