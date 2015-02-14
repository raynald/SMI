from github import Github
from github import Issue
import numpy as np
import re

org = 'mantle'
repo = 'mantle'
issue_number = '201'

class iIssue():
    def removeQuoteAndLink(self, s):
        link_pattern_str = ur'''(!?)\[([^\]]*)\]\(([^)]+)\)'''
        quote_pattern_str = ur'''(>)([^\n$]+)(\n|$)'''
        rep_str = ur''''''
        result = re.sub(link_pattern_str, rep_str, s)
        return re.sub(quote_pattern_str, rep_str, result)
    def removeNonAscii(self, s): return "".join(i for i in s if ord(i)<128)

    def printOut(self, name, date, body):
        newStr = self.removeQuoteAndLink(body)
        newStr = self.removeNonAscii(newStr).replace('\r\n',' ').replace(",","~")
        #save file here
        if name in self.user_poll:
            self.user_poll[name] += newStr
        else:
            self.user_poll[name] = newStr
        with open('yash/'+org+'_data/'+repo+'_'+issue_number+'.csv', 'a') as f:
            f.write(name+","+str(date)+","+newStr+"\n")

    def setUp(self, url):
        self.login = ""
        self.password = ""
        self.g = Github(self.login, self.password)
        self.user_poll = {}
        username = url.split('/')[3]
        repo = url.split('/')[4]
        issue_id = int(url.split('/')[6])
        self.repo = self.g.get_user(username).get_repo(repo)
        self.issue = self.repo.get_issue(issue_id)
        self.printOut(self.issue.user.login, self.issue.updated_at, self.issue.body)
        for comment in self.issue.get_comments():
            self.printOut(comment.user.login, comment.updated_at, comment.body)
        #save another file
        with open('yash/'+org+'_data/poll'+repo+'_'+issue_number+'.csv', 'a') as f:
            for item in self.user_poll:
                f.write(item + ","+self.user_poll[item]+"\n")

iIssue().setUp("https://github.com/" + org + "/" + repo + "/issues/" + issue_number)
