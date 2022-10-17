import unittest
from BobsBurgersAccounts import CLIENT_ID,REFRESH_TOKEN,ACCESS_TOKEN_URL
import requests
from os import listdir
from square.client import Client
from decouple import config

class TestInventory(unittest.TestCase):

    def test_connecting_sdk(self):
        client = Client(
            access_token= config('INVENTORY_ACCESS_TOKEN'),
            environment="production"
        )

        result = client.catalog.list_catalog()
        self.assertTrue(result.is_success(), 'result is succesful')


    def test_csv_file_exists(self):
        self.assertEqual(len(listdir('../csv/inventory')), 1)

if __name__ == '__main__':
    unittest.main()