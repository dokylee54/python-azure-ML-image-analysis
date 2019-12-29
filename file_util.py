'''
    write csv
'''
# if append_check=1 -> append, else just override
def write_list_to_csv(colname_names, row_list, filename, append_check):
    import csv
    
    ## check append_check parameter
    if(append_check): append_check = 'a'
    else: append_check = 'w'
    
    ## open file
    with open(filename, append_check, newline='') as file: 
        
        writer = csv.writer(file) 

        ## column names
        if row_list != '': 
            writer.writerow(colname_names)

        ## rows
        writer.writerows(row_list)


'''
    move file
'''
# moving a file to different directory
def move_file(filename, src_dir, des_dir):
    import shutil

    shutil.move(src_dir + filename, des_dir + filename)



if __name__ == "__main__":
    pass