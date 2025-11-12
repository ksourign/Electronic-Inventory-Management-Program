import csv
from datetime import datetime, date

datesorted = [] #final ServiceDatesList sorted (dates sorted asc w/ corresponding item_id)
PastServiceDate_array = []


with open (r"ServiceDatesList.csv", 'r') as csv_servicedates:
    PastServiceDate_csv = csv.reader (csv_servicedates)
    next(PastServiceDate_csv) #skips header row in csv file "item_id, service_date"
    for i in PastServiceDate_csv:
        datesorted.append (datetime.strptime(i[1], "%m/%d/%Y").date()) 
        # extracts and appends position 1 (service_Date) for each row of csv data [item_id (0), service_date (1)] into datesorted array,
        # while also converting from string dates into datetime objects to sort dates least to greatest
        
        # Ex:
        # # before: [[7346234, 9/1/2020],...]
        # # after: [datetime.date(2020, 9, 1),...]
        
        PastServiceDate_array.append(i) #appends original csv into an array to be used for corresponding sorted dates with item_id later
  

    datesorted.sort () #dates sorted asc
    datesorted = [[x] for x in datesorted]
    # Ex: datesorted [[datetime.date(2020, 5, 27)], [datetime.date(2020, 7, 2)], [datetime.date(2020, 7, 3)],...]


# looping thru datesorted to match corresponding item_id in PastServiceDate_array
    for i in datesorted:
        for j in PastServiceDate_array:
            if i[0] == datetime.strptime(j[1], "%m/%d/%Y").date(): #comparing sorted date objects with date objects of PastServiceDate_array (original csv)
                i[0] = j[1] 
                #date object of sorted date, i[0], becomes the item_id, j[1]
                # before: [[datetime.date(2020, 5, 27)],...] ---> after: [['5/27/2020'],...]

                i.insert(0, j[0])  
                # inserts corresponding item_id, j[0], to the start (0) of the individual item list to match original csv
                # before: [['5/27/2020'],...] ---> after: [['9034210', '5/27/2020'],...]
    
    print(datesorted)











