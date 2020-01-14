#!/bin/bash
set -e

#Create temp directory and enter it
# shellcheck disable=SC1069

function create_temp_dirs(){
  echo "Creating temp file, entering..."
  [ -d "./c-xapi" ] && rm -rf ./c-xapi
  mv ./xapi ./c-xapi
  cp -r ./c-xapi ./xapi
  cd ./xapi
}

function perform_composer_php(){
  echo "Running php installer to create vendor directory..."
  if [[ "$OSTYPE" == "linux-gnu" ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    php -r "readfile('https://getcomposer.org/installer');" | php; rm -rf vendor; php composer.phar install --prefer-source
  elif [[ "$OSTYPE" == "msys" ]]; then
    php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
    php composer-setup.php
    php composer.phar install --prefer-source
    rm composer-setup.php
  fi
  echo "DONE!"
}

function create_zip(){
  echo "Remove old zip-file if it is there"
  test -f ./xapi.zip && rm xapi.zip

  echo "Zipping..."
  zip -r xapi.zip ./xapi
}

function pause(){
  read -r -p "$*"
}

function perform_file_editing(){
  #Delete unnecessary stuff!
  echo "Deleting tests..."
  rm -rf tests/
  echo "Deleting unnecessary vendor stuff..."
  rm -rf vendor/bin/
  rm -rf vendor/doctrine/
  rm -rf vendor/learninglocker/
  rm -rf vendor/phpdocumentor/
  rm -rf vendor/phpspec/
  rm -rf vendor/phpunit/
  rm -rf vendor/sebastian/
  rm -rf vendor/symfony/
  rm -rf vendor/webmozart/

  #Delete package and lock files in the main directory
  echo "Deleting package and lock files..."
  rm composer.json
  rm composer.lock
  rm composer.phar
  rm package.json
  rm package-lock.json
  rm phpunit.xml

  #Copy the store.php to the directory
  echo "Copying log directory..."
  mkdir classes/log/
  cd ..
  cp -r ./zip-dependencies/store.php ./xapi/classes/log/
}

#Pre script checks
if ! [ -x "$(command -v php)" ]; then
  pause "PHP is not installed or is not found in PATH, script cannot continue..."
elif ! [ -x "$(command -v zip)" ]; then
  pause "the zip command is not installed, please visit the docker setup wiki... Script cannot continue"
else
  create_temp_dirs
  perform_composer_php
  perform_file_editing
  create_zip

  echo "Cleaning up..."
  rm -rf ./xapi
  mv ./c-xapi ./xapi
fi





