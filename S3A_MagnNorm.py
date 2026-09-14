import time
import numpy as np
import general_functions as fnc
import S3a_ResetTesti as S3a_ResetTesti
import Role as Role

def check_magn_norm(sensor_data):
    result = {
        "reset_success": False,       
        "MagnSucess": False, 
            }

    check_time_0 = S3a_ResetTesti.check_reset_test(sensor_data)
        
    if not check_time_0.get("reset_success", False):
        print("Reset Testi: BAŞARISIZ!!! Magn Norm Testi Yapılamaz!")
        return result
            
    result["reset_success"] = True

    magnX = sensor_data.magnX
    magnY = sensor_data.magnY
    magnZ = sensor_data.magnZ
    
    magn_norm = np.sqrt(magnX ** 2 + magnY ** 2 + magnZ ** 2)
    max_magn_norm = np.max(magn_norm)
    min_magn_norm = np.min(magn_norm)

    if (0.95 <= np.mean(magn_norm)  <= 1.05) and max_magn_norm <= 1.05 and min_magn_norm >= 0.95:
        result["MagnSucess"]= True
        #print("Test 11: \n Magn Norm Testi: \n Sonuç: BAŞARILI")
        #print("Max Value of Magn Norm:", max_magn_norm)
        #print("Min Value of Magn Norm:", min_magn_norm)
    else:
        result["MagnSucess"]= False
        #print("Test 11: \n Magn Norm Testi: \n Sonuç: BAŞARISIZ")
        #print("Max Value of Magn Norm:", max_magn_norm)
        #print("Min Value of Magn Norm:", min_magn_norm)

    return result



def S3A_MagnNormTesti(dlg, device_sn, base_path, sub_folder, sleep_time):

    fnc.navigate_to_folder(dlg, device_sn, base_path, sub_folder)
        
    

    time.sleep(1)
    print("Sistemi 1. Konuma Getirin")
    print("Masadan uzak şekilde sistemi tutun")
    time.sleep(3)
    print("Kayıt başladıktan sonra Magn Norm değeri 1 olan ortamda sırasıyla sistemi\n 1, 2, 3, 4, 5 ve 6.konumu getirin")
    
    Role.Role()
    
    log_magn_norm_folder = fnc.auto_start(dlg, device_sn, base_path, sub_folder, sleep_time)

    try:
        sensor_data_magn_norm = fnc.parse_log(log_magn_norm_folder)
    except (FileNotFoundError, ValueError) as e:
        #print(f"Parse edilemedi: {e}")
        return None

        
    result_magn_norm = check_magn_norm(sensor_data_magn_norm)

    return result_magn_norm