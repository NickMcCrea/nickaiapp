#!/bin/bash

# Check if number of days was provided
if [ -z "$1" ]; then
    echo "Please provide the number of days as an argument."
    exit 1
fi

# Set the number of days
days=$1

# Get the commit hash from X days ago
old_commit=$(git rev-list -1 --before="$days days ago" HEAD)

# Show files changed since that commit
git diff --name-only $old_commit HEAD
