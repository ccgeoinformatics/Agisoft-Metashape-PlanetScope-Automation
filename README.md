# Automated Agisoft Metashape Processing of PlanetScope Image Pairs

## Description
This script automates the processing of PlanetScope image pairs in Agisoft Metashape. It loads image pairs whose file names are listed in a CSV file, adds them to a Metashape document, and performs various processing steps, including camera alignment, depth map generation, and DSM (Digital Surface Model) export. By default, the script uses the "NIR" band as the primary channel, but this can be changed as needed.

## Requirements and Compatibility
- **Python version**: 3.x
- **Agisoft Metashape version**: 2.1 or higher
- **Metashape Python Module**: Must be installed. Download from [Agisoft](https://www.agisoft.com/downloads/installer/). For installation instructions, refer to the [installation guide](https://agisoft.freshdesk.com/support/solutions/articles/31000148930-how-to-install-metashape-stand-alone-python-module).

## Preparations
1. **Create `imagepairs.csv`** without column names. This file should have 3 columns:
   - Column 1: Pair number
   - Column 2: Image 1 filename
   - Column 3: Image 2 filename
   
   Refer to the sample CSV file included with this script for formatting.

2. **Prepare Image Folder**: Create a folder named "images" and copy all required image files (.TIF) and their associated RPC text files into this folder.

## Usage
1. Ensure that Agisoft Metashape is installed on your system.
2. Place the script in the same directory as the `imagepairs.csv` file and the "images" folder.
3. If processing large batches, create multiple CSV files (e.g., `imagepairs_batch1.csv`, `imagepairs_batch2.csv`). Number pairs continuously across batches to avoid overwriting outputs.
4. Start Agisoft Metashape. If using a dedicated GPU, configure Metashape to use it: `Tools` → `Preferences` → `GPU`.
5. Run the script within Agisoft Metashape: `Tools` → `Run Script`.
6. For multiple batches, update the CSV file name in the script accordingly.

## Important Notes
1. **Running the Script Outside Metashape**: The script can run independently of Metashape, but issues may arise during report export. Running within Metashape is recommended.
2. **Coordinate System Selection**: During initial processing, the script prompts for manual coordinate system selection. For some applications, a geoid-based vertical coordinate system (VCS), such as EGM2008, maybe necessary. For instructions on custom CRS setup, refer to [this guide](https://agisoft.freshdesk.com/support/solutions/articles/31000148332-how-to-use-height-above-geoid-for-the-coordinate-system). To skip custom VCS, set `new_crs = Metashape.CoordinateSystem("EPSG::32651")`.
3. **Error Logging**: Check `error_log.txt` after each run for any errors.

## Author
**Jojene R. Santillan**  
Email: [jrsantillan@carsu.edu.ph](mailto:jrsantillan@carsu.edu.ph), [santillan@ipi.uni-hannover.de](mailto:santillan@ipi.uni-hannover.de)  
Date: 13 November 2024
