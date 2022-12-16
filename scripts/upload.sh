#!/bin/sh

if [ $# -eq 0 ]; then
  echo "Missing username: upload.sh username"
fi

rsync -av --exclude 'website/__pycache__' --exclude 'website/image_catalog.json' --exclude 'website/database.db' --exclude 'venv' --exclude '.git' --exclude 'export' --exclude 'instance' --exclude '.idea' -e ssh . $1@130.226.140.46:/opt/questionnaire
