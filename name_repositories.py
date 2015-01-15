#!/usr/bin/env python2

import xlsxwriter
from github import Github
import os

class RepositoryCreation():
    def Convert26(self, num):
        col_num = ""
        while num != 0:
            col_num = str(unichr(65 + (num-1) % 26)) + col_num
            num = (num - 1) / 26
        return col_num
    def CheckOut(self, org_name):
        if not os.path.exists(org_name):
            os.makedirs(org_name)
        self.login = "oecyc"
        self.password = "eth123456"
        self.g = Github(self.login, self.password)
        self.org = self.g.get_organization(org_name)
        self.repos_poll = self.org.get_repos()
        for repos in self.repos_poll:
            workbook = xlsxwriter.Workbook(org_name + '/' + repos.name + '.xlsx')
            worksheet = workbook.add_worksheet()
            owner_name = repos.owner.name
            count = 0
            user_poll = repos.get_stats_contributors()
            for stat in user_poll:
                count += 1
                worksheet.write('A' + str(count), stat.author.login)
                if stat.author.name == owner_name:
                    worksheet.write('B' + str(count), 'owner')
                else:
                    worksheet.write('B' + str(count), 'non-owner')
                worksheet.write('C' + str(count), stat.author.email)
                weeks_commits = stat.weeks
                col = 4
                for commits in weeks_commits:
                    col_num = self.Convert26(col)
                    col += 1
                    worksheet.write(col_num + str(count), str(commits.a) + ',' + str(commits.c) + ',' + str(commits.d) + ',' + str(commits.w))
            workbook.close()

if __name__ == '__main__':
    RepositoryCreation().CheckOut('facebook')

