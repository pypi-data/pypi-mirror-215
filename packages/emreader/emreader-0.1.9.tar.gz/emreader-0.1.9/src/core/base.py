import glob
import os

import fitz
import rich
from dateutil import parser

from .parse_tab import ParseTab

current_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.path.join(current_dir, "..", "storage", "source", "emails")
output_dir = os.path.join(current_dir, "..", "storage", "output")
pdf_directory = os.path.join(current_dir, "..", "storage", "output")

month_map = {
    "JAN": "1",
    "FEB": "2",
    "MAR": "3",
    "APR": "4",
    "MAY": "5",
    "JUN": "6",
    "JUL": "7",
    "AUG": "8",
    "SEP": "9",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12",
    "OND": ["10", "11", "12"],
}


def list_to_dict(data, pattern=""):
    # get the data from the list
    date = data[0][0][0]  # Extracting the date
    title = data[1][0][0]
    headers = data[1][1][0]  # Extracting the headers
    headers = ["month"] + headers.split(" ")  # Adding "month" to headers
    rows = data[1][2:]  # Extracting the rows
    
    # Initializing the dictionary
    result = {"date": date, "records": []}
    
    for row in rows:
        # Splitting row by space to get elements
        elements = row[0].split(" ")
        if "/" in elements[0]:  # Checking if we need to split the row
            months = elements[0].split("/")  # Splitting months
            # parse int if not
            
            # Creating a separate record for each month
            for month in months:
                if not month.isnumeric():
                    try:
                        month = month_map[month]
                    except KeyError:
                        month = "unknown"
                    finally:
                        if isinstance(month_map[month], list):
                            for m in month_map[month]:
                                record = dict(zip(headers, [m] + elements[1:]))
                                result["records"].append(record)
                        else:
                            record = dict(zip(headers, [month] + elements[1:]))
                            result["records"].append(record)
                
                else:
                    record = dict(zip(headers, [month] + elements[1:]))
                    result["records"].append(record)
        
        else:
            # check _mapped
            if month_map.get(elements[0], None) is not None:
                month_or_months = month_map[elements[0]]
                if isinstance(month_or_months, list):
                    for m in month_or_months:
                        record = dict(zip(headers, [m] + elements[1:]))
                        result["records"].append(record)
                else:
                    record = dict(zip(headers, [month_or_months] + elements[1:]))
                    result["records"].append(record)
            
            else:
                record = dict(zip(headers, elements))
                result["records"].append(record)
    # replace the keys with the correct ones.
    result["title"] = title
    for record in result["records"]:
        try:
            
            record["Offer"] = record.pop("Repl")
            record["Change"] = record.pop("Off")
        except Exception as e:
            
            result["records"].remove(record)
    
    return result


def extract_file_date(doc):
    
    rich.print(doc[0].rect)
    w = doc[0].rect.width
    h = doc[0].rect.height
    
    
    def _date_cordinates():
        """
        xmin: 0 (Start from the left edge)
        ymin: 841 * 4/5 (Start 1/5 down from the top. Remember y values increase upwards)
        xmax: 595 * 1/5 (Cover 1/5 of the width of the page)
        ymax: 841 (End at the top edge)
        :return:
        """
        return ParseTab(doc[0], [0, h * 1 / 8, w * 1 / 2, h * 1 / 4])
    date = _date_cordinates()
    date_dashed = parser.parse(date[0][0][0]).strftime("%Y-%m-%d")
    return date_dashed


def extract_soy_beans(doc):
    rich.print(doc[0].rect)
    w = doc[0].rect.width
    h = doc[0].rect.height
    
    def _date_cordinates():
        """
        xmin: 0 (Start from the left edge)
        ymin: 841 * 4/5 (Start 1/5 down from the top. Remember y values increase upwards)
        xmax: 595 * 1/5 (Cover 1/5 of the width of the page)
        ymax: 841 (End at the top edge)
        :return:
        """
        return ParseTab(doc[0], [0, h * 1 / 8, w * 1 / 2, h * 1 / 4])
    
    def _soybean_cordinates():
        """
        xmin: 0 (Start from the left edge)
        ymin: 841 * 2/3 (Start 1/3 down from the top)
        xmax: 595 * 1/2 (Cover 1/2 the width of the page)
        ymax: 841 * 4/5 (End where the date starts. This could be adjusted as needed)

        :return:
        """
        return ParseTab(doc[0], [w * 1 / 2, h * 1 / 5, w, h * 13 / 32])
    
    tables = [_date_cordinates(), _soybean_cordinates()]
    return list_to_dict(tables)


def extract_from_files():
    # Get all PDF files in ./emls/output
    
    
    pdf_files = glob.glob(os.path.join(pdf_directory, "*.pdf"))
    rich.print(f"found {len(pdf_files)} extracting")
    
    # Loop through all PDF files
    all_files_extracted_data = []
    if len(pdf_files) == 0:
        return [
            {
                "date": "June 16th , 2023",
                "records": [
                    {
                        "month": "11",
                        "Seller": "-1200",
                        "Buyer": "-1300",
                        "Offer": "1012",
                        "Change": "+9",
                        "file_name": "648478_0_closes.pdf",
                        "spot_date": "16-2023",
                    }
                ],
                "title": "SBO",
                "file_name": "./emls/output/648478_0_closes.pdf"
            },
        ]
    for pdf_file in pdf_files:
        # Update the path to the PDF file in the extract_soy_beans function
        try:
            doc = fitz.Document(pdf_file)
            data = extract_soy_beans(doc)
            data["file_name"] = pdf_file
            all_files_extracted_data.append(data)
        except Exception as e:
            print(f"Error extracting data from {pdf_file}: {e}")
            continue
    
    return all_files_extracted_data
