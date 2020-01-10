import requests
import os

# File dynamically loads from git so repo changes are made near constantly
if __name__ == '__main__':
    #https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/main.py
    response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/main.py")
    with open("main.py",'w+') as file:
        file.write(str((response.text).encode("utf-8")))
    file.close()

    # This is incredibly hacky but, eh.

    # If Mac then, ...
    if os.name == "posix":
        os.system('python3 main.py')
    
    # If Windows then, ...
    elif os.name == "nt":
        os.system('python main.py')