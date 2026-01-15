import csv
from datetime import datetime, date

service_date_list = [] #appends items past its service_date + sorts service_date asc from "ServiceDatesList.csv" (item_id, service_date)
past_service_date_list = [] #appends all records from "ServiceDatesList.csv" into an array

#Output Format for both lists: [['item_id','service_date'], ['item2_id', 'item2_service_date']]

with open ("csv_inputs/ServiceDatesList.csv", 'r') as csv_servicedates: #opening file obj
    serviceDate_list_csv = csv.reader (csv_servicedates) #creating csv reader obj
    next(serviceDate_list_csv) #skips header row in csv file "item_id, service_date"

    service_date_list = [[y for y in x]for x in serviceDate_list_csv]

#strips beginning or ending white spaces first
service_date_list = [[y.strip() for y in x] for x in service_date_list]

#append the item record if it's not null
service_date_list = [[y for y in x if y != ''] for x in service_date_list] 

#copy service date records over to create past_service_date_list
past_service_date_list = service_date_list.copy()

#filter service date records to include where service date is past today's date by converting to dates for comparison 
past_service_date_list = [x for x in past_service_date_list if datetime.strptime(x[1],"%m/%d/%Y").date() < date.today()]

#sort dates least to greatest
past_service_date_list.sort(key=lambda x:datetime.strptime(x[1],"%m/%d/%Y").date()) #this SORTS DATES from least to greatest


if __name__ == "__main__": #only run this code if executing this file directly
    print('service_date_list')
    for row in service_date_list:
        print(row)
    print()

    print('past_service_date_list')
    for row in past_service_date_list:
        print(row)