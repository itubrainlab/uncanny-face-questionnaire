#!/bin/sh
chmod -R 777 .
cp nginx.site /etc/nginx/sites-enabled/questionnaire
cp site.conf /etc/supervisor/conf.d/questionnaire.conf
supervisorctl reload