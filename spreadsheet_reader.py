#!/usr/bin/env python
import csv

def parseData():
    my_data = []

    with open('test_EC_.csv', 'rU') as csvfile:
        csvReader = csv.reader(csvfile, dialect='excel')
        i = 0
        for row in csvReader:
            if i > 0 and i < 5:
                my_data.append({'Title': row[0], 'Value': row[1], 'row': i})
            if i >= 5:
                if row[0] != '':
                    my_data.append({'ModuleNum': row[0], 'row': i})


            i += 1
    print(my_data)

parseData()
