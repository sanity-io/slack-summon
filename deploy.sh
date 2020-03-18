#!/bin/bash
gcloud functions deploy summon --region=europe-west1 --allow-unauthenticated --env-vars-file env.yaml --trigger-http --runtime python37

