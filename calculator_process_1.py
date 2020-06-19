#!/usr/bin/env python3
import sys
import csv
from multiprocessing import Process, Queue

class Arguments:
    def __init__(self):
        self.para = sys.argv[1:]
        self.o = self.para[self.para.index('-o') + 1]
        self.d = self.para[self.para.index('-d') + 1]
        self.c = self.para[self.para.index('-c') + 1]

class Configuration:
    def __init__(self, config_file):
        self.config_dict = {}
        #self.q2 = queue2

    def configuration_process(self, queue2):
        with open(config_file) as f:
            for line in f:
                key, value = line.split('=')
                try:
                    self.config_dict[key.strip()] = float(value.strip())
                except:
                    print("Configuration Fault.")
            self.config_dict['insurance'] = self.insurance_sum
        queue2.put(self.config_dict)

    @property
    def insurance_sum(self):
        return (self.config_dic['YangLao'] + self.config_dict['YiLiao'] + self.config_dict['ShiYe'] + self.config_dict['GongJiJin'])

class Worker:
    def __init__(self, worker_file, queue1):
        self.worker_list = []
        self.worker_file = worker_file
        self.q = queue1
    def worker_process(self):
        with open(worker_file) as f:
            self.worker_list = list(csv.reader(f))
        self.q.put(self.worker_list)

class Calculate:
    def __init__(self, queue1, queue2, storage_path):
        self.worker_list = queue1.get(timeout=1)
        print('------------------------------Calculate')
        self.config_dict = queue2.get()
        self.storage_path = storage_path

    def calculate(self):
        for worker in self.worker_list:
            salary = float(worker[1])
            if salary < self.config_dict['JiShuL']:
                insurance = self.config_dict['JiShuL'] * self.config_dict['insurance']
            elif salary > self.config_dict['JiShuH']:
                insurance = self.config_dict['JiShuH'] * self.config_dict['insurance']
            else:
                insurance = salary * salary.config_dict['insurance']
            worker.append(format(insurance, '.2f'))
            worker.append(format(self.tax_pay(salary, insurance), '.2f'))
            worker.append(format(salary - insurance - self.tax_pay(salary, insurance), '.2f'))

    def tax_pay(self, salary, insurance):
        self.tax = salary - insurance - 5000 #start point
        if self.tax < 0:
            return 0
        elif self.tax <= 3000:
            return self.tax * 0.03
        elif self.tax <= 12000:
            return self.tax * 0.1 - 210
        elif self.tax <= 25000:
            return self.tax * 0.2 - 1410
        elif self.tax <= 35000:
            return self.tax * 0.25 -2660
        elif self.tax <= 55000:
            return self.tax * 0.3 - 4410
        elif sefl.tax <= 80000:
            return self.tax * 0.35 - 7160
        else:
            return self.tax * 0.45 - 15160

    def storage_file(self):
        with open(self.storage_path, 'w') as f:
            csv.writer(f).writerows(self.worker_list)

if __name__ == '__main__':
    queue1 = Queue()
    queue2 = Queue()

    para = Arguments()
    conf = Configuration(para.c, queue2)
    wokr = Worker(para.d, queue1)
    clcu = Calculate(queue1, queue2, para.o)

    process_list = []
    process_list.append(Process(target = wokr.worker_process))
    process_list.append(Process(target = conf.configuration_process))

    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

    proc1 = Process(target = clcu.calculate)
    proc1.start()
    proc1.join()
    proc2 = Process(target = clcu.storage_file)
    proc2.start()
    proc2.join()
