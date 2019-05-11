import requests
import json
import os

class Auto:

	def store_file(link):
		response = requests.get(link).content


	def get_full_list(wd):
		cache = []
		response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",headers={'Cache-Control': 'no-cache'})
		data = json.loads(response.content)
		for name in data:
			try:
				file = open(wd+"/libs/"+str(name)+".py",'r')
				if file:
					os.remove(wd+"/libs/"+str(name)+".py")
					Auto.store_file("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/libs/"+str(name)+".py")
			except Exception as error:
				
				# File doesn't exist or working directory is pointed somewhere else
				Auto.store_file("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/libs/"+str(name)+".py")

			cache.append(name)
		return cache


	def get_repo_list():
		cache = {}
		response = requests.get("https://raw.githubusercontent.com/RbxAPI/Docs-Bot/rewrite/api_list.json",headers={'Cache-Control': 'no-cache'})
		data = json.loads(response.content)
		i = 0
		for name in data:
			cache[i] = {"name":name,"link":data[name]}
			i = i + 1
		return cache