import subprocess
import os

def mirror_website(url, output_directory):
    try:
        command = f"httrack {url} -O {output_directory}"
        subprocess.run(command, check=True, shell=True)
        print(f"Website mirrored successfully in {output_directory}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while mirroring the website: {e}")

url = "https://www.evelyntan.net/"
output_directory = "C:\\Websites"
mirror_website(url, output_directory)


url_formatted = url.replace("https://", "").replace("/", "").strip()

html = []


for subdir, dirs, files in os.walk(output_directory):
    if url_formatted in subdir:  
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):
                full_path = os.path.join(subdir, file)
                html.append(full_path)

file_path = "html.txt"
with open(file_path, 'a') as file:
    for path in html:
        print(path)
        file.write(path + "\n")

print(f"Paths of all HTML files have been saved to {file_path}")