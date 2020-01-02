import subprocess
import os
import glob

import parameters

def cmd_auto_execute(bashcmd):
    
    # execute cmd with subprocess.run()
    try:
        output = subprocess.run(" ".join(bashcmd.split()), stderr=subprocess.PIPE, shell=True, cwd="/Users/dokylee/Desktop/commu-lab/azure-img-processing")
    except output.stderr as e:
        print('Error: ' + e.decode("utf-8"))
    
    ## Print output
    print(output)


def get_filelist(path, keyword):
    # get keyword file list
    file_list = [f for f in next(os.walk(path))[2] if keyword in f]
    return file_list


if __name__ == '__main__':
    # argument
    bashcmd1 = "python sumup_instagram_img_info.py"
    bashcmd2 = "python azure_img_analysis_multi.py"
    bashcmd3 = "python main_instagram_analysis.py"

    '''
    #### (1.1)
    print('#'*20, bashcmd1)
    cmd_auto_execute(bashcmd1)
    print('#'*20, '\n')
    ####


    #### (1.2)
    images_before = glob.glob(parameters.images_before_path + "*.*")
    if not images_before:
        print('#'*20,'1.2', bashcmd1)
        cmd_auto_execute(bashcmd1)
        print('#'*20, '\n')
    ####
    '''


    #### (2)
    print('#'*20, bashcmd2)
    path = parameters.images_before_path
    keyword = ".jpg"

    # get file list with the ".jpg" string
    file_list = get_filelist(path, keyword)
    file_list_len = len(file_list)

    # execute command with the condition
    while file_list:
        print('progress:', len(file_list), file_list_len)
        cmd_auto_execute(bashcmd2)

        # refresh a value of the file list
        file_list = get_filelist(path, keyword)
    print('#'*20, '\n')
    ####


    #### (3)
    print('#'*20, bashcmd3)
    cmd_auto_execute(bashcmd3)
    print('#'*20, '\n')
    ####

    print('success!!...')