#!/usr/bin/env python2

"""
 time, name of person and possibly email id, and the place of change.
"""
import xlsxwriter
from github import Github
import os

class ChangeLogCreation():
    def Convert26(self, num):
        col_num = ""
        while num != 0:
            col_num = str(unichr(65 + (num-1) % 26)) + col_num
            num = (num - 1) / 26
        return col_num
    def CheckOut(self, org_name):
        if not os.path.exists(org_name):
            os.makedirs(org_name)
        self.login = ""
        self.password = ""
        self.g = Github(self.login, self.password)
        self.org = self.g.get_user("openstack")
        for repos in self.org.get_repos():
            workbook = xlsxwriter.Workbook(org_name + '/' + repos.name + '.xlsx')
            worksheet = workbook.add_worksheet()
            owner_login = repos.owner.login
            count = 0
            if repos.size > 0:
                commits_poll = repos.get_commits()
                print "Done!", repos.name
                for commit_type in commits_poll:
                    commit = commit_type.commit
                    count += 1
                    worksheet.write('A' + str(count), commit.last_modified)
                    worksheet.write('B' + str(count), commit.author.name)
                    worksheet.write('C' + str(count), commit.author.email)
                    worksheet.write('D' + str(count), commit.message)
                workbook.close()

if __name__ == '__main__':
    ChangeLogCreation().CheckOut('openstack')
