import os, sys
import spacy
from timeit import default_timer as timer
from pyspark.ml.pipeline import PipelineModel
from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
import os, sys, json
from pyspark.ml.feature import Tokenizer, CountVectorizer, StopWordsRemover, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
import pandas as pd
import numpy as np

nlp = spacy.load('en_core_web_sm')
def getWordAnalysis(word):
    doc = nlp(u"{}".format(word))
    posList = ""
    depList = ""
    tagList = ""
    for i, token in enumerate(doc):
        if "subj" in token.dep_: subj = token
        #print(f"{token.text:{10}} {token.pos_:{10}} {token.tag_:{10}} {token.dep_:{10}} {spacy.explain(token.tag_)}")
        posList += f"{token.pos_} " 
        depList += f"{token.dep_} "
        tagList += f"{token.tag_} " 
    
    return [posList.strip(), depList.strip(), tagList.strip()]

datasetPath = os.path.abspath(os.path.dirname(sys.argv[0]) + "/../Chatbot-from-Movie-Dialogue-master")
lines = open(os.path.join(datasetPath,'movie_lines.txt'), encoding='utf-8', errors='ignore').read().split('\n')
conv_lines = open(os.path.join(datasetPath,'movie_conversations.txt'), encoding='utf-8', errors='ignore').read().split('\n')

listOfConvos = []
for c in conv_lines:
    try:
        c = c.split(' +++$+++ ')
        clist = c[3].replace('[', '')
        clist = clist.replace(']', '')
        clist = clist.replace("'", '').split(', ')
        listOfConvos.append(clist)
    except Exception as e:
        print(f"Import convo list error: {e}")
        continue

dictOfConvos = {}
for l in lines:
    try:
        l = l.split(' +++$+++ ')
        dictOfConvos[l[0]] = l[4]
    except Exception as e:
        print(f"Import conversations error: {e}")

listOfQuestions = []
listOfAnswers = []
listPosX = []
listDepX = []
listTagX = []
listPosY = []
listDepY = []
listTagY = []
for doneNum, convos in enumerate(listOfConvos):
    for i, c in enumerate(convos):
        if i == 0:
            listOfQuestions.append(dictOfConvos[c])
            listOut = getWordAnalysis(dictOfConvos[c])
            listPosX.append(listOut[0])
            listDepX.append(listOut[1])
            listTagX.append(listOut[2])
        elif i == 1:
            listOfAnswers.append(dictOfConvos[c])
            listOut = getWordAnalysis(dictOfConvos[c])
            listPosY.append(listOut[0])
            listDepY.append(listOut[1])
            listTagY.append(listOut[2])
        else:
            listOfQuestions.append(listOfAnswers[len(listOfAnswers) - 1])
            listPosX.append(listPosY[len(listPosY) - 1])
            listDepX.append(listDepY[len(listDepY) - 1])
            listTagX.append(listTagY[len(listTagY) - 1])
            
            listOfAnswers.append(dictOfConvos[c])
            listOut = getWordAnalysis(dictOfConvos[c])
            listPosY.append(listOut[0])
            listDepY.append(listOut[1])
            listTagY.append(listOut[2])
        
    print(f"Loaded: {doneNum} / {len(listOfConvos)} ({round(doneNum/len(listOfConvos) * 100, 1)}%) conversations", end='\r')
    if doneNum == 100: break

sparkDict = {
    'POS_Input' : listPosX,
    'DEP_Input' : listDepX,
    'TAG_Input' : listTagX,
    'POS_Output' : listPosY,
    'DEP_Output' : listDepY,
    'TAG_Output' : listTagY    
}
sparkDf = pd.DataFrame(sparkDict)
pathHold = os.path.join(os.path.dirname(sys.argv[0]),r'hold.csv')
sparkDf.to_csv(pathHold,index=True)

###? Pyspark stuff ?###
root_path = os.path.abspath(os.path.dirname(sys.argv[0]) + "/../../")
os.environ['JAVA_HOME'] = os.path.join(root_path,r'Spark_files\Java\JDK')
sys.path.append(os.path.join(root_path,r'Spark_files\Java\JDK\bin'))
os.environ['SPARK_HOME'] = os.path.join(root_path,r'Spark_files\spark')
os.environ['HADOOP_HOME'] = os.path.join(root_path,r'Spark_files\winutils')
sys.path.append(os.path.join(root_path,r'Spark_files\spark\bin'))


print(os.environ['SPARK_HOME'])
print(os.environ['HADOOP_HOME'])
print(os.environ['JAVA_HOME'])
print(os.path.join(os.environ.get("SPARK_HOME"), 'bin/spark-submit.cmd'))
try:
    print(os.environ['PYSPARK_SUBMIT_ARGS'])
except:
    print("no problem with PYSPARK_SUBMIT_ARGS")

conf = SparkConf().set('spark.driver.host','127.0.0.1').set('spark.driver.maxResultSize','3g')
sc = SparkContext(master='local', appName='myAppName',conf=conf)

print(sc.version)
sql = SQLContext(sc)

sparkDf = sql.read.csv(pathHold, header=True, inferSchema=True)
sparkDf = sparkDf.drop(sparkDf.columns[0])
sparkDf.printSchema()
sparkDf.show()

for var in ['POS', 'DEP', 'TAG']:
    sparkDf = Tokenizer(inputCol=f"{var}_Input", outputCol=f"{var}_Input_Tokens").transform(sparkDf)
    sparkDf = StopWordsRemover(inputCol=f"{var}_Input_Tokens", outputCol=f"{var}_Input_StopRemoved").transform(sparkDf)
    sparkDf = CountVectorizer(inputCol=f"{var}_Input_StopRemoved", outputCol=f"{var}_Input_Raw").fit(sparkDf).transform(sparkDf)
    sparkDf = IDF(inputCol=f"{var}_Input_Raw", outputCol=f"{var}_Input_Vectorized").fit(sparkDf).transform(sparkDf)
    
    sparkDf = Tokenizer(inputCol=f"{var}_Output", outputCol=f"{var}_Output_Tokens").transform(sparkDf)
    sparkDf = StopWordsRemover(inputCol=f"{var}_Output_Tokens", outputCol=f"{var}_Output_StopRemoved").transform(sparkDf)
    sparkDf = CountVectorizer(inputCol=f"{var}_Output_StopRemoved", outputCol=f"{var}_Output_Raw").fit(sparkDf).transform(sparkDf)
    sparkDf = IDF(inputCol=f"{var}_Output_Raw", outputCol=f"{var}_Output_Vectorized").fit(sparkDf).transform(sparkDf)
    
    sparkDf = sparkDf.drop(f"{var}_Input_Tokens", f"{var}_Input_StopRemoved", f"{var}_Input_Raw")
    sparkDf = sparkDf.drop(f"{var}_Output_Tokens", f"{var}_Output_StopRemoved", f"{var}_Output_Raw")
    
pandasdf = sparkDf.toPandas()
pandasdf.to_csv(pathHold)

xTrain = []
for i in range(len(pandasdf['POS_Input_Vectorized'])):
    x = []
    x.extend(pandasdf['POS_Input_Vectorized'][i])
    x.extend(pandasdf['DEP_Input_Vectorized'][i])
    x.extend(pandasdf['TAG_Input_Vectorized'][i])
    xTrain.append(x)

xTrain = np.array(xTrain)
yTrainPOS = np.array(pandasdf['POS_Output_Vectorized'])

num_features = len(xTrain[0])
num_output_POS = len(yTrainPOS[0])