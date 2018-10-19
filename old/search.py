import os,sys
def search(directory, text):
    files=os.listdir(directory)
    print files
    x=0
    while x<len(files):
        if files[x] !="pdata":
            sys.stdout.write("checking " + files[x])
            openfile=open(os.path.join(directory,files[x]))
            if text in openfile.read().lower():
                sys.stdout.write("...it contains "+ text+"\n")
            else:
                sys.stdout.write("...done\n")
            openfile.close()
        x=x+1
#search("LMO_3BrAP_1/20", "dp")
#search('C:/Program Files/Python/27/Lib/site-packages/nmrglue/fileio','unit conversion')
print os.getcwd()
search(os.getcwd(), "uc")
