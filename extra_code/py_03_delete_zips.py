import os
import sys
import re

del_or_not = input("Do you want to delete the zip files? Enter 'y' for yes and 'n' for no: ")

if del_or_not.lower()[0] != 'y':
  print("No deletion of zip files will take place.")
  sys.exit(1)

curr_dir = os.getcwd()
parent_dir = os.path.dirname(curr_dir)

count = 0

for folders, _, files in os.walk(parent_dir):
  for file in files:
    if re.search(r'^zipped_file_', file):
      print(f"Deleting file: {file}")
      os.remove(os.path.join(folders, file))
      count+=1

if count == 0:
  print("No zipped files found. So, nothing deleted.")
else:
  print(f"{count} files deleted.")
