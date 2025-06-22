import os
import sys
import zipfile
import datetime
import re

file_path = "py_01_article_topic_generator.py"

r = datetime.datetime.today()
todayyy = f"{r.day}-{r.month}-{r.year}_{r.hour}-{r.minute}-{r.second}"

zipper_file_name = f"zipped_file_{todayyy}.zip"

zipper = zipfile.ZipFile(zipper_file_name, 'w')
zipper.write(file_path, compress_type = zipfile.ZIP_DEFLATED)
zipper.close()

# unzipper_file_name = f"unzipped_file_{todayyy}"

unzipper = zipfile.ZipFile(zipper_file_name, 'r')
unzipper.extractall(path = f"/Users/rakshita/Downloads/")
print(f"\nDownload of file: {file_path} complete! Check your downloads folder :) \n")
unzipper.close()

del_or_not = input("Do you want to delete the zip files? Enter 'y' for yes and 'n' for no: ")

if del_or_not.lower()[0] != 'y':
  print("No deletion of zip files will take place.")
  sys.exit(1)

curr_dir = os.getcwd()

count = 0

for folders, _, files in os.walk(curr_dir):
  for file in files:
    if re.search(r'^zipped_file_', file):
      print(f"Deleting file: {file}")
      os.remove(os.path.join(folders, file))
      count+=1

if count == 0:
  print("No zipped files found. So, nothing deleted.")
else:
  print(f"{count} files deleted.")
