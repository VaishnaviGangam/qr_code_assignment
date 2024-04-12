import os
from typing import List
import qrcode
import logging
from pathlib import Path
from app.config import SERVER_BASE_URL, SERVER_DOWNLOAD_FOLDER

def list_qr_codes(directory_path: Path) -> List[str]:
    """
    Retrieves the filenames of all QR code images in the specified directory.
    Args:
        directory_path (Path): The path to the directory containing QR code images.
    Returns:
        A list of filenames (str) for QR codes found in the directory.
    """
    try:
        # List all files ending with '.png' in the specified directory.
        return [f for f in os.listdir(directory_path) if f.endswith('.png')]
    except FileNotFoundError:
        logging.error(f"Directory is not available : {directory_path}")
        raise
    except OSError as e:
        logging.error(f"An OS error occurred while listing the QR codes: {e}")
        raise

def generate_qr_code(data: str, path: Path, fill_color: str = 'red', back_color: str = 'white', size: int = 10):
    """
    Creates a QR code with the provided data and saves it to the specified file path.
    Parameters:
        data (str): The data to encode in the QR code.
        path (Path): The path where the QR code image will be saved.
        fill_color (str): The color of the QR code.
        back_color (str): The background color of the QR code.
        size (int): The size of each box in the QR code grid.
    """
    logging.debug("QR code generation has started")
    try:
        qr = qrcode.QRCode(version=1, box_size=size, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(str(path))
        logging.info(f"QR code saved successfully to: {path}")
    except Exception as e:
        logging.error(f"Failed to generate or save QR code: {e}")
        raise

def delete_qr_code(file_path: Path):
    """
    Deletes the specified QR code image file.
    Parameters:
        file_path (Path): The path of the QR code image file to delete.
    """
    logging.debug(f"File path: {file_path}")
    if file_path.is_file():
        file_path.unlink()  # Delete the file
        logging.info(f"QR code {file_path.name} deleted successfully")
    else:
        logging.error(f"QR code {file_path.name} not found for deletion")
        raise FileNotFoundError(f"QR code {file_path.name} not found")

def create_directory(directory_path: Path):
    """
    Creates a directory at the specified path if it doesn't already exist.
    Parameters:
        directory_path (Path): The path of the directory to create.
    """
    logging.debug('Attempting to create directory')
    try:
        directory_path.mkdir(parents=True, exist_ok=True)  # Create the directory and any parent directories
    except FileExistsError:
        logging.info(f"Directory already exists: {directory_path}")
    except PermissionError as e:
        logging.error(f"Permission denied when trying to create directory {directory_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error creating directory {directory_path}: {e}")
        raise
