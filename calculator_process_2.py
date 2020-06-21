#!/usr/bin/env python3

import sys
import csv
from multiprocessing import Process, Queue
from queue import Empty

class Arguments:
    '''Deal the parameter in order line'''
    def __init__(self):
        self.para = sys.argv[1:]
        self.o = self.para[self.para.index('-o') + 1]
        self.d = self.para[self.para.index('-d') + 1]
        self.c = self.para[self.para.index('-c') + 1]

class Configuration:
    '''Read configuration file'''
    def __init__(self, config_file):
        self.config = {}
        self.read_config_file(config_file)
    
    def read_config_file(self, config_file):
        with open(config_file) as f:
            for line in f:
                key, value = line.split('=')
                self.config[key.strip()] = float(value)
            self.config['insurance'] = (self.config['YangLao'] + self.config['YiLiao'] + self.config['GongJiJin'] + self.config['ShiYe'])

class Worker:
    '''Read the worker's information in worker_file'''
    def __init__(self, worker_file):
        with open(worker_file) as f:
            self.data = list(csv.reader(f))

    def send_to_queue(self, queue):
        for i in self.data:
            queue.put(i)

class Calculate:
    '''Calculate those data'''
    @classmethod
    def tax_pay(cls, q1, q2):
        while True:
            try:
                worker_id, salary = q1.get(timeout = 1)
                worker_info = [worker_id] + cls.calculate_salary(int(salary))
                print(worker_info)
                q2.put(worker_info)
            except:
                return

    @staticmethod
    def calculate_salary(salary):
        '''Use the salary number to calculate the insurance, tax and salary after pay tax'''
        social_insurance = salary * config['insurance']
        if salary < config['JiShuL']:
            social_insurance = config['JiShuL'] * config['insurance']
        if salary > cofnig['JiShuH']:
            social_insurance = config['JiShuH'] * config['insurance']

        salary_need_pay_tax = salary - social_insurance - 5000

        if salary_need_pay_tax <= 0:
            tax = 0
        elif salary_need_pay_tax <= 3000:
            tax = salary_need_pay_tax * 0.03
        elif salary_need_pay_tax <= 12000:
            tax = salary_need_pay_tax * 0.1 - 210
        elif salary_need_pay_tax <= 25000:
            tax = salary_need_pay_tax * 0.2 - 1410
        elif salary_need_pay_tax <= 35000:
            tax = salary_need_pay_tax * 0.25 - 2660
        elif salary_need_pay_tax <= 55000:
            tax = saalry_need_pay_tax * 0.3 - 4410
        elif salary_need_pay_tax <= 80000:
            tax = salary_need_pay_tax * 0.35 - 7160
        else:
            tax = salary_need_pay_tax * 0.45 - 15160

        salary_after_tax = salary - social_insurance - tax

        return [salary, 
                format(social_insurance, '.2f'),
                format(tax, '.2f'),
                format(salary_after_tax, '.2f')
        ]

class WriteData:
    '''Write data into storage file'''
    @classmethod
    def write_data(cls, queue):
        with open(args.o, 'w') as f:
            while True:
                try:
                    data = queue.get(timeout = 1)
                    csv.writer(f).writerow(data)
                except:
                    return

if __name__ == '__main__':
    args = Arguments()
    config = Configuration(args.c).config
    worker = Worker(args.d)

    queue1 = Queue()
    queue2 = Queue()

    process_1 = Process(target=worker.send_to_queue, args=(queue1,))
    process_2 = Process(target=Calculate.tax_pay, args=(queue1, queue2))
    process_3 = Process(target=WriteData.write_data, args=(queue2,))
    
    process_1.start()
    process_2.start()
    process_3.start()

    process_1.join()
    process_2.join()
    process_3.join()

