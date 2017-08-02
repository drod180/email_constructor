#!/usr/bin/env python
import csv
import os

input_file = os.path.dirname(os.path.realpath(__file__)) + '/constructedEmail_.csv'
# Get Module info and CTA info and return it as a dictionary
def parseModules(data, module_count):
    modules_dicts = []
    module_dict = {}
    module_start = 5

    for i in range (0, module_count):
        module_dict = {}
        module_dict['moduleType'] = data[module_start + i][1][1]
        module_dict['moduleName'] = data[module_start + i][1][2]
        module_dict['headline']   = data[module_start + i][1][3]
        module_dict['bodyCopy']   = data[module_start + i][1][4]
        module_dict['legalCopy']  = data[module_start + i][1][5]
        module_dict['ctaCount']   = data[module_start + i][1][6]

        for j in range (0, int(module_dict['ctaCount'])):
            module_dict['cCopy' + str(j)]  = \
                data[module_start + i][3 + (j * 2)][2]
            module_dict['cType' + str(j)]  = \
                data[module_start + i][3 + (j * 2)][3]
            module_dict['cColor' + str(j)] = \
                data[module_start + i][3 + (j * 2)][4]
            module_dict['cUrl' + str(j)]   = \
                data[module_start + i][3 + (j * 2)][5]

        modules_dicts.append(module_dict)

    return modules_dicts

def parseData():
    cta_col = 6
    header_data = []
    module = []
    module_rows = []
    module_row_count = 0
    input_file
    with open(input_file, 'rU') as csvfile:
        next(csvfile) #Ignore header
        csvReader = csv.reader(csvfile, dialect='excel')
        i = 0
        for row in csvReader:
            if i < 5:
                header_data.append({row[0]: row[1]})
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


    return header_data + module_rows


def parse():
    my_data = parseData()
    parsed_modules = parseModules(my_data, int(my_data[1]['Number of Modules']))
    parsed_data = [dict(my_data[0].items() +
                        my_data[1].items() +
                        my_data[2].items() +
                        my_data[3].items() +
                        my_data[4].items())] + parsed_modules

    return parsed_data
parse()
