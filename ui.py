import streamlit as st
import os
import json

st.title("Lambda Automation With Config (LAWC) UI")

st.markdown("""
This tool automatically configures your Lambda function template by replacing placeholders with actual values provided in your JSON configuration.
""")

# Input fields for absolute paths and JSON configuration.
template_path = st.text_input("Enter the absolute path to the template Lambda function folder:")
destination_path = st.text_input("Enter the absolute path to the destination folder:")
json_config = st.text_area("Paste your JSON configuration here:", height=300)

# Button to trigger the automation.
if st.button("Configure Lambda Function"):
    try:
        # Validate template folder.
        if not os.path.isdir(template_path):
            raise Exception("Error: Template folder not found.")
        if not any(os.scandir(template_path)):
            raise Exception("Error: Template folder is empty.")

        # Validate and parse JSON configuration.
        try:
            config = json.loads(json_config)
        except Exception as e:
            raise Exception("Error: Invalid JSON configuration. " + str(e))

        # Validate destination folder (create if it doesn't exist).
        if not os.path.exists(destination_path):
            try:
                os.makedirs(destination_path)
            except Exception as e:
                raise Exception("Error: Could not create destination folder. " + str(e))
        elif not os.path.isdir(destination_path):
            raise Exception("Error: Destination path is not a folder.")

        # Extract file name mapping if it exists and remove it from the config.
        file_name_maps = {}
        special_key = "file_name_maps (Special Property)"
        if special_key in config:
            if isinstance(config[special_key], dict):
                file_name_maps = config[special_key]
            del config[special_key]

        # Process each file in the template folder recursively.
        for root, dirs, files in os.walk(template_path):
            # Determine relative directory.
            rel_dir = os.path.relpath(root, template_path)
            if rel_dir == ".":
                rel_dir = ""
            dest_dir = os.path.join(destination_path, rel_dir)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for file in files:
                src_file_path = os.path.join(root, file)
                # Read the file as text.
                try:
                    with open(src_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    st.warning(f"Warning: Could not read file {src_file_path} as text. Skipping. Error: {str(e)}")
                    continue

                # Replace all placeholders with corresponding values from the JSON config.
                for placeholder, replacement in config.items():
                    # Ensure the replacement is a string.
                    content = content.replace(placeholder, str(replacement))

                # Determine new file name based on the mapping (if provided).
                rel_file_path = os.path.join(rel_dir, file) if rel_dir else file
                new_file_rel_path = file_name_maps.get(rel_file_path)
                if new_file_rel_path:
                    new_file_path = os.path.join(destination_path, new_file_rel_path)
                    new_file_dir = os.path.dirname(new_file_path)
                    if not os.path.exists(new_file_dir):
                        os.makedirs(new_file_dir)
                else:
                    new_file_path = os.path.join(dest_dir, file)

                # Write the modified content to the destination file.
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        st.success("Lambda function configured successfully.")
    except Exception as err:
        st.error(str(err))
