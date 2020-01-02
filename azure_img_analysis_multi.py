# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import json
import glob
import requests
import pprint
import matplotlib.pyplot as plt

import file_util
import parameters

'''

- Reference:

https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa


- Response format example:

{
    "categories": [
        {
            "name": "abstract_",
            "score": 0.00390625
        },
        {
            "name": "outdoor_",
            "score": 0.01171875,
            "detail": {
                "landmarks": []
            }
        },
        {
            "name": "text_sign",
            "score": 0.29296875
        }
    ],
    "color": {
        "dominantColorForeground": "Brown",
        "dominantColorBackground": "Brown",
        "dominantColors": [
            "Brown"
        ],
        "accentColor": "3F2C69",
        "isBwImg": false,
        "isBWImg": false
    },
    "description": {
        "tags": [
            "cabinet",
            "indoor",
            "table",
            "sitting",
            "kitchen",
            "truck",
            "counter",
            "plane",
            "large",
            "oven",
            "white",
            "parked",
            "airplane"
        ],
        "captions": [
            {
                "text": "a plane sitting on top of a counter",
                "confidence": 0.2861623561670009
            }
        ]
    },
    "requestId": "3e7c405b-e456-4070-9609-a329678ec9fa",
    "metadata": {
        "width": 1080,
        "height": 720,
        "format": "Jpeg"
    }
}


'''

if __name__ == "__main__":

    # Replace 'parameters.subscription_key' with your valid subscription key.
    subscription_key = parameters.subscription_key
    assert subscription_key # check if subscription_key exists -> if not, exit

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the "westus" region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"

    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                'Content-Type': 'application/octet-stream'}

    params     = {'visualFeatures': 'Categories,Description,Color',
                    'details': 'Landmarks'}


    # Set 'images' to the local path of an image that you want to analyze.
    images = glob.glob(parameters.images_before_path + "*.*")

    # count filenumber
    f_num = 1

    ####
    for img in images:

        if(f_num % 1000 == 0):
            print('progress:', f_num)

        try:

            # Read the image into a byte array
            print(img)

            # parse filename
            f_filename, f_shortcode, f_category, _ = file_util.parse_filename(img)            

            # read the image
            image_data = open(img, "rb").read()    

            response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data
            )

            # raise a error if status code is not '200 OK'
            response.raise_for_status()

            print('status code:', response.status_code)

            # The 'analysis' object contains various fields that describe the image. The most
            # relevant caption for the image is obtained from the 'description' property.
            analysis = response.json()


            ### specific analysis (you can **change** this part)

            # pretty print json
            # print(json.dumps(analysis, indent=4))

            # analysis list
            img_colorlist = analysis['color']['dominantColors']
            img_categorylist = analysis['categories']
            img_taglist = analysis['description']['tags']

            # empty handling(1) - if colorlist is empty
            if not img_colorlist:   
                foreground_color = analysis['color']['dominantColorForeground']
                background_color = analysis['color']['dominantColorBackground']
                img_colorlist = [foreground_color, background_color]


            # analysis list -> string
            img_color = ', '.join(img_colorlist)
            img_tag = ', '.join(img_taglist)

            # empty handling(1) - if colorlist is empty
            if not img_taglist:
                img_tag = 'tag list is empty'

            # initialize the variables used in image analysis
            img_food = img_animal = img_person = 0

            ## check the list of category
            for c in img_categorylist:

                # check: food?
                if ('food' in c):
                    img_food = 1
                    
                # check: animal?
                if ('animal' in c):
                    img_animal = 1

                # check: person?
                if ('person' in c) or ('people' in c):
                    img_person = 1
            ##


            ## check the list of tag
            for t in img_taglist:

                # check: food?
                if ('food' in t):
                    img_food = 1
                    
                # check: animal?
                if ('animal' in t):
                    img_animal = 1

                # check: person?
                if ('person' in t) or ('people' in t):
                    img_person = 1
            ##


            # combine all info
            img_analysislist = [f_num, f_filename, f_shortcode, img_food, img_animal, img_person, img_color, img_tag]

            ###


            # move this img to after-analysis folder
            file_util.move_file(f_filename, parameters.images_before_path, parameters.images_after_path)

            # write in a csv file
            colname_names = ''
            if f_num == 1:
                colname_names = ['num', 'file name', 'shortcode', 'food[1] / non-food[0]', 'animal[1] / non-animal[0]', 
                                'person[1] / non-person[0]', 'dominant color', 'all tags'] 
                
            row_list = [img_analysislist]
            file_util.write_list_to_csv(colname_names, row_list, parameters.f2_path, 1) 

            # increase filenumber
            f_num += 1

        except:
            print('ERROR:', img)

    ####