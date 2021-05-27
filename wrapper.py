import subprocess, URLs
print("Infinitely running the file. (To stop this, add a file called \"sotp\" in the working directory.)")
while True:
    try:
        open("sotp")
    except Exception:
        pass
    else:
        print("sotpping")
        sys.exit(0)
    try:
        URLs.main()
    except URLs.NonexistentUrl as ename:
        print("NonexistentUrl - %s"%ename)
    except Exception as ename:
        print(f"Error - {ename}")
