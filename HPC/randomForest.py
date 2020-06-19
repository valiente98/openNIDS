"""
	Created by valiente98 on 2020.
"""

import matplotlib
#Include it for running this class in HPC.
matplotlib.use('Agg')
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
import pickle
from sklearn.metrics import roc_curve, precision_recall_curve, auc, make_scorer, accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.utils import resample
import sys

#Random forest class.
class RandomForest():

	"""
		Constructor, where
		-> estimators: number of decision trees (int).
		-> attackType: attack detected by the model (string).
	"""
	def __init__(self, estimators, attackType):

		#Create the random forest with the given number of decision trees which use a single thread-
		self.rf = RandomForestClassifier(n_estimators = estimators, verbose=1, n_jobs = 1)		
		#Directory where results will be stored.
		self.resultsPath = "results/" + attackType + "/"
		#ML model name.
		self.modelName = self.resultsPath + "model" + attackType + ".sav"
		self.attackType = attackType
		#General-purpose classifier flag.
		self.isGeneralModel = False
		
	#Train the model given the training dataset.
	def trainModel(self, train_features, train_labels):
		
		self.rf.fit(train_features, train_labels)
		#Saves the model using pickle module.
		self.saveModel(self.modelName)
	
	#Saves the model using pickle module.
	def saveModel(self, modelName):
		
		pickle.dump(self.rf, open(modelName, 'wb'))
		
	#Loads the model using pickle modul.
	def loadModel(self):
		
		return pickle.load(open(self.modelName, 'rb'))
	
	#Evaluation metrics are computed in this method.
	def computeMetrics(self, test_features, test_labels):
		
		model = self.loadModel()
		#Creates the file containing numerical evaluation metrics.
		f = open(self.resultsPath + "metrics.txt","w+")
		f.write("Metrics for " + self.attackType + " attack.\n")
		
		#Predicted labels by model of test label.
		predicted_labels = [label for label in model.predict(test_features)]
		
		#Computes accuracy.
		self.accuracy = model.score(test_features, test_labels)

		#Computes precision, recall and FB-score.
		#General model -> results are the average weighted by the correctly classified instances.
		if self.isGeneralModel == True:
			self.precision, self.recall, self.fbscore, samplesPerClass = precision_recall_fscore_support(test_labels.values, predicted_labels, average="weighted")
		
		else:
			self.precision, self.recall, self.fbscore, samplesPerClass = precision_recall_fscore_support(test_labels.values, predicted_labels, average="binary")
		
		#Store numerical metrics in the metrics file.
		f.write("Accuracy: " + str(self.accuracy) + "\n")
		f.write("Precision: " + str(self.precision) + "\n")
		f.write("Recall: " + str(self.recall) + "\n")
		f.write("Fscore: " + str(self.fbscore) + "\n")
		f.write("\n")

		#Computes confusion matrix. Stored in the metrics file.
		f.write("Confusion Matrix:\n\n")
		if self.isGeneralModel == True:
			labels = [1, 2, 3, 4, 0]
			f.write(pd.DataFrame(confusion_matrix(test_labels, predicted_labels, labels),
				columns=['SSH', 'FTP', 'DoS', 'DDoS', 'benign'], index=['pred_SSH', 'pred_FTP', 'pred_DoS', 'pred_DDoS', 'pred_benign']).to_string())
		
		else:			
			labels = [1, 0]
			f.write(pd.DataFrame(confusion_matrix(test_labels, predicted_labels, labels),
				columns=['malign', 'benign'], index=['predicted_malign', 'predicted_benign']).to_string())

		f.write("\n")
		f.close()

		#Computes ROC curve and feature improtances for attack-specified models.
		if self.isGeneralModel == False:
			self.rocCurve(test_labels, predicted_labels)
			self.featureImportances(model)
	
	#Feature importances figure.
	def featureImportances(self, model):
		
		#Calculate feature importances		
		importances = model.feature_importances_
		#Sort feature importances in descending order
		indices = np.argsort(importances)[::-1]
		
		#Creates and stores the figure.
		feat = plt.figure(figsize=(20, 15))
		plt.title("Feature Importances")
		plt.bar(range(len(indices)), importances[indices], orientation='vertical', align='edge', width=0.3)
		plt.xticks(range(len(indices)), [self.feature_list[i] for i in indices], rotation=90)		
		plt.savefig(self.resultsPath + "featureImportances.png")
		plt.close(feat)

	#ROC curve figure.
	def rocCurve(self, testLabels, predictedLabels):		
		
		#Generates a no skill prediction (majority class)
		ns_probs = [0 for _ in range(len(testLabels))]		
		#Keeps probabilities for the positive outcome only
		lr_probs = predictedLabels	
		#Computes roc curves
		ns_fpr, ns_tpr, _ = roc_curve(testLabels, ns_probs)
		lr_fpr, lr_tpr, _ = roc_curve(testLabels, lr_probs)
		roc = plt.figure()
		plt.plot(ns_fpr, ns_tpr, linestyle='--', label='No Skill')
		plt.plot(lr_fpr, lr_tpr, marker='.', label='Random Forest')
		plt.xlabel('False Positive Rate')
		plt.ylabel('True Positive Rate')
		plt.legend()
		plt.savefig(self.resultsPath + "rocCurve.png")
		plt.close(roc)	

	#Change labels to 0 (Bening) and  1 (Malign)
	def numericalLabels(self, labelColumn):
		
		labels = []

		#General model labels.
		if self.isGeneralModel == True:

			for x in labelColumn:
				#Do not change the "Label" text.
				if x != 'Label':
					
					if x == 'Benign':
						labels.append(0)

					else:
						if "SSH" in x:
							labels.append(1)
						elif "FTP" in x:
							labels.append(2)
						elif "DoS" in x:
							labels.append(3)
						elif "DDOS" in x:
							labels.append(4)
			
				else:
					labels.append(np.nan)
		#Binary classification problems labels.
		else:
		
			for x in labelColumn:
				
				#Do not change the "Label" text.
				if x != 'Label':
					
					if x == 'Benign':
						labels.append(0)
					
					else:					
						labels.append(1)
							
				else:
					labels.append(np.nan)
			
		return labels
	
	#Parse dataset coluns to float numbers.
	#Notice that "errors=coerce" will set any wrong cell in NaN.
	def parseColumnsToFloat(self, dataFrame):
		
		#Delete these columns from the dataset -> not used in training.
		notValidColumns = ["Flow ID", "Src IP", "Src Port", "Dst IP", "Timestamp"]
		#Get all other columns.
		columns = [col for col in list(dataFrame.columns) if col not in notValidColumns]
		#Creates an empty dataframe.
		df = pd.DataFrame()
		
		for c in columns:	
			
			#Appends numerical labels column in the new dataframe.
			if c == "Label":				
				df[c] = pd.to_numeric(self.numericalLabels(dataFrame[c]), errors='coerce')

			#Appends the feature columns.
			else:
				df[c] = pd.to_numeric(dataFrame[c], errors='coerce')
		
		#Removes all rows containing NaN cells.	
		df.dropna(inplace=True)

		#Store processed dataset into results fodler.
		df.to_csv(self.resultsPath + "processedDataset.csv", index=False, columns=columns)
		
		return df
	
	#Split dataset in training and testing datasets.
	#If processed dataset is available, use it.
	def splitDataset(self, datasetPath, isProcessed=False):
		
		#Reads the dataset file.
		data = pd.read_csv(datasetPath)
		
		#If general model -> flag to true.
		if "General" in datasetPath:
			self.isGeneralModel = True
		
		#Parse columns if not processed dataset.
		if isProcessed == False:
			data_parsed = self.parseColumnsToFloat(data)
		
		else:
			data_parsed = data
		
		#Delete infinite values present in the data.
		infiniteIndex = data_parsed.index[np.isinf(data_parsed).any(1)]
		data_rs = data_parsed.drop(infiniteIndex)
		
		#Get all features and the labels.
		features = data_rs.iloc[:, 0:-2]
		labels = data_rs.Label
		self.feature_list = list(features.columns)

		#Splits training and testing data randomly.
		return train_test_split(features, labels, test_size = 0.25)


#Sources
#https://www.scitepress.org/Papers/2018/66398/66398.pdf
#https://towardsdatascience.com/random-forest-in-python-24d0893d51c0tec
#https://towardsdatascience.com/fine-tuning-a-classifier-in-scikit-learn-66e048c21e65
#https://core.ac.uk/download/pdf/82689462.pdf
#https://www.hindawi.com/journals/scn/2019/1574749/ or http://downloads.hindawi.com/journals/scn/2019/1574749.pdf
#https://python-graph-gallery.com/radar-chart/
#http://www.apnorton.com/blog/2016/12/19/Visualizing-Multidimensional-Data-in-Python/
#https://www.datasciencecentral.com/profiles/blogs/python-implementing-a-k-means-algorithm-with-sklearn
#https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
#https://thispointer.com/python-pandas-how-to-drop-rows-in-dataframe-by-conditions-on-column-values/
#https://stackoverflow.com/a/27232309
#https://elitedatascience.com/imbalanced-classes
