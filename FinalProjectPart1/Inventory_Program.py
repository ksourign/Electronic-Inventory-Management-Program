import csv
from datetime import datetime, date
from Asc_Date_Sort_ServiceDatesList_csv import service_date_sorted 
from full_inventory_manu_asc import full_inventory_list

#writing FullInventory.csv - writing all items in inventory ex: [item_id,manufacturer,item_type,price,service_date,if_damaged]
def writing_full_inventory_csv():
    with open('csv_outputs/FullInventory.csv', 'w', newline='') as full_inventory_csv: #file obj, returns csv file
        write_full_inventory_csv = csv.writer(full_inventory_csv) #csv writer object
        write_full_inventory_csv.writerows(full_inventory_list)
    print("FullInventory.csv written successfully!")


#writing {Item_type}Inventory.csv - writing csv files for different item_type in inventory ex: PhoneInventory.csv [item_id,manufacturer,price,service_date,if_damaged]
def writing_item_type_csv():
    diff_item_type = [] #storing diff item_type
    for i in full_inventory_list: #looping thru items in inventory to target i[2], which is the item_type (ex: laptop, phone)
        x_item_type_list = []
        if(i[2] not in diff_item_type): #if item_type not in item_type[], then loop thru full_inventory for that diff item_type
            diff_item_type.append(i[2]) #append new item_type ['phone','laptop'...]
            with open(f"csv_outputs/{i[2].capitalize()}Inventory.csv", 'w', newline='') as item_type_csv: #creating {Item_type}Inventory.csv file (ex: "LaptopInventory.csv")
                write_csv_item_type = csv.writer(item_type_csv)
                for j in full_inventory_list: #for appending item records related to the item_type chosen, i[2]. Loop item_type, i[2], in full_inventory_list until it's done
                    if i[2] == j[2]: #if the item_type, i[2], == j[2] then write down tht item_type record, (j), into {item_type}Inventory.csv
                        
                        x_item_type_list.append(j[0:2]+j[3:])                        

                x_item_type_list.sort(key=lambda x: x[0]) #sorting each item record by item_id

                write_csv_item_type.writerows(x_item_type_list) #appending item record in full_inventory[] for item_type, i[2] ; j[0:2]+j[3:] is here to remove item_type. 2347800,Apple + 999,7/3/2020
                print(f'{i[2].capitalize()}Inventory.csv written successfully!')
                

#writing PastServiceDateInventory.csv - writing all items where today's date is greater than an item's service date, ex: PastServiceDateInventory.csv [item_id,manufacturer,item_type,price,service_date,if_damaged]
def writing_past_service_date_csv():
    past_service_date_list = []
    with open('csv_outputs/PastServiceDateInventory.csv', 'w', newline='') as past_service_date_csv: #creating PastServiceDateInventory csv file
        write_csv_past_service_date = csv.writer(past_service_date_csv)
        for i in service_date_sorted:
            if datetime.strptime(i[1], "%m/%d/%Y").date() < date.today():
                for j in full_inventory_list:
                    if j[0] == i[0]: #comparing item_id from service_date_sorted[] and full_inventory_list []
                        past_service_date_list.append(j) #appending item record from full_inventory_list [] where today's date is item's service date
                        
        write_csv_past_service_date.writerows(past_service_date_list)
    print("PastServiceDateInventory.csv written successfully!")
        


#writing DamagedInventory.csv - writing all damaged items, sorted most to least expensive, ex: DamagedInventory.csv [item_id,manufacturer,item_type,price,service_date]
def writing_damaged_inventory_csv():
    damaged_inventory_list = []
    with open ('csv_outputs/DamagedInventory.csv', 'w', newline='') as damaged_inventory_csv:
        write_csv_damaged_inventory = csv.writer(damaged_inventory_csv)
        for i in full_inventory_list:
            if len(i) == 6: #item records w/len of 6 indicates that it is damaged (Ex: ['7346234', 'Lenovo', 'laptop', '239', '9/1/2020', 'damaged'] vs ['1009453', 'Lenovo', 'tower', '599', '10/1/2020'])
                damaged_inventory_list.append(i)

        damaged_inventory_list.sort(key=lambda x: int(x[3]), reverse=True) #most expensive to least expensive
        write_csv_damaged_inventory.writerows(i[:-1] for i in damaged_inventory_list )
    


if __name__ == "__main__":
    print('Full Inventory List:')
    writing_full_inventory_csv()
    
    print()
    print('Item Type Inventory List:')
    writing_item_type_csv()
    
    print()
    print('Past Service Date List:')
    writing_past_service_date_csv()
    
    print()
    print('Damaged Inventory List:')
    writing_damaged_inventory_csv()

