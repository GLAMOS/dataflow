import os
import pandas as pd

doi_release_file = r'V:\GlacioBaseData\VolumeChange\_mhuss_results\results_20251202\dV_DOI2025_allcomb.csv'
wgms_submission_file = r'V:\GlacioBaseData\VolumeChange\wgms_submission_file_change.txt'

rows = []

with open(doi_release_file, "r",encoding="utf-8") as f:
    next(f)  # skip line 1
    next(f)  # skip line 2
    next(f)  # skip line 3
    next(f)  # skip line 4
    next(f)  # skip line 5
    next(f)  # skip line 6
    next(f)  # skip line 7
    next(f)  # skip line 8

    for line in f:
        elements = line.strip().split(',')  # split on whitespace
        rows.append(elements)

df = pd.DataFrame(rows) # build panda dataframe from all rows

# Rename all rows
df = df.rename(columns={0: 'SGI-ID', 1: 'source-start', 2:'source-end', 3:'date_start',4:'date_end',5:'A_start',6:'outline_start',7:'A_end',8:'outline_end',9:'dV',10:'dV_mean',11:'Bgeod',12:'sigma',13:'coverage',14:'rho_dv',15:''})


#df_wgms = {'glacier_name', 'glacier-id','begin_outline_id','end_outline_id','begin_date','begin_date_unc','end_date','end_date_unc','area m²','elevation_change','elevation_change_unc','volume_change','volume_change_unc.','begin_platform','begin_method','end_platform','end_method','investigators','agencies','references','remarks'}

list = df.values.tolist()

with open(wgms_submission_file, 'w', encoding='utf8') as file:
    for element in list:
        glacier_name = element[15]
        glacier_id = element[0]
        begin_outline_id = element[6]
        end_outline_id = element[8]

        begin_year = element[3][0:4]
        if element[3][4:8] == str(9999):
            begin_date = begin_year + '-' + '09-01'
            begin_date_unc = '30'
        else:
            begin_date = begin_year + '-' + element[3][4:6] + '-' + element[3][6:8]
            begin_date_unc = '0'

        end_year = element[4][0:4]
        if element[4][4:8] == str(9999):
            end_date = end_year + '-' + '09-01'
            end_date_unc = '30'
        else:
            end_date = end_year + '-' + element[4][4:6] + '-' + element[4][6:8]
            end_date_unc = '0'

        del begin_year
        del end_year

        period = int(element[4][0:4]) - int(element[3][0:4])

        area_t0 = float(element[5])
        area_t1 = float(element[7])
        area_mean_m2 = int(((area_t0 + area_t1) / 2) * 1000000) # area in [m2]
        area = area_mean_m2

        dV_m3 = int(float(element[9]) * 1000000000)
        elevation_change = round(dV_m3 / area_mean_m2,2)
        sigma = float(element[12])
        elevation_change_unc = round((sigma / 0.85) * period,2)

        volume_change = dV_m3
        volume_change_unc = round((sigma / 0.85) * period * area_mean_m2,2)

        print(area_mean_m2, dV_m3, sigma)

        begin_platform = 'air'
        begin_method = 'photo'
        end_platform = 'air'
        end_method = 'photo'
        investigators = 'Matthias Huss (1)'
        agencies ='1. ETH Zürich > VAW'
        references = '10.18750/volumechange.2025.r2025'
        remarks = ''

        # prepare data to write to file
        data = [glacier_name, glacier_id, str(begin_outline_id),str(end_outline_id), str(begin_date), str(begin_date_unc), str(end_date), str(end_date_unc), str(area), str(elevation_change), str(elevation_change_unc), str(volume_change), str(volume_change_unc),begin_platform,begin_method,end_platform,end_method, investigators, agencies, references, remarks]
        line = ','.join(data)

        # write line to file
        file.write(line+'\n')




