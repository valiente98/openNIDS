#!/bin/bash

#Created by valiente98 on 2020.

interface=$1
time_interval=5

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pcap_dir="${script_dir}"/pcap
output_dir="${script_dir}"/csv

## Capture traffic -> PCAP file.
[[ "$(grep -c "$interface" /proc/net/dev)" == "0" ]] && echo "The interface is NOT found!" && exit 255
[[ ! -d "$output_dir" ]] && echo "The output directory does NOT exist!" && exit 255

pcap_file=${pcap_dir}/'packets.pcap'
options="-n -nn -N -s 0"

sudo timeout ${time_interval} tcpdump ${options} -i ${interface} -w "${pcap_file}"


## Convert packets in net flows -> CSV file.
echo "+++ CICFlowMeter PCAP-to-CSV Converter +++"
rm -f csv/*.csv
rm -f csv/*/*.csv

# CICFlowMeter-3.0/bin/CICFlowMeter
"${script_dir}"/CICFlowMeters/CICFlowMeter-3.0/bin/CICFlowMeter "${pcap_file}" "${output_dir}"

echo "+++ Remove ${pcap_file}"
rm -f "${pcap_file}"
