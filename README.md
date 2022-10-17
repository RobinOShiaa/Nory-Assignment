# NoryAI Assignment
#### Installation
You must have Python 3.10 installed to run. 

#### Installing requirements.
pip install -r requirements.txt

#### Setting up Environment Variables:
ACCOUNT_CLIENT_ID = 'ACCOUNT_CLIENT_IID'
ACCOUNT_REFRESH_TOKEN = 'ACCOUNT_REFRESH_TOKEN'
INVENTORY_ACCESS_TOKEN = 'INVENTORY_ACCESS_TOKEN'
CSV_ACCOUNT_PATH = './csv/accounts/BobsBurgersAccounts' 
CSV_INVENTORY_PATH = './csv/inventory/BobsBurgersInventory'

#### Running
Part 1 of the Assignment can be run using:
py BobsBugersAccounts.py or running associated bat file getAccounts.bat
The results of this can then be found in /csv/accounts/

Part 2 of the Assignment can be run two ways. One for fetching the actual data and another for indexing this data. 
To fetch the data run the following:
    py BobsBurgersInventory.py or running getInventory.bat

To search the data use:
    py BobsBurgersInventory.py search