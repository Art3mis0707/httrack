import os
import json

# Directories where your images and HTML files are stored
images_dir = 'C:\\Images\\Individual'
html_dir = 'C:\\Images\\HTML'

# JSON file to save the mapping
output_json_path = 'C:\\Images\\image_html_mapping.json'

def create_image_html_mapping(images_dir, html_dir, output_json_path):
    mapping = {}

    # List all image files
    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
    
    for image_file in image_files:
        # Construct HTML file name by replacing image extension with .txt
        base_name = os.path.splitext(image_file)[0]
        html_file_name = f'{base_name}.txt'
        
        # Construct full paths to the image and HTML files
        html_file_path = os.path.join(html_dir, html_file_name)
        
        # Read the HTML code from the file
        if os.path.exists(html_file_path):
            with open(html_file_path, 'r', encoding='utf-8') as html_file:
                html_code = html_file.read()
            mapping[image_file] = html_code
        else:
            print(f"Warning: No HTML code file found for {image_file}")
    
    # Save the mapping to a JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(mapping, json_file, ensure_ascii=False, indent=4)
    
    print(f"Image-HTML mapping saved to {output_json_path}")

create_image_html_mapping(images_dir, html_dir, output_json_path)
