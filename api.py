# Part 3: (7 points) Model inference server and deployment

from flask import Flask, request
from PIL import Image
import tensorflow as tf
import numpy as np
import io

app = Flask(__name__)

model = tf.keras.models.load_model('models/alt_lenet.keras')

# A model summary endpoint GET /summary providing metadata about the model.
# Note: This endpoint must be accept requests to: GET /summary and it must return a JSON response.
@app.route('/summary', methods=['GET'])
def model_summary():
   return {
      "version": "v1",
      "name": "alt_lenet",
      "description": "Classify buildings as burned or not burned. Model utilizing Alternate-Lenet-CNN architecture, with accuracy of 0.9667 on test data",
      "number_of_parameters": 2601153
   }

# An inference endpoint POST /inference that can perform classification on an image.
# Note: This endpoint must accept requests to POST /inference. It must accept a binary message payload containing the image without any preprocessing to classify, and it must return a JSON response containing the results of the inference. The JSON response must be a JSON object (not a list) and include a top-level attribute, prediction, with values damage or no_damage. For example: { "prediction": "damage"}. The grader is automated and will be looking for these exact values so be sure to review your code carefully and make sure it conforming to the requirements (and use the grader code, see below).
@app.route('/inference', methods=['POST'])
def perform_classification():
    # check if the post request has the file part
    if 'image' not in request.files:
        return '{"error": "Invalid request; pass a binary image file as a multi-part form under the image key."}'
    
    try:
        # preprocess
        # get the data in form of filestorage object
        # filestorage.stream returns a file-like object, which Image.open takes as input parameter
        data = request.files['image'] 
        img = Image.open(data)
        img = img.resize((128, 128)) # resize to params of trained model
        img_array = np.array(img) / 255.0 
        img_list = np.expand_dims(img_array, axis=0) # to specify one sample in batch
    except Exception as e:
        return {"error": f"Could not process the binary image; details: {e}"}, 404


    try:
        res = model.predict(img_list)
    except Exception as e:
        return {"error": f"Issues after model predict was called: {e}"}, 420

    score = float(res[0])
    retval = "damage" if score < 0.5 else "no_damage"
    return { "prediction": retval}

# start the development server
if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0')

    