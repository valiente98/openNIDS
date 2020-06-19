#!/bin/bash

#Created by valiente98 on 2020.

echo "+++ Installing openNIDS dependencies +++"

sudo apt install python3
sudo apt install python3-pip
sudo pip3 install pyside2
sudo pip3 install pandas
sudo pip3 install -U scikit-learn
sudo apt install openjdk-14-jre-headless
sudo apt install libpcap-dev
sudo pip3 install argparse
