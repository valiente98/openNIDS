# openNIDS
Heuristic-based NIDS over Machine Learning. Full document available in this [link](http://hdl.handle.net/10230/45892).

![Output sample](https://github.com/valiente98/openNIDS/blob/master/openNIDS.gif)


*This project is the result of the final degree project done for my Baschelor's degree in Computer Engineering*

### Introduction
openNIDS is an *open-source* heuristic-based NIDS available for Linux detecting four types of attacks developed in Python 3.0+. Random Forest classifier ML algorithm provided scikit-learn module is used for generating the four attack-specified classifiers. The traffic of a monitored network is captured and classified as benign or malign traffic. The four attacks detected by openNIDS and the tools used for performing them are:

- [x] `SSH brute-force login attacks:`	Patator.
- [x] `FTP brute-force login attacks:`	Patator.
- [x] `DoS attacks:`	Slowloris.
- [x] `DDoS attacks:` LOIC (Windows).

The results are displayed in a PySide2 GUI. Thus, this project has been divided in two folders:

* **HPC/**: contains all the necessary Python 3.0+ and bash scrips for training the attack-specified classifiers. As four attacks are detected, four attack-specified classifiers are trained from the CSE-CIC-IDS2018 dataset (check the link in references section). HPC is only available for DTIC memebers of Universitat Pompeu Fabra (Barcelona).  

* **openNIDS-code/**: contains all the necessary files for running the GUI. TCPDUMP_and_CICFlowMeter project was modified for using it. The GUI is created using PySide2 module which is completely *open-source* and very similar to PyQt5.

openNIDS GUI execution can be summarized in four steps, as follows:

* Step 1: raw packets are captured and stored in a PCAP file during a time interval through tcpdump.
* Step 2: network flows are generated from the PCAP file and stored in a CSV file using CICFlowMeter.
* Step 3: network flows are analysed by the attack-specified classifiers and the labels are predicted using pickle module.
* Step 4: the information computed by openNIDS about the traffic is updated and displayed in the GUI using PySide2 module.

### Requirements
As some tools and modules are used, a script is provided for installing all the required dependencies. For running it, go to openNIDS home directory. Run:

```bash
cd openNIDS/
```

Make the script executable by sudo user/s by running:

```bash
chmod +x installDependencies.sh
```

Finally, install the dependencies by running:

```bash
sudo ./installDependencies.sh
```

*Note*: openNIDS must be run as sudo.

### Usage
First, go to "openNIDS-code" directory by running:

```bash
cd openNIDS-code/
```

For running openNIDS, a network interface must be given. You can check the available options by running `python3 openNIDS.py --help`. The interface is the only attribute needed by openNIDS. By default, **lo** network interface is set.

Finally, run the following command for starting openNIDS GUI: 

```bash
sudo python3 openNIDS.py -i <network_interface>
```

*Note*: openNIDS must be run as sudo because TCPDUMP is used for capturing raw packets.

### References

- [Random forest classifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html).
- [PySide2](https://pypi.org/project/PySide2/).
- [pickle](https://docs.python.org/3/library/pickle.html).
- [CSE-CIC-IDS2018 dataset](https://www.unb.ca/cic/datasets/ids-2018.html).
- [TCPDUMP_and_CICFlowMeter](https://github.com/iPAS/TCPDUMP_and_CICFlowMeter).

