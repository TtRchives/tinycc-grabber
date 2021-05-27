import subprocess, json, random, sys

url = ""
try:
    with open("file.json") as file:
        urls = json.load(file)
except Exception:
    urls = {}
for i in range(0,random.randint(1,10)):
    url += chr(random.choice((random.randint(65,90), random.randint(97,122), random.randint(48,57)))) #first one: uppercase; second one: lowercase; third one: numebes
print("Pinging URL %s"%url)
j=subprocess.Popen([("""curl -w "%%{url_effective}\n" -I -L -s -S tiny.cc/%s -o /dev/null"""%url)], shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stuff=j.communicate()
if j.returncode != 0:
    print("Failed; exiting.")
    sys.exit(1)
print(stuff)
urls[url] = stuff[0].decode("utf-8").replace("\n","")
if urls[url] == f"tiny.cc/{url}" or urls[url] == f"https://tiny.cc/{url}" or urls[url] == f"http://tiny.cc/{url}":
    print("Nonexistent URL")
    sys.exit(2)
    del urls[url]
with open("file.json","w+") as file:
    file.write(json.dumps(urls))
