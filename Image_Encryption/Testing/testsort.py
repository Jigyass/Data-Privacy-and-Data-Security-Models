import os
import shutil
import random

def transfer_images(src_dir, dest_dir, num_images=600):
    # Ensure source and destination directories are different
    if src_dir == dest_dir:
        raise ValueError("Source and destination directories must be different")

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # List all files in the source directory
    files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    
    # Check if there are enough images
    if len(files) < num_images:
        raise ValueError("Not enough images in the source directory")

    # Randomly select images
    selected_files = random.sample(files, num_images)

    # Copy selected images to the destination directory
    for file in selected_files:
        shutil.copy(os.path.join(src_dir, file), os.path.join(dest_dir, file))

    print(f"Transferred {num_images} images to {dest_dir}")

# Example usage
source_directory = '/home/jigyas/Github/Data-Privacy-and-Data-Security-Models/Image_Encryption/Testing/Unsort/flickr30k_images'
destination_directory = '/home/jigyas/Github/Data-Privacy-and-Data-Security-Models/Image_Encryption/Testing/Testing_images'
transfer_images(source_directory, destination_directory)

