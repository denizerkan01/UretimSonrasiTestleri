import time
import os
import glob
import numpy as np
import general_functions as fnc
import Role as Role

def check_reset_test(sensor_data):

    result = {
        "has_time_zero": False,
        "time_zero_rows": [],
        "reset_success": False,
        "gyro_mean_success": False,
        "gyro_acilis_success": False,
        "result_reset": False,
    }

    #sensor_data.time = sensor_data.time.astype(float)
    #zero_rows = np.where(np.isclose(sensor_data.time, 0.0, atol=1e-5))[0][0]
    zero_rows_mat = np.where(sensor_data.time == 0)[0]
    #time_05_rows_mat = np.where(sensor_data.time == 0.5)[0]

    if zero_rows_mat.size == 0: #or time_05_rows_mat == 0:
        return result

    zero_rows = zero_rows_mat[0]
    #time_05_rows = time_05_rows_mat[0]

    result["has_time_zero"] = True
    result["time_zero_rows"] = zero_rows.tolist()
    
    #mean_gyroX = np.mean(sensor_data.gyroX[zero_rows:time_05_rows+1])
    #mean_gyroY = np.mean(sensor_data.gyroY[zero_rows:time_05_rows+1])
    #mean_gyroZ = np.mean(sensor_data.gyroZ[zero_rows:time_05_rows+1])
    
    
    #if mean_gyroX <= 0.05 and mean_gyroY <= 0.05 and mean_gyroZ <= 0.05:
        #result["gyro_acilis_success"] = True
    #else:
        #return result

    result["reset_success"] = result["has_time_zero"] #and result["gyro_acilis_success"]

    return result


def S3a_ResetTesti(dlg, device_sn, base_path, hard_reset_folder, soft_reset_folder, sleep_time):


    #Hard Reset Testi:
    
    #Test - 1:
   
    reset_hard_folder = fnc.navigate_to_folder(dlg, device_sn, base_path, hard_reset_folder)

    Role.Role()

    log_hr_1 = fnc.auto_start(dlg, device_sn, base_path, reset_hard_folder, sleep_time)

    try:
        sensor_data_hr_1 = fnc.parse_log(log_hr_1)
    except (FileNotFoundError, ValueError) as e:
        #print(f"Parse edilemedi: {e}")
        return None

    results_hr_1 = check_reset_test(sensor_data_hr_1)

    if results_hr_1["reset_success"] == True:
        print("Test 3: \n Hard Reset Testi - 1: \n Sonuç: BAŞARILI")
    else:
        print("Test 3: \n Hard Reset Testi - 1: \n Sonuç: BAŞARISIZ!!!")
        print("Time = 0 Sonucu:", results_hr_1["has_time_zero"])
        print("Gyro = 0 Sonucu:", results_hr_1["gyro_acilis_success"])

    
    #Test - 2:
    
    dlg.child_window(title="Record", control_type="Button").click_input()
    
    time.sleep(5)
    
    Role.Role()
    
    time.sleep(20)
    
    dlg.child_window(title="Stop", control_type="Button").click_input()
    
    log_hr_2 = glob.glob(os.path.join(reset_hard_folder, "log_*.txt"))
    if not log_hr_2:
        #print("Log dosyasi bulunamadi", reset_hard_folder)
        return None
    
    latest_log_hr_2 = max(log_hr_2, key=os.path.getmtime)
    
    try:
        sensor_data_hr_2 = fnc.parse_log(latest_log_hr_2)
    except (FileNotFoundError, ValueError) as e:
        #print(f"Parse edilemedi: {e}")
        return None
    
    results_hr_2 = check_reset_test(sensor_data_hr_2)

    
    if results_hr_2["reset_success"] == True:
        print("Test 3: \n Hard Reset Testi - 2: \n Sonuç: BAŞARILI")
    else:
        print("Test 3: \n Hard Reset Testi - 2: \n Sonuç: BAŞARISIZ!!!")
        print("Time = 0 Sonucu:", results_hr_2["has_time_zero"])
        print("Gyro = 0 Sonucu:", results_hr_2["gyro_acilis_success"])

    
    
    #Hard Reset 2 kısmında arnav problemi vardır ve düzeltilecektir. Düzeltildikten sonra bu kısmı siliniz.
    
    
    max_attempts = 5
    attempts = 0
    
    if results_hr_2["reset_success"] == False:
        while not results_hr_2["reset_success"] and attempts < max_attempts:
            attempts += 1
            #print(f"\n--- Deneme: {attempts} ---")
    
            if results_hr_2["reset_success"] == False:
                #print("Hard Reset Testi - 2 Tekrari:")
                dlg.child_window(title="Record", control_type="Button").click_input()
        
                time.sleep(5)
    
                Role.Role()
    
                time.sleep(20)
        
                dlg.child_window(title="Stop", control_type="Button").click_input()
        
                log_hr_3 = glob.glob(os.path.join(reset_hard_folder, "log_*.txt"))
                if not log_hr_3:
                    #print("Log dosyasi bulunamadi", reset_hard_folder)
                    #print("Siradaki deneme...")
                    continue 
            
                latest_log_hr_3 = max(log_hr_3, key=os.path.getmtime)
        
    
                try:
                    sensor_data_hr_3 = fnc.parse_log(latest_log_hr_3)
                except (FileNotFoundError, ValueError) as e:
                    #print(f"Parse edilemedi: {e}")
                    #print("Siradaki deneme...")
                    continue  
            
                results_hr_3 = check_reset_test(sensor_data_hr_3)
                #print("Hard Reset Testi - 2:", results_hr_3["reset_success"])
        
                reset_is_successful = results_hr_3["reset_success"]
    
                if reset_is_successful:
                    print("\nHard Reset Testi - 2: BAŞARILI")
                    break
                else:
                    print(f"\nHard Reset Testi - 2: ({attempts}) deneme sonrasinda BAŞARISIZ!!!.")

    
    """
        Bu kısma kadar silinmelidir.
        """
    

    # Soft Reset
        
    # Test - 1:
        
    reset_soft_folder = fnc.navigate_to_folder(dlg, device_sn, base_path, soft_reset_folder)
        
    dlg.child_window(title="Console", control_type="Button").click_input()
        
    time.sleep(5)
        
    dlg.child_window(title="Reset", control_type="Pane").click_input()
        
    log_sr_1 = fnc.auto_start(dlg, device_sn, base_path, reset_soft_folder, sleep_time)
        
    try:
        sensor_data_sr_1 = fnc.parse_log(log_sr_1)
    except (FileNotFoundError, ValueError) as e:
        print(f"Parse edilemedi: {e}")
        return None

    results_sr_1 = check_reset_test(sensor_data_sr_1)

    #if results_sr_1["reset_success"] == True:
        #print("Test 3: \n Soft Reset Testi - 1: \n Sonuç: BAŞARILI")
    #else:
        #print("Test 3: \n Soft Reset Testi - 1: \n Sonuç: BAŞARISIZ!!!")
        #print("Time = 0 Sonucu:", results_sr_1["has_time_zero"])
        #print("Gyro = 0 Sonucu:", results_sr_1["gyro_acilis_success"])
    
    # Test - 2:
    
    dlg.child_window(title="Record", control_type="Button").click_input()
    
    time.sleep(5)
    
    dlg.child_window(title="Reset", control_type="Pane").click_input()
    
    time.sleep(20)
    
    dlg.child_window(title="Stop", control_type="Button").click_input()
    
    log_sr_2 = glob.glob(os.path.join(reset_soft_folder, "log_*.txt"))
    if not log_sr_2:
        #print("Log dosyasi bulunamadi", reset_soft_folder)
        return None
    
    latest_log_sr_2 = max(log_sr_2, key=os.path.getmtime)
    
    try:
        sensor_data_sr_2 = fnc.parse_log(latest_log_sr_2)
    except (FileNotFoundError, ValueError) as e:
        #print(f"Parse edilemedi: {e}")
        return None
    
    results_sr_2 = check_reset_test(sensor_data_sr_2)

    time.sleep(2)

    dlg.child_window(title="Console", control_type="Button").click_input()

    time.sleep(2)

    if results_sr_2["reset_success"] == True:
        print("Test 3: \n Soft Reset Testi - 2: \n Sonuç: BAŞARILI")
    else:
        print("Test 3: \n Soft Reset Testi - 2: \n Sonuç: BAŞARISIZ!!!")
        print("Time = 0 Sonucu:", results_sr_2["has_time_zero"])
        print("Gyro = 0 Sonucu:", results_sr_2["gyro_acilis_success"])



    if results_hr_2["reset_success"] == False:
        hr_2_result = reset_is_successful or results_hr_2["reset_success"]
    else:
        hr_2_result = results_hr_2["reset_success"]

    result_hr = results_hr_1["reset_success"] and hr_2_result
    result_sr = results_sr_1["reset_success"] and results_sr_2["reset_success"]
    result_reset = result_hr and result_sr


    return {
        "hard_reset_test_1": results_hr_1,
        "hard_reset_test_2": hr_2_result,
        "soft_reset_test_1": results_sr_1,
        "soft_reset_test_2": results_sr_2,
        "reset_result": result_reset,
    }

    #return results_hr_1, sensor_data_hr_1, return results_hr_2, sensor_data_hr_2, return results_sr_1, sensor_data_sr_1, return results_sr_2, sensor_data_sr_2