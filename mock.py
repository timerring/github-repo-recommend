import requests

urls = [
    "https://api.github.com/repos/OpenGithubs/weekly",
]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer <your_github_token>",
    "X-GitHub-Api-Version": "2022-11-28"
}
data = {
    "title": "【开源自荐】Your Project Name",
    "body": """
### 项目名称
Your Project Name

### 开源地址
https://github.com/YourProjectName

### 项目文档
https://YourProjectName.com/

### 项目简介
Your Project Description

### 项目功能

Your Project Features

### 项目架构

"""
}
for url in urls:
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())