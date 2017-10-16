# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
from config import UPS_NAME_AFTER_LOGIN

FILES_FOLDER = 'files/'

class UPSRaportFetcher:

    def __init__(self, userID='', password='', days=1, displayPerPage=50):
        self.session = requests.Session()
        self.login_payload = {
            'loc': 'pl_PL',
            'returnto': 'https%3A%2F%2Fwww.ups.com%2Fpl%2Fpl%2Fshipping.page',
            'forgotpassword': 'YZ',
            'connectWithSocial': 'YZ',
            'userID': str(userID),
            'getTokenWithPassword': '',
            'password': str(password),
            'ioElapsedTime': 5048,
            'ioBlackBox': '',
            'CSRFToken': None
        }
        self.request_payload = {
            "ActionOriginPair": "ExportHistory___ShippingHistory",
            "TC_TIME_STAMP": int(str(round(time.time(), 3)).replace('.', '')),
            "loc": "pl_PL",
            "RedirectHref": "",
            "app-context": "/uis",
            "uri": "create",
            "CSRFToken": None,
            "noOfRecords": None,
            "indexValue": -1,
            "test": "",
            "days": days,
            "rangeSelected": "",
            "sortOrder": "D",
            "sortColumn": "Column3",
            "refreshPage": "false",
            "scrollPage": "scroll(1)",
            "voidPage": "",
            "currentPage": "",
            "htmlShipmentToVoid": "",
            "toPage": "",
            "customsearch": "false",
            "adminSummaryFlag": "true",
            "queryListFlag": "false",
            "rsiStatus": "",
            "searchType": "Personal+Search",
            "requestType": "",
            "searchAllLocations": "false",
            "selectedQuery": "",
            "dispSummaryFlag": "true",
            "selectedShipments#1": "",
            "selectedShipments#2": "",
            "shipFrom": "",
            "shipTo": "",
            "uploadTime": "",
            "pkgCount": "",
            "intlDocId": "",
            "shipTrackNo": "",
            "serviceType": "",
            "selectRange": 1,
            "displayPerPage": displayPerPage
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
        })
        self.csv_data = None
        self.logged_in = False

    def log_in(self):
        login_url = 'https://www.ups.com/lasso/login'
        response = self.session.get(login_url)
        soup = BeautifulSoup(response.content)
        self.login_payload['CSRFToken'] = self.get_csrf_token(soup)
        time.sleep(1)

        response = self.session.post(login_url, data=self.login_payload)
        self.logged_in = UPS_NAME_AFTER_LOGIN in response.text
        print('Logged in? {}'.format(self.logged_in))
        time.sleep(1)

    def get_csrf_token(self, soup):
        token = soup.find('input', {'name': 'CSRFToken'})
        return token['value']

    def update_headers_for_shipping_history_request(self):
        self.session.headers.update({
            'Host': 'www.ups.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'https://www.ups.com/uis/create',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '760',
            'Upgrade-Insecure-Requests': '1'
        })

    def get_shipping_history(self):
        url = 'https://www.ups.com/uis/create?loc=pl_PL&ActionOriginPair=ShippingHistory___StartSession'
        request = self.session.get(url)
        response = request.content
        soup = BeautifulSoup(response)
        self.request_payload["noOfRecords"] = self.count_no_of_records(soup)
        self.request_payload["CSRFToken"] = self.get_csrf_token(soup)
        self.update_headers_for_shipping_history_request()
        self.session.post('https://www.ups.com/uis/create', self.request_payload)
        time.sleep(1)
        csv_data = self.download_csv_shipping_history()
        self.csv_data = csv_data.content.decode('utf-8')

    def download_csv_shipping_history(self):
        csv_data = self.session.get('https://www.ups.com/uis/ExportPage?loc=pl_PL', data={'loc':'pl_PL'})
        return csv_data

    def save_csv_shipping_history_to_file(self, filename):
        with open(FILES_FOLDER + str(filename) + '.csv', 'w') as file:
            file.write(self.csv_data)
        print('File saved as {}'.format(filename))

    def count_no_of_records(self, soup):
        time.sleep(2)
        table = soup.find_all(class_="dataTable")
        table = table[0]
        rows = table.findChildren(['tr'])
        rows_number = len(rows) - 1
        return rows_number

    def main(self):
        if self.login_payload != '':
            self.log_in()
            if self.logged_in == True:
                self.get_shipping_history()
            else:
                print('Wrong login or password!')
        else:
            print('Can\'t sign in without login credentials')

if __name__ == '__main__':
    raport_fetcher = UPSRaportFetcher(userID='', password='', days=1, displayPerPage=50)
    raport_fetcher.main()
    raport_fetcher.save_csv_shipping_history_to_file('csv_shipping_history')