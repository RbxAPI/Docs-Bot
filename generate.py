import requests
import os

# Requirements install per every bot start / restart
def install_requirements():
    with open('requirements.txt','r',encoding='utf-8') as file:

        # Hacky way to get rid of '/n' in list items
        requirements = list(map(lambda requirement: requirement.strip(), file.readlines()))
        for requirement in requirements:
            os.system(f'pip install {requirement}')


# File dynamically loads from git so repo changes are made near constantly
def generate(file,**kwargs):
    directory = kwargs.get("directory", None)
    encoding = kwargs.get("encoding", 'utf-8')
    location = file[file.find("/")+1:]

    # If directory, append to location
    if directory:
        location = f'{directory}/{location}'

    # Check to see if file path actually exists
    if not os.path.exists(location):
        print(f'Path "{location}" is not valid.')
        exit()

    response = requests.get(f'https://raw.githubusercontent.com/RbxAPI/Docs-Bot/{file}')
    with open(location,'w+',encoding=encoding) as file:
        file.write(response.text)
    file.close()

    # Windows to Mac / Linux / Unix Encoding
    if os.name == "nt":
        with open(location,'rb') as file:
            content = file.read()
        content.replace(b'\r\n', b'\n')
        with open(location,'wb') as file:
            file.write(content)
        file.close()
    
    # Mac / Linux / Unix to Windows Encoding
    elif os.name == "posix":
        with open(location,'rb') as file:
            content = file.read()
        content.replace(b'\n', b'\r\n')
        with open(location,'wb') as file:
            file.write(content)
        file.close()
    
    # Unsupported Operating System
    else:
        print(f'Your operating system "{os.name}" is not supported.')
        exit()

if __name__ == '__main__':
<<<<<<< HEAD
    generate('rewrite/requirements.txt')
    install_requirements()
    generate('rewrite/main.py')
=======
    generate('rewrite/main.py')
>>>>>>> 97cd6873fe00bb5ce17f41467ba3dc1533e4e226
