#!/usr/bin/env python3

#importing required libraries.
import operator
import re
from collections import defaultdict


#initializing a default dictonary with value [0,0] for each key.
per_user = defaultdict(lambda:[0,0])

#initializing the Error dictionary.
error_dic = {}

#Opening Log file and reading through it line by line.
with open("syslog.log") as file:
    lines = file.readlines()
    for line in lines:
        result = re.search(r'(INFO|ERROR) ([\w\' ]*) (\[.*\] )?\(([\w\.]*)\)', line) #This REGEX searches and extracts groups such as the INFO or ERROR message, username and ID of the log.
        if result.groups()[0] == "INFO":
            per_user[result.groups()[3]] = [per_user[result.groups()[3]][0]+1,per_user[result.groups()[3]][1]] #Adds 1 to the INFO column of the respective username.
        elif result.groups()[0] == "ERROR":
            per_user[result.groups()[3]] = [per_user[result.groups()[3]][0],per_user[result.groups()[3]][1]+1] #Adds 1 to the ERROR column of the respective username.
            error_dic[result.groups()[1]] = error_dic.get(result.groups()[1],0)+1  #Counts the number of times each ERROR message occurs.
            
error_sort = sorted(error_dic.items(), key=operator.itemgetter(1),reverse=True) #Sorting error dictionary in descending order of number of ERRORS.
user_sort = sorted(per_user.items(), key=operator.itemgetter(0)) #Sorting user statistics dictionary in ascending order of the username.

with open('error_message.csv', 'w') as f: #Converting the sorted ERROR messages to csv format with ERROR and ERROR COUNT as Columns.
    f.write("%s,%s\n"%("Error", "Count"))
    for err,num in error_sort:
        f.write("%s,%s\n"%(err,num))
        
with open('user_statistics.csv', 'w') as user: #Converting the sorted USER STATISTICS to csv format with USERNAME INFO ERROR as Columns.
    user.write("%s,%s,%s\n"%("Username", "INFO", "ERROR"))
    for usr,lst in user_sort:
        user.write("%s,%s,%s\n"%(usr,lst[0],lst[1]))
