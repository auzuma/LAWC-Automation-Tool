import os
import json
import sys

def main():
    print("Welcome to LAWC – Auzuma Technologies's FIRST automation tool!")
    
    # Prompt user for required paths
    template_path = input("Enter the absolute path to the template Lambda function folder: ").strip()
    config_file_path = input("Enter the absolute path to the JSON configuration file: ").strip()
    destination_path = input("Enter the absolute path to the destination folder: ").strip()

    # Validate template folder
    if not os.path.isdir(template_path):
        print("Error: Template folder not found.")
        sys.exit(1)
    if not any(os.scandir(template_path)):
        print("Error: Template folder is empty.")
        sys.exit(1)

    # Validate and load JSON configuration file
    if not os.path.isfile(config_file_path):
        print("Error: JSON configuration file not found.")
        sys.exit(1)
    try:
        with open(config_file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print("Error: Invalid JSON configuration file. " + str(e))
        sys.exit(1)

    # Ensure destination folder exists (or create it)
    if not os.path.exists(destination_path):
        try:
            os.makedirs(destination_path)
        except Exception as e:
            print("Error: Could not create destination folder. " + str(e))
            sys.exit(1)
    elif not os.path.isdir(destination_path):
        print("Error: Destination path is not a folder.")
        sys.exit(1)

    # Extract file name mapping if it exists and remove it from config for content replacements
    file_name_maps = {}
    special_key = "file_name_maps (Special Property)"
    if special_key in config:
        if isinstance(config[special_key], dict):
            file_name_maps = config[special_key]
        del config[special_key]

    # Recursively process each file in the template folder
    for root, dirs, files in os.walk(template_path):
        # Determine the relative directory from the template root
        rel_dir = os.path.relpath(root, template_path)
        if rel_dir == ".":
            rel_dir = ""
        dest_dir = os.path.join(destination_path, rel_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for file in files:
            src_file_path = os.path.join(root, file)
            # Read the file as text
            try:
                with open(src_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Warning: Could not read file {src_file_path} as text. Skipping. Error: {str(e)}")
                continue

            # Replace all placeholders with corresponding values from the JSON config
            for placeholder, replacement in config.items():
                content = content.replace(placeholder, replacement)

            # Determine new file name based on the mapping (if provided)
            rel_file_path = os.path.join(rel_dir, file) if rel_dir else file
            new_file_rel_path = file_name_maps.get(rel_file_path)
            if new_file_rel_path:
                new_file_path = os.path.join(destination_path, new_file_rel_path)
                new_file_dir = os.path.dirname(new_file_path)
                if not os.path.exists(new_file_dir):
                    os.makedirs(new_file_dir)
            else:
                new_file_path = os.path.join(dest_dir, file)

            # Write the modified content to the destination file
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    print("Lambda function configured successfully.")

if __name__ == "__main__":
    main()
