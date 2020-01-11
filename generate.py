import requests
import os

# File dynamically loads from git so repo changes are made near constantly
if __name__ == '__main__':
    #https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/main.py
    response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/main.py")
    with open("main.py",'w+',encoding='utf-8') as file:
        file.write(response.text)
    file.close()

    # Windows to Mac / Linux / Unix Encoding
    if os.name == "nt":
        with open("main.py",'rb') as file:
            content = file.read()
        content.replace(b'\r\n', b'\n')
        with open("main.py",'wb') as file:
            file.write(content)
        file.close()
    
    # Mac / Linux / Unix to Windows Encoding
    if os.name == "posix":
        with open("main.py",'rb') as file:
            content = file.read()
        content.replace(b'\n', b'\r\n')
        with open("main.py",'wb') as file:
            file.write(content)
        file.close()
    
    # Unsupported Operating System
    else:
        print(f'Your operating system "{os.name}" is not supported.')
        exit()