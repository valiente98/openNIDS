"""
	Created by valiente98 on 2020.
"""

import sys
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCharts import QtCharts
import datetime
import time
import pandas as pd
import pickle
import numpy as np
import subprocess
import os
import argparse


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PCAP_DIR = ROOT_DIR + "/pcap/"
CSV_DIR = ROOT_DIR + "/csv/"

modelDoS = ROOT_DIR + "/models/modelDoS.sav"
modelDDoS = ROOT_DIR + "/models/modelDDoS.sav"
modelSSH = ROOT_DIR + "/models/modelSSH.sav"
modelFTP = ROOT_DIR + "/models/modelFTP.sav"

#Progress bar style.
BAR_STYLE = """
QProgressBar{
    background-color: lightgreen;
    margin-left: 3px;
    border-radius: 5px;
}

QProgressBar::chunk {
    background-color: red;
    border-radius: 5px;
}
"""

#Initial window.
class WaitFlows(QtWidgets.QWidget):

	def __init__(self, parent=None):

		super(WaitFlows, self).__init__()

		#Arguments of the program.
		self.args = parse()

		#Create dialog.
		label = QtWidgets.QLabel('Waiting for flows...')
		label.setAlignment(QtCore.Qt.AlignCenter)
		
		#Add elements.
		grid = QtWidgets.QGridLayout()
		grid.setSpacing(10)
		grid.addWidget(label, 1, 3)
		self.setLayout(grid)
		
		#Main windows.
		self.mainDialog = ShowFlows()

		#Define windows parameters and show window.
		self.setGeometry(60, 60, 575, 500)
		self.setWindowTitle('openNIDS')
		self.setFixedSize(self.width(), self.height())
		self.show()
		
		#After 1 second run start condition.
		QtCore.QTimer.singleShot(1000, lambda: self.startCondition())

	#Checks if traffic is detected for showin main window.
	def startCondition(self):

		#Captures and cretaes net flows.
		subprocess.call(["./idsCapture.sh", self.args.interface])
		csvLines = 0

		#Get flows.
		csvFlows = subprocess.check_output(["find", "csv/", "-name", "*.csv"]).decode("utf-8")
		csvFlows = csvFlows.split("\n")[0]
		print(csvFlows)
		print()
		
		#If there are flows compute the total number of them.
		try:
			out = subprocess.check_output(["wc", "-l",  csvFlows])
			csvLines = int(out.split()[0])
		except:
			QtCore.QTimer.singleShot(100, lambda: self.startCondition())
		
		#Display main window is traffic is captured.
		if( csvLines > 1 ):
			print("\n Flows received!!!\n")
			self.mainDialog.show()
			self.close()
			self.mainDialog.updateGui()
		
		#After 100 ms run the start condition again.
		else:			
			QtCore.QTimer.singleShot(100, lambda: self.startCondition())

#-----------------------------------------------------------------------------------------------------

#Main window.
class ShowFlows(QtWidgets.QWidget):
	
	#Cosntructor
	def __init__(self, parent=None):

		super(ShowFlows, self).__init__()

		#Arguments of the program.
		self.args = parse()
	
		#Widgets data variables.
		self.benignFlows = 0
		self.malignFlows = 0
		self.benign = 0
		self.malign = 0
		self.tcpFlows = 0
		self.udpFlows = 0
		self.othersFlows = 0
		self.tcp = 0
		self.udp = 0
		self.others = 0
		self.series = None
		
		#Not used columns.
		self.wrongColumns = ["Flow ID", "Src IP", "Src Port", "Dst IP", "Timestamp", "Label", "Idle Min"]	
		self.DoS = 0
		self.DDoS = 0
		self.SSH = 0
		self.FTP = 0

		#Models.
		self.modelDoS = pickle.load(open(modelDoS, 'rb'))
		self.modelDDoS = pickle.load(open(modelDDoS, 'rb'))
		self.modelSSH = pickle.load(open(modelSSH, 'rb'))
		self.modelFTP = pickle.load(open(modelFTP, 'rb'))
		
		#Creates the GUI.
		self.initUI()

	#Set the corresponding widgets of the GUI.
	def initUI(self):					
		
		#Creates malign-benign bar label.
		self.benignLabel = QtWidgets.QLabel('Benign flows = ' + str(self.benignFlows) + ' (' + str(self.benign) + '%)')
		self.benignLabel.setStyleSheet("color: green")
		self.malignLabel = QtWidgets.QLabel('Malign flows = ' + str(self.malignFlows) + ' (' + str(self.malign) + '%)')
		self.malignLabel.setStyleSheet("color: red")
		
		#Creates malign-bening bar.
		self.binaryBar = QtWidgets.QProgressBar(self)
		self.binaryBar.setMaximum(100)
		self.binaryBar.setValue(self.malign)
		self.binaryBar.setTextVisible(False)
		self.binaryBar.setStyleSheet(BAR_STYLE)
		
		#Creates protocol lables.
		tcpLabel = QtWidgets.QLabel('TCP')		
		udpLabel = QtWidgets.QLabel('UDP')
		othersLabel = QtWidgets.QLabel('Others')
		
		#Creates grid.
		grid = QtWidgets.QGridLayout()
		grid.setSpacing(10)

		#Adds malign-bening bar and labels.				
		grid.addWidget(self.malignLabel, 1, 1)
		grid.addWidget(self.benignLabel, 1, 2)
		self.binaryBar.setGeometry(140, 82, 370, 20)
		
		#Adds protocol labels.
		grid.addWidget(tcpLabel, 1, 0)		
		grid.addWidget(udpLabel, 2, 0)
		grid.addWidget(othersLabel, 3, 0)
		
		#Creates and adds protocol bars.
		self.tcpBar = QtWidgets.QProgressBar(self)
		self.tcpBar.setGeometry(10, 53, 120, 20)
		self.tcpBar.setMaximum(100)
		self.tcpBar.setValue(self.tcp)
		
		self.udpBar = QtWidgets.QProgressBar(self)
		self.udpBar.setGeometry(10, 107, 120, 20)
		self.udpBar.setMaximum(100)
		self.udpBar.setValue(self.udp)
		
		self.othersBar = QtWidgets.QProgressBar(self)
		self.othersBar.setGeometry(10, 165, 120, 20)
		self.othersBar.setMaximum(100)
		self.othersBar.setValue(self.others)
		
		#Creates and sets grab button.
		grab_btn = QtWidgets.QPushButton('Grab Screen')
		grab_btn.clicked.connect(self.grabScreen)
		grab_btn.setMaximumWidth(120)
		
		grid.addWidget(grab_btn, 8, 0)
		
		#Creates and adds pie chart.
		pieChart = self.create_piechart()		
		grid.addWidget(pieChart, 3, 1, 7, 2)
				
		#Set grid.
		self.setLayout(grid)

		#Set main window.
		self.setGeometry(60, 60, 575, 500)
		self.setWindowTitle('openNIDS')
		self.setFixedSize(self.width(), self.height())

	#Update GUI information displayed.
	def updateGui(self):
		
		#Gets CSV file name.
		csvFlows = subprocess.check_output(["find", "csv/", "-name", "*.csv"]).decode("utf-8")
		csvFlows = csvFlows.split("\n")[0]
		
		#Reads the network flows from CSV file and store them in a dataFrame.
		df = pd.read_csv(csvFlows)
		
		#For each network flow in dataFrame.
		for item, row in df.iterrows():
		
			#Drop not used columns from dataFrame.
			row = row.drop(labels=self.wrongColumns)
			rowData = pd.DataFrame(row).transpose()
			
			#Attack-specified classifiers predict label.
			predictDoS = self.modelDoS.predict(rowData)
			predictDDoS = self.modelDDoS.predict(rowData)
			predictSSH = self.modelSSH.predict(rowData)
			predictFTP = self.modelFTP.predict(rowData)

			#Sets the counter of malign and beingn traffic.
			if( predictDoS > 0 or predictDDoS > 0 or predictSSH > 0 or predictFTP > 0):
				self.malignFlows += 1
				
			else:
				self.benignFlows += 1
			
			#Compute percentage of malign and benign traffic.
			self.benign = round((self.benignFlows/(self.benignFlows + self.malignFlows)) * 100)
			self.malign = 100 - self.benign
	
			#Update benign label.
			self.benignLabel.setText('Benign flows = ' + str(self.benignFlows) + ' (' + str(self.benign) + '%)')
			
			#Update malign label.
			self.malignLabel.setText('Malign flows = ' + str(self.malignFlows) + ' (' + str(self.malign) + '%)')								

			#Update binary bar.
			self.binaryBar.setValue(self.malign)

			#Extracts net flow protocol.
			protocol = row['Protocol']
			
			if protocol == 6:
				self.tcpFlows += 1

			elif protocol == 17:
				self.udpFlows += 1
				
			else:
				self.othersFlows += 1
			
			#Sets protocol labels.
			self.tcp = round((self.tcpFlows/(self.tcpFlows + self.udpFlows + self.othersFlows)) * 100)
			self.udp = round((self.udpFlows/(self.tcpFlows + self.udpFlows + self.othersFlows)) * 100)
			self.others = 100 - self.tcp - self.udp
			
			#Update protocol bars.
			self.tcpBar.setValue(self.tcp)
			self.udpBar.setValue(self.udp)		
			self.othersBar.setValue(self.others)
			
			#Update pieChart.
			
			#Extracts destination port.
			dport = row['Dst Port']
			
			#Possible DoS or DDoS attack.
			if dport == 80:				
			
				if predictDoS > 0:
					self.DoS += 1
				
				elif predictDDoS > 0:
					self.DDoS += 1

			#Possible SSH attack.
			elif dport == 22:
				#Correct SSH/FTP detection bug
				if predictSSH + predictFTP > 0:
					self.SSH += 1

				#Some patator pkts are considered DoS as bruteforce.
				if predictDoS > 0:
					self.SSH += 1
			
			#Possible FTP attack.
			elif dport == 21:
				#Correct SSH/FTP detection bug
				if predictSSH + predictFTP > 0:
					self.FTP += 1

				#Some patator pkts are considered DoS as bruteforce.
				if predictDoS > 0:
					self.FTP += 1
				
			#Update pie chart info.
			self.updatePieChart()
		
		#Iterate loop after 0.5 seconds.
		QtCore.QTimer.singleShot(500, lambda: self.iterateUpdateLoop())
	
	#Iterates the loop .
	def iterateUpdateLoop(self):
		
		#Captures and creates the network flows.
		subprocess.call(["./idsCapture.sh", self.args.interface])
		#Updates GUI info.
		QtCore.QTimer.singleShot(100, lambda: self.updateGui())
		
	#Update pie chart info.
	def updatePieChart(self):
		
		#Remove data from pie chart.
		self.chart.removeSeries(self.series)
		
		#Creates new pie chart data -> series.
		self.series = QtCharts.QPieSeries()
		self.series.append("Benign", self.benignFlows)
		item = self.series.append("DoS", self.DoS)
		item.setBrush(QtGui.QColor("salmon"))
		item = self.series.append("DDoS", self.DDoS)
		item.setBrush(QtGui.QColor("blue"))
		item = self.series.append("SSH", self.SSH)
		item.setBrush(QtGui.QColor(0, 255, 255))
		item = self.series.append("FTP", self.FTP)
		item.setBrush(QtGui.QColor(255, 0, 255))
		
		#Adds slice.
		slice = QtCharts.QPieSlice()
		slice = self.series.slices()[0]
		slice.setExploded(True)
		slice.setLabelVisible(True)
		slice.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
		slice.setBrush(QtCore.Qt.green)
		
		#Adds data to pie chart.
		self.chart.addSeries(self.series)
	
	#Compute the time now for naming the screenshots.
	def computeTime(self):

		now = datetime.datetime.now()
		return str(now.year) + "-" + '{:02d}'.format(now.month) + "-" + '{:02d}'.format(now.day) + " " + '{:02d}'.format(now.hour) + ":" + '{:02d}'.format(now.minute) + ":" + '{:02d}'.format(now.second)

	#Take screenshots.
	def grabScreen(self):

		screen = QtWidgets.QApplication.primaryScreen()
		screenshot = screen.grabWindow( self.winId() )
		screenshot.save("/screenshots/" + self.computeTime() + "_IDS.png", "png")

		buttonReply = QtWidgets.QMessageBox.question(self, 'Screenshot', "Screenshot done.", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

	#Creates pie chart.
	def create_piechart(self):
		
		#Creates pie chart data.
		self.series = QtCharts.QPieSeries()
		self.series.append("DoS", 0)
		self.series.append("DDoS", 0)
		self.series.append("Benign", 0)
		self.series.append("SSH", 0)
		self.series.append("FTP", 0)
		
		#Adds slice.
		slice = QtCharts.QPieSlice()
		slice = self.series.slices()[2]
		slice.setExploded(True)
		slice.setLabelVisible(True)
		slice.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 2))
		slice.setBrush(QtCore.Qt.green)
		
		#Create chart.
		self.chart = QtCharts.QChart()
		self.chart.legend().hide()
		self.chart.addSeries(self.series)
		self.chart.createDefaultAxes()
		self.chart.setTitle("Attacks Pie Chart")
		
		#Adds legend.
		self.chart.legend().setVisible(True)
		self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)	
		self.chart.setBackgroundVisible(False);	
		
		#Render pie chart.
		chartview = QtCharts.QChartView(self.chart)
		chartview.setRenderHint(QtGui.QPainter.Antialiasing)
		
		return chartview
	
#Parse the arguments of the program.
def parse():
	
	#Creates and instance of argument parser.
    parser = argparse.ArgumentParser()
    
    #Interface from where capture traffic argument.
    parser.add_argument("-i","--interface", help="TCPDUMP interface used", default="lo")
    
    #Return the arguments parsed.
    return parser.parse_args()

#Main method.
def main():
	
	#Creates a PySide2 app.
    app = QtWidgets.QApplication(sys.argv)
	#Creates and instance of initial window and display it.
    first = WaitFlows()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

