# -*- coding: utf-8 -*-

import pandas
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment, Font, Border, Side
from openpyxl import Workbook
from config import FILES_FOLDER, CSV_FILENAME, XLSX_FILENAME

class CSVData:
    """
    Reads a .csv file and creates DataFrame using Pandas module.
    """
    def __init__(self, filename):
        self.filename = filename
        self.data_frame_original = None
        self.data_frame_processed = None

    def read_csv_pandas(self):
        data_frame = pandas.read_csv(FILES_FOLDER + self.filename + '.csv')
        self.data_frame_original = data_frame

    def filter_columns(self):
        columns_that_we_need = [
            'Data wysłania', 'Numer monitorowania przesyłki', 'Numeru Referencyjnego 1',
            'Liczba paczek w przesyłce', 'Wyślij do - nazwa firmy lub nazwisko',
            'Wyślij do - wiersz adresu 1', 'Wyślij do - kod pocztowy',
            'Wyślij do - miasto', 'Wskaźnik anulowania'
        ]
        self.data_frame_processed = self.data_frame_original.filter(items=columns_that_we_need)

    def drop_duplicates_in_data_frame(self, data_frame):
        data_frame.drop_duplicates(inplace=True)
        self.reset_index(data_frame)
        return data_frame
    """
    def drop_anulowane(self, data_frame):
        data_frame[data_frame['Wskaźnik anulowania'] != 'Anulowane']
        return data_frame
    """
    def reset_index(self, data_frame):
        data_frame.reset_index(inplace=True, drop=True)
        data_frame.index += 1

    def rename_columns(self, data_frame):
        names_pairs = {
            'Data wysłania': 'Data',
            'Numer monitorowania przesyłki': 'Nr listu',
            'Numeru Referencyjnego 1': 'Nr ref.',
            'Liczba paczek w przesyłce': 'Szt.',
            'Wyślij do - nazwa firmy lub nazwisko': 'Odbiorca',
            'Wyślij do - wiersz adresu 1': 'Adres',
            'Wyślij do - wiersz adresu 2': 'Adres_2',
            'Wyślij do - wiersz adresu 3': 'Adres_3',
            'Wyślij do - kod pocztowy': 'Kod  ',
            'Wyślij do - miasto': 'Miasto',
        }
        data_frame.rename(columns=names_pairs, inplace=True)
        return data_frame

    def main(self):
        self.read_csv_pandas()
        self.filter_columns()
        self.data_frame_processed = self.drop_duplicates_in_data_frame(self.data_frame_processed)
        self.data_frame_processed = self.rename_columns(self.data_frame_processed)

class CreateExcelFile:
    """
    Needs a filename and DataFrame object
    """
    def __init__(self, filename, data_frame=None):
        self.data_frame = data_frame
        self.workbook = Workbook()
        self.active_worksheet = self.workbook.active
        self.active_worksheet.title = filename

    def fill_worksheet_using_data_frame_object(self):
        for r in dataframe_to_rows(self.data_frame, index=True, header=True):
            if r[-1] != 'Anulowane':  # checking value of 'Anulowane'
                self.active_worksheet.append(r[:-1]) # avoiding column 'Anulowane'

        font = Font(size=10)
        for column in self.active_worksheet.columns:
            for cell in column:
                cell.border = self.get_borders()
                cell.font = font

        font = Font(size=10, bold=True)
        for cell in self.active_worksheet['A'] + self.active_worksheet[1]:
            cell.font = font
            #cell.style = 'Pandas'

    def fix_column_widths_in_place(self):
        """
        Changes widths of columns according to data inside them
        """
        dims = {'A': 2} #column A has no values, just index
        for row in self.active_worksheet.rows:
            for cell in row:
                if cell.value:
                    try:
                        dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)-1))
                    except:
                        pass
        for col, value in dims.items():
            self.active_worksheet.column_dimensions[col].width = value

    def get_borders(self):
        borders = Border(
            left=Side(border_style='thin', color='FF000000'),
            right=Side(border_style='thin', color='FF000000'),
            top=Side(border_style='thin', color='FF000000'),
            bottom=Side(border_style='thin', color='FF000000')
               )
        return borders

    def add_title_at_bottom(self):
        index = self.active_worksheet['B'][-1].row + 2  # find last cell with value and add 2 to find index of bottom title
        self.active_worksheet['C' + str(index)].value = 'PROTOKÓŁ PRZEKAZANIA TOWARU Z DNIA ' + self.active_worksheet['B2'].value
        self.active_worksheet['C' + str(index)].alignment = Alignment(horizontal="center")
        self.active_worksheet['C' + str(index)].font = Font(bold=True)
        self.active_worksheet.merge_cells(start_row=index, start_column=3, end_row=index, end_column=8)

    def save_excel_file(self, filename):
        self.workbook.save(FILES_FOLDER + filename + '.xlsx')

    def main(self):
        self.fill_worksheet_using_data_frame_object()
        self.fix_column_widths_in_place()
        self.add_title_at_bottom()

if __name__ == '__main__':
    data_frame = CSVData(CSV_FILENAME)
    data_frame.main()

    excel_file = CreateExcelFile(XLSX_FILENAME, data_frame=data_frame.data_frame_processed)
    excel_file.main()
    excel_file.save_excel_file(XLSX_FILENAME)