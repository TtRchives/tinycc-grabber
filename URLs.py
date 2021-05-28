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
    def __init__(self, provider="http://tiny.cc"):
        self.pos = 0
        self.GetConfig()
        self.provider = provider
        self.url = ""
        self.chars = []
        temp_str = "abcdefghijklmnopqrstuvwxyz" + "abcdefghijklmnopqrstuvwxyz".upper() + "1234567890"
        for character in temp_str:
            self.chars.append(character)
        del temp_str
        #self.incremental = incremental
    def GetURL(self, urlRange=(1,10), provider="http://tiny.cc", forceSet=None):
        if forceSet is not None:
            self.url = forceSet
            return self.url
#        if self.incremental:
#            incrementData = self.GetIncremental()
#            self.url = incrementData[0]
#            if incrementData[1] == 1:
#                return self.url
#            for i in range(0,incrementData[1] - 1):
#                self.url += self.GetIncremental()[0]
        while self.url in list(self.urls) or self.url == "":
            self.url = ""
            for i in range(0,random.randint(*urlRange)):
                self.url += chr(random.choice((random.randint(65,90), random.randint(97,122), random.randint(48,57)))) #first one is uppercase; 2nd is lowercase; 3rd: numbers
        return self.url
    def GetConfig(self, retconfig=False):
        """
        param retconfig (deprecated): Returns the dictionary. **This may use a LOT of ram, and will substantially slow things down**
        """
        try:
            with open("file.json") as file:
                self.urls = json.load(file)
        except Exception:
            self.urls = {}
        if retconfig: return self.urls
    def GetDownload(self):
        self.j = subprocess.Popen(["""curl -w "%%{redirect_url}" -ILsS %s/%s -o /dev/null --max-redirs 1"""%(self.provider,self.url)], shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE) #https://unix.stackexchange.com/a/515645/401349 and https://unix.stackexchange.com/a/157219/401349
        self.output = self.j.communicate()
        if self.j.returncode != 0:
            if self.j.returncode != 47:
                raise DownloadError(self.output)
        return self.output, self.url, self.j.returncode
    GetResult = GetDownload
    def WriteFile(self):
        self.urls[self.url] = self.output[0].decode("utf-8").split('\n')[0].replace("\n","")
        if self.urls[self.url] == f"tiny.cc/{self.url}" or self.urls[self.url] == f"https://tiny.cc/{self.url}" or self.urls[self.url] == f"http://tiny.cc/{self.url}" or self.urls[self.url] == "":
            raise NonexistentUrl(self.url)
        with open("file.json","w+") as file:
            file.write(json.dumps(self.urls))
#    def GetIncremental(self):
#        raise NotImplementedError
#        try:
#            self.pos += 1
#            if self.char[self.pos] == "0":
#                self.lengthpos += 1
#                self.pos = 0
#            return (self.char[self.pos], self.length[self.lengthpos])
#        except (NameError, AttributeError) as ename:
#            import traceback
#            traceback.print_exc()
#            self.char = []
#            for item in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890":
#                self.char.append(item)
#            self.length = (1,2,3,4,5,6,7,8,9,10)
#            self.pos = 0
#            self.lengthpos = 0
#            return (self.char[self.pos],self.length[self.lengthpos])

def wrapper():
    """
    Example wrapper
    """
    try:
        with open("provider") as file:
            prov = file.read()
    except Exception:
        prov = "tiny.cc"
    datums = URL(provider=prov) #create instance
    datums.GetURL((1,25)) #get a random url with a length from 1 to 6
    print(f"Pinging URL {datums.url}") #you can also modify datums.url, you can use that for tracker stuff (just make a wrapper that changes this variable as necessary instead of running GetURL())
    datums.GetDownload() #download the url
    datums.WriteFile() #write to json file
main = wrapper
if __name__ == "__main__":
    main()
