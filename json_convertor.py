import os
import json

# Directories containing HTML and JS files
html_dir = 'C:\\Images\\HTML'
js_dir = 'C:\\Images\\JS'

# Path to the output JSON file
output_json_path = 'C:\\Images\\index.json'

def create_html_js_mapping(html_dir, js_dir, output_json_path):
    # Initialize an empty dictionary for the mapping
    mapping = {}

    # List all HTML files in the HTML directory
    html_files = [f for f in os.listdir(html_dir) if os.path.isfile(os.path.join(html_dir, f))]

    for html_file in html_files:
        # Construct the base name and corresponding JS file name
        base_name = os.path.splitext(html_file)[0]
        js_file_name = f'{base_name}.txt'
        
        # Paths to the HTML and JS files
        html_file_path = os.path.join(html_dir, html_file)
        js_file_path = os.path.join(js_dir, js_file_name)

        # Initialize variables to hold file contents
        html_code = ""
        js_code = ""

        # Read the HTML file content if it exists
        if os.path.exists(html_file_path):
            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_code = file.read()
        
        # Read the JS file content if it exists
        if os.path.exists(js_file_path):
            with open(js_file_path, 'r', encoding='utf-8') as file:
                js_code = file.read()
        
        # Update the mapping if both files exist
        if html_code and js_code:
            mapping[html_code] = js_code
        else:
            print(f"Warning: Missing matching file for {html_file}")

    # Write the mapping to the JSON file
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(mapping, json_file, ensure_ascii=False, indent=4)
    
    print(f"HTML-JS mapping updated in {output_json_path}")

# Call the function to create the mapping
create_html_js_mapping(html_dir, js_dir, output_json_path)
