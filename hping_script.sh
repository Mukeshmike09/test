#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

if [ $# -ne 2 ]; then
  echo "Required Number of arguments not passed!!!!!"
  echo "Usage: /root/hping_script.sh <ip> <config file name>"
  echo "Ex: sh /root/hping_script.sh 172.26.2.132 /root/config_hping.yaml"
  exit 1
fi

ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -t -t -q root@localhost << EOF

/usr/bin/python3 /root/network_test_runner.py "$1" "$2"

exit
EOF
