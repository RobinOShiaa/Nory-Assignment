import csv
import pandas as pd
import logger
from datetime import date
from decouple import config

utils_logger = logger.get_logger("utils_logger")
utils_logger.info('hello')

def _get_ids_by_modifier_id(mod_id: str, df: pd.DataFrame) -> pd.DataFrame:
    '''Return an item which contains a given modifier_id 
    Args:
        - mod_id (str): modifier id
        - df (DataFrame): DataFrame to fetch mod_id
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Item ids based off Modifier id: {mod_id}')
    result = df.loc[df.sub_id==mod_id,'item_id']
    utils_logger.info(result)
    return result

def _get_modifiers_by_item_id(id=str, df=pd.DataFrame) -> pd.DataFrame:
    '''Return all modifiers realted to a given item id 
    Args:
        - id (str): item id
        - df (DataFrame): DataFrame to fetch id
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Modifiers based off Item id: {id}')
    result = df.loc[df.item_id==id,'sub_id':'sub_name']
    utils_logger.info(result)
    return result

def _get_modifier_by_id(mod_id: str, df: pd.DataFrame) -> pd.DataFrame:
    '''Return a modifier by its id.
    Args:
        - mod_id (str): modifier id
        - df (DataFrame): DataFrame to fetch mod_id
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Item ids based off Modifier id')
    result = df.loc[df.modifier_id==mod_id,'modifier_id':'sub_name']
    utils_logger.info(result)
    return result

def _get_modifier_by_name(mod_name=str, df=pd.DataFrame) -> pd.DataFrame:
    '''Return a modifier by it's name
    Args:
        - mod_name (str): modifier name
        - df (DataFrame): DataFrame to fetch mod_name
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Modifier By Name : {mod_name}')
    result = df.loc[df.name_y==mod_name,:]
    utils_logger.info(result)
    return result

# I think this is incorrect
def _get_all_items_with_modifier(df: dict):
    utils_logger.info('[Query:CSV] Get All Modifiers')
    result = df.loc[:,:]
    utils_logger.info(result)
    return result

def _dict_to_csv(dir: str, data: dict) -> None:
    '''Convert dict to CSV.
    Args:
        - dir (str): directory to write to
        - data (dict): data to write to csv
    '''
    try:
        utils_logger.info('Attempting to write CSV')
        with open(dir, 'w+') as csvfile:
            fieldnames = data[0].keys()
            utils_logger.info(f'headers {fieldnames}')
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
            utils_logger.info('CSV finished writing')

    except IOError as e:
        utils_logger.error(f"I/O error: {e} ")
def _create_df(items: dict, modifiers: dict) -> pd.DataFrame:
    items_csv = []
    for item in items:
        for modifier in items[item]["modifiers"]:
            items_csv.append({
                "item_id": item,
                "name": items[item]["name"],
                "present_at_all_locations": items[item]["present_at_all_locations"],
                "modifier_id": modifier["id"],
                "enabled": modifier["enabled"]
            })
    
    utils_logger.info(f'ITEMS {items_csv}')

    modifier_csv = []
    for modifier in modifiers:
        for mod in modifiers[modifier]["modifiers"]:
            modifier_csv.append({
                "modifier_id": modifier,
                "name": modifiers[modifier]['name'],
                "absent": str(modifiers[modifier]["absent_at_location_ids"]),
                "sub_id": mod["id"],
                "sub_name": mod["name"]
            })
    
    
    utils_logger.info(f'MODIFIERS\n{modifier_csv}')
    
    items_df = pd.DataFrame(items_csv)
    utils_logger.info(f'ITEMS_DATAFRAME\n{items_df}')
    
    modifiers_df = pd.DataFrame(modifier_csv)
    utils_logger.info(f'MODIFIERS_DATAFRAME\n{modifiers_df}')

    df = pd.merge(items_df, modifiers_df, on='modifier_id', how='inner')
    utils_logger.info(f'ITEMS JOIN MODIFIERS DATAFRAMES\n {df}')

    return df

def _df_to_csv(df: pd.DataFrame, path: str, file_name: str):
    df.to_csv(f'{path}{file_name}-{date.today()}.csv', encoding='utf-8', index=False)