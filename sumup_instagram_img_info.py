import glob
import sys

import parameters
import file_util


'''

- instagram crawling tool: 
        'instaloader'

- Command: 
        instaloader --login {instagram id} --password {instagram password}
        --count=30000 
        --filename-pattern={date_utc}!{shortcode} 
        --no-videos --geotags --comments 
        --post-metadata-txt="date_utc:{date_utc}\ncaption:{caption}\nlikes:{likes}\ncomments:{comments}" "#seoul"

- Reference:
        https://instaloader.github.io/

'''


def separate_img_imginfo(images_before):

    for f in images_before:

        try:
        
            f_filename, _, f_category, f_extension = file_util.parse_filename(f)

            if f_extension != '.jpg': continue

            # if file is a image
            if f_category == '':
                file_util.move_file(f_filename, parameters.images_info_before_path, parameters.images_before_path) 
                continue

            if f_category.split('_')[1].isdigit():
                file_util.move_file(f_filename, parameters.images_info_before_path, parameters.images_before_path) 

        except:
            print('ERROR:', f)



def get_txt_info(info, filename):

    # read a file
    with open(info, 'r') as f:
        data = f.read()

        # data format : date_utc:{date_utc}\ncaption:{caption}\nlikes:{likes}\ncomments:{comments}
        parsed_data = data.split('\\n')

        f_date = parsed_data[0].split('date_utc')[1][1:]
        f_like = parsed_data[2].split('likes')[1][1:]
        f_comment = parsed_data[3].split('comments')[1][1:].split('\n')[0]
            
        # count the number of '#' in caption
        f_hashtag = parsed_data[1].count('#')

    # move to 'after' folder
    file_util.move_file(filename, parameters.images_info_before_path, parameters.images_info_after_path)

    return f_date, f_like, f_comment, f_hashtag

def get_gps_info(info, filename):
    # read a file
    with open(info, 'r') as f:
        data = f.readlines()
        f_gps = data[0].split('\n')[0]
        f_gps_detail = data[1]

    # move to 'after' folder
    file_util.move_file(filename, parameters.images_info_before_path, parameters.images_info_after_path)

    return f_gps, f_gps_detail
    

def get_each_imginfo_list(images_info, f_num):
    std_shortcode = ''

    # initialize info list
    f_gps = f_gps_detail = ''

    
    for info in images_info:

        try:

            # parsed 'info'
            f_filename, f_shortcode, f_category, f_extension = file_util.parse_filename(info)

            # only need a txt file
            if (f_extension != '.txt') or ('old' in f_category): 

                # move to 'after' folder
                file_util.move_file(f_filename, parameters.images_info_before_path, parameters.images_info_after_path)
                continue

            ## [File Type1] {date}!{shortcode}.txt
            if f_category == '':
                # if this is the 1st iteration
                if std_shortcode == '': 
                    std_shortcode = f_shortcode
                    f_date, f_like, f_comment, f_hashtag = get_txt_info(info, f_filename)

                elif (std_shortcode != '') and (std_shortcode == f_shortcode):
                    f_date, f_like, f_comment, f_hashtag = get_txt_info(info, f_filename)
                        
            ##


            ## [File Type2] {date}!{shortcode}_location.txt
            if f_category == '_location':
                # if this is the 1st iteration
                if std_shortcode == '':
                    std_shortcode = f_shortcode
                    f_gps, f_gps_detail = get_gps_info(info, f_filename)

                elif (std_shortcode != '') and (std_shortcode == f_shortcode):
                    f_gps, f_gps_detail = get_gps_info(info, f_filename)

            ##

            

        except:
            print('ERROR:', info)

    # combine a whole extracted information with 'imginfo_list'
    # imginfo_list = [filenumber, shortcode, date, like, comment, hashtag, gps, gps detail]
    imginfo_list = [f_num, std_shortcode, f_date, f_like, f_comment, f_hashtag, f_gps, f_gps_detail]

    return imginfo_list


if __name__ == "__main__":

    # Set 'images_info' to the local path of an image's information that you want to analyze.
    images_info = glob.glob(parameters.images_info_before_path + "*.*")


    # separate img and imginfo into different directory
    images_before = glob.glob(parameters.images_before_path + "*.*")
    if not images_before:
        separate_img_imginfo(images_info)
        print('separated... please run this code again')
        sys.exit(0)

        
    # count filenumber
    f_num = 1

    # for printing progress
    cnt = 1

    while images_info:

        if(cnt % 1000 == 0):
            print('progress:', cnt)
    
        # get a list of the related information filenames for each image
        imginfo_list = get_each_imginfo_list(images_info, f_num)
        # print(imginfo_list)

        # refresh images_info
        images_info = glob.glob(parameters.images_info_before_path + "*.*")   

        # write in a csv file
        colname_names = ''
        if f_num == 1:
            colname_names = ['num', 'shortcode', 'date', 'like', 'comment', 'hashtag', 'gps', 'gps detail']
            
        row_list = [imginfo_list]
        file_util.write_list_to_csv(colname_names, row_list, parameters.f1_path, 1)    

        # increase filenumber
        f_num += 1
        
        cnt += 1



