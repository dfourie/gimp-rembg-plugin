# AI Remove Background GIMP Plugin

This GIMP plugin allows users to remove image backgrounds using AI-powered tools like [rembg](https://github.com/danielgatis/rembg). The plugin integrates with GIMP to offer a simple way to remove backgrounds. It can process a single image or all open images in GIMP.

As this plugin uses some AI models, it is recommended to use a virtual environment to install all the ML dependencies to avoid conflicts with other Python packages.

## Features

- **AI-Powered Background Removal:** Removes the background using the `rembg` tool, an AI-powered background removal library.
- **Batch Process:** Process all open images in GIMP with a single click.

## Requirements

- **GIMP 2.10+**
- **Python 2.7** (GIMP uses Python 2.7 for its plugins)
- **Python 3.x** (For `rembg` to work)
- **rembg**: You need to have the `rembg` package installed in Python 3.x.

## Installation

1. **Clone or Download** this repository.
   ```bash
   git clone https://github.com/dfourie/gimp-rembg-plugin.git

2. Make a virtual environment somewhere and install the required packages.
   ```bash
   python3 -m venv gimp-plugin-env
   source venv/bin/activate
   ```
3. Install the onyx runtime according to this guide:
   https://onnxruntime.ai/getting-started

   Typically you will install something like:
   ```
    pip install onnxruntime
   ```
4. Once onyx runtime is installed, install the rembg package:
   ```bash
   pip install "rembg[cli]"
   ```
5. Make a note of the location of your virtual environment folder's location. You will need this to configure the plugin in GIMP.




3.  **Copy the Plugin to GIMP**:

    -   Copy the `remove-background` folder to your GIMP plugins folder:
        -   **Windows:** `C:\Users\YourUserName\AppData\Roaming\GIMP\2.10\plug-ins`
        -   **Linux:** `/home/YourUserName/.config/GIMP/2.10/plug-ins`
        -   **macOS:** `/Users/YourUserName/Library/Application Support/GIMP/2.10/plug-ins`
4.  **Restart GIMP** to load the plugin.

Usage
-----

1.  **Open GIMP** and load an image.
2.  Go to **Python-Fu > AI Remove Background...**.
3.  Set the virtual environment path to the one you created earlier.
4.  Configure the options as per your needs:
    -   **Model:** Choose which AI model to use for background removal.
    -   **Alpha Matting:** Enable alpha matting for smoother edges.
    -   **Process all Open Images:** Process all open images in GIMP in batch mode.
5.  Click **OK** to run the plugin.

Plugin Options
--------------

| Option | Description |
| ------ | ----------- |

| **Model** | Select from different AI models (e.g., `u2net`, `sam`, `isnet-anime`). |
| **Alpha Matting** | Refine the edges of the background removal using alpha matting. |
| **Alpha Matting Erode Size** | Set the size for edge refinement when using alpha matting. |
| **Process all Open Images** | Apply the plugin to all open images in GIMP. |

Example Workflow
----------------

1.  Open an image in GIMP that you want to remove the background from.
2.  Select **AI Remove Background** from the Python-Fu menu.
3.  Run the plugin and watch as the background is removed and the image is processed.

Contributing
------------

Feel free to open issues or submit pull requests to improve this plugin! Contributions are always welcome.

License
-------

This project is licensed under the **GPLv3** License - see the <LICENSE> file for details.

Acknowledgments
---------------

-   **rembg**: This plugin integrates with [rembg](https://github.com/danielgatis/rembg) to handle AI-powered background removal.
-   **GIMP**: The GNU Image Manipulation Program, a free and open-source image editor.
