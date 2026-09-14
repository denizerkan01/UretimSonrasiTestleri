import os
import sys
import time
import pyperclip
import shutil
import serial.tools.list_ports
from types import SimpleNamespace
from pywinauto.keyboard import send_keys
from pywinauto.application import Application
import general_functions as fnc

import DataSelectTesti as DataSelectTesti
import KalibrasyonKontrolTesti as KalibrasyonKontrolTesti
import S3a_ResetTesti as S3a_ResetTesti
import S3A_AccNormGyroAcilisTesti as S3A_AccNormGyroAcilisTesti
import S3A_AccDondurmeTesti as S3A_AccDondurmeTesti
import config_structure as config_structure
import S3A_EulerKontrolTesti as S3A_EulerKontrolTesti
import S3A_GyroZTesti as S3A_GyroZTesti
import S3A_MagnNorm as S3A_MagnNormTesti
from pywinauto.timings import TimeoutError as PWTimeoutError
import Role as Role
import Sonuc as Sonuc

path_arview = r"C:\Program Files\ArView\ArView.exe"
base_path = os.path.dirname(os.path.abspath(__file__)) 

def device_pn(device_folder):

    dlg = launch_arview(path_arview) 
    time.sleep(5)

    ports = list(serial.tools.list_ports.comports())
    
    target_standard = fnc.find_port("Standard", ports)
    #target_standard = fnc.find_port("Enhanced", ports)
    
    if fnc.try_connect(dlg, target_standard, "Standard"):
        print("Connect device with Standard Port")

    else:
        sys.exit("!!! Can't Connect to the Device !!!")

    dlg.child_window(title="Settings", control_type="Button").click_input()
    time.sleep(5)
    dlg.child_window(title="Copy to Clipboard", control_type="Pane").click_input()
    time.sleep(5)
    send_keys("%{F4}")
    dlg.child_window(title="Disconnect", control_type="Button").click_input()
    time.sleep(5)
    send_keys("%{F4}")

    device_info_folder = os.path.join(base_path, device_folder)

    config_path = os.path.join(device_info_folder, "config.txt")
    clipboard_content = pyperclip.paste()
    
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(clipboard_content)

    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('DevicePN'):
                return line.split('=', 1)[1].strip().strip('"')
    return None
    
def device_sn(device_folder):

    dlg = launch_arview(path_arview) 
    time.sleep(5)

    ports = list(serial.tools.list_ports.comports())
    
    target_standard = fnc.find_port("Standard", ports)
    #target_standard = fnc.find_port("Enhanced", ports)
    
    if fnc.try_connect(dlg, target_standard, "Standard"):
        print("Connect device with Standard Port")
    else:
        sys.exit("!!! Can't Connect to the Device !!!")



    dlg.child_window(title="Settings", control_type="Button").click_input()
    time.sleep(5)
    dlg.child_window(title="Copy to Clipboard", control_type="Pane").click_input()
    time.sleep(5)
    send_keys("%{F4}")
    dlg.child_window(title="Disconnect", control_type="Button").click_input()
    time.sleep(5)
    send_keys("%{F4}")

    devicesn_folder = os.path.join(base_path, device_folder)

    config_path = os.path.join(devicesn_folder, "config.txt")
    clipboard_content = pyperclip.paste()
    
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(clipboard_content)


    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('DeviceSN'):
                return line.split('=', 1)[1].strip().strip('"')
    return None
    
def launch_arview(path):
    app = Application(backend="uia").start(path)
    dlg = app.window(auto_id="FormMain", control_type="Window")
    dlg.wait("visible ready", timeout=60)
    return dlg
    
def find_limit_file(pn_dvc, file_path):

    limit_file_path = os.path.join(file_path, "Limit Dosyaları")
    limit_file_path = os.path.join(limit_file_path, f"{pn_dvc}_limitdegerleri_v00.txt")
    s3a_limitdegerleri_v00 = {}

    with open(limit_file_path, "r", encoding="utf-8") as file:
        exec(file.read(), {}, s3a_limitdegerleri_v00) 

    return s3a_limitdegerleri_v00

def create_folder(base_path):

    relative_paths = [
        "Device",
        "Test Sonuclari",
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Acc Norm Testi", "Acilis Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Acc Norm Testi", "Dondurme Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Data Select"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Euler Kontrol Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Gyro Z Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Kalibrasyon Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Magn Testi"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Reset Testi", "Hard Reset"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "Reset Testi", "Soft Reset"),
        os.path.join("UretimSonrasiTesti", "S3A", "example_folder", "UART Testi"),
    ]

    for rel_path in relative_paths:
        full_path = os.path.join(base_path, rel_path)
        #if os.path.exists(full_path):
            #print(f"Klasör '{full_path}' belirlenen konumda bulunmaktadır.")
        #else:
        os.makedirs(full_path, exist_ok=True)
            #print(f"Klasör '{full_path}' konumunda oluşturulmuştur.")

    
def s3a_main():
    
    
    device_folder_name = "Device"

    create_folder(base_path)

    sn_dvc = device_sn(device_folder_name)
    #print(sn_dvc)
    
    pn_dvc = device_pn(device_folder_name)
    #print(pn_dvc)
    
    #print("Base Path:", base_path)
    limit_data = find_limit_file(pn_dvc, base_path)
    limits = SimpleNamespace(**limit_data)
    
    time.sleep(5)

    dlg = launch_arview(limits.arview_path) 
    
    ports = list(serial.tools.list_ports.comports())
    
    target_standard = fnc.find_port("Standard", ports)
    #target_standard = fnc.find_port("Enhanced", ports)

    if not fnc.try_connect(dlg, target_standard, "Standard"):
        sys.exit("!!! Can't Connect to the Device !!!")

    #SN'ye uygun şekilde dosya aranır yoksa yeni dosya açılır
    uretim_folder_path = os.path.join(base_path, r"UretimSonrasiTesti")
    example_folder_path = os.path.join(uretim_folder_path, r"S3A")
    
    s3a_example_folder = os.path.join(example_folder_path, r"example_folder")
    s3a_sn_folder = os.path.join(example_folder_path, sn_dvc)

    try:
        shutil.copytree(s3a_example_folder, s3a_sn_folder)
    except FileExistsError:
        print(f"Dosya '{sn_dvc}' klasörde oluşturulmuştur")
    #

    
        #deneme github
    
    #Test - 1: Data Select Kontrol Testi
    print("***Test 1: Data Select Kontrol Testi")
    config_structure.config_structure_data_select_s3a(dlg, limits.checkbox_states_general)
    results_Data_Select = DataSelectTesti.DataSelectTest(dlg, sn_dvc, example_folder_path, limits.data_select_folder, limits.expected_columns_general, limits.sleep_time_data_select)
    print("***Test 1: Data Select Kontrol Testi TAMAMLANDI")
    
    # Test - 2: Kalibrasyon Kontrol Testi
    print("***Test 2: Kalibrasyon Kontrol Testi")
    config_structure.config_structure_kalibrasyon_kontrol_s3a(dlg, limits.checkbox_states_general)
    results_Kalibrasyon_Kontrol = KalibrasyonKontrolTesti.KalibrasyonKontrolTesti(dlg, example_folder_path, sn_dvc, limits.firmware_version, limits.device_name, limits.ref_matrix_acc, limits.ref_matrix_gyro, limits.ref_matrix_magn, limits.kalibrasyon_kontrol_folder)
    print("***Test 2: Kalibrasyon Kontrol Testi TAMAMLANDI")
    
    # Test 3: Reset Testi
    print("***Test 3: Reset Testi")
    config_structure.config_structure_reset_s3a(dlg, limits.checkbox_states_general)
    results_Reset = S3a_ResetTesti.S3a_ResetTesti(dlg, sn_dvc, example_folder_path, limits.hard_reset_folder, limits.soft_reset_folder, limits.sleep_time_reset_testi)
    print("***Test 3: Reset Testi TAMAMLANDI")
    
    # Test 4: ACC Norm ve Gyro Açılış Testi
    print("***Test 4: Acc Norm ve Gyro Açılış Testi")
    config_structure.config_structure_acc_norm_gyro_acilis_s3a(dlg, limits.checkbox_states_general)
    results_Acc_Acilis = S3A_AccNormGyroAcilisTesti.S3A_AccNormGyroAcilisTesti(dlg, sn_dvc, example_folder_path, limits.acc_acilis_folder, limits.acc_acilis_successfull_needed, limits.max_ok_acc_norm_value, limits.min_ok_acc_norm_value, limits.max_best_acc_norm_value, limits.min_best_acc_norm_value, limits.sleep_time_acc_norm_gyro_acilis)
    print("***Test 4: Acc Norm ve Gyro Açılış Testi TAMAMLANDI")
    ##
    #Test 5: Acc Döndürme Testi
    print("***Test 5: Acc Döndürme Testi")
    config_structure.config_structure_acc_dondurme_s3a(dlg, limits.checkbox_states_general)
    results_Acc_Dondurme = S3A_AccDondurmeTesti.S3A_AccDondurmeTesti(dlg, sn_dvc, example_folder_path, limits.acc_dondurme_folder, 0.05, 0.2, limits.sleep_time_acc_dondurme)
    print("***Test 5: Acc Döndürme Testi TAMAMLANDI")
    
    #Test 6: Euler Kontrol Testi
    print("***Test 6: Euler Kontrol Testi")
    config_structure.config_structure_euler_kontrol_s3a(dlg, limits.checkbox_states_general)
    results_Euler_Kontrol = S3A_EulerKontrolTesti.S3A_EulerKontrolTesti(dlg, sn_dvc, example_folder_path, limits.euler_kontrol_folder, limits.euler_kontrol_folder, limits.max_roll_value, limits.min_roll_value, limits.max_pitch_value, limits.min_pitch_value, limits.sleep_time_euler_kontrol)
    print("***Test 6: Euler Kontrol Testi TAMAMLANDI")
    
    #Test 7: Gyro Z Testi
    print("***Test 7: Gyro Z Testi")
    config_structure.config_structure_gyroz_s3a(dlg, limits.checkbox_states_magn)
    results_Gyro_Z = S3A_GyroZTesti.S3A_GyroZTesti(dlg, sn_dvc, example_folder_path, limits.gyro_z_folder, limits.sleep_time_gyroz)
    print("***Test 7: Gyro Z Testi TAMAMLANDI")
    
    #Test 8: Magn Norm Testi
    print("***Test 8: Magn Norm Testi")
    config_structure.config_structure_magn_s3a(dlg, limits.checkbox_states_magn)
    result_Magn_Norm = S3A_MagnNormTesti.S3A_MagnNormTesti(dlg, sn_dvc, example_folder_path, limits.magn_norm_folder, limits.sleep_time_magn)
    print("***Test 8: Magn Norm Testi TAMAMLANDI")
    
    #Test 9: UART Testi
    print("***Test 9: UART Testi")
    dlg.child_window(title="Disconnect", control_type="Button").click_input()
    
    ports = list(serial.tools.list_ports.comports())
    target_enhanced = fnc.find_port("Enhanced", ports)
    target_standard = fnc.find_port("Standard", ports)

    result_UART = False
    
    if fnc.try_connect(dlg, target_enhanced, "Enhanced"):
        #print("UART ile bağlanıldı")
        result_UART = True
    else:
        #print("UART ile bağlanılamadı")
        result_UART = False

    dlg.child_window(title="Disconnect", control_type="Button").click_input()
    
    if fnc.try_connect(dlg, target_standard, "Standard"):
        #print("Standart Port ile bağlanıldı")
        result_232 = True
    else:
        #print("Standart Port ile bağlanılamadı")
        result_232 = False

    result_conn = result_UART and result_232
    print("***Test 9: UART Testi TAMAMLANDI")
    Sonuc.Sonuc(pn_dvc, sn_dvc, base_path, results_Data_Select, results_Kalibrasyon_Kontrol, results_Reset, results_Acc_Acilis, results_Acc_Dondurme, results_Euler_Kontrol, results_Gyro_Z, result_Magn_Norm, result_conn)
    print("Test Sonuçları Sonuç Dokümanına Yazılmıştır")            
            
       
if __name__ == "__main__":
    s3a_main()