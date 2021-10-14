from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import os, sys, json
from pyspark.ml.feature import Tokenizer, CountVectorizer, StopWordsRemover, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
import pandas as pd
import time
from os import environ

##### SET ENVIRON VARIABLES ####
os.environ['JAVA_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\Java\JDK')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\Java\JDK\bin'))
os.environ['SPARK_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\spark')
os.environ['HADOOP_HOME'] = os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\winutils')
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),r'Spark_files\spark\bin'))
################################

'''
os.environ['JAVA_HOME'] = r'C:\\Users\\nusai\\OneDrive\\Desktop\\Coding-projects\\Axel-Voice-Assistant\\Axel-Voice-Assistant\\Spark_files\\Java\\JDK'
sys.path.append(r'C:\\Users\\nusai\\OneDrive\\Desktop\\Coding-projects\\Axel-Voice-Assistant\\Axel-Voice-Assistant\\Spark_files\\Java\\JDK\\bin')
os.environ['SPARK_HOME'] = r'C:\\Users\\nusai\\OneDrive\\Desktop\\Coding-projects\\Axel-Voice-Assistant\\Axel-Voice-Assistant\\Spark_files\\spark'
os.environ['HADOOP_HOME'] = r'C:\\Users\\nusai\\OneDrive\\Desktop\\Coding-projects\\Axel-Voice-Assistant\\Axel-Voice-Assistant\\Spark_files\\winutils'
sys.path.append(r'C:\\Users\\nusai\\OneDrive\\Desktop\\Coding-projects\\Axel-Voice-Assistant\\Axel-Voice-Assistant\\Spark_files\\spark\\bin')
'''


print(environ['SPARK_HOME'])
print(environ['HADOOP_HOME'])
print(environ['JAVA_HOME'])
try:
    print(environ['PYSPARK_SUBMIT_ARGS'])
except:
    print("no problem with PYSPARK_SUBMIT_ARGS")

conf = SparkConf().set('spark.driver.host','127.0.0.1').set('spark.driver.maxResultSize','3g')
sc = SparkContext(master='local', appName='myAppName',conf=conf)

print(sc.version)
sql = SQLContext(sc)

with open(os.path.join(os.path.dirname(sys.argv[0]),'config.json')) as jsonFile:
    jsonConfigFile = json.load(jsonFile)
    readPath = os.path.join(os.path.dirname(sys.argv[0]),r'Train_Data\{}'.format(jsonConfigFile['CSV TRAIN DATA'].strip()))
    writePath = os.path.join(os.path.dirname(sys.argv[0]),r'PySpark_Models\{}'.format(jsonConfigFile['MODEL NAME'].strip()))

print(readPath)
df = sql.read.csv(readPath,header=True,inferSchema=True)
df.printSchema()
df.show()

tokenizer = Tokenizer(inputCol='Phrases', outputCol='myTokens') #sSplits words
stopwordsRemover = StopWordsRemover(inputCol='myTokens',outputCol='filteredTokens') #Removes stop words
vectorizer = CountVectorizer(inputCol='filteredTokens',outputCol='rawFeatures') #(amount of words, [list of raised index], [values of said index])
idf = IDF(inputCol='rawFeatures',outputCol='vectorizedFeatures')

lr = LogisticRegression(featuresCol='vectorizedFeatures', labelCol='State')
path = os.path.join(os.path.dirname(sys.argv[0]),'model')

pipeline = Pipeline(stages=[tokenizer,stopwordsRemover,vectorizer,idf,lr])

lrModel = pipeline.fit(df)
lrModel.stages[0].write().overwrite().save(os.path.join(writePath,r'tokenizer'))
lrModel.stages[1].write().overwrite().save(os.path.join(writePath,r'stopWords'))
lrModel.stages[2].write().overwrite().save(os.path.join(writePath,r'vectorizer'))
lrModel.stages[3].write().overwrite().save(os.path.join(writePath,r'idf'))
lrModel.stages[4].write().overwrite().save(os.path.join(writePath,r'lr'))