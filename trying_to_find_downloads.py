import os

# cur_dir = r"C:\\Users\\Username\\Documents\\MyFile.txt"
cur_dir = os.getcwd()
c_dir = cur_dir

demarcator = ''

if '/' in cur_dir:
  demarcator = '/'
  c_dir = cur_dir.split('/')

elif '\\\\' in cur_dir:
  demarcator = '\\\\'
  c_dir = cur_dir.split('\\\\')

elif '\\' in cur_dir:
  demarcator = '\\'
  c_dir = cur_dir.split('\\')

c_d = c_dir[1:]

for i in c_d:
  if i == '':
    c_d.remove('')
  if i == " ":
    c_d.remove(" ")

numFold = 1
joined = ""
found_path = ""

while numFold <= len(c_d):
  if demarcator == '/':
    joined = demarcator + demarcator.join(c_d[0:numFold])
  elif demarcator == '\\' or demarcator == '\\\\':
    joined = "C:" + demarcator + demarcator.join(c_d[0:numFold])

  # print(joined)
  # print(type(joined))

  for folder, _ , files in os.walk(joined):
    if folder == 'Download' or folder == 'Downloads':
      found_path = joined
      break

  numFold += 1

print(joined)
print(found_path)
