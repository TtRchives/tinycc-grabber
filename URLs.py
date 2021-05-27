import subprocess, json, random, sys

class DownloadError(RuntimeError):
    """
    Provides the output from Popen.communicate(), the entire tuple, each byte as a bytes string along with the exception (you will probably need to decode it with .decode("utf-8")).
    To access it, use something like "except URLs.DownloadError as output:" and then it will be saved as variable output
    """
class NonexistentUrl(BaseException):
    """
    Provides the URL that was tried along with the exception.
    To access it, use something like "except URLs.NonexistentUrl as url:" and then it will be saved as variable url
    """
class URL:
    """
    You CAN change variables inside this!
    For example, to archive a specific url, instead of calling GetURL just change instance.url = "id"
    NOTE: The url variable DOES NOT contain the tiny.cc/, or the https, or http, or anything! For example, id 62hd would turn into https://tiny.cc/62hd.
    """
    def __init__(self):
        self.GetConfig()
    def GetURL(self, urlRange=(1,10)):
        self.url = ""
        while self.url in list(self.urls) or self.url == "":
            self.url = ""
            for i in range(0,random.randint(*urlRange)):
                self.url += chr(random.choice((random.randint(65,90), random.randint(97,122), random.randint(48,57)))) #first one is uppercase; 2nd is lowercase; 3rd: numbers
    def GetConfig(self):
        try:
            with open("file.json") as file:
                self.urls = json.load(file)
        except Exception:
            self.urls = {}
    def GetDownload(self):
        self.j = subprocess.Popen(["""curl -w "%%{redirect_url}" -ILsS tiny.cc/%s -o /dev/null --max-redirs 1"""%self.url], shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE) #https://unix.stackexchange.com/a/515645/401349 and https://unix.stackexchange.com/a/157219/401349
        self.output = self.j.communicate()
        if self.j.returncode != 0:
            if self.j.returncode != 47:
                raise DownloadError(self.output)
    GetResult = GetDownload
    def WriteFile(self):
        self.urls[self.url] = self.output[0].decode("utf-8").split('\n')[0].replace("\n","")
        if self.urls[self.url] == f"tiny.cc/{self.url}" or self.urls[self.url] == f"https://tiny.cc/{self.url}" or self.urls[self.url] == f"http://tiny.cc/{self.url}" or self.urls[self.url] == "":
            raise NonexistentUrl(self.url)
        with open("file.json","w+") as file:
            file.write(json.dumps(self.urls))

def main():
    datums = URL()
    datums.GetURL()
    print(f"Pinging URL {datums.url}") #you can also modify datums.url, you can use that for tracker stuff (just make a wrapper that changes this variable as necessary instead of running GetURL())
    datums.GetDownload()
    datums.WriteFile()

if __name__ == "__main__":
    main()
