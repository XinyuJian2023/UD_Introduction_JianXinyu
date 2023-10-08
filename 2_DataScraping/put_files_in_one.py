import os
import csv

def merge_file():
    dict_list = []
    files = os.listdir('./data/.')
    for file in files:
        with open('./data/' + file,mode='r',encoding='utf-8') as f:
            with open('merge2.csv',mode='a',encoding='utf-8') as f2:
                f2.write(f.read())
    with open('merge2.csv',mode='r',encoding='utf-8') as f2:
        with open('merge.csv',mode='a',encoding='utf-8',newline='') as f:
            lines = csv.reader(f2)
            for line in lines:
                dict_list.append({
                    'Name': line[0],
                    'Date': line[1],
                    'state': line[2],
                    'story': line[3],
                    'URL': line[4]
                })
                # print(line)
                # break
            print(dict_list)
            headers = dict_list[0].keys()
            csv_write = csv.DictWriter(f,fieldnames=headers)
            csv_write.writeheader()
            for i in dict_list:
                csv_write.writerow(i)
    os.remove('./merge2.csv')



