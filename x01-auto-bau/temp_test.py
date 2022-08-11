#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This program is used to auto BAU JOB, it's in the first dev stage."""
# import git

# from git import RemoteReference
# from colorama import Fore, Style
import github.Label
from github import Github
import keyring

import requests

repo_name = "ComputerConceptsLimited/PreProd"
# print(github_pr(repo_name, branch_name))  # PullRequest(title="Auto-BAU-PR test", number=39)
github_access_token = keyring.get_password("git_token", "Ivanjin_king")


def pull_request_reviewer_add(repo_owner, repo, pull_number, github_access_token):
    """Put git repo owner,repo name,path,file then return response code"""
    headers = {"Authorization": f"token {github_access_token}", "Accept": "application/vnd.github.v3+json"}
    repo_url = f" https://api.github.com/repos/{repo_owner}/{repo}/pulls/{pull_number}/requested_reviewers"
    data = '{"reviewers":["test"]}'
    response = requests.post(repo_url, data=data, headers=headers)
    print(response.status_code)
    return response.status_code  # 201 create succcessfuly

def pull_request_assignees(repo_owner, repo, pull_number, github_access_token):
    """Put git repo owner,repo name,path,file then return response code"""
    headers = {"Authorization": f"token {github_access_token}", "Accept": "application/vnd.github.v3+json"}
    repo_url = f" https://api.github.com/repos/{repo_owner}/{repo}/assignees/{'Ivanjin-king'}"
    #data = '{"assignees":["Ivanjin-king"]}'
    response = requests.get(repo_url, headers=headers)
    print(response.status_code)
    return response.status_code  # 201 create succcessfuly
def pull_request_list_labels(repo_owner, repo, pull_number, github_access_token):
    """Put git repo owner,repo name,path,file then return response code"""
    headers = {"Authorization": f"token {github_access_token}", "Accept": "application/vnd.github.v3+json"}
    repo_url = f" https://api.github.com/repos/{repo_owner}/{repo}/issues/{pull_number}/labels"
    #data = '{"assignees":["Ivanjin-king"]}'
    response = requests.get(repo_url, headers=headers)
    print(response.status_code)
    return response.status_code  # 201 create succcessfuly

repo_owner = "ComputerConceptsLimited"
repo = "PreProd"
pull_number = 42
reviewer_add_result = pull_request_reviewer_add(repo_owner, repo, pull_number, github_access_token)
if reviewer_add_result == 201:
    print("review add successfullly")

assignees =pull_request_assignees(repo_owner, repo, pull_number, github_access_token)
print('assignees',assignees)

labels = pull_request_list_labels(repo_owner, repo, pull_number, github_access_token)
print('labels',labels)


g = Github(github_access_token)
repo = g.get_repo(repo_name)
pulls = repo.get_pulls(state="open", sort="created")
for pr in pulls:
    print(pr.number)

issue = repo.get_issue(number=42)
print(issue)

x = github.Label.Label
print(x.name)

# usernames_involved.add(review.user.username)

# pr = repo.get_pull()
# print(pr)
# pr = repo.get_repo(39)
# print(pr)
# github_repo = g.get_repo(repo_name)
# pr_title = input("Input PR Title:")
# pr_summary = input("Input PR Summary: ")
#
# body = f"""{pr_summary}
# TESTS
# - [x] mac address 'check' request
# - [x] user address 'check' request
# """
# pr = github_repo.create_pull(title=f"{pr_title}", body=body, head='x01-auto-bau', base="main")


# create a pull request with pygithub library

# """initialize the repo"""
# # my_repo_path = "/workspaces/PreProd"
# my_repo_path = "/home/nsgivanj/PycharmProjects/PreProd"
# repo = git.Repo(my_repo_path)
# # repo.git.checkout('x01-auto-bau')
# pre_commit_failure = False
# print("start")
# while pre_commit_failure is False:
#     try:
#         commit_msg = input("Message for GIT COMMIT :")
#         repo.git.add(all=True)
#         print(repo.index.commit(commit_msg))
#         pre_commit_failure = True
#     except Exception as e:
#         print(e)
#         pre_commit_failure = False
#         print(Fore.RED, "Pre Commit Failed, Fix It Then Commit Again")
#         print(Style.RESET_ALL)
# print("finish")
# x = repo.git.status()
# print(x)
# 333444555666777

# (venv) ➜  PreProd git:(x01-auto-bau) ✗ curl -X POST -H 'Authorization: token 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' -H "Accept: application/vnd.github.v3+json"  https://api.github.com/repos/ComputerConceptsLimited/PreProd/issues/42/label
# s -d '{"assignees":["Ivanjin-king"]}'
# {
#   "message": "Invalid request.\n\nNo subschema in \"anyOf\" matched.\nFor 'anyOf/0', {\"assignees\"=>[\"Ivanjin-king\"]} is not an array.\nFor 'anyOf/1', {\"assignees\"=>[\"Ivanjin-king\"]} is not an array.\n\"assignees\" is not a permitted key.\n\"labels\" wasn't supplied.",
#   "documentation_url": "https://docs.github.com/rest/reference/issues#add-labels-to-an-issue"
# }
# (venv) ➜  PreProd git:(x01-auto-bau) ✗ curl -X POST -H 'Authorization: token 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' -H "Accept: application/vnd.github.v3+json"  https://api.github.com/repos/ComputerConceptsLimited/PreProd/issues/42/labels -d '{"label":["bug"]}'
# {
#   "message": "Invalid request.\n\nNo subschema in \"anyOf\" matched.\nFor 'anyOf/0', {\"label\"=>[\"bug\"]} is not an array.\nFor 'anyOf/1', {\"label\"=>[\"bug\"]} is not an array.\n\"label\" is not a permitted key.\n\"labels\" wasn't supplied.",
#   "documentation_url": "https://docs.github.com/rest/reference/issues#add-labels-to-an-issue"
# }
# (venv) ➜  PreProd git:(x01-auto-bau) ✗ curl -X POST -H 'Authorization: token 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' -H "Accept: application/vnd.github.v3+json"  https://api.github.com/repos/ComputerConceptsLimited/PreProd/issues/42/labels -d '["bug"]'
# [

