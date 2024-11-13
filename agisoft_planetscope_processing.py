# Script Name: Automated Agisoft Metashape Processing of PlanetScope Image Pairs
# Purpose: Automates PlanetScope image pair processing in Agisoft Metashape, including camera alignment,
#          depth map generation, and DSM export.
# Author: Jojene R. Santillan (jrsantillan@carsu.edu.ph, santillan@ipi.uni-hannover.de)
# Date: 13 November 2024
# Compatible with: Agisoft Metashape 2.0+, Python 3.x
# Note: Requires an imagepairs.csv file and a folder of images as specified in the README.md.


import Metashape
import os
import logging
import time, csv

# Checking compatibility
# compatible_major_version = "2.1" 
# found_major_version = ".".join(Metashape.app.version.split('.')[:2])
# if found_major_version != compatible_major_version:
#    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))
    
script_directory = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(script_directory, 'output')

# Configure logging
log_file_path = os.path.join(script_directory, 'error_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.ERROR, format='%(asctime)s - %(message)s')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load image pairs from csv file. 
image_pairs_file = os.path.join(script_directory, 'imagepairs.csv') # Update the file name if you have several csv files (e.g., imagepairs_batch1.csv, imagepairs_batch2.csv, etc), and only wanted to process a specific batch.
with open(image_pairs_file, 'r') as f:
    image_pairs = [line.strip().split(",") for line in f.readlines()]

# Create a Metashape document
doc = Metashape.Document()
doc.save(os.path.join(output_folder, 'project.psx')) # Change to your desired project name. If you have several batches, maybe you can rename it as 'project_batch1.psx'
new_crs = Metashape.app.getCoordinateSystem("Select Coordinate System") # When prompted, select the appropriate coordinate system.

for pair_number, image1_filename, image2_filename in image_pairs:
    try:
        image1_path = os.path.join(script_directory, 'images', image1_filename)
        image2_path = os.path.join(script_directory, 'images', image2_filename)

        if not os.path.exists(image1_path) or not os.path.exists(image2_path):
            error_message = f"Image files not found for pair {pair_number}: {image1_filename}, {image2_filename}"
            print(error_message)
            logging.error(error_message)
            continue

        # Add a new chunk to the document and rename it based on the pair number
        chunk = doc.addChunk()
        chunk.label = f"Pair {pair_number}"
        #chunk.crs = Metashape.CoordinateSystem("EPSG::32651")
        doc.save()

        # Adding specified photos
        chunk.addPhotos([image1_path, image2_path], load_rpc_txt=True)
        doc.save()
        
        chunk.primary_channel = 3
		# The above will set the Primary Channel to NIR assuming a 4-band image with Band 1 = Blue (0), Band 2 = Green (1), Band 3 = Red (2), Band 4 = NIR (3)
        # If using RGB images, primary channel can be set to 1, 2, or 3 depending on which band has the best quality for image matching. Setting
        # the value for -1 will make use of all (RGB) bands
		# This numbering is different to the band numbering when manually configured within Agisoft Metashape.
        
        for camera in chunk.cameras:
            camera.reference.location = new_crs.project(chunk.crs.unproject(camera.reference.location))
        chunk.crs = new_crs
        chunk.updateTransform()
        doc.save()
        
        chunk.matchPhotos(keypoint_limit=40000, tiepoint_limit=4000, generic_preselection=True, reference_preselection=True)
        doc.save()
        chunk.alignCameras()
        doc.save()
        chunk.buildDepthMaps(downscale=1, filter_mode=Metashape.MildFiltering)
        doc.save()

        has_transform = chunk.transform.scale and chunk.transform.rotation and chunk.transform.translation
        if has_transform:
            chunk.buildPointCloud(source_data=Metashape.DepthMapsData,point_colors=True, point_confidence=True)
            chunk.buildDem(source_data=Metashape.PointCloudData,interpolation=Metashape.DisabledInterpolation) # Interpolation is disabled.
        doc.save()
        
        # Generate report
        report_path = (os.path.join(output_folder, f'report_Pair_{pair_number}.pdf'))
        chunk.exportReport(report_path,title=f'Processing Report for Pair {pair_number}',description=f'Images: {image1_filename}, {image2_filename}')

        #Export DSM
        if chunk.elevation:
            chunk.exportRaster(os.path.join(output_folder, f'dsm_pair{pair_number}.tif'), source_data=Metashape.ElevationData, resolution=3.5, resolution_x=3.5, resolution_y=3.5) # Do not forget to change the value of resolution, resolution_x, and resolution_y
            doc.save()

        print(f'Processing finished for Pair {pair_number}.')
    
    except Exception as e:
        error_message = f"Error processing Pair {pair_number}: {e}"
        print(error_message)
        logging.error(error_message)
        continue

# Save the Metashape document
doc.save()
