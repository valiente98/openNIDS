"""
	Created by valiente98 on 2020.
"""

import pandas as pd
import os.path

#Files path.
dosPath = "Dataset/DoS/"
ddosPath = "Dataset/DDoS/"
bruteforcePath = "Dataset/Bruteforce/"
generalPath = "Dataset/General/"

#Attack files.
dosFiles = [ dosPath + "Friday-16-02-2018_TrafficForML_CICFlowMeter.csv", dosPath + "Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv"]

ddosFiles = [ddosPath + "Thuesday-20-02-2018_TrafficForML_CICFlowMeter.csv", ddosPath + "Wednesday-21-02-2018_TrafficForML_CICFlowMeter.csv"]

bruteforceFile = bruteforcePath + "Wednesday-14-02-2018_TrafficForML_CICFlowMeter.csv"

generalFiles = [generalPath + "DoS.csv", generalPath + "DDoS.csv", generalPath + "Bruteforce.csv"]

#Main method.
def main():

	createDosCsv()
	createDDosCsv()
	createBruteforceCsv()
	createGeneralCsv()
	
#Combines both source files for creating the DoS dataset.
def createDosCsv():
	
	#Checks whether the resulting file is not created.
	if os.path.isfile(dosPath + "DoS.csv") == False:
		
		print("Building DoS dataset...")
		#Combines both source files.
		combined_csv = pd.concat([pd.read_csv(f) for f in dosFiles])
		header = pd.read_csv(dosFiles[0]).columns
		combined_csv.to_csv(dosPath + "DoS.csv", index=False, columns=header)
		print("DoS dataset done.")
		
#Same as DoS.
def createDDosCsv():
	
	if os.path.isfile(ddosPath + "DDoS.csv") == False:
	
		print("Building DDoS dataset...")
		combined_csv = pd.concat([pd.read_csv(f) for f in ddosFiles])
		header = pd.read_csv(ddosFiles[0]).columns
		combined_csv.to_csv(ddosPath + "DDoS.csv", index=False, columns=header)
		print("DDoS dataset done.")

#Creates SSH and FTP dataset.
def createBruteforceCsv():

	if os.path.isfile(bruteforcePath + "SSH.csv") == False or os.path.isfile(bruteforcePath + "FTP.csv") == False:
	
		print("Building Bruteforce dataset...")
		df = pd.read_csv(bruteforceFile)
		cols = df.columns
		ssh_data = []
		ftp_data = []
		
		#Benign data in both datasets.
		for index, row in df.iterrows():

			if "SSH" in row['Label']:
				ssh_data.append(row)
			
			elif "FTP" in row['Label']:
				ftp_data.append(row)
			
			elif "Benign" in row['Label']:
				ssh_data.append(row)
				ftp_data.append(row)

		ssh_csv = pd.DataFrame(ssh_data, columns = cols)		
		ftp_csv = pd.DataFrame(ftp_data, columns = cols)

		ssh_csv.to_csv(bruteforcePath + "SSH.csv", index=False, columns=cols)
		ftp_csv.to_csv(bruteforcePath + "FTP.csv", index=False, columns=cols)
		print("Bruteforce dataset done.")

#Creates General dataset.
def createGeneralCsv():

	if os.path.isfile(generalPath + "General.csv") == False:
	
		print("Building General dataset...")
		data = []

		for f in generalFiles:
			
			df = pd.read_csv(f)
			
			#Remove wrong features.
			if "Flow ID" == list(df.columns)[0]:
				df.drop(df.columns[[0, 1, 2, 3]], axis=1, inplace=True)
			
			data.append(df)

		combined_csv = pd.concat(data)
		header = pd.read_csv(generalFiles[0]).columns
		combined_csv.to_csv(generalPath + "General.csv", index=False, columns=header)
		print("General dataset done.")

	
if __name__ == "__main__":
	main()
