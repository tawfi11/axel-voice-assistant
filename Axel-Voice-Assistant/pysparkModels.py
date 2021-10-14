from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import os, sys
from pyspark.ml.feature import Tokenizer, CountVectorizerModel, StopWordsRemover, IDFModel
from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml import PipelineModel
import pandas as pd

def getModel(modelName, modelType): #Gets the model from modelType
    
    if modelType == 'lr':
        pathModel = os.path.join(os.path.dirname(sys.argv[0]),r'Models\PySpark_Models\{}'.format(modelName))
        lr = LogisticRegressionModel.read().load(os.path.join(pathModel,r'lr'))
        tokenizer = Tokenizer.read().load(os.path.join(pathModel,r'tokenizer'))
        stopwordsRemover = StopWordsRemover.read().load(os.path.join(pathModel,r'stopWords'))
        vectorizer = CountVectorizerModel.read().load(os.path.join(pathModel,r'vectorizer'))
        idf = IDFModel.read().load(os.path.join(pathModel,r'idf'))
        return PipelineModel(stages=[tokenizer,stopwordsRemover,vectorizer,idf,lr])


def chooseState(speech, model):
    query = {'Phrases' : [speech]}
    queryDF = pd.DataFrame.from_dict(query)
    pathHold = os.path.join(os.path.dirname(sys.argv[0]),r'Axel Usage Files\hold.csv')
    queryDF.to_csv(pathHold,index=True)
    queryDF = sql.read.csv(pathHold, header=True, inferSchema=True)
    queryDF = queryDF.drop(queryDF.columns[0])
    predictions = modelDict[model].transform(queryDF)

    probability = predictions.select('probability').collect()
    predictions = predictions.select('prediction').collect()
    prediction = [ row.prediction for row in predictions][0]
    probability = [row.probability for row in probability][0][int(prediction)]
    os.remove(pathHold)    
    return (int(prediction), probability)



javaHomePath = os.path.join(os.path.dirname(sys.argv[0]),r'Spark_files\Java\JDK')
javaPath = os.path.join(os.path.dirname(sys.argv[0]),r'Spark_files\Java\JDK\bin')
sparkHomePath = os.path.join(os.path.dirname(sys.argv[0]),r'Spark_files\spark')
hadoopHomePath = os.path.join(os.path.dirname(sys.argv[0]),r'Spark_files\winutils')
sparkPath = os.path.join(os.path.dirname(sys.argv[0]),r'Spark_files\spark\bin')

##### SET ENVIRON VARIABLES ####
os.environ['JAVA_HOME'] = javaHomePath
sys.path.append(javaPath)
os.environ['SPARK_HOME'] = sparkHomePath
os.environ['HADOOP_HOME'] = hadoopHomePath
sys.path.append(sparkPath)

print(f"JAVA_HOME: {javaHomePath}")
print(f"JAVA in path: {javaPath}")
print(f"SPARK_HOME: {sparkHomePath}")
print(f"HADOOP_HOME: {hadoopHomePath}")
print(f"SPARK in path: {sparkPath}")
################################



conf = SparkConf().set('spark.driver.host','127.0.0.1')
sc = SparkContext(master='local', appName='myAppName',conf=conf)
sc.setLogLevel("OFF")
sql = SQLContext(sc)

modelDict = {}
spotifyModel = getModel('Spotify','lr')
modelDict['Spotify'] = spotifyModel

