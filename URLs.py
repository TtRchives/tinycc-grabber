import subprocess, json, random, sys

class DownloadError(RuntimeError):
    pass
class NonexistentUrl(BaseException):
    pass
class URL:
    def __init__(self):
        self.GetConfig()
    def GetURL(self, urlRange=(1,10)):
        self.url = ""
        while self.url in list(self.urls) or self.url == "":
            for i in range(0,random.randint(*urlRange)):
                self.url += chr(random.choice((random.randint(65,90), random.randint(97,122), random.randint(48,57)))) #first one is uppercase; 2nd is lowercase; 3rd: numbers
    def GetConfig(self):
        try:
            with open("file.json") as file:
                self.urls = json.load(file)
        except Exception:
            self.urls = {}
    def GetDownload(self):
        print(f"Pinging URL {self.url}")
        self.j = subprocess.Popen(["""curl -w "%%{url_effective}" -I -L -s -S tiny.cc/%s -o /dev/null"""%self.url], shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.output = self.j.communicate()
        if self.j.returncode != 0:
            raise DownloadError(self.output)
    GetResult = GetDownload
    def WriteFile(self):
        self.urls[self.url] = self.output[0].decode("utf-8")
        if self.urls[self.url] == f"tiny.cc/{self.url}" or self.urls[self.url] == f"https://tiny.cc/{self.url}" or self.urls[self.url] == f"http://tiny.cc/{self.url}":
            raise NonexistentUrl(self.url)
        with open("file.json","w+") as file:
            file.write(json.dumps(self.urls))

def main():
    datums = URL()
    datums.GetURL()
    datums.GetDownload()
    datums.WriteFile()

if __name__ == "__main__":
    main()
