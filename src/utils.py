import csv
from numpy import NaN
import pandas as pd
import logger
from datetime import date
from decouple import config

utils_logger = logger.get_logger("utils_logger")

def _get_modifier_by_modid(mod_id: str, df: pd.DataFrame) -> pd.DataFrame:
    '''Return a modifier by its id.
    Args:
        - mod_id (str): modifier id
        - df (DataFrame): DataFrame to fetch mod_id
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Modifier based off Modifier id\n')
    result = df.loc[df.modifier_id==mod_id,'modifier_id':'sub_name']
    utils_logger.info(result)
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return

def _get_sub_modifier_by_name(mod_name=str, df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Sub_Modifier By Name : {mod_name}\n')
    result = df.loc[df.sub_name==mod_name,:]
    utils_logger.info(result)
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return

def _get_sub_modifier_by_id(mod_id=str, df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Sub_Modifier By ID : {mod_id}\n')
    result = df.loc[df.sub_id==mod_id,:]
    utils_logger.info(result)
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return

def _get_modifier_by_name(mod_name=str, df=pd.DataFrame) -> pd.DataFrame:
    '''Return a modifier by it's name
    Args:
        - mod_name (str): modifier name
        - df (DataFrame): DataFrame to fetch mod_name
    Returns:
        - result (DataFrame):  
    '''
    utils_logger.info(f'[Query:CSV] Modifier By Name : {mod_name}\n')
    result = df.loc[df.name_y==mod_name,:]
    utils_logger.info(result)
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return

def _get_items_by_mod_enabled_with_absentlocations(df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Enabled modifier True with absence in locations\n')
    result1 = df.loc[df.enabled==True,:]
    result2 = df.loc[df.absent!='0',:]
    result = pd.merge(result1,result2, on="modifier_id")
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return 

def _get_items_by_mod_enabled(df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Enabled modifier True')
    result1 = df.loc[df.enabled==True,:]
    result2 = df.loc[df.absent=='0',:]
    result = pd.merge(result1,result2, on="modifier_id")
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')
    return 

def _get_items_by_id(itemid=str, df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Item By ID : {itemid}\n')
    result = df.loc[df.item_id==itemid,:]
   
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')

def _get_items_by_name(itemname=str, df=pd.DataFrame) -> pd.DataFrame:
    utils_logger.info(f'[Query:CSV] Item By Name : {itemname}\n')
    result = df.loc[df.name_x==itemname,:]
    if(len(result) > 0):
        utils_logger.info(result)
        return result
    utils_logger.error('No Results Obtained')



def _dict_to_csv(dir: str, data: dict) -> None:
    '''Convert dict to CSV.
    Args:
        - dir (str): directory to write to
        - data (dict): data to write to csv
    '''
    try:
        utils_logger.info('Attempting to write CSV\n')
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