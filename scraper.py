import os
import pyperclip

def get_directory_structure(root_dir, exclude_dirs=None):
    """
    Create a nested dictionary that represents the folder structure of root_dir
    """
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git']

    dir_structure = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude specified directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        folder = os.path.relpath(dirpath, root_dir)
        subdir = dir_structure
        if folder != '.':
            for part in folder.split(os.sep):
                subdir = subdir.setdefault(part, {})
        subdir.update({filename: None for filename in filenames if not filename.startswith('.') and filename.endswith('.py')})
    return dir_structure

def dict_to_str(d, indent=0):
    """
    Convert the directory structure dictionary to a string for display
    """
    lines = []
    for key, value in d.items():
        lines.append('    ' * indent + str(key))
        if isinstance(value, dict):
            lines.extend(dict_to_str(value, indent + 1))
    return lines

def scrape_files_to_clipboard(directory):
    content = ""
    # Add the directory structure
    dir_structure = get_directory_structure(directory)
    content += "### Directory Structure\n"
    content += "\n".join(dict_to_str(dir_structure))
    content += "\n\n"

    # Add the content of each file
    for dirpath, dirnames, filenames in os.walk(directory):
        # Exclude specified directories
        dirnames[:] = [d for d in dirnames if d not in ['__pycache__', '.git']]
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                content += f"### {filename}\n"
                with open(file_path, 'r') as file:
                    content += file.read()
                content += "\n\n"
    pyperclip.copy(content)
    print("Project contents and directory structure copied to clipboard.")

if __name__ == "__main__":
    target_directory = os.getcwd()  # Use the current working directory
    scrape_files_to_clipboard(target_directory)
