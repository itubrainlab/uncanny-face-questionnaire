#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Missing username: remote_monitor.sh username"
fi

ssh -t $1@130.226.140.46 "cd /opt/questionnaire && python3 db_info.py"