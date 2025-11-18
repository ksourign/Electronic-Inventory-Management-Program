import csv
from datetime import datetime, date
from Asc_Date_Sort_ServiceDatesList_csv import service_date_sorted 
from Full_Inventory_Manu_asc import full_inventory_list

#writing FullInventory.csv - writing all items in inventory ex: [item_id,manufacturer,item_type,price,service_date,if_damaged]
def writing_full_inventory_csv():
    print('Full Inventory List:')
    with open('csv_outputs/FullInventory.csv', 'w', newline='') as full_inventory_csv: #file obj, returns csv file
        write_full_inventory_csv = csv.writer(full_inventory_csv) #csv writer object
        write_full_inventory_csv.writerows(full_inventory_list)
    print("FullInventory.csv written successfully!")


#writing {Item_type}Inventory.csv - writing csv files for different item_type in inventory ex: PhoneInventory.csv [item_id,manufacturer,price,service_date,if_damaged]
def writing_item_type_csv():
    print('\nItem Type Inventory List:')
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
    print('\nPast Service Date List:')
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
    print('\nDamaged Inventory List:')
    damaged_inventory_list = []
    with open ('csv_outputs/DamagedInventory.csv', 'w', newline='') as damaged_inventory_csv:
        write_csv_damaged_inventory = csv.writer(damaged_inventory_csv)
        for i in full_inventory_list:
            if len(i) == 6: #item records w/len of 6 indicates that it is damaged (Ex: ['7346234', 'Lenovo', 'laptop', '239', '9/1/2020', 'damaged'] vs ['1009453', 'Lenovo', 'tower', '599', '10/1/2020'])
                damaged_inventory_list.append(i)

        damaged_inventory_list.sort(key=lambda x: int(x[3]), reverse=True) #most expensive to least expensive
        write_csv_damaged_inventory.writerows(i[:-1] for i in damaged_inventory_list )

    print("DamagedInventory.csv written successfully!")



#PART 2########################################################################################################################

def clean_user_input(user_input):
# Returns clean user input (ex: [[manufacturer,item_type]])
    user_input = [user_input.split()] #splitting str userinput into an array (ex: user_input = "apple phone") --> (ex: [['apple','phone']])

    #checking if user inputs a manufacturer and an item_type
    manufacturer_list = {i[1].lower() for i in full_inventory_list} #created a set to remove duplicate manufacturers
    item_type_list = {i[2] for i in full_inventory_list}


    #Go through the stages of cleaning user_input to become [[manufacturer, item_type]] before checking inventory for item

    #Checking LENGTH of user_input
    # Error Message: Wrong Format Inputted. Please Try Again [ex: "apple phone"]
    # if user_input includes more than just manufacturer and item_type (more than len of 2)
    if len(user_input[0]) < 2:
        print ('Wrong Format Inputted. Please Try Again [ex: "apple phone"]', user_input)
        return False
    

    # Clean user input:
    # 1) checks if user inputted a valid manufacturer and item_type from inventory
    # 2) reverse list order into [[manufacturer, item_type]] if user_input has it backwards
    
    # Method: Remove irrelevant words by finding which word NOT in item_type_list or manufacturer_list

    # Scenarios:
    # (Ex: 'nice nice nice apple apple laptop', 'nice apple computer')
    
    elif len(user_input[0]) > 2:
        for i in user_input[0].copy(): #looping through a copy of the list to identify elements to remove in the original list. Must do this to avoid skipping elements when modifying the original list
            if i not in manufacturer_list and i not in item_type_list:
                user_input[0].remove(i) #THIS WILL RETURN A LIST
        user_input = [list(set(user_input[0]))]
        # print ('iam here',user_input, len(user_input[0])) #for removing duplicate manufacturerse and item_type (
        


        # if len(user_input[0]) == 2:
        #     print ("I am here",user_input)
            
        # else:
        #     print(f"No such item in inventory [IN ELSE]{user_input,len(user_input)}")
        #     return False
                
    
        #AFTER CLEANING user_input, it could either be (manu,item_type) or (item_type,manu) 
    if len(user_input[0]) == 2:
        #correct format inputted [[manufacturer,item_type]]
        # print( 'len = 2 method',user_input )
        if user_input[0][0] in manufacturer_list and user_input[0][1] in item_type_list: #checks if user_input = [[manufacturer,item_type]]
            # print( 'correct input from user',user_input )
            return user_input
        
        #correct format inputted but reversed [[item_type, manufacturer]]
        elif user_input[0][0] in item_type_list and user_input[0][1] in manufacturer_list: #checks if user_input = [[item_type,manufacturer]]
            user_input[0].reverse() #reverse user_input
            # print('this is reversed', user_input)
            return user_input
        
        else: #samsung samsung?
            print(f"No such item in inventory i am here {user_input}")
            return False

    else: #for when len(user_input) = 0 or (ex: after cleaning process: [['x', 'z']] -> [[]])
        print(f"No such item in inventory {user_input}")
        return False
    


        
        
def check_inventory(user_input):

# start finding item in inventory

    print("\nYour Item is:")

    
    for i in full_inventory_list: #[[],[],[]]
        if user_input[0][0] == i[1].lower() and user_input[0][1] == i[2]: #if user's manufacturer,j[0], is equal to i[1](manufacturer position) AND i[2](item_type)
            print(i[0], i[1], i[2], i[3]) #print the item_id, manufacturer, item_type, price
    
    

        

if __name__ == "__main__":

    # Part 1 (Creating CSV Outputs)
    writing_full_inventory_csv()
    writing_item_type_csv()
    writing_past_service_date_csv()
    writing_damaged_inventory_csv()




    # Part 2 (Interactive Inventory Query Capability)
    
    print('\nInventory Program')
    # userinput = input("Enter manufacturer and item type [ex: 'apple phone']: ") #ex: userinput = 'apple phone'
    userinput = ""
    while userinput != 'q':
        userinput = input("\nEnter a Number from the Menu Below: \n"
        "[1] Find items given manufacturer [ex: 'apple'] \n"
        "[2] Find items given manufacturer and item type [ex: 'apple phone']: \n"
        "[3] Find damaged items\n"
        "[4] Find items past its service date \n"
        "[5] Find the most and least expensive items\n\n"
        "[q] Quit Inventory Program \n\n"
        "Menu Number:")

        
        while userinput == '2':
            userinput_for_2 = input('\nPlease Enter Manufacturer and Item Type [ex: "apple phone"]\n[m] Back to Menu\n\n>')
                        
            if userinput_for_2 != 'm':
                if clean_user_input(userinput_for_2) != False: #False would mean [[]] after removing items that are not manufacturer and item_type, True would mean [[manu,item_type]], also ensuring user is not exiting out of #2 task
                    check_inventory(clean_user_input(userinput_for_2)) #checking_inventory() only when item confirmed to be in inventory after clean_user_input()
                    
                    
                
            if userinput_for_2 == 'm':
                break

            # print(userinput) 
            # print(clean_user_input(userinput))
        
            






