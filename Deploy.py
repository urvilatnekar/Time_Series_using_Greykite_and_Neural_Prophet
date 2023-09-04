# Importing required packages
from flask import Flask
from flask_restful import Resource, Api #This package is an extension for Flask that simplifies the creation of RESTful APIs.
from . import Utils

#The constructor for the LoanPred class takes a single argument, model. This argument is expected to be a machine learning model that will be used for predictions. 
# The model is passed as an argument when creating an instance of this class.
class Pred(Resource):
    def __init__(self, model):
        self.model = model
    #This method handles HTTP GET requests to the resource. However, in the current implementation, it always returns a JSON response with the key 'ans' set to 'success'.
    #  This is a simple placeholder response and doesn't use the machine learning model yet.
    def get(self):
        return{'ans': 'success'}

# Function to deploy the model on flask
#This function is responsible for initializing the Flask web application and setting up the API route to serve the machine learning model.
#load_path: This argument is expected to be a file path pointing to a pre-trained machine learning model.
#Inside the function:
#An instance of the Flask application is created as app.
#An instance of the Flask-RESTful API is created as api.
#The machine learning model is loaded from the specified load_path using a function called Utils.load_model. The loaded model is stored in the uploaded_model variable.
def init(load_path):
    app = Flask(__name__)
    api = Api(app)

    uploaded_model = Utils.load_model(load_path)
#This line configures the Flask-RESTful API to map the LoanPred resource to the root URL '/'. 
# The resource_class_kwargs argument specifies that the model parameter of the Pred class should be set to the uploaded_model loaded earlier.
    api.add_resource(Pred, '/', resource_class_kwargs={'model': uploaded_model})
    app.run(port=12345)
