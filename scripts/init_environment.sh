#!/bin/bash

LIGHTBLUE='\033[1;34m'
LIGHTYELLOW='\033[0;33m'
NC='\033[0m'

development="development"
production="production"
testing="testing"

if [[ $1 == $development ]]; then
  export DJANGO_SETTINGS_MODULE=quantumapp.dev.settings
elif [[ $1 == $production ]]; then
  export DJANGO_SETTINGS_MODULE=quantumapp.prod.settings
elif [[ $1 == $testing ]]; then
  export DJANGO_SETTINGS_MODULE=quantumapp.settings
else
  echo -e "${LIGHTYELLOW}Error${NC}"
  echo "Please provide valid argument."
  echo "Options include: development, production, testing"
  echo -e "    ${LIGHTBLUE}Example: make init_enviroment testing${NC}"
fi
