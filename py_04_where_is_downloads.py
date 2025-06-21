import os

home_dir = os.path.expanduser("~")
found_path = ""

for folders, _ , files in os.walk(home_dir):
  for folder in folders:
    if folder == 'Download' or folder == 'Downloads':
      found_path = folder.getcwd()
      break

print(found_path)
