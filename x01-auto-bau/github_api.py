import github.Label
import github
from github import Github
import keyring
import requests
import yaml
import json
class github_ccl_corp():
    """Supper class"""
    github_access_token = keyring.get_password("git_token", "Ivanjin_king")
    repo_org = "ComputerConceptsLimited"
    repo_name = "PreProd"
    #repo_name = "ansible-prod"
    headers = {"Authorization": f"token {github_access_token}", "Accept": "application/vnd.github.v3+json"}
    base_url = f"https://api.github.com/repos/{repo_org}/"
class github_api():
    def __init__(self,repo_org,repo_name,github_access_token,headers,base_url):
        self.github_access_token = github_access_token
        self.repo_org = repo_org
        self.repo_name = repo_name
        self.headers = headers
        self.base_url = base_url
def github_api_instance_get(specific_api_url):
    url = github_init.base_url + github_init.repo_name + specific_api_url
    response = requests.get(url, headers=headers)
    raw_content = response.content.decode('UTF-8', 'strict')
    content = yaml.safe_load(raw_content)  # alternative: yaml.load(raw_content,Loader=yaml.FullLoader)
    return response,content
def github_api_instance_post(specific_api_url,data):
    url = github_init.base_url + github_init.repo_name + specific_api_url
    response = requests.post(url, data=data, headers=headers)
    raw_content = response.content.decode('UTF-8', 'strict')
    content = yaml.safe_load(raw_content)  # alternative: yaml.load(raw_content,Loader=yaml.FullLoader)
    return response,content
def github_api_instance_put(specific_api_url,data):
    url = github_init.base_url + github_init.repo_name + specific_api_url
    response = requests.put(url, data = data, headers=headers)
    raw_content = response.content.decode('UTF-8', 'strict')
    content = yaml.safe_load(raw_content)  # alternative: yaml.load(raw_content,Loader=yaml.FullLoader)
    return response,content
#Base function
def list_repo_project():
    """Input repo org and headers, return github repo projects"""
    specific_api_url = "/projects"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    labels = [label['name'] for label in content[1]]
    ##list project columns, return card ID, then we can add the pr to the project.
    # url = 'https://api.github.com/projects/3577984/columns'
    # response = requests.get(url, headers=headers)
    # raw_content = response.content.decode('UTF-8', 'strict')
    # content = yaml.safe_load(raw_content)
    # print (content)

    return labels
def list_repo_labels():
    """Input repo name, return all repo labels(list)."""
    specific_api_url = "/labels"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    labels = [label['name'] for label in content[1]]
    return labels
def list_org_members(repo_org,headers):
    """Input repo org and headers, return github org members"""
    url =  f"https://api.github.com/orgs/{repo_org}/members"
    response = requests.get(url, headers=headers)
    raw_content = response.content.decode('UTF-8', 'strict')
    content = yaml.safe_load(raw_content)  # alternative: yaml.load(raw_content,Loader=yaml.FullLoader)
    org_mems = [mem ['login']for mem in content]
    return org_mems

def get_repo_assignees():
    """Input repo name, return all assignees(list)."""
    specific_api_url = "/assignees"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    assignees = [assignee['login'] for assignee in content[1]]
    return assignees
def get_repo_pr_reviewers(pull_number):
    """Input repo name,pr number, return all current assigned reviewers(list)."""
    specific_api_url = f"/pulls/{pull_number}/requested_reviewers"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    reviewers = [reviewer['login'] for reviewer in content[1]['users']]
    return reviewers
def get_pr_labels(pr_number):
    """Put git repo owner,repo name,path,file then return response code"""
    specific_api_url =  f"/issues/{pr_number}/labels"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    return content[1][0]['name'] # 201 create succcessfuly
def get_pr_request_owner(pr_number):
    """Put git repo owner,repo name,path,file then return response code"""
    specific_api_url =  f"/issues/{pr_number}"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    return content[1]['user']['login']# 201 create succcessfuly

def post_repo_labels(issue_number,label_name):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/issues/{issue_number}/labels"
    data = f'["{label_name}" ]'
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content
def post_repo_assignee(issue_number,assignee):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/issues/{issue_number}/assignees"
    data = {"assignees": [f"{assignee}"]}
    data = json.dumps(data)
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content
def post_repo_reviewer(issue_number,reviewer):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/pulls/{issue_number}/requested_reviewers"
    data = {"reviewers": [f"{reviewer}"]}
    data = json.dumps(data)
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content

"""Basic org info for github intance initialization."""
github_ccl_corp()#Corprate instance initialization
github_access_token = github_ccl_corp.github_access_token
repo_org = github_ccl_corp.repo_org
repo_name = github_ccl_corp.repo_name
headers = github_ccl_corp.headers
base_url = github_ccl_corp.base_url
github_init = github_api(repo_org,repo_name,github_access_token,headers,base_url)#Github request instance initialization
"""Specific info for the individual task."""
pr_number = 43
label_name = "documentation"
assignee = 'Ivanjin-king'
reviewer = 'leonbroadbent'
repo_labels = list_repo_project()
#print(repo_labels)
pr_label =get_pr_request_owner(pr_number)
print(pr_label)
#data = '{"label":["bug"]}'

# post_label = post_repo_labels(repo_name,pr_number,label_name)
# print(post_label[0])

#org_mem = get_org_mems(repo_name)
# print(org_mem)

## assignee = '["Ivanjin-king"]'
#'{"assignees":["assignees"]}'
