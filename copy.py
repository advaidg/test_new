import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

# Python 2 compatibility
try:
    input = raw_input
except NameError:
    pass

def copy_file(file_name, source_dir, dest_dir):
    try:
        file_name = file_name.strip().replace(",", "")
        source_path = os.path.join(source_dir, file_name)
        dest_path = os.path.join(dest_dir, file_name)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            print("Copied {} to {}".format(file_name, dest_dir))
        else:
            print("File {} not found in {}".format(file_name, source_dir))
    except Exception as e:
        print("Error copying {}: {}".format(file_name, str(e)))

def copy_files(source_dir, dest_dir, filename_list, num_workers=8):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    try:
        with open(filename_list, 'r') as f:
            files = f.readlines()
    except IOError:
        print("File {} not found.".format(filename_list))
        return
    except Exception as e:
        print("Error reading file list: {}".format(str(e)))
        return

    # Python 2 does not support ThreadPoolExecutor directly, use a workaround
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
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
