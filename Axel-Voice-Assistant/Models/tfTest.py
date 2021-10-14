from re import L
import tensorflow as tf
import numpy as np
import pandas as pd

from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import os, sys,json
from pyspark.ml.feature import Tokenizer, CountVectorizer, StopWordsRemover, IDF
from pyspark.ml import Pipeline


def convertToOneHot(arr):
    numOfCols = max(arr) + 1
    oneHot = []
    for element in arr:
        hold = [0] * numOfCols
        hold[element] = 1
        oneHot.append(np.array(hold.copy()))
    
    return oneHot



os.environ['JAVA_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\Java\JDK')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\Java\JDK\bin'))
os.environ['SPARK_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\spark')
os.environ['HADOOP_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\winutils')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\spark\bin'))

conf = SparkConf().set('spark.driver.host','127.0.0.1').set('spark.driver.maxResultSize','3g')
sc = SparkContext(master='local', appName='myAppName',conf=conf)

print(sc.version)
sql = SQLContext(sc)

with open(os.path.join(os.path.dirname(sys.argv[0]),'config.json')) as jsonFile:
    jsonConfigFile = json.load(jsonFile)
    dataPath = os.path.join(os.path.dirname(sys.argv[0]),r'Train_data\{}'.format(jsonConfigFile['CSV TRAIN DATA'].strip()))

df = sql.read.csv(dataPath,header=True,inferSchema=True)
df.show()

tokenizer = Tokenizer(inputCol='Phrases', outputCol='myTokens') #sSplits words
stopwordsRemover = StopWordsRemover(inputCol='myTokens',outputCol='filteredTokens') #Removes stop words
vectorizer = CountVectorizer(inputCol='filteredTokens',outputCol='rawFeatures') #(amount of words, [list of raised index], [values of said index])
idf = IDF(inputCol='rawFeatures',outputCol='vectorizedFeatures')

pipeline = Pipeline(stages=[tokenizer,stopwordsRemover,vectorizer,idf])
pipelineFit = pipeline.fit(df)
df = pipelineFit.transform(df)
df.show()

df = df.toPandas()

xTrain = []
for arr in df['vectorizedFeatures'].values:
    arr = arr.toArray()
    xTrain.append(arr)

yTrain = convertToOneHot(df['State'].values)

df = pd.DataFrame(list(zip(xTrain, yTrain)),columns=['features','state'])
df = df.sample(frac=1).reset_index(drop=True)

xTrain, yTrain = (df['features'].values , df['state'].values)


