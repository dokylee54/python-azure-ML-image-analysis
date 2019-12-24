import json
import glob
import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Replace <Subscription Key> with your valid subscription key.
subscription_key = "21cb274b0d724d51a80bd0163173f1f3"
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

# open result file
f = open("C:\\Users\\dokyl\\바탕 화면\\test\\instalooter result\\제천\\cog_results.json", 'w')

# Set image_path to the local path of an image that you want to analyze.
images = glob.glob("C:\\Users\\dokyl\\바탕 화면\\test\\instalooter result\\제천\\*.*")

for image_path in images:

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
       analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    json.dump(analysis, f, indent=4)
    print(analysis)
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    # Display the image and overlay it with the caption.
    image = Image.open(BytesIO(image_data))
    plt.imshow(image)
    plt.show()
    plt.axis("off")
    _ = plt.title(image_caption, size="x-large", y=-0.1)

f.close()