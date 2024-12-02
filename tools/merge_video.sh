#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_dir> <output_dir> <output_file>"
    exit 1
fi

input_dir="$1"
output_dir="$2"
output_file="$3"

mkdir -p "$output_dir"

# Step 1: Re-encode and resize videos
for f in "$input_dir"/*; do
    if [[ -f "$f" ]]; then
        ffmpeg -i "$f" -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
        -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k "$output_dir/$(basename "$f")"
    fi
done

# Step 2: Create the file list
cd "$output_dir" || exit
rm -f file_list.txt
for f in *.mp4; do
    echo "file '$f'" >> file_list.txt
done

# Step 3: Concatenate videos
ffmpeg -f concat -safe 0 -i file_list.txt -c copy "$output_file"

