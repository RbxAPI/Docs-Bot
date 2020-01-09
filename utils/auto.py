import requests
import json
import os
import sys
from pathlib import Path


class Auto:

    @staticmethod
    def get_repo_list():
        cache = {}
        response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",
                                headers={"Cache-Control": "no-cache"})
        data = json.loads(response.content)
        return data