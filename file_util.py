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
    with open(filename, append_check, newline='', encoding='utf-8') as file: 
        
        writer = csv.writer(file) 

        ## column names
        if row_list != '': 
            writer.writerow(colname_names)

        ## row_list is not a list -> just one row
        if(len(row_list)==1):
            writer.writerow(row_list[0])

        ## row_list is a list
        else:
            writer.writerows(row_list)


'''
    move file
'''
# moving a file to different directory
def move_file(filename, src_dir, des_dir):
    import shutil

    shutil.move(src_dir + filename, des_dir + filename)


'''
    parse a filename made by 'instaloader' library
'''
def parse_filename(f):

    f_filename = f.split('/')[-1]
    
    temp = f_filename.split('!')[1]
    
    f_extension = temp[-4:]
    f_shortcode = temp[:11]
    f_category = temp[11:-4]

    return f_filename, f_shortcode, f_category, f_extension


if __name__ == "__main__":
    pass