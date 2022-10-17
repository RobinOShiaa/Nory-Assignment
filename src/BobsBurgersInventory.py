from re import M
from square.client import Client
import pandas as pd
from decouple import config
from utils import  _get_items_by_id, _get_items_by_mod_enabled, _get_items_by_mod_enabled_with_absentlocations, _get_items_by_name, _get_modifier_by_modid, _get_modifier_by_name, _df_to_csv, _create_df, _get_sub_modifier_by_id, _get_sub_modifier_by_name
import sys
from datetime import date
import logger

nory_inventory_logger = logger.get_logger('nory_inventory_logger')

def _retreive_catalog():
    nory_inventory_logger.info('Connecting to Application within Square developer')
    client = Client(
        access_token= config('INVENTORY_ACCESS_TOKEN'),
        environment="production"
    )

    result = client.catalog.list_catalog()
    if result.is_success():
        result = result.body["objects"]
        nory_inventory_logger.info(f'Results retrieved {result}')
        return result

    elif result.is_error():
        nory_inventory_logger.error(result.errors)

def _format_catalog(catalog):
            items = {}
            modifiers = {}

            for item in catalog:
                if item["type"] == "ITEM":
                    mod_list = item.get("item_data").get("modifier_list_info")           
                    items[item["id"]] = {
                        "present_at_all_locations": item["present_at_all_locations"],
                        "name": item["item_data"]["name"],
                        "modifiers": [{ "id": i["modifier_list_id"], "enabled": i["enabled"] } for i in mod_list] if (mod_list != None) else []
                    }

                elif item["type"] == "MODIFIER_LIST":
                    mod_data = item.get("modifier_list_data").get("modifiers")
                    modifiers[item["id"]] = {
                        "name": item["modifier_list_data"]["name"],
                        "absent_at_location_ids": ' '.join(item.get("absent_at_location_ids")) if (item.get("absent_at_location_ids") != None) else '0' ,
                        "modifiers": [{ 
                            "id": i["id"], 
                            "name": i["modifier_data"]["name"],
                        } for i in mod_data]
                    }
        
            return items, modifiers


if __name__ == "__main__":
    print()
    if len(sys.argv) == 1:
        catalog = _retreive_catalog()
        items, modifiers = _format_catalog(catalog)
        nory_inventory_logger.info(f'ITEMS_DATASET:\n {items}')
        nory_inventory_logger.info(f'MODIFIERS_DATASET:\n {modifiers}')

        df = _create_df(items, modifiers)
        _df_to_csv(df, path=config("CSV_INVENTORY_PATH"), file_name="BobsBurgersInventory")

    elif(len(sys.argv) >= 2):

        try:
            df = pd.read_csv(f'{config("CSV_INVENTORY_PATH")}BobsBurgersInventory-{date.today()}.csv')
        except:
            nory_inventory_logger.info('Latest CSV Not Created, Please Run program by default first to create csv to read')

        func = sys.argv[1]
        user_input = (' ').join(sys.argv[2:])

        if func == "search_by_modid":
            _get_modifier_by_modid(user_input, df)

        elif func == "search_by_modname":
            _get_modifier_by_name(user_input, df)

        elif func == "search_by_sub_modname":
            _get_sub_modifier_by_name(user_input, df)

        elif func == "search_by_sub_modid":
            _get_sub_modifier_by_id(user_input, df)

        elif func == "search_by_items_id":
            _get_items_by_id(user_input, df)

        elif func == "search_by_items_name":
            _get_items_by_name(user_input,df)

        elif func == "search_by_modifier_enabled_with_absent_locations":
            _get_items_by_mod_enabled_with_absentlocations(df)

        elif func == "search_by_modifier_enabled":
            _get_items_by_mod_enabled(df)

        else:
            nory_inventory_logger.error('Invalid argument')



    else:
        nory_inventory_logger.error("Invalid argument to Nory Inventory Search System")

