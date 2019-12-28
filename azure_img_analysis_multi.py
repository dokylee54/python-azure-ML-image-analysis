# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import json
import glob
import requests
import pprint
import matplotlib.pyplot as plt

'''

Reference:

https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa

'''

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "<Subscription Key>"
assert subscription_key

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



# open result file
f = open("test.json", 'w')



# Set image_path to the local path of an image that you want to analyze.
images = glob.glob("test_folder/test_img/*.*")


#
for img in images:
    # Read the image into a byte array
    print(img)
    image_data = open(img, "rb").read()    

    response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data
    )

    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()

    # save json result
    json.dump(analysis, f, indent=4)

    # pretty print json
    print(json.dumps(analysis, indent=4))
#


f.close()