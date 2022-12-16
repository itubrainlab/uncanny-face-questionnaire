#!/bin/sh
chmod -R 777 .
cp config/nginx.site /etc/nginx/sites-enabled/questionnaire
cp config/site.conf /etc/supervisor/conf.d/questionnaire.conf
supervisorctl reload