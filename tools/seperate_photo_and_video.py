import os
import shutil

def move_movie_files(source_folder, destination_folder, movie_extensions=None):
    # Default movie file extensions if none are provided
    if movie_extensions is None:
        movie_extensions = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpeg", ".webm"}

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through the files in the source folder
    for filename in os.listdir(source_folder):
        # Get the file's full path
        file_path = os.path.join(source_folder, filename)

        # Check if it's a file and has a movie file extension
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in movie_extensions:
            try:
                # Move the file to the destination folder
                shutil.move(file_path, destination_folder)
                print(f"Moved: {filename}")
            except Exception as e:
                print(f"Failed to move {filename}: {e}")

# Example usage
source = r"/home/bardd/photo/xr_24"
destination = r"/home/bardd/photo/selected"

move_movie_files(source, destination)