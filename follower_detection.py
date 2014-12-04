#!/usr/bin/env python2
from github import Github

class iFollower():
    def setUp(self, url):
        self.login = "oecyc"
        self.password = "eth123456"
        self.g = Github(self.login, self.password)
        username = url.split('/')[3]
        self.repo = self.g.get_user(username).get_followers()
        for i in self.repo:
            with open('follower.csv', 'a') as f:
                f.write(user.name+',')

iFollower().setUp("https://github.com/shykes")
