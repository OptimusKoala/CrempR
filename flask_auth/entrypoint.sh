#!/bin/sh

# Attendre MariaDB (maximum 60 secondes)
wait-for-it ${DB_HOST}:3306 -t 60

# Démarrage de Flask après attente
python app.py