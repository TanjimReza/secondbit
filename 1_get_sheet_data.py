import json
from datetime import datetime
import gspread


def save_json_to_file(data, file_path):
    with open(file_path, "w") as file_to_write:
        json.dump(data, file_to_write, indent=4)


def access_google_sheet():
    gc = gspread.service_account(filename="creds.json")
    sh = gc.open_by_key("SHEET_URL")

    worksheet = sh.get_worksheet(2)
    print(worksheet.title)
    # return
    count = 0 
    #! A loop through the rows one by one
    output_json = {}
    for index, row in enumerate(worksheet.get_all_records(), start=0):
        # print(f"Row {index}: {row}")
        SKU = (
            row["B"].strip().split()[-1]
            if len(row["B"].strip().split()) > 1
            else row["B"].strip()
        )
        output_json[SKU] = row
        print(f"Row {index+1}: {SKU}, DONE.")
        count += 1
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_json_to_file(output_json, f"output_{current_time}.json")
    print(f"Total Product: {count}")


# Call the function to test it
start_time = datetime.now()
access_google_sheet()
end_time = datetime.now()
time_diff = end_time - start_time
seconds = time_diff.total_seconds()
print(f"Time taken: {seconds:.2f} seconds")
