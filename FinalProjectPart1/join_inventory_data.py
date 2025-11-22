#Creates manufacturerList_sorted[] - appends clean csv items by removing whitespaces and not including null if_damaged + sorts manufacturer, item_type asc from "ManufacturerList.csv" (item_id,manufacturer,item_type,if_damaged)
#Creates full_inventory_list[] - appends item_id data from manufacturerList_sorted[] & price_sorted[] & service_date_list[]

# Output format: manufacturerList_sorted [['item_id', 'manufacturer', 'item_type'],...]
# Output format: full_inventory_list[[item_id,manufacturer, item_type, item_price,service_date,if_damaged],[],..]


import csv
from sort_filter_ServiceDatesList_csv import service_date_list 
from sort_PriceList_csv import price_list
from datetime import datetime, date


manufacturerList_sorted = []
full_inventory_list = []

with open ("csv_inputs/ManufacturerList.csv", 'r') as csv_manufacturerlist: #file obs
    manufacturerlist_csv = csv.reader (csv_manufacturerlist, skipinitialspace=True) #csv reader obj
    next(manufacturerlist_csv) #skips header row in csv file "item_id, service_date"

    for i in manufacturerlist_csv:
        cleaned_item = [j.strip() for j in i if j!=''] #removes whitepsaces in csv while ignoring the last comma to prevent appending a null, 'if_damaged' field
        manufacturerList_sorted.append(cleaned_item) #appending the clean item into manufacturerList_sorted[]
    manufacturerList_sorted.sort(key=lambda x: (x[1], x[2])) #sorts items by manufacturer, item_type asc




#joining item_id data from manufacturerList_sorted[] & price_sorted[] & service_date_list[]

#manufacturerList_sorted [['item_id', 'manufacturer', 'item_type'], ['item2_id', 'item2_manufacturer', 'item_2_itemType']...]
#price_sorted[['item_id', 'price'], ['item2_id', 'item2_price']...]
#service_date_list [['item_id','service_date'], ['item2_id', 'item2_service_date']...]
for i in manufacturerList_sorted:
    for j in price_list:
        for k in service_date_list:
            if i[0] == j[0] and i[0] == k[0]: #if item_id in manufacturerList_sorted MATCHES item_id in price_list AND item_id in service_date_list
                if 'damaged' in i: #if item is damaged in manufacturerList
                    item_id_data_joined = i[:3] + j[1:] + k[1:] + i[-1:] #Concatenating lists together [item_id, manufacturer, item_type] + [price] + [service_date] + [if_damaged] = [item_id,manufacturer, item_type, item_price,service_date,if_damaged]
                else:    
                    item_id_data_joined = i +  j[1:] + k[1:] #Concatenating lists together [item_id, manufacturer, item_type] + [price] + [service_date] = [item_id,manufacturer, item_type, item_price,service_date]
                    
                    #j[1:] Slicing the j list inside of the price_list to only include the price element in pos 1
                    #k[1:] Slicing the k list inside of the service_date_list to only include the service_date element in pos 1
            
                full_inventory_list.append(item_id_data_joined) #appends the new item record that includes [item_id,manufacturer, item_type, item_price,service_date,if_damaged] into full_inventory_list[]

if (__name__ == "__main__"):
    print('manufacturerList_sorted', manufacturerList_sorted)
    print()
    print('full inventory list', full_inventory_list)