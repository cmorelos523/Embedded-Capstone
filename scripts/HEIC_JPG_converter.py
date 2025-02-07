import os
import subprocess

def convert_heic_to_jpg(input_folder, output_folder):
    """Convert all HEIC images in input_folder to JPG using heif-convert and save them to output_folder."""
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".heic"):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name.replace(".HEIC", ".jpg").replace(".heic", ".jpg"))

            try:
                # Use heif-convert to convert HEIC to JPG
                subprocess.run(["heif-convert", input_path, output_path], check=True)
                print(f"Converted: {file_name} -> {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {file_name}: {e}")


# Example usage
input_folder = "/home/kpa/Data/newdata"  # Change to your input folder
output_folder = "/home/kpa/Data/newdata"  # Change to your output folder


# convert_heic_to_jpg(input_folder, output_folder)



import os

def delete_file_of_type(input_folder, file_type):
    """
    Deletes all files of a specific type in the given folder.

    Args:
        input_folder (str): The path to the folder containing the files.
        file_type (str): The file extension to delete (e.g., '.HEIC', '.jpg').
    """
    if not os.path.exists(input_folder):
        print(f"Folder '{input_folder}' does not exist.")
        return

    deleted_files = 0
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(file_type.lower()):  # Case insensitive check
            file_path = os.path.join(input_folder, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_files += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    if deleted_files == 0:
        print(f"No files with extension '{file_type}' found in '{input_folder}'.")

# Example usage:
delete_file_of_type(input_folder, ".HEIC")  # Deletes all .HEIC files in the 'heic_images' folder
