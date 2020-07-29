# Importing essential libraries
from flask import Flask, render_template, request
#import pickle
import numpy as np

import rpy2.robjects as robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects import pandas2ri

r = robjects.r

numpy2ri.activate()
pandas2ri.activate()

readRDS = robjects.r['readRDS']
WindeModel = readRDS('/home/smohammad/OtherProject/Quality-Of-Wine/WineModel.rds')
WindeModel= pandas2ri.py2ri(WindeModel)

#df = pandas2ri.rpy2
# do something with the dataframe

#import pyreadr
#result = pyreadr.read_r('/home/smohammad/OtherProject/Quality-Of-Wine/WineModel.rds') # also works for RData

# Load the Random Forest CLassifier model
#WindeModel = "/home/smohammad/OtherProject/Quality-Of-Wine/WineModel.rds"

# Load the Random Forest CLassifier model
#filename = 'wine-model.pkl'
#classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        AGST = float(request.form['AGST'])
        HarvestRain = int(request.form['HarvestRain'])
        WinterRain = int(request.form['WinterRain'])
        Age = int(request.form['Age'])
        
        data = np.array([[AGST, HarvestRain, WinterRain,Age]])
        #my_prediction = classifier.predict(data)
        my_prediction = r.predict(WindeModel,data)
        
        return render_template('result.html', prediction=my_prediction)

if __name__ == '__main__':
	app.run(debug=True)
