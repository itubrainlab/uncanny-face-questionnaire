#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Missing username: export_and_download.sh username"
fi

ssh -t $1@130.226.140.46 "cd /opt/questionnaire && python3 export.py"
rsync -av -e ssh $1@130.226.140.46:/opt/questionnaire/export .