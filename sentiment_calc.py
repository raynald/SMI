#!/usr/bin/env python2
import csv
import numpy as np

class Sen_calc():
    dic = dict()
    def dictCreate(self):
        with open('domarval.csv', 'rU') as file:
            myReader = csv.reader(file, delimiter = ',')
            for row in myReader:
                self.dic[row[1]] = row[2:]
    def featGenerate(self):
        with open('out.csv', 'r') as file:
            myReader = csv.reader(file, delimiter = ',')
            for row in myReader:
                line = row[2].split(' ')
                feature = np.array([])
                visit = dict()
                for word in line:
                    if not word in visit.keys() and word in self.dic.keys():
                        visit[word] = 1
                        cur = np.array(self.dic[word],dtype=float)
                        if len(feature) == 0:
                            feature = np.array(cur)
                        else:
                            feature = np.vstack((feature, cur))
                with open('feature.csv','a') as file:
                    if len(feature.shape) == 1:
                        mean = np.array(feature)
                    else :
                        mean = np.mean(feature, axis=0)
                    file.write(row[0]+','+row[1]+','+row[2])
                    for ind in range(len(mean)):
                        file.write(','+str(mean[ind]))
                    file.write('\n')
Sen_calc().dictCreate()
Sen_calc().featGenerate()

