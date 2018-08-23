# Project OneSteward

## Overview 
 - "OneSteward" or "One Steward Alliance" is aimed to be a cloud-based service that allows small to medium sized companies in the service sector (travel agencies, appostile agents etc) to revolutionize the quality of their services at no extra cost.
 - Alliance members create and manage their orders in the cloud. Their customers can check the status of their orders via web or ios/android app. Upon registration, customers can further manager their accounts and interact with participating companies in an more efficient way.

## Advantages
 - online order status updates 
 - online inqueries, resolution center
 - redundant data protection
 - standardized yet customizable process for each type of service
 - shared business resources among affiliated companies
 
## Phase 1
 - Build:
   - REST API using Flask and SQL
   - prototype web app using Flask
   - Dockerize web app and rest-api (Current stage)
   - prototype ios app using swift
 - Test:


## Build and Run Dockerized web app
 - Optional: generate postgres Dockerfile from create_postgres_dockerfile.py script
   - cd ./rest_api/web/
   - python create_postgres_dockerfile.py
   - cd ..

 - Optional: run docker in virtualbox using docker-machine
   - docker-machine create -d virtualbox dev;
   - eval "$(docker-machine env dev)"

 - Essential: build docker containers and create database tables
   - docker-compose build
   - docker-compose up -d
   - docker-compose run --rm web python ./instance/db_create.py

  

Author: Shawn Yang
Email: shawnyang610@gmail.com
