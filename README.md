This document will provide instructions for starting and stopping the inference server while using the docker-compose file. 
Examples of how to make requests to your inference server will also be provided.

Required files:
    - Dockerfile
    - docker-compose.yml
    - api.py
    - /models
        - alt_lenet.keras
    - /data

Once files have been downloaded to your repository, run:
    docker-compose up

This will start the inference server on port 5000. To test a request from inference server you can run:
    curl localhost:5000/summary

    And the expected output should be the inference server description:
    {
      "description": "Classify buildings as burned or not burned. Model utilizing Alternate-Lenet-CNN architecture, with accuracy of 0.9667 on test data",
      "name": "alt_lenet",
      "number_of_parameters": 2601153,
      "version": "v1"
    }


There are two api endpoints in our server:
        
    '/summary'
        - GET request, returns metadata about the model in JSON format
        
    '/inference'
        - POST request, accepting a binary payload message as input, returns JSON formatted "prediction" with values "damage" or "no_damaged"
        - Endpoint uses flask.Request.files to handle file upload, expecting payload in "image" field
        - Data will be preprocessed to fit parameters that alt_lenet.keras model was trained on

    
        
        










