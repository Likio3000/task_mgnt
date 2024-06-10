import os
import pyperclip

def scrape_files_to_clipboard(directory):
    content = ""
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                content += f"### {filename}\n"
                with open(file_path, 'r') as file:
                    content += file.read()
                content += "\n\n"
    pyperclip.copy(content)
    print("Project contents copied to clipboard.")

if __name__ == "__main__":
    target_directory = os.getcwd()  # Use the current working directory
    scrape_files_to_clipboard(target_directory)
