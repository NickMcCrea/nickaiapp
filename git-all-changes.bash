#!/bin/bash

# Check if number of days was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <days>"
    exit 1
fi

# Set the number of days
days=$1

# Get the commit hash from X days ago
old_commit=$(git rev-list -1 --before="$days days ago" HEAD)

# Show detailed changes for all files since that commit
git diff $old_commit HEAD
