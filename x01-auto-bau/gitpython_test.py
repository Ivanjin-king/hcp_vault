#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This program is used to auto BAU JOB, it's in the first dev stage."""
import git
from git import RemoteReference
from colorama import Fore, Style
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
def get_pr_request_owner(pr_number):
    """Put git repo owner,repo name,path,file then return response code"""
    specific_api_url =  f"/issues/{pr_number}"
    content = github_api_instance_get(specific_api_url=specific_api_url)
    return content[1]['user']['login']# 201 create succcessfuly
def post_repo_reviewer(issue_number,reviewer):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/pulls/{issue_number}/requested_reviewers"
    data = {"reviewers": [f"{reviewer}"]}
    data = json.dumps(data)
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content
def post_repo_assignee(issue_number,assignee):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/issues/{issue_number}/assignees"
    data = {"assignees": [f"{assignee}"]}
    data = json.dumps(data)
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content
def post_repo_labels(issue_number,label_name):
    """Input repo name, return all repo labels(list)."""
    specific_api_url = f"/issues/{issue_number}/labels"
    data = f'["{label_name}" ]'
    content = github_api_instance_post(specific_api_url=specific_api_url,data=data)
    return content
def master_make_sure(master_name):
    """Input master_name,return 'ready' or 'failed' to check if git is in the master branch and up to date."""
    branch = repo.active_branch
    # print(branch.name)
    if branch.name == master_name:
        if repo.git.pull() == "Already up to date.":
            pull_result = "Yes"
        else:
            pull_result = "Git pull failed"
    else:
        repo.git.stash("save")
        print(Fore.RED, "Your change has been stashed")
        print(Style.RESET_ALL)
        repo.git.checkout(master_name)
        if repo.git.pull() == "Already up to date.":
            pull_result = "Yes"
        else:
            pull_result = "Git pull failed"
    return pull_result
def branch_name_check(branch_name):
    """Input a new branch name return 0 for duplicated name, 1 for good name."""
    for branch in repo.branches:
        if branch.name == branch_name:
            # print(branch.name)
            return 0
    return 1
def create_new_branch_and_remote_setup(branch_name):
    """Input a branch name to setup a new branch and upstream."""
    # branch_name = input("INPUT BRANCH NAME PLEASE:")
    # while branch_name_check(branch_name) == 0:
    #     branch_name = input("DUPLICATED NAME,INPUT BRANCH NAME PLEASE:")
    remote_name = "origin"
    # origin = repo.remote(remote_name)
    repo.head.reference = repo.create_head(branch_name)
    rem_ref = RemoteReference(repo, f"refs/remotes/{remote_name}/{branch_name}")
    repo.head.reference.set_tracking_branch(rem_ref)
    repo.git.push()
    branch = repo.active_branch
    return branch
def commit_change():
    pre_commit_failure = False
    while pre_commit_failure is False:
        try:
            commit_msg = input("Message for GIT COMMIT :")
            repo.git.add(all=True)
            print(repo.index.commit(commit_msg))
            pre_commit_failure = True
        except Exception as e:
            print(e)
            pre_commit_failure = False
            print(Fore.RED, "Pre Commit Failed, Fix It Then Commit Again")
            print(Style.RESET_ALL)
def github_pr(org_repo_name, branch_name, github_access_token):
    g = Github(github_access_token)
    github_repo = g.get_repo(org_repo_name)
    pr_title = input("Input PR Title:")
    pr_summary = input("Input PR Summary: ")
    body = f"""{pr_summary}
    TESTS
    - [x] mac address 'check' request
    - [x] user address 'check' request
    """
    pr = github_repo.create_pull(title=f"{pr_title}", body=body, head=branch_name, base="main")
    return pr
def pull_request_reviewer_add(repo_owner, repo_n, pull_number, github_access_token):
    """Put git repo owner,repo name,path,file then return response code"""
    headers = {"Authorization": f"token {github_access_token}", "Accept": "application/vnd.github.v3+json"}
    repo_url = f" https://api.github.com/repos/{repo_owner}/{repo_n}/pulls/{pull_number}/requested_reviewers"
    data = '{"reviewers":["leonbroadbent"]}'
    response = requests.post(repo_url, data=data, headers=headers)
    print(response.status_code)
    return response.status_code  # 201 create succcessfuly


"""initialize the repo with gitpython library"""
# my_repo_path = "/workspaces/PreProd"
my_repo_path = "/home/nsgivanj/PycharmProjects/PreProd"
repo = git.Repo(my_repo_path)
"""Basic org info for github intance initialization."""
github_ccl_corp()#Corprate instance initialization
github_access_token = github_ccl_corp.github_access_token
repo_org = github_ccl_corp.repo_org
repo_name = github_ccl_corp.repo_name
headers = github_ccl_corp.headers
base_url = github_ccl_corp.base_url
github_init = github_api(repo_org,repo_name,github_access_token,headers,base_url)#Github request instance initialization

# def main():
"""Do the main module, this is working flow in term of normal BAU."""
# x = repo.git.status()
master_name = "main"
github_access_token = keyring.get_password("git_token", "Ivanjin_king")
branch = repo.active_branch
print(Fore.RED, "You are working at '", branch.name, "' now.")
print(Style.RESET_ALL)
ask_build_branch = input("Would you like to create a new branch(yes/no)?: ")
if ask_build_branch == "yes":
    branch_name = input("INPUT BRANCH NAME PLEASE:")
    branch_name_check_result = branch_name_check(branch_name.lower())
    while branch_name_check_result == 0:
        print(Fore.RED, f"{branch_name.upper()} already existed")
        print(Style.RESET_ALL)
        branch_name = input("INPUT BRANCH NAME PLEASE:")
        branch_name_check_result = branch_name_check(branch_name.lower())
    master_check = master_make_sure(master_name)
    if master_check == "Yes":
        print("Git is on master and up-to-date? :", master_check)
        # create_new_branch_and_remote_setup(branch_name)
elif ask_build_branch == "no":
    print(Fore.RED, f"You are working at {branch.name}")
    print(Fore.RED, "You are secure to remedy files")
    print(Style.RESET_ALL)

finish_check = input("Have you finished change?(yes/no):")
while finish_check != "yes":
    finish_check = input("Have you finished change yet? :")
input("have you type 'git status' in terminal:(yes/no)")  # it's a bug??
while finish_check != "yes":
    finish_check = input("have you type 'git status' in terminal:")
# status = repo.git.status()
repo.git.add(all=True)
# subprocess.check_output(["git", "add", "."])
differ = repo.git.diff(repo.head.commit.tree)
print(differ)
if differ == '':
    print(Fore.RED,'There are no any change at all!!!')
    quit()
else:
    commit_change_yes = input(Fore.GREEN +"Would you like to commit and push to remote?(yes/no)")
    print(Style.RESET_ALL)
    if commit_change_yes == "yes":
        commit_change()
        print(repo.remotes.origin.push())
        print(Fore.RED, "Commit was successful and push to remote")
        print(Style.RESET_ALL)
        # create a pull request with pygithub library
        pr_request = input("Create a Pull request?(yes/no)")
        if pr_request == "yes":
            #repo_name = "ComputerConceptsLimited/PreProd"
            org_repo_name = repo_org+'/'+repo_name
            label_name = "documentation"
            reviewer = 'leonbroadbent'
            branch_name = repo.active_branch.name
            pr_result = github_pr(org_repo_name, branch_name, github_access_token)
            pr_number =pr_result.number  # PullRequest(title="Auto-BAU-PR test", number=39)
            assignee = get_pr_request_owner(pr_number)# add assignee
            reviewer_add_result = post_repo_reviewer(pr_number,reviewer)# return response and content
            post_repo_assignee(pr_number, assignee)
            post_repo_labels(pr_number, label_name)
            if reviewer_add_result[0].status_code == 201:
                print("review add successfullly")
    # else:
    #     print("not master")

#
# if __name__ == "__main__":
#     main()

