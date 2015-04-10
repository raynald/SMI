#!/usr/bin/env python

import xlsxwriter
import time
import xlrd
from github import Github
from datetime import date
import os

class Fill():
    def Convert26(self, num):
        col_num = ""
        while num != 0:
            col_num = str(unichr(65 + (num-1) % 26)) + col_num
            num = (num - 1) / 26
        return col_num
    def CheckOut(self):
        self.login = "oecyc"
        self.password = "eth123456"
        self.g = Github(self.login, self.password)

        workbook = xlrd.open_workbook('multileve.xlsx')
        sheet = workbook.sheet_by_name('PreciseData.csv')
        names = sheet.col_values(0)
        for index in xrange(2,len(names)):
            owner = self.g.get_user(names[index])
            workbook = xlsxwriter.Workbook('out.xlsx')
            worksheet = workbook.add_worksheet()
            repos = owner.get_repos()
            _num_repos = 0
            for item in repos:
                _num_repos += 1
            created = owner.created_at.date()
            _days = (date.today() - created).days
            _company = owner.company
            _contributions = owner.contributions
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
    Fill().Main()
