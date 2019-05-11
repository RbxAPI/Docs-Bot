import requests
import json
import os
import sys
from pathlib import Path


class Auto:

    @staticmethod
    def store_file(link, filename):
        response = requests.get(link).content
        with open(filename, 'wb') as f:
            f.write(response)

    @staticmethod
    def get_full_list():
        cache = []
        response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",
                                headers={'Cache-Control': 'no-cache'})
        data = json.loads(response.content)
        for name in data:
            local_file = f"{sys.path[0]}/libs/{name}.py"
            remote_file = f"https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/libs/{name}.py"
            file = Path(local_file)
            if file.exists():
                os.remove(local_file)
            Auto.store_file(remote_file, local_file)
            cache.append(name)
        return cache

    @staticmethod
    def get_repo_list():
        cache = {}
        response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",
                                headers={'Cache-Control': 'no-cache'})
        data = json.loads(response.content)
        for i, name in enumerate(data):
            cache[i] = {"name": name, "link": data[name]}
        return cache
