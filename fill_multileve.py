#!/usr/bin/env python

#import xlsxwriter
import time
import xlrd
from github import Github
from datetime import date
import os
import urllib, json

class Fill():
    def Main(self):
        self.login = ""
        self.password = ""
        self.g = Github(self.login, self.password)

        book = xlrd.open_workbook('multileve.xlsx')
        sheet = book.sheet_by_name('PreciseData.csv')
        names = sheet.col_values(0)
        with open("fill_out.csv", 'a') as f:
            f.write("num of repository, tenure, company, organizations, starred, num of gists, number of following, number of followers, contributions, collaborators\n")
            for index in xrange(2,len(names)):
                owner = self.g.get_user(names[index])
                repos = owner.get_repos()
                _num_repos = 0
                for item in repos:
                    _num_repos += 1
                created = owner.created_at.date()
                _tenure = (date.today() - created).days
                _company = owner.company
                if _company == None:
                    _company = ""
                _contributions = owner.contributions
                if _contributions == None:
                    _contriutions = ""
                _collaborators = owner.collaborators
                if _collaborators == None:
                    _collaborators = ""
                org_url = owner.organizations_url
                response = urllib.urlopen(org_url)
                data = json.loads(response.read())
                _orgs = ""
                for i in xrange(len(data)):
                    _orgs += data[i]["login"] + ";"
                starred_url = "https://api.github.com/users/"+ owner.login + "/starred"#owner.starred_url
                response = urllib.urlopen(starred_url)
                data = json.loads(response.read())
                _starred = ""
                for i in xrange(len(data)):
                    _starred += data[i]["full_name"] + ";"
                gist_url = "https://api.github.com/users/" + owner.login + "/gists"
                response = urllib.urlopen(gist_url)
                data = json.loads(response.read())
                _num_gists = len(data)
                _num_following = owner.following
                _num_followers = owner.followers
                count = 0
                print "Done!", owner.login
                f.write(str(_num_repos) + "," + str(_tenure) + "," + _company + "," + _orgs + "," + _starred + "," + str(_num_gists) + "," + str(_num_following) + "," + str(_num_followers) + "," + str(_contributions) + "," + str(_collaborators) + "\n")
if __name__ == '__main__':
    Fill().Main()
