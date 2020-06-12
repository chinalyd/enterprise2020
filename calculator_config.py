#!/user/bin/env python3

import sys
import csv

class Arguments:
    def __init__(self):
        self.argument = sys.argv[1:]
        self.c = self.argument[self.argument.index('-c')+1]
        self.d = self.argument[self.argument.index('-d')+1]
        self.o = self.argument[self.argument.index('-o')+1]

class Configuration:
    def __init__(self, configfile):
        self.config_dict = {}
        with open(configfile) as f:
            for line in f:
                key, value = line.split('=')
                try:
                    self.config_dict[key.strip()] = float(value.strip())
                except:
                    print('parameter Fualt.')
                    exit()
        self.config_dict['Insurance'] = self.sum_insurance_ratio

    @property
    def JiShuL(self):
        return self.config_dict['JiShuL']
    @property
    def JiShuH(self):
        return self.config_dict['JiShuH']
    @property
    def sum_insurance_ratio(self):
        return (self.config_dict['YangLao'] + self.config_dict['YiLiao'] + self.config_dict['ShiYe'] + self.config_dict['GongJiJin'])

class Worker:
    def __init__(self, workerfile):
        self.worker_data = []
        with open(workerfile) as f:
            self.worker_data = list(csv.reader(f))
       # for worker in self.worker_data:
        #    print(worker)

class Deal:
    def __init__(self, worker_data, config_data, storagepath):
        self.worker_list = worker_data
        self.config_data = config_data
        self.storagepath = storagepath

    def calculate(self):    
        #print(self.worker_list)
        for worker in self.worker_list:
           # print(worker[1])
            salary = float(worker[1])
            if salary < self.config_data['JiShuL']:
                insurance = self.config_data['JiShuL'] * self.config_data['Insurance']
            elif salary > self.config_data['JiShuH']:
                insurance = self.config_data['JiShuH'] * self.config_data['Insurance']
            else:
                insurance = salary * self.config_data['Insurance']
            worker.append(format(insurance, '.2f'))
            worker.append(format(self.tax_compute(salary, insurance), '.2f'))
            worker.append(format(salary - insurance - self.tax_compute(salary, insurance), '.2f'))
        
    def tax_compute(self, salary, insurance):
        self.tax = salary - insurance  - 5000 #Start Point
        if self.tax < 0:
            return 0
        elif self.tax <= 3000:
            return self.tax * 0.03
        elif self.tax <= 12000:
            return self.tax * 0.1 - 210
        elif self.tax <= 25000:
            return self.tax * 0.2 - 1410
        elif self.tax <= 35000:
            return self.tax * 0.25 - 2660
        elif self.tax <= 55000:
            return self.tax * 0.3 - 4410
        elif self.tax <= 80000:
            return self.tax * 0.35 - 7160
        else:
            return self.tax * 0.45 - 15160

    def storagefile(self):
        with open(self.storagepath, 'w') as f:
            csv.writer(f).writerows(self.worker_list)


if __name__ == '__main__':
    para = Arguments()
    conf = Configuration(para.c)
    wokr = Worker(para.d)
    deal = Deal(wokr.worker_data, conf.config_dict, para.o)
    deal.calculate()
    deal.storagefile()
