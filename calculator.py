#!/usr/bin/env python3

import sys

def tax(idcard, salary):
    #tax_pay = salary - salary * (0.08 + 0.02 + 0.005 + 0.06) - 5000
    tax_pay = salary - 5000
    if tax_pay <=  3000:
        tax_pay = tax_pay * 0.03 - 0
    elif tax_pay > 3000 and tax_pay <= 12000:
        tax_pay = tax_pay * 0.1 - 210
    elif tax_pay > 12000 and tax_pay <= 25000:
        tax_pay = tax_pay * 0.2 - 1410
    elif tax_pay > 25000 and tax_pay <= 35000:
        tax_pay = tax_pay * 0.25 - 2660
    elif tax_pay > 35000 and tax_pay <= 55000:
        tax_pay = tax_pay * 0.3 - 4410
    elif tax_pay > 55000 and tax_pay <= 80000:
        tax_pay = tax_pay * 0.35 - 7160
    else:
        tax_pay = tax_pay * 0.45 - 15160
    if tax_pay >= 0:
        salary = salary - tax_pay - salary * 0.165    
    else:
        salary = salary * 0.835
    print("{}:{:.2f}".format(idcard, salary))
                
if __name__ == '__main__':
    for item in sys.argv[1:]:
        idcard, salary = item.split(':')
        try:
            idcard = int(idcard)
            salary = int(salary)
        except:
            print("Parameter Error")
        tax(idcard, salary)

