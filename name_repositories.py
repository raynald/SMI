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
        self.login = ""
        self.password = ""
        self.g = Github(self.login, self.password)
        self.org = self.g.get_organization(org_name)
        for repos in self.org.get_repos():
            workbook = xlsxwriter.Workbook(org_name + '/' + repos.name + '.xlsx')
            worksheet = workbook.add_worksheet()
            owner_login = repos.owner.login
            count = 0
            user_poll = repos.get_stats_contributors()
            while user_poll == None:
                user_poll = repos.get_stats_contributors()
            print "Done!", repos.name
            for stat in user_poll:
                count += 1
                worksheet.write('A' + str(count), stat.author.login)
                if stat.author.login == owner_login:
                    worksheet.write('B' + str(count), 'owner')
                else:
                    worksheet.write('B' + str(count), 'collaborator')
                worksheet.write('C' + str(count), stat.author.email)
                weeks_commits = stat.weeks
                col = 4
                old_month = 0
                old_year = 0
                old_c = 0
                for commits in weeks_commits:
                    if commits.w.month == old_month:
                        old_c += commits.c
                    else:
                        if old_month > 0:
                            col_num = self.Convert26(col)
                            col += 1
                            worksheet.write(col_num + str(count), str(old_year) + '/' + str(old_month) + ':' + str(old_c))
                        old_month = commits.w.month
                        old_year = commits.w.year
                        old_c = commits.c
            workbook.close()

if __name__ == '__main__':
    RepositoryCreation().CheckOut('facebook')

