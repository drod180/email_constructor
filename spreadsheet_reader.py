#!/usr/bin/env python
import csv

# Get Module info and CTA info and return it as a dictionary
def parseModule():
    print("module")

def parseData():
    cta_col = 6
    my_data = []
    module = []
    module_rows = []
    module_row_count = 0
    with open('test_EC_.csv', 'rU') as csvfile:
        next(csvfile) #Ignore header
        csvReader = csv.reader(csvfile, dialect='excel')
        i = 0
        for row in csvReader:
            if i < 5:
                my_data.append({'Title': row[0], 'Value': row[1]})
            else:
                if row[0] != '':
                    module_row_count += 2

            if module_row_count > 0:
                module_row_count -= 1
                # Add more rows if we have CTAs
                if row[cta_col] != "" and row[cta_col] != 'Number of CTAs':
                    module_row_count += (int(row[cta_col]) * 2)

                module.append(row)
                
            if module_row_count == 0:
                if module != []:
                    module_rows.append(module)
                    module = []

            i += 1
    print(my_data)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n")
    print(module_rows[0])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n")
    print(module_rows[1])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\n")
    print(module_rows[2])

parseData()
