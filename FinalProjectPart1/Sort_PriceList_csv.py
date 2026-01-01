#Creates price_list[] - appends items from "PriceList.csv" (item_id, price)
#Creates price_sorted_desc[] - sorts item prices desc from "PriceList.csv" (item_id, price)

#Output Format for both lists: [['item_id','price'], ['item2_id', 'item2_price']]

import csv
price_list = []
price_sorted_desc = []

with open (r"csv_inputs/PriceList.csv", 'r') as csv_price:
    PriceList_csv = csv.reader(csv_price)  #creates csv reader object - ex: <_csv.reader object at 0x00000214E82C6BC0>
    next(PriceList_csv) #skips header row in csv file "item_id, price"
    
    for i in PriceList_csv:
        price_list.append(i) #appends original csv to correspond sorted price with item_id later
        
    price_sorted_desc = price_list.copy() #price_sorted_desc[] is a copy of price_list[]
    
    price_sorted_desc.sort(key=lambda x: int(x[1]), reverse = True) #sorts item prices desc (most to least expensive) by converting str(price) into int(price) before checking


if __name__ == "__main__": #only run this code if executing this file directly
    print('price_sorted_desc',price_sorted_desc)
    print()
    print('price_list', price_list)