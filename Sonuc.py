import openpyxl
import os
from openpyxl.styles import Alignment
from openpyxl.styles import Font

HEADERS = {
    "A": ("Device SN\\Test Adımları", 30),
    "B": ("Data Select Testi", 30),
    "C": ("Kalibrasyon Kontrol Testi", 30),
    "D": ("Reset Testi", 30),
    "E": ("ACC Norm ve Gyro Açılış Testi", 40),
    "F": ("Acc Döndürme Testi", 30),
    "G": ("Euler Kontrol Testi", 30),
    "H": ("Gyro Z Testi", 30),
    "I": ("Magn Norm Testi", 30),
    "J": ("UART Testi", 30),
}

def _ensure_headers(sheet):

    sheet.row_dimensions[1].height = 30
    for col, (text, width) in HEADERS.items():
        sheet.column_dimensions[col].width = width
        cell = sheet[f"{col}1"]
        if cell.value != text:
            cell.value = text
            cell.font = Font(size=14, bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center')

def find_row_by_sn(sheet, sn):
    row = 2
    while True:
        cell_value = sheet.cell(row=row, column=1).value
        if cell_value is None:
            return None  
        if cell_value == sn:
            return row
        row += 1

def write_result(sheet, sn, column, value, red=False):
    row = find_row_by_sn(sheet, sn)
    if row is None:
        #print(f"Could not write result — {sn} not found in column A")
        return
    cell = sheet.cell(row=row, column=column)
    cell.value = value
    if red:
        cell.font=Font(color="FF0000")

def Sonuc(pn, sn, base_path, results_Data_Select, results_Kalibrasyon_Kontrol, results_Reset, results_Acc_Acilis, results_Acc_Dondurme, results_Euler_Kontrol, results_Gyro_Z, result_Magn_Norm, result_conn):
    folder_path = os.path.join(base_path, "Test Sonuclari")
    os.makedirs(folder_path, exist_ok=True)
    excel_folder_path = os.path.join(folder_path, "TestSonuclari.xlsx")

    if os.path.exists(excel_folder_path):
        wb = openpyxl.load_workbook(excel_folder_path)
        sheet = wb[pn] if pn in wb.sheetnames else wb.create_sheet(pn)
    else:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = pn

    _ensure_headers(sheet)  

    row = 2
    while True:
        cell_value = sheet.cell(row=row, column=1).value

        if cell_value is None:
            sheet.cell(row=row, column=1).value = sn
            #print(f"No match found — wrote {sn} at row {row}")
            break

        if cell_value == sn:
            #print(f"Matched at row {row}: {cell_value}")
            break

        row += 1


    if results_Data_Select["is_valid"] == True:
        write_result(sheet, sn, 2, "Geçti") 
    else:
        write_result(sheet, sn, 2, "Kaldı", red=True) 

    if results_Kalibrasyon_Kontrol["calib_ctrl_success"] == True:
        write_result(sheet, sn, 3, "Geçti") 
    else:
        write_result(sheet, sn, 3, "Kaldı", red=True)

    if results_Reset["reset_result"] == True:
        write_result(sheet, sn, 4, "Geçti") 
    else:
        write_result(sheet, sn, 4, "Kaldı", red=True) 
        

    if results_Acc_Acilis == True:
        write_result(sheet, sn, 5, "Geçti") 
    else:
        write_result(sheet, sn, 5, "Kaldı", red=True) 

    if results_Acc_Dondurme["AccDondurmeSuccess"] == True:
        write_result(sheet, sn, 6, "Geçti") 
    else:
        write_result(sheet, sn, 6, "Kaldı", red=True) 


    if results_Euler_Kontrol["EulerSuccess"] == True:
        write_result(sheet, sn, 7, "Geçti") 
    else:
        write_result(sheet, sn, 7, "Kaldı", red=True) 

    if results_Gyro_Z["GyroZSucess"] == True:
        write_result(sheet, sn, 8, "Geçti") 
    else:
            write_result(sheet, sn, 8, "Kaldı", red=True) 


    if result_Magn_Norm["MagnSucess"] == True:
        write_result(sheet, sn, 9, "Geçti") 
    else:
        write_result(sheet, sn, 9, "Kaldı", red=True) 


    if result_conn == True:
        write_result(sheet, sn, 10, "Geçti") 
    else:
        write_result(sheet, sn, 10, "Kaldı", red=True) 

        

    wb.save(excel_folder_path)