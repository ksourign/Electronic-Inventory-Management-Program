#Takes "PriceList.csv" (item_id, price) and creates a list that sorts price greatest to least with corresponding ID [[item_id, price]]

import csv
pricesorted = []
PriceList_array = []

with open ("PriceList.csv", 'r') as csv_price:
    PriceList_csv= csv.reader(csv_price)  #creates csv reader object - ex: <_csv.reader object at 0x00000214E82C6BC0>
    next(PriceList_csv) #skips header row in csv file "item_id, price"
    for i in PriceList_csv:
        pricesorted.append(int(i[1]))
        # extracts and append position 1 (item price) for each row of csv data [item_id (0), price (1)] into pricesorted array,
        # while also converting from string numbers into int numbers to sort from expensive to least expensive

        # Ex:
        # before: [['3001265','1200'],...]
        # after: [1200,...]
        
        PriceList_array.append(i) #appends original csv to correspond sorted price with item_id later
        

    pricesorted.sort(reverse = True)  #sorting item prices expensive to least expensive
    # print("pricesorted array",pricesorted)
    # pricesorted array [1200, 999, 799, 599, 534, 345, 239]

    pricesorted = [str(x) for x in pricesorted]
    # ex: pricesorted ['1200', '999', '799', '599', '534', '345', '239']

    pricesorted = [[x] for x in pricesorted] #wrapping each price into its own list
    # ex: pricesorted [['1200'], ['999'], ['799'], ['599'], ['534'], ['345'], ['239']]


# looping thru pricesorted to match corresponding item_id in PriceList_array
for i in pricesorted:
    for j in PriceList_array:
        if i[0] == j[1]:
            i.append(j[0])

# ex: pricesorted array [[3001265,'1200'], [2347800,'999'], [2390112, '799'], [1009453, '599'], [1167234, '534'], [9034210,'345'], [7346234,'239']]
print(pricesorted)


