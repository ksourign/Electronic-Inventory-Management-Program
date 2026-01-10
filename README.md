## Electronic Inventory Management System
Users can easily query inventory data through a terminal-based menu by providing 3 CSV files to merge, and they will receive generated CSV reports of merged inventory data.


**Business Problem:** Company wants to query inventory data easily, but data for 1 item is in 3 separate csv files. Data from csv files must be merged to create reports.

**Inventory CSV Files:**  
- ***ManufacturerList.csv*** 
    - item_id, manufacturer, item_type, if_damaged
- ***PriceList.csv*** 
    - item_id, price
- ***ServiceDatesList.csv***  
    - item_id, service_date

**CSV Reports:**
- ***DamagedInventory.csv*** - damaged items
    - item_id, manufacturer, item_type, price, service_date
- ***FullInventory.csv*** - full inventory 
    - item_id, manufacturer, item_type, price, service_date, if_damaged
- ***PastServiceDateInventory.csv*** - items past its service date
    - item_id, manufacturer, item_type, price, service_date, if_damaged
- ***{item_type}Inventory.csv*** - items of the same item type
    - item_id, manufacturer, price, service_date, if_damaged
    - EX: ***PhoneInventory.csv***, ***LaptopInventory.csv***, ***TowerInventory.csv***




### Method
 

- **sort_filter_ServiceDatesList_csv.py**
    - Creates **past_service_date_list []** & **service_date_list []** from ***ServiceDatesList.csv***
    - **service_date_list[]** - appended items from csv
    - **past_service_date_list[]** - appended items past its service_date & sorts service_date asc
    - Format for both lists: [[item_id, service_date], [], ...]
    

- **sort_PriceList_csv.py**
    - Creates **price_list []** & **price_sorted []** from ***PriceList.csv*** 
    - **price_list []** - appended items from csv
    - **price_sorted_desc []** - sorts item prices desc
    - Format for both lists: [[item_id, price], [], ...]

- **join_inventory_data.py**
    - Merge inventory data - creates **full_inventory_list []** by importing **service_date_list** & **price_list**
    - Creates **manufacturerList_sorted []** from  ***ManufacturerList.csv***
    - **manufacturerList_sorted []** - appends clean csv items by removing whitespaces & not including null if_damaged & sorts manufacturer, item_type asc
    - Format:
        - **full_inventory_list** [[item_id, manufacturer, item_type, item_price, service_date, if_damaged], [], ...]
        - **manufacturerList_sorted** [[item_id, manufacturer, item_type], ...]



