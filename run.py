# -*- coding: utf-8 -*-

from fetch_raport import UPSRaportFetcher
from create_raport import CSVData, CreateExcelFile
from config import UPS_LOGIN, UPS_PASSWORD, DAYS, DISPLAY_PER_PAGE, CSV_FILENAME, XLSX_FILENAME

if __name__ == '__main__':
    raport_fetcher = UPSRaportFetcher(userID=UPS_LOGIN, password=UPS_PASSWORD, days=DAYS, displayPerPage=DISPLAY_PER_PAGE)
    raport_fetcher.main()
    raport_fetcher.save_csv_shipping_history_to_file(CSV_FILENAME)

    data_frame = CSVData(CSV_FILENAME)
    data_frame.main()

    excel_file = CreateExcelFile(XLSX_FILENAME, data_frame=data_frame.data_frame_processed)
    excel_file.main()
    excel_file.save_excel_file(XLSX_FILENAME)