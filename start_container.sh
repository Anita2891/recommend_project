#!/bin/bash
set -e

# Pull the Docker image from Docker Hub
docker pull 45628/recommend-project:latest

# Run the Docker image as a container
echo
docker run -d -p 5001:5000 45628/recommend-project:latest
