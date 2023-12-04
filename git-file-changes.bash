#!/bin/bash

# Check if file name and number of days were provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <filename> <days>"
    exit 1
fi

# Set the file name and number of days
filename=$1
days=$2

# Get the commit hash from X days ago
old_commit=$(git rev-list -1 --before="$days days ago" HEAD)

# Show diff of the file since that commit
git diff $old_commit HEAD -- "$filename"
