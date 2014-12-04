from github import Github
from github import Issue
import re

class iIssue():
    def printOut(self, name, date, body):
        newStr = ""
        for word in filter (lambda x:re.match("^[a-zA-Z]+$",x),[x for x in list(re.split("[\s:/,.:]",body))]):
            newStr += word + " "
        with open('out.csv', 'a') as f:
            f.write(name+","+str(date)+","+newStr+"\n")

    def setUp(self, url):
        #self.login = ""
        #self.password = ""
        self.g = Github()#self.login, self.password)
        username = url.split('/')[3]
        repo = url.split('/')[4]
        issue_id = int(url.split('/')[6])
        self.repo = self.g.get_user(username).get_repo(repo)
        self.issue = self.repo.get_issue(issue_id)
        self.printOut(self.issue.user.login, self.issue.updated_at, self.issue.body)
        for comment in self.issue.get_comments():
            self.printOut(comment.user.login, comment.updated_at, comment.body)

iIssue().setUp("https://github.com/twbs/bootstrap/issues/2054")
