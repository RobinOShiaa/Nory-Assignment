
# NoryAI Assignment
#### Installation
You must have Python 3.10 installed to run. 

#### Installing requirements.
```
pip install -r requirements.txt
```

#### Setting up Environment Variables:
Create a .env file in src directory and declare the following enviroment variables.
```
ACCOUNT_CLIENT_ID = 'ACCOUNT_CLIENT_IID' 
ACCOUNT_REFRESH_TOKEN = 'ACCOUNT_REFRESH_TOKEN' 
INVENTORY_ACCESS_TOKEN = 'INVENTORY_ACCESS_TOKEN' 
CSV_ACCOUNT_PATH = '../csv/accounts/BobsBurgersAccounts' 
CSV_INVENTORY_PATH = '../csv/inventory/BobsBurgersInventory' 
```

#### Running
Part 1 of the Assignment can be run using: 
```
py BobsBugersAccounts.py
``` 
Or by running the `getAccounts.bat` file. 
The results of this can then be found in `/csv/accounts/` 

Part 2 of the Assignment can be run two ways.
One for fetching the actual data and another for indexing this data.
To fetch the data run the following: 
  ```
  py BobsBurgersInventory.py 
```
Or by running the `getInventory.bat`file.

To search the data use:
```
    py BobsBurgersInventory.py search_by_modid MOD_ID
    py BobsBurgersInventory.py search_by_modname MOD_NAME
    py BobsBurgersInventory.py search_by_sub_modname SUB_MODF_NAME
    py BobsBurgersInventory.py search_by_sub_modid SUB_MOD_ID
    py BobsBurgersInventory.py search_by_items_id ITEM_ID
    py BobsBurgersInventory.py search_by_items_name ITEM_NAME
    py BobsBurgersInventory.py search_by_modifier_enabled_with_absent_locations LOCATION
    py BobsBurgersInventory.py search_by_modifier_enabled MOD_ID
```