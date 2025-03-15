#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modified GIMP plugin to remove backgrounds from images
# with an option to process all open images.
# Original author: James Huang <elastic192@gmail.com>
# Modified by: Tech Archive <medium.com/@techarchive>
# Date: 13/9/24

from gimpfu import *
import os
import tempfile
import platform
import subprocess

import json

# Configuration for saving preferences
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PLUGIN_DIR, "config.json")


def save_config(venv_path):
    """Save configuration to a JSON file"""
    try:
        config = {"venv_path": venv_path}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return True
    except Exception as e:
        return False


def load_config():
    """Load configuration from a JSON file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            return config.get("venv_path", "")
        except Exception:
            return ""
    return ""


tupleModel = (
    "u2net",
    "u2net_human_seg",
    "u2net_cloth_seg",
    "u2netp",
    "silueta",
    "isnet-general-use",
    "isnet-anime",
    "sam",
)

# Load saved virtual environment path at module initialization
DEFAULT_VENV_PATH = load_config()


def remove_background(
    image,
    drawable,
    selModel,
    AlphaMatting,
    aeValue,
    venv_path,
):
    removeTmpFile = False
    tdir = tempfile.gettempdir()
    jpgFile = os.path.join(tdir, "Temp-gimp-0000.jpg")
    pngFile = os.path.join(tdir, "Temp-gimp-0000.png")

    # Start an undo group so all operations can be undone with one action
    image.undo_group_start()
    # Get the currently active layer
    curLayer = pdb.gimp_image_get_active_layer(image)
    # Get the offsets of the current layer
    x1, y1 = curLayer.offsets

    # Save the current layer to a temporary JPEG file
    pdb.file_jpeg_save(image, curLayer, jpgFile, jpgFile, 0.95, 0, 1, 0, "", 0, 1, 0, 0)

    # Get Python executable from the virtual environment
    if not venv_path or not os.path.exists(venv_path):
        pdb.gimp_message("Invalid virtual environment path: {}".format(venv_path))
        image.undo_group_end()
        return

    # Determine Python executable path based on OS
    if platform.system() == "Windows":
        pythonExe = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # macOS or Linux
        pythonExe = os.path.join(venv_path, "bin", "python")

    # Check if Python executable exists
    if not os.path.exists(pythonExe):
        pdb.gimp_message("Python executable not found at: {}".format(pythonExe))
        image.undo_group_end()
        return

    # Build the rembg command using rembg.cli
    cmd = [pythonExe, "-m", "rembg.cli", "i", "-m", tupleModel[selModel]]
    if AlphaMatting:
        cmd.extend(["-a", "-ae", str(int(aeValue))])
    cmd.extend([jpgFile, pngFile])

    # Create a clean environment that doesn't inherit Python-related variables
    clean_env = {}

    # Copy only essential environment variables, excluding Python-related ones
    for key in ("HOME", "PATH", "USER", "LANG", "TERM"):
        if key in os.environ:
            clean_env[key] = os.environ[key]

    # Add system path if not already included (for finding system libraries)
    if "PATH" not in clean_env:
        clean_env["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin"

    # Execute the command with the clean environment
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            env=clean_env,  # Use the clean environment
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            pdb.gimp_message("rembg error:\n" + stderr.decode("utf-8"))
            image.undo_group_end()
            return
    except Exception as e:
        pdb.gimp_message("Failed to execute rembg:\n" + str(e))
        image.undo_group_end()
        return
    # If we reach this point, the background removal was successful, so save the config
    save_config(venv_path)

    # Load the output PNG as a new layer
    if os.path.exists(pngFile):
        new_image = pdb.gimp_file_load(pngFile, pngFile)
        # Get the layer from the new image
        new_layer = pdb.gimp_image_get_active_layer(new_image)
        # Copy the layer to the original image
        new_layer_copy = pdb.gimp_layer_new_from_drawable(new_layer, image)
        # Add the layer to the original image
        pdb.gimp_image_insert_layer(image, new_layer_copy, None, -1)
        # Position the new layer at the same offset as the original
        pdb.gimp_layer_set_offsets(new_layer_copy, x1, y1)
        # Set a meaningful name for the layer
        pdb.gimp_item_set_name(new_layer_copy, "Background Removed")
        # Close the temporary image
        pdb.gimp_image_delete(new_image)
    else:
        pdb.gimp_message("Output PNG file was not created.")

    # End the undo group
    image.undo_group_end()
    # Refresh all displays to show the changes
    gimp.displays_flush()

    # Clean up temporary files
    if removeTmpFile:
        try:
            os.remove(jpgFile)
            os.remove(pngFile)
        except Exception:
            pass


def python_fu_RemoveBG(
    image,
    drawable,
    selModel,
    AlphaMatting,
    aeValue,
    process_all_images,
    venv_path,
):
    if process_all_images:
        # Get a list of all open images in GIMP
        images = gimp.image_list()
        # Iterate through each image
        for img in images:
            # Get the active layer for the current image
            drawable = pdb.gimp_image_get_active_layer(img)
            remove_background(
                img,
                drawable,
                selModel,
                AlphaMatting,
                aeValue,
                venv_path,
            )
    else:
        remove_background(
            image,
            drawable,
            selModel,
            AlphaMatting,
            aeValue,
            venv_path,
        )


register(
    "python_fu_RemoveBG",
    "AI Remove image background",
    "Remove image backgrounds using AI with an option to process all open images.",
    "Tech Archive",
    "GPLv3",
    "2023",
    "<Image>/Python-Fu/AI Remove Background...",
    "RGB*, GRAY*",
    [
        (PF_OPTION, "selModel", "Model", 0, tupleModel),
        (PF_TOGGLE, "AlphaMatting", "Alpha Matting", False),
        (PF_SPINNER, "aeValue", "Alpha Matting Erode Size", 15, (1, 100, 1)),
        (PF_TOGGLE, "process_all_images", "Process all open images", False),
        (PF_STRING, "venv_path", "Virtual Environment Path", DEFAULT_VENV_PATH),
    ],
    [],
    python_fu_RemoveBG,
)

main()
