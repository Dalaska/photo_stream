#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

input_dir="$1"
output_file="file_list.txt"

# Check if the provided directory exists
if [ ! -d "$input_dir" ]; then
    echo "Error: Directory '$input_dir' does not exist."
    exit 1
fi

# Create or overwrite the file_list.txt
> "$output_file"

# Loop through .mp4 files in the directory
for file in "$input_dir"/*.mp4; do
    if [[ -f "$file" ]]; then
        echo "file '$(basename "$file")'" >> "$output_file"
    fi
done

echo "file_list.txt created successfully in the current directory."

