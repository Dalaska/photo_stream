from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter
import os
from PIL import Image, ImageOps
import numpy as np

def create_video_from_images(image_folder, output_filename, durations, fps=1, video_width=1280, video_height=720):
    """
    Create a video from images in a specified folder.

    Parameters:
    - image_folder (str): The folder where images are stored.
    - output_filename (str): The name of the output video file.
    - durations (list or float): Duration(s) in seconds for each image.
                                 Can be a single float or a list of floats.
    - fps (int): Frames per second for the video.
    - video_width (int): Width of the output video.
    - video_height (int): Height of the output video.
    """
    # Target directory for the generated video
    video_folder = os.path.join('static', 'videos')
    os.makedirs(video_folder, exist_ok=True)
    output_path = os.path.join(video_folder, output_filename)

    # Get list of image files
    image_files = sorted([
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ])

    # Check if images are found
    if not image_files:
        print("No images found in the specified folder.")
        return

    # If durations is a single float, create a list with the same duration for all images
    if isinstance(durations, (int, float)):
        durations = [durations] * len(image_files)

    # Check if durations match the number of images
    if len(durations) != len(image_files):
        print("Number of durations does not match the number of images.")
        return

    print(f"Total images: {len(image_files)}")
    print(f"Output video will be saved to: {output_path}")

    # Prepare the video writer
    writer = FFMPEG_VideoWriter(
        output_path,
        (video_width, video_height),
        fps=fps,
        codec='libx264',
        bitrate='500k',
        preset='ultrafast',
        threads=4
    )

    try:
        for img_path, duration in zip(image_files, durations):
            print(f"Processing {img_path} with duration {duration}s")

            # Open the image
            img = Image.open(img_path)

            # Resize and process the image
            img = resize_and_fill(img, video_width, video_height)

            # Convert image to numpy array
            frame = np.array(img)

            # Calculate the number of frames to write for this image
            num_frames = int(duration * fps)

            # Write the frame multiple times based on duration and fps
            for _ in range(num_frames):
                writer.write_frame(frame)

            # Close the image to free memory
            img.close()

    finally:
        # Close the writer to finalize the video file
        writer.close()

    print(f"Video successfully created: {output_path}")

def resize_and_fill(img, target_width, target_height):
    """
    Resize and process the image to match the target dimensions.

    - For landscape images: Fill the frame completely, potentially cropping.
    - For portrait images: Match the height, maintain aspect ratio, and add side borders.

    Returns the processed image.
    """
    # Get current image size
    img_width, img_height = img.size

    # Determine if the image is landscape or portrait
    if img_width >= img_height:
        # Landscape or square image
        # Resize and crop to fill the frame
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height

        if img_ratio > target_ratio:
            # Image is wider than target aspect ratio
            # Resize based on height, then crop width
            scale = target_height / img_height
            new_width = int(img_width * scale)
            img_resized = img.resize((new_width, target_height), Image.LANCZOS)
            # Calculate cropping parameters
            left = (new_width - target_width) // 2
            right = left + target_width
            img_cropped = img_resized.crop((left, 0, right, target_height))
        else:
            # Image matches or is narrower than target aspect ratio
            # Resize based on width, then crop height
            scale = target_width / img_width
            new_height = int(img_height * scale)
            img_resized = img.resize((target_width, new_height), Image.LANCZOS)
            # Calculate cropping parameters
            top = (new_height - target_height) // 2
            bottom = top + target_height
            img_cropped = img_resized.crop((0, top, target_width, bottom))

        return img_cropped

    else:
        # Portrait image
        # Resize based on height, maintain aspect ratio
        img_resized = img.resize((int(img_width * target_height / img_height), target_height), Image.LANCZOS)

        # Create a new image with the target size and black background
        new_img = Image.new('RGB', (target_width, target_height), (0, 0, 0))

        # Calculate position to paste the resized image (centered)
        paste_x = (target_width - img_resized.width) // 2
        new_img.paste(img_resized, (paste_x, 0))

        return new_img

if __name__ == "__main__":
    # Parameters
    image_folder = 'images'                   # Folder containing images
    output_filename = 'generated_video.mp4'   # Output video file name
    # durations can be a single number or a list of durations
    duration_per_image = 30.0                 # Duration in seconds for each image
    # durations = [60.0, 30.0, 45.0]         # Or specify individual durations
    fps = 0.1                                   # Low FPS for static images
    video_width = 1280                        # Width of the video
    video_height = 720                        # Height of the video

    # If you want the same duration for all images
    durations = duration_per_image
    # If you want individual durations, uncomment and set the list
    # durations = [60.0, 30.0, 45.0]  # Durations for each image

    # Create the video from images
    create_video_from_images(image_folder, output_filename, durations, fps, video_width, video_height)
