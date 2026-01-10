#Electronic Inventory Management Program

""" 
Manipulates csv inputs (ManufacturerList, PriceList, ServiceDatesList) to generate csv reports for users to view the following:
1. FullInventory.csv - all item_id data (all item_id data joined from ManufacturerList.csv, PriceList.csv, ServiceDatesList.csv)
2. DamagedInventory.csv - all damaged items in inventory
3. {item_type}.csv - multiple csv reports for each item type in inventory
4. PastServiceDateInventory.csv - all items past its service_date

Includes an interactive, terminal-based query capability. 
Users will be given a menu with numbers to input into the terminal to query items from the inventory.
"""

import csv
from sort_filter_ServiceDatesList_csv import past_service_date_list
from join_inventory_data import full_inventory_list
from datetime import datetime, date

#writing FullInventory.csv - writing all items in inventory ex: [item_id,manufacturer,item_type,price,service_date,if_damaged]
def writing_full_inventory_csv(print_output = True): 
    
    
    print('Full Inventory List:')

    with open('csv_reports/FullInventory.csv', 'w', newline='') as full_inventory_csv: #file obj, returns csv file
        write_full_inventory_csv = csv.writer(full_inventory_csv) #csv writer object
        write_full_inventory_csv.writerows(full_inventory_list)
    
    if print_output == True:
        print("FullInventory.csv written successfully!")
    else:
        return full_inventory_list


#writing {Item_type}Inventory.csv - writing csv files for different item_type in inventory ex: PhoneInventory.csv [item_id,manufacturer,price,service_date,if_damaged]
def writing_item_type_csv():
    print('\nItem Type Inventory List:')
    diff_item_type = [] #storing diff item_type
    for i in full_inventory_list: #looping thru items in inventory to target i[2], which is the item_type (ex: laptop, phone)
        x_item_type_list = []
        if(i[2] not in diff_item_type): #if item_type not in item_type[], then loop thru full_inventory for that diff item_type
            diff_item_type.append(i[2]) #append new item_type ['phone','laptop'...]
            with open(f"csv_reports/{i[2].capitalize()}Inventory.csv", 'w', newline='') as item_type_csv: #creating {Item_type}Inventory.csv file (ex: "LaptopInventory.csv")
                write_csv_item_type = csv.writer(item_type_csv)
                for j in full_inventory_list: #for appending item records related to the item_type chosen, i[2]. Loop item_type, i[2], in full_inventory_list until it's done
                    if i[2] == j[2]: #if the item_type, i[2], == j[2] then write down tht item_type record, (j), into {item_type}Inventory.csv
                        
                        x_item_type_list.append(j[0:2]+j[3:])                        

                x_item_type_list.sort(key=lambda x: x[0]) #sorting each item record by item_id

                write_csv_item_type.writerows(x_item_type_list) #appending item record in full_inventory[] for item_type, i[2] ; j[0:2]+j[3:] is here to remove item_type. 2347800,Apple + 999,7/3/2020
                print(f'{i[2].capitalize()}Inventory.csv written successfully!')
                

#writing PastServiceDateInventory.csv - writing all items where today's date is greater than an item's service date, ex: PastServiceDateInventory.csv [item_id,manufacturer,item_type,price,service_date,if_damaged]
def writing_past_service_date_csv(print_output = True):

    if print_output == True:
        print('\nPast Service Date List:')
    
    past_service_date_array = [] #itemid, manufacturer, item_type, price, service_date, if_damaged

    with open('csv_reports/PastServiceDateInventory.csv', 'w', newline='') as past_service_date_csv: #creating PastServiceDateInventory csv file
        write_csv_past_service_date = csv.writer(past_service_date_csv)
        for i in past_service_date_list:
            for j in full_inventory_list:
                if i[0] == j[0]: #find where item_id from past_service_date_list[] and full_inventory_list[] match
                    write_csv_past_service_date.writerow(j) #write the item row in full_inventory_list
                    past_service_date_array.append(j)
                    
    if print_output == True:
        print("PastServiceDateInventory.csv written successfully!")
    else:
        return past_service_date_array
        


#writing DamagedInventory.csv - writing all damaged items, sorted most to least expensive, ex: DamagedInventory.csv [item_id,manufacturer,item_type,price,service_date]
    
def writing_damaged_inventory_csv(print_output = True): #calling writing_damaged_inventory_csv() equates to print_output = True, #print_output = True paramater is here to control printing statement vs returning the damaged_inventory_list for a different method, three_query_damaged_items(damaged_items_list) 
    if print_output == True:
        print('\nDamaged Inventory List:')

    damaged_inventory_list = []
    with open ('csv_reports/DamagedInventory.csv', 'w', newline='') as damaged_inventory_csv:
        write_csv_damaged_inventory = csv.writer(damaged_inventory_csv)
        for i in full_inventory_list:
            if len(i) == 6: #item records w/len of 6 indicates that it is damaged (Ex: ['7346234', 'Lenovo', 'laptop', '239', '9/1/2020', 'damaged'] vs ['1009453', 'Lenovo', 'tower', '599', '10/1/2020'])
                damaged_inventory_list.append(i)

        damaged_inventory_list.sort(key=lambda x: (-int(x[3]),datetime.strptime(x[4],"%m/%d/%Y").date())) #most expensive to least expensive
        write_csv_damaged_inventory.writerows(i[:-1] for i in damaged_inventory_list )
    
    if print_output == True:
        print("DamagedInventory.csv written successfully!")
    else:
        return damaged_inventory_list



#PART 2########################################################################################################################

def clean_user_input(user_input):
# Returns clean user input (ex: [[manufacturer,item_type]])
    user_input = [user_input.split()] #splitting str userinput into an array (ex: user_input = "apple phone") --> (ex: [['apple','phone']])
    # print('split',user_input)
    #checking if user inputs a manufacturer and an item_type
    print(user_input)
    manufacturer_list = return_manufacturers(print_output = False)
    # print('manu list', manufacturer_list)


    # manufacturer_list = {i[1].lower() for i in full_inventory_list} #created a set to remove duplicate manufacturers
    item_type_list = {i[2] for i in full_inventory_list}


    #Go through the stages of cleaning user_input to become [[manufacturer, item_type]] before checking inventory for item

    #Checking LENGTH of user_input
    # Error Message: Wrong Format Inputted. Please Try Again [ex: "apple phone"]
    # if user_input includes more than just manufacturer and item_type (more than len of 2)
    if len(user_input[0]) < 2:
        if user_input[0][0].capitalize() in manufacturer_list:
            # print("user input <2")
            return user_input #keeps valid manufacturer
        
            # print ('Wrong Format Inputted. Please Try Again [ex: "apple phone"]', user_input)
            
        else:
            if user_input[0][0].capitalize() not in manufacturer_list or user_input[0][0].lower() not in item_type_list:
                user_input[0].remove(user_input[0][0])
                print('i am here')
                return user_input
        
    

    # Clean user input:
    # 1) checks if user inputted a valid manufacturer and item_type from inventory
    # 2) reverse list order into [[manufacturer, item_type]] if user_input has it backwards
    
    # Method: Remove irrelevant words by finding which word NOT in item_type_list or manufacturer_list

    # Scenarios:
    # (Ex: 'nice nice nice apple apple laptop', 'nice apple computer')
    
    if len(user_input[0]) > 2:
        for i in user_input[0].copy(): #looping through a copy of the list to identify elements to remove in the original list. Must do this to avoid skipping elements when modifying the original list
            if i.capitalize() not in manufacturer_list and i not in item_type_list:
                user_input[0].remove(i) #THIS WILL RETURN A LIST
        user_input = [list(set(user_input[0]))] #converting the set into a list - diff from list({user_input[0]})
        # print('userinput > 2, I converted to set', user_input)
        print('i am removing', user_input)




    #VALID INPUT
    if len(user_input[0]) == 2:
        # print('im in here')
        #correct format inputted [[manufacturer,item_type]]
        # print( 'len = 2 method',user_input )
        if user_input[0][0].capitalize() in manufacturer_list and user_input[0][1].lower() in item_type_list: #checks if user_input = [[manufacturer,item_type]]
            # print( 'correct input from user',user_input )
            return user_input
        
        #VALID INPUT but reversed [[item_type, manufacturer]]
        elif user_input[0][0].lower() in item_type_list and user_input[0][1].capitalize() in manufacturer_list: #checks if user_input = [[item_type,manufacturer]]
            user_input[0].reverse() #reverse user_input
            # print('this is reversed', user_input)
            # print('I reverse')
            return user_input
        
        # elif user_input[0][0].lower() in item_type_list and user_input[0][1].lower() in item_type_list:
        #     return "multiple_manu_itemType"

        # elif user_input[0][0].capitalize() in manufacturer_list and user_input[0][1].capitalize() in manufacturer_list:
        #     return "multiple_manu_itemType"

        else:
            for i in user_input[0].copy(): #looping through a copy of the list to identify elements to remove in the original list. Must do this to avoid skipping elements when modifying the original list
                if i.capitalize() not in manufacturer_list and i not in item_type_list:
                    user_input[0].remove(i) #THIS WILL RETURN A LIST
            user_input = [list(set(user_input[0]))]
            return user_input

    else:
        # if len(user_input[0])>2: #len is still > 2 after cleaning
        #     return "multiple_manu_itemType"
        # else:
        #     return user_input #empty [[]]
        return user_input


    # return user_input
    # else:#for len(user_input[0]) <= 1 OR multiple manuitemtype
    #     
    #     else:
    #         return user_input




    #     else: #samsung samsung?
    #         print("__________________________________________________________________")
    #         print(f"No such item in inventory i am here {user_input}")
    #         return False
    #         print("__________________________________________________________________")

    # else: #for when len(user_input) = 0 or literally no valid manu or item_type (ex: after cleaning process: [['x', 'z']] -> [[]])
    #     print(f"No such item in inventory IN LAST ELSE {user_input}")
    #     return user_input, False
        
     #LITERALLY NOTHING MATCHES
        


#return manufacturer set
def return_manufacturers(print_output = True):
    manufacturer_set = set() #using a set bc we want to remove duplicate manufacturers. 

    for i in full_inventory_list:
        manufacturer_set.add(i[1]) #Bc it's a set, duplicates will be checked before added into the set
    
    manufacturer_set = list(manufacturer_set) #turning set into a list to use indexing
    manufacturer_set.sort()


    if print_output == True:
        print('Manufacturers In Inventory: ', end="")
        for i in manufacturer_set:
            if i != manufacturer_set[len(manufacturer_set)-1]:
                print(i + ", ", end="")
            else:
                print(i, end="")
    else:
        return manufacturer_set


#return unique manufacturer + item_type
def return_manufacturers_itemType():
    
    dict_unique_manufacturer_itemType = {}
    for i in full_inventory_list:
        if i[1] not in dict_unique_manufacturer_itemType:
            dict_unique_manufacturer_itemType[i[1]] = set()
        dict_unique_manufacturer_itemType[i[1]].add(i[2])
    
    
    dict_unique_manufacturer_itemType = {key: sorted(list(value)) for key,value in dict_unique_manufacturer_itemType.items()} #converting the value type (set) into a list to sort values asc
    for i in dict_unique_manufacturer_itemType.items():
        manu_item_types = i[0] + ': '
        for j in i[1]:
            if j != i[1][len(i[1])-1]:
                manu_item_types += j + ', '
            else:
                manu_item_types += j
        print(manu_item_types)
    
    return dict_unique_manufacturer_itemType


#[1]find items in inventory given manufacturer
def one_query_manufacturer(user_input):
    print("__________________________________________________________________")

    if user_input != False:
    #clean user input can be a valid manufacturer or item_type tho.
    # how to remove the item_type here

    


        print("Output:")

        for i in full_inventory_list:
            if i[1] == user_input[0][0].capitalize():
                print(i[0],i[1], i[2], f'${i[3]}.00',i[4])
        print("__________________________________________________________________")

    else:
        print("testing q1")
        

#[2]find item in inventory given manufacturer + item_type
def query_manu_itemType(user_input):
    # print("after cleaning", user_input)

    print('i am here',user_input)
    if len(user_input[0]) == 2:
    
        print("__________________________________________________________________")
        # print(f'\nInventory for {user_input[0][0].capitalize()} {user_input[0][1].lower()}s:')

        item_count = 0
        inventory_string = ""
        
        for i in full_inventory_list: #[[],[],[]]
            if user_input[0][0].capitalize() == i[1] and user_input[0][1].lower() == i[2]: #if user's manufacturer,j[0], is equal to i[1](manufacturer position) AND i[2](item_type)
                item_count += 1
                for j in i:
                    if j == i[3]:
                        inventory_string += '$' + j + '.00 '
                        # print(f'${j}.00 ', end="")      
                    else:
                        if j == i[len(i)-1] and i != full_inventory_list[len(full_inventory_list)-1]:
                            inventory_string += j
                        else:
                            inventory_string += j + " "
                

        if item_count == 0:
            print('\nERROR: Item Does Not Exist')

        if len(inventory_string) > 0:
            inventory_string = f'\nInventory for {user_input[0][0].capitalize()} {user_input[0][1].lower()}s:\n' + inventory_string
            print(inventory_string+"\n"+"__________________________________________________________________")
                
    else:#len of userinput[0] =2 (for when the user only inputted a manufacturer or item_type)
        print("__________________________________________________________________")
        print('\nERROR: Invalid Input. Please Enter a Valid Manufacturer and Item Type.')
        print("__________________________________________________________________")



    # if user_input == "multiple_manu_itemType" :
    #     print("__________________________________________________________________")
    #     print("\nERROR: Please Enter Only 1 Manufacturer and Item Type", user_input)
    #     print("__________________________________________________________________")
    
    # elif len(user_input[0]) == 1 or user_input == [[]]: #lenovo fds fds, but i want to address "multiple_manu_itemType"
    #     print("__________________________________________________________________")
    #     print("\nERROR: Please Enter a Valid Manufacturer and an Item Type")
    #     print("__________________________________________________________________")




#[3]find damaged items in inventory
def view_damaged_items(damaged_items_list):
    print('\nDamaged Inventory List:')
    for i in damaged_items_list:
        print(i[0],i[1], i[2],f'${i[3]}.00', i[4])
    print("__________________________________________________________________")


#[6]view full inventory
def view_full_inventory():
    print()
    full_inventory_list = writing_full_inventory_csv(print_output = False)
    
    for i in full_inventory_list:
        for j in i:
            if j == i[3]:
                print (f'${j}.00 ', end="")
            else:
                print(j + " ", end="")
        print()
    
    print("__________________________________________________________________")

#[4]view items past its service date
def view_past_service_date():
    
    items_past_service_date = []

    print("\nItems Past their Service Date:")

    items_past_service_date = writing_past_service_date_csv(print_output = False)

    for i in items_past_service_date:
        for j in i:
            if j == i[3]:
                print(f'${j}.00 ', end="")
            else:
                print(j + " ", end="")
        print()
    print("__________________________________________________________________")


# [5] view items in service date
    
def view_in_service_date():
    items_past_service_date = []
    print("\nInventory Past their Service Date:")

    items_past_service_date = writing_past_service_date_csv(print_output = False)

    for i in full_inventory_list:
        if i[0] not in [j[0] for j in items_past_service_date]: #if item_id in full_inventory_list NOT IN the list of ALL item_id past its service date
            for j in i:
                if j == i[3]:
                    print(f'${j}.00 ', end="")
                else:
                    print(j + " ", end="")
            print()
    print("__________________________________________________________________")

#View Items from Most Expensive to Cheapest, also printing out max and min
def view_price_desc():
    print('\nInventory from Most to Least Expensive:')
    inventory_price_sorted = full_inventory_list.copy() #copying full_inventory_list
    inventory_price_sorted.sort(key=lambda x: int(x[3]), reverse = True) #sorting price desc of each item

    #printing the item data
    for i in inventory_price_sorted:
        for j in i:
            if j == i[3]:
                print(f'${j}.00 ', end="")
            else:
                print(j + " ", end="")
        print()

    print("__________________________________________________________________")

#View Undamaged Items
def view_undamaged_items(damaged_items_list):
    print("\nUndamaged Inventory:")
    for i in full_inventory_list:
        if i[0] not in [j[0] for j in damaged_items_list]:
            
            for j in i:
                if j == i[3]:
                    print(f'${j}.00 ', end="")
                else:
                    print(j + " ", end="")
            print()
    print("__________________________________________________________________")

  

#i want to print it ONCE it finishes the full inventory loop

if __name__ == "__main__":

    # Part 1 (Generating CSV Outputs)
    writing_full_inventory_csv()
    writing_item_type_csv()
    writing_past_service_date_csv()
    writing_damaged_inventory_csv()



    # Part 2 (Interactive, Terminal-based Query Capability)
    print('\nElectronic Inventory Management Program')
    # userinput = input("Enter manufacturer and item type [ex: 'apple phone']: ") #ex: userinput = 'apple phone'
    
    #testmethod
    
    
    userinput = ""
    
    while userinput != 'q':
        # if type(userinput) == str and len(userinput) != 0:
        #     print("Enter a Valid Menu Number (1-5)")
        #     userinput = ""
        # else:
        

        
        userinput = input("\nInventory Query Menu: \n"
        "[1] View Items Given Manufacturer \n"
        "[2] View Items Given Manufacturer and Item Type\n"
        "[3] View Damaged Items\n"
        "[4] View Undamaged Items\n"
        "[5] View Items Past their Service Date \n"
        "[6] View Items within their Service Date \n"
        "[7] View Items from Most to Least Expensive\n"
        "[8] View Full Inventory\n\n"

        "[q] Quit Inventory Program \n"
        "__________________________________________________________________\n\n"
        "Enter Menu Number [1-8]:")
        
        while userinput not in ("1","2","3","4","5","6","7","8"):
            userinput = input("Enter Menu Number [1-8]:")
            print()
        
        if userinput == '1':
            print("[1] View Items Given Manufacturer")

        elif userinput == '2':
            print("[2] View Items Given Manufacturer and Item Type")

        elif userinput == '3':
            print("[3] View Damaged Items")


        elif userinput == '4':
            print("[4]View Undamaged Items")
              
        elif userinput == '5':
            print("[5] View Items Past their Service Date")

        elif userinput == '6':
            print("[6] View Items within their Service Date")
            
        elif userinput == '7':
            print("[7] View Items from Most to Least Expensive")

        elif userinput == '8':
            print("[8] View Full Inventory")
         
        
        print("__________________________________________________________________")

        while userinput == '1': #View Items Given Manufacturer [Ex: 'apple']
            print()
            
            return_manufacturers()
            print('\n')
            # print("\n\n[m] Back to Menu\n")
            print('Enter [m] to Return to Menu')
            userinput_for_task = input('Enter Manufacturer:')
            
            if userinput_for_task != 'm':
                print(clean_user_input(userinput_for_task))
                # one_query_manufacturer(clean_user_input(userinput_for_task))

            if userinput_for_task == 'm':
                print("__________________________________________________________________")
                userinput_for_task = ""
                break


        while userinput == '2': #View Items Given Manufacturer and Item Type [ex: 'apple phone']
            
            #show list of manufacturrs and item_type
            print('\nAvailable Manufacturers and Item Types in Inventory:\n')
            return_manufacturers_itemType()
            print()

            print('Enter [m] to Return to Menu')
            userinput_for_task = input('Enter Manufacturer and Item Type [ex: "apple phone"]:')
                        
            if userinput_for_task != 'm':
                # print(userinput_for_task)
                # print(clean_user_input(userinput_for_task))
                # if clean_user_input(userinput_for_task) != False: #False would mean [[]] after removing items that are not manufacturer and item_type, True would mean [[manu,item_type]], also ensuring user is not exiting out of #2 task
                # clean_user_input(userinput_for_task)
                query_manu_itemType(clean_user_input(userinput_for_task)) #checking_inventory() only when item confirmed to be in inventory after clean_user_input()
                    
            if userinput_for_task == 'm':
                print("__________________________________________________________________")
                userinput_for_task = ""
                break
            

        if userinput == '3': #View Damaged Items
            
            damaged_items = writing_damaged_inventory_csv(print_output = False) #returns the damaged_inventory_list returned in the method, writing_damaged_inventory_csv() 
            view_damaged_items(damaged_items)

            userinput_for_task = input('\nEnter [m] to Return to Menu:')
            
            while userinput_for_task != 'm':
                
                userinput_for_task = input('Enter [m] to Return to Menu:')

            # userinput_for_task = ""
            print("__________________________________________________________________")


        elif userinput == '4': #View Undamaged Items
            ######new method
            damaged_items = writing_damaged_inventory_csv(print_output = False) #returns the damaged_inventory_list returned in the method, writing_damaged_inventory_csv() 
            view_undamaged_items(damaged_items)
            
            userinput_for_task = input('\nEnter [m] to Return to Menu:')

            while userinput_for_task != 'm':
                
                userinput_for_task = input('Enter [m] to Return to Menu:')
            print("__________________________________________________________________")


        elif userinput == '5': #View Items Past their Service Date
            view_past_service_date()
            userinput_for_task = input('\nEnter [m] to Return to Menu:')
            
            while userinput_for_task != 'm':
                userinput_for_task = input('Enter [m] to Return to Menu:')

            print("__________________________________________________________________")


        elif userinput == '6': #View Items within their Service Date
            view_in_service_date()
            userinput_for_task = input('\nEnter [m] to Return to Menu:')
            while userinput_for_task != 'm':
                userinput_for_task = input('Enter [m] to Return to Menu:')
                
            print("__________________________________________________________________")
        
        
        elif userinput == '7': #View Items from Most to Least Expensive
            
            view_price_desc()
            userinput_for_task = input('\nEnter [m] to Return to Menu:')
            while userinput_for_task != 'm':
                userinput_for_task = input('Enter [m] to Return to Menu:')
            print("__________________________________________________________________")

        elif userinput == '8': #View Full Inventory
            view_full_inventory()
            userinput_for_task = input('\nEnter [m] to Return to Menu:')
            while userinput_for_task != 'm':
                userinput_for_task = input('Enter [m] to Return to Menu:')
            print("__________________________________________________________________")
            

            # print(userinput) 
            # print(clean_user_input(userinput))
        
            






