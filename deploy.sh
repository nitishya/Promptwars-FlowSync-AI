#!/bin/bash

# Ensure a project ID is provided or configured in gcloud
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "No Google Cloud project configured. Please run: gcloud config set project [YOUR_PROJECT_ID]"
    exit 1
fi

echo "Deploying FlowSync AI to Google Cloud Run in project: $PROJECT_ID"

gcloud run deploy flowsync-ai \
    --source . \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080

echo "Deployment complete!"
