import json
import os
import shutil
import zipfile

# Set predefined names and paths


# 1. Copy DEMO.zip to DEMO_2.zip
def copy_zip_file(demo_zip_path, output_zip_path):
    shutil.copy(demo_zip_path, output_zip_path)


# 2. Extract DEMO_2.zip
def extract_zip_file(zip_path, output_folder_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_folder_path)


# 3. Modify slider_export.txt
def modify_slider_export(output_folder_path, extracted_file_name, new_data):
    slider_export_path = os.path.join(output_folder_path, extracted_file_name)
    with open(slider_export_path, "r") as file:
        data = json.load(file)

    # Replace the specified fields with 'DEMO TEXT'
    data["title"] = new_data["SKU"]
    data["alias"] = new_data["SKU"]

    data["params"]["shortcode"] = f"[rev_slider alias={new_data["SKU"]}][/rev_slider]"

    data["slides"][0]["layers"]["2"]["text"] = new_data["i"]
    data["slides"][0]["layers"]["6"]["text"] = new_data["j"]
    data["slides"][0]["layers"]["9"]["text"] = new_data["k"]

    # Save the updated JSON back to the file
    with open(slider_export_path, "w") as file_to_write:
        json.dump(data, file_to_write, indent=4)


def create_final_zip(output_folder_path, output_zip_final_path):
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_zip_final_path), exist_ok=True)

    with zipfile.ZipFile(output_zip_final_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the archive name without the parent directory
                arcname = os.path.relpath(file_path, output_folder_path)
                zipf.write(file_path, arcname)


def process_zip_file(filename, data):
    
    print(f"Processing {filename}...", end="\r")
    
    FILE_NAME = filename
    TEMPLATE_ZIP_FILENAME_EXT = "DEMO.zip"

    # FILE_NAME_ZIP = f"{FILE_NAME}.zip"
    TEMP_EXTRACTED_FOLDER = f"TemporaryExtraction\\{FILE_NAME}"
    MODIFIED_FILE_NAME_EXT = "slider_export.txt"
    OUTPUT_DIR = "CompleteSliders"

    # 1. Copy DEMO.zip to DEMO_2.zip
    # copy_zip_file(TEMPLATE_ZIP_FILENAME_EXT, FILE_NAME_ZIP)

    # 2. Extract DEMO_2.zip
    extract_zip_file(TEMPLATE_ZIP_FILENAME_EXT, TEMP_EXTRACTED_FOLDER)

    # 3. Modify slider_export.txt
    modify_slider_export(TEMP_EXTRACTED_FOLDER, MODIFIED_FILE_NAME_EXT, data)

    # 4. Create the final zip file
    create_final_zip(TEMP_EXTRACTED_FOLDER, f"{OUTPUT_DIR}\\{FILE_NAME}.zip")

    # 5. Clean up the temporary extraction folder
    # shutil.rmtree(TEMP_EXTRACTED_FOLDER)

    print(f"Processing of {FILE_NAME} completed successfully!", end="\r")


# demo_zip_path = "DEMO.zip"
# output_zip_name = "DEMO_2"
# output_zip_path = f"{output_zip_name}.zip"
# output_folder_path = f"POC\\{output_zip_name}"
# extracted_file_name = "slider_export.txt"

new_data = {
    "SKU": "SKUSKUSKU",
    "i": "OVERVIEW FULL TEXT HERE",
    "j": "CASEBANDDETAILS_1\nCASEBANDDETAILS_2\nCASEBANDDETAILS_3",
    "k": "DIALMOVEMENTDETAILS_1\nDIALMOVEMENTDETAILS_2",
}

