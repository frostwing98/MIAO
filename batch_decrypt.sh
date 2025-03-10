#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -lt 2 ]; then
    echo "Usage: ./batch_decrypt.sh path/to/ids.txt output_directory"
    exit 1
fi

# Get the file path and output directory from the arguments
id_file=$1
output_dir=$2

# Check if the file exists
if [ ! -f "$id_file" ]; then
    echo "File not found: $id_file"
    exit 1
fi

# Read the list of wxids from the provided file and process each one
while IFS= read -r wxid; do
    # Call the decrypt.sh script with the current wxid and output directory
    ./decrypt2.sh "$wxid" "$output_dir"
done < "$id_file"
