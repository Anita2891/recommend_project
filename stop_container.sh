#!/bin/bash
set -e

# Stop the running container (if any)
containerid=$(docker ps | awk 'NR>1 {print $1}' | tail -n 1)  # Get the latest container ID
if [ -n "$containerid" ]; then
    echo "Removing container: $containerid"
    docker rm -f "$containerid"
else
    echo "No running containers to remove."
fi
