import pandas as pd
from pyspark.ml import PipelineModel
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import os, sys, json
from pyspark.ml.feature import Tokenizer, CountVectorizerModel, StopWordsRemover, IDFModel
from pyspark.ml.classification import LogisticRegressionModel

conf = SparkConf().set('spark.driver.host','127.0.0.1')
sc = SparkContext(master='local', appName='myAppName',conf=conf)
sql = SQLContext(sc)

with open(os.path.join(os.path.dirname(sys.argv[0]),'config.json')) as jsonFile:
    jsonConfigFile = json.load(jsonFile)
    readPath = os.path.join(os.path.dirname(sys.argv[0]),r'Test_States\{}'.format(jsonConfigFile['STATE TEST'].strip()))
    pathModel = os.path.join(os.path.dirname(sys.argv[0]),r'PySpark_Models\{}'.format(jsonConfigFile['MODEL NAME'].strip()))

lr = LogisticRegressionModel.read().load(os.path.join(pathModel,r'lr'))
tokenizer = Tokenizer.read().load(os.path.join(pathModel,r'tokenizer'))
stopwordsRemover = StopWordsRemover.read().load(os.path.join(pathModel,r'stopWords'))
vectorizer = CountVectorizerModel.read().load(os.path.join(pathModel,r'vectorizer'))
idf = IDFModel.read().load(os.path.join(pathModel,r'idf'))
pipeline = PipelineModel(stages=[tokenizer,stopwordsRemover,vectorizer,idf,lr])

actionDict = {}

with open(os.path.join(os.path.dirname(sys.argv[0]),readPath),'r') as stateFile:
    for line in stateFile.readlines():
        state,action = tuple(line.split(':'))
        action = action.replace('\n','').strip()
        state = state.replace('\n','').strip()
        if action == None or state == None:
            continue
        
        actionDict[int(state)] = action

while True:
    query = {'Phrases' : [input('What would you like Axel to do: ')]}
    queryDF = pd.DataFrame.from_dict(query)
    pathHold = os.path.join(os.path.dirname(sys.argv[0]),r'hold.csv')
    queryDF.to_csv(pathHold,index=True)
    queryDF = sql.read.csv(pathHold, header=True, inferSchema=True)
    queryDF = queryDF.drop(queryDF.columns[0])
    predictions = pipeline.transform(queryDF)

    probability = predictions.select('probability').collect()
    predictions = predictions.select('prediction').collect()
    prediction = [ row.prediction for row in predictions][0]
    probability = [row.probability for row in probability][0][int(prediction)]
    print(f"{actionDict[int(prediction)]} ({probability * 100}%)")
    os.remove(pathHold)
