import os
def startproject():
    for dirs in ["./db","./staic","./templates"]:
        os.mkdir(dirs)
    for files in [".\\cookies.txt",".\\debug.txt","webapp.py"]:
        with open(files,"a",encoding="UTF8") as f:
            pass
startproject()