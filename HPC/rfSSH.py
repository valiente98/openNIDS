"""
	Created by valiente98 on 2020.
"""

from randomForest import RandomForest
	
def main():

	#Instance of RandomForest class with 100 decision trees.
	rf = RandomForest(100, "SSH")

	#Split dataset into training and testing data randomly.
	train_features, test_features, train_labels, test_labels = rf.splitDataset("Dataset/Bruteforce/SSH.csv")

	print('Training Features Shape:', train_features.shape)
	print('Training Labels Shape:', len(train_labels))
	print('Testing Features Shape:', test_features.shape)

	#Train the model and compute metrics.
	rf.trainModel(train_features, train_labels)
	rf.computeMetrics(test_features, test_labels)

if __name__ == "__main__":
	main()
