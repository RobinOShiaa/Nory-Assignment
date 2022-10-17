import requests
from datetime import date
from decouple import config
from utils import _dict_to_csv
import logger

ACCESS_TOKEN_URL = 'https://id.planday.com/connect/token'
API_BASE_URL = 'https://openapi.planday.com/'
CLIENT_ID  = config('ACCOUNT_CLIENT_ID')
REFRESH_TOKEN = config('ACCOUNT_REFRESH_TOKEN') 
nory_accounts_logger = logger.get_logger("nory_accounts_logger")

def _get_access_token() -> str:
    nory_accounts_logger.info(f'Sending POST request to {ACCESS_TOKEN_URL} to retrieve access token using APP_ID & TOKEN in body of request')
    return requests.post(
        ACCESS_TOKEN_URL,
        headers = {'Content-Type': "application/x-www-form-urlencoded"},
        data={
            "client_id": CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
    ).json()['access_token']
    
def _get_api_endpoint(endpoint: str, access_token: str) -> dict:
    nory_accounts_logger.info(f'Performing GET request: {API_BASE_URL} in order to retrieve data at endpoint: {endpoint}')
    ''' Returns the results for a given endpoint.
    Args:
        - endpoint (string): url endpoint
        - access_token (string): Bearer token
    '''
    return requests.get(
        f'{API_BASE_URL}{endpoint}',
        headers={
            "X-ClientId": CLIENT_ID,
            "Authorization": f'Bearer {access_token}'
        }
    ).json()['data']

def getCountry(city):
    result = requests.post('https://countriesnow.space/api/v0.1/countries/population/cities',
    data={
        "city": city
    })
    try:
        return result.json()['data']['country']
    except:
        return 'N/A'
    

def _format_employees(employees: dict) -> list:
    '''Reduce the employees list to only include required information.
    Args:
        - employees (dict): 'hr/v1/employees' response
    '''
    return [{
        "id": emp["id"],
        "full_name": f'{emp["firstName"]} {emp["lastName"]}',
        "email": emp["email"],
        "addresss_1": emp.get("street1"),
        "address_2": emp.get("street2"),
        "city": emp.get("city"),
        "postcode": emp.get("zip"),
        "country": getCountry(emp.get("city")),
        "iban": "N/A",
        "bic": "N/A",
        "hired_date": emp.get("hiredDate"),
        "department": emp.get("departments")[0] if (len(emp.get("departments")) > 0) else 'N/A',
        "employeeGroups": emp.get("employeeGroups")[0] if (len(emp.get("employeeGroups")) > 0) else 'N/A',
    } for emp in employees]
    
def _get_employee_group_as_string(group_id: str, access_token: str) -> str:
    return _get_api_endpoint(f'/hr/v1/employeegroups/{group_id}', access_token)['name']

def _get_employee_department_as_string(department_id, access_token) -> str:
    return _get_api_endpoint(f'/hr/v1/departments/{department_id}', access_token)['name']

def _update_employee_data(employees: dict, access_token: str) -> None:
    '''In place modification of employees to include wageType, wageRate, position & department.
    Args: 
        - employees (list): list of employees
        - access_token (string): Bearer token
    '''
    for emp in employees:
        try:
            result = _get_api_endpoint(f'/pay/v1/payrates/employeeGroups/{emp["employeeGroups"]}/employees/{emp["id"]}', access_token)
            emp["wage_type"] = result["wageType"]
            emp["wage_rate"] = result["rate"]
            emp["position"] = _get_employee_group_as_string(emp["employeeGroups"], access_token)
            emp["department"] = _get_employee_department_as_string(emp["department"], access_token)
            
        except Exception as e:
            emp["wage_type"] = "N/A"
            emp["wage_rate"] = "N/A"

        emp.pop("employeeGroups", None)
        emp.pop("id", None)

if __name__ == "__main__":
    access_token = _get_access_token()
    employees = _get_api_endpoint('hr/v1/employees', access_token)
    nory_accounts_logger.info(f'ACCOUNTS: {employees}')

    formatted = _format_employees(employees)
    _update_employee_data(formatted, access_token)
    _dict_to_csv(f'{config("CSV_ACCOUNT_PATH")}BobsBurgersAccounts-{date.today()}.csv', formatted)