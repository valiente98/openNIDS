# openNIDS
Heuristic-based NIDS over Machine Learning.

<img src="https://github.com/javiln8/wifi_spartan/blob/master/images/logo.png?raw=true" width="500">

*This application was developed for my Telecommunications Engineering bachelor's final thesis.*
*This project is the result of the final degree project done for my Baschelor's degree in Computer Engineering*


### Introduction
openNIDS is an *open-source* heuristic-based NIDS available for Linux detecnting four types of attacks using Random Forest ML algorithm developed in Python 3.0+. The four attacks detected by openNIDS and the tools used for performing them are:

* SSH brute-force login attacks:	Patator.
* FTP brute-force login attacks:	Patator.
* DoS attacks:	Slowloris.
* DDoS attacks: LOIC (Windows).

The results are displayed in a PySide2 GUI. Thus, this project has been divided in two folders:

* HPC: contains all the necessary Python 3.0+ and bash scrips for training the attack-specified classifiers. As four attacks are detected, four attack-specified classifiers are trained from the CSE-CIC-IDS2018 dataset (check the link in references section). HPC is only available for DTIC memebers of Universitat Pompeu Fabra (Barcelona).
* openNIDS-code: contains all the necessary files for running the GUI. TCPDUMP_and_CICFlowMeter project was modified for using it. The GUI is created using PySide2 module which is *open-source* and very similar to PyQt5. 

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

*Note*: openNIDS must be run as sudo because of TCPDUMP, the tool 

### Usage
Run `python3 wifi_spartan.py --help` to see all available commands and options. To see all available options of a function, run `python3 wifi_spartan.py <module> --help`.

Wi-Fi spartan modules:
- [x] `scan`: wireless spectrum scanner
- [x] `deauth`: deauthentication attack to attempt to capture the 4-way handshake
- [x] `pmkid`: PMKID client-less attack
- [x] `spoof scan`: local network hosts scanner
- [x] `spoof spy`: MiTM attack with ARP spoofing
- [x] `automata`: wardriving automation with deep reinforcement learning techniques.


### Future implementations
- [ ] `jam`: WiFi jamming with packet flooding
- [ ] `rogue`: Evil Twin attack
- [ ] `crack`: dictionary attack to attempt to crack the PSK

### References

- Deep learning model applied to wardriving inspired by [evilsocket/pwnagotchi](https://github.com/evilsocket/pwnagotchi).

