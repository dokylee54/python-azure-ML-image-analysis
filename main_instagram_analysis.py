import parameters
import file_util

import pandas as pd

'''
- usage:
        1.1 'python sumup_instagram_img_info.py'

        1.2 again 'python sumup_instagram_img_info.py', 
            if output instruction is given like 'separated... please run this code again'

        2. 'python azure_img_analysis_multi.py'

        3. 'python main_instagram_analysis.py'

'''


if __name__=='__main__':

    # open result file
    df1 = pd.read_csv(parameters.f1_path, index_col=None, header=0).fillna('-')
    df2 = pd.read_csv(parameters.f2_path, index_col=None, header=0).fillna('-')

    # # compare df2's shortcode with df1's shortcode 
    # df_list = []

    # header list & header parameter for 'to_csv' function
    df_colnames = list(df2) + list(df1)[2:] 
    header_check = 1

    ####
    for df2_idx in range(df2.shape[0]):

        # for printing progress
        if df2_idx % 100 == 0:
            print("progress:", df2_idx, "/", df2.shape[0])

        df2_rowlist = df2.iloc[df2_idx].tolist()
        df2_shortcode = df2_rowlist[2]
        
        ###
        for df1_idx in range(df1.shape[0]):

            df1_rowlist = df1.iloc[df1_idx].tolist()
            df1_shortcode = df1_rowlist[1]

            if df2_shortcode == df1_shortcode:

                df2_rowlist+=df1_rowlist[2:]    # merge

                if df2_idx == 1:    # if it is the first row
                    header_check = False

                df = pd.DataFrame([df2_rowlist], columns =df_colnames)    # dataframe
                df.to_csv(parameters.f_path, index=False, header=header_check, encoding='utf-8-sig', mode='a')   # append

                continue

            else:
                print("no matching", "*"*20)

                
        ###
    ####



    # # combined list -> csv file
    # df_colnames = list(df2) + list(df1)[2:] # header list
    # df = pd.DataFrame(df_list, columns =df_colnames)    # dataframe
    # df.to_csv(parameters.f_path, index=False, header=1, encoding='utf-8-sig', mode='a')   # append

    print('merge the csv files successfully...')
