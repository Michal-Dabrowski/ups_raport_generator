# -*- coding: utf-8 -*-

import datetime

UPS_LOGIN = ''
UPS_PASSWORD = ''
UPS_NAME_AFTER_LOGIN = '' #your account name on ups.com after signing in, it's different than your login.
DISPLAY_PER_PAGE = 50
DAYS = 1
FILES_FOLDER = 'files/'
TODAY = datetime.datetime.today().strftime("%Y-%m-%d")
CSV_FILENAME = 'csv_shipping_history_' + str(TODAY)
XLSX_FILENAME = 'raport_ups_' + str(TODAY)