#Creates past_service_date_list[] - appends items past its service_date + sorts service_date asc from "ServiceDatesList.csv" (item_id, service_date)
#Creates service_date_list[] - appends all records from "ServiceDatesList.csv" into an array

#Output Format for both lists: [['item_id','service_date'], ['item2_id', 'item2_service_date']]

import csv
from datetime import datetime, date

service_date_list = []
past_service_date_list = []

with open ("csv_inputs/ServiceDatesList.csv", 'r') as csv_servicedates: #opening file obj
    serviceDate_list_csv = csv.reader (csv_servicedates) #creating csv reader obj
    next(serviceDate_list_csv) #skips header row in csv file "item_id, service_date"

    for i in serviceDate_list_csv:
        if datetime.strptime(i[1], "%m/%d/%Y").date() < date.today(): #comparing item_date with today's date
            past_service_date_list.append(i) #appends the item past its service date
        service_date_list.append(i) #appending all records from "ServiceDatesList.csv"
    past_service_date_list.sort(key=lambda x:datetime.strptime(x[1],"%m/%d/%Y").date()) #sort service_dates asc of items past its service_date
    


if __name__ == "__main__": #only run this code if executing this file directly
    print('service_date_list',service_date_list)
    print()
    print('past_service_date_list', past_service_date_list)