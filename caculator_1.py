#!/usr/bin/env python3

import sys
import csv

class Args(object):
    def __init__(self):
        self.argv = sys.argv[1:]
        self.c = self.argv[self.argv.index('-c')+1]
        self.d = self.argv[self.argv.index('-d')+1]
        self.o = self.argv[self.argv.index('-o')+1]

class Config(object):
    def __init__(self, configfile):
        self._config = dict()
        with open(configfile) as f:
            for line in f.readlines():
                key, value = line.strip().split('=')
                try:
                    self._config[key.strip()] = float(value.strip())
                except:
                    print('Parameter Error')
                    exit()
    def get_config(self, key):
        try:
            return self._config[key]
        except:
            print('Config Error')
            exit()


class UserData(object):
    def __init__(self, userdatafile):
        self.userdata = {}
        with open(userdatafile) as f:
            for line in f.readlines():
                key, value = line.strip().split(',')
                try:
                    self.work_id = int(key.strip())
                    self.salary = int(value.strip())
                except:
                    print('Parameter Error')
                    exit()
         
    def calculator(self):
#calculate tax
#salary_after_tax
#insurance
        self.tax = 0
        self.salary_after_tax = self.salary - self.tax - self.insurance

    def dumptofile(self, outputfile):
#storage to *.csv file
        with open(outputfile, 'w') as f:
            data  = [self.


if __name__ == '__main__':
#create object
    argument = Argv()
    config = Config('test.cfg')
    #config.get_config('')
