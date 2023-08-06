import json
import fitz
import rich
from dateutil import parser
import pandas as pd

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


def list_to_dict(data):
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
        print(elements)
        if "/" in elements[0]:  # Checking if we need to split the row
            months = elements[0].split("/")  # Splitting months
            # parse int if not

            # Creating a separate record for each month
            for month in months:
            
                if not month.isnumeric():
                    try:
                        month = month_map[month]
                        print(month)
                    except KeyError:
                        print(f"Unknown month: {month}")
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


def pdf_to_image():
    doc = fitz.open("./files/closes.pdf")
    page = doc[0]
    zoom = 0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    pix.save("page-%i.png" % page.number)


def transform_dataframe(
    data, pivot_value="Seller"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    This transforms a formatted dataframe to what we need.
    Source:
        {
        "date": "June 16th , 2023",
        "records": [
            {
                "month": "11",
                "Seller": "-1200",
                "Buyer": "-1300",
                "Offer": "1012",
                "Change": "+9"
                "file_name:"s"
                "spot_date":""
            },...
        ],
        "title": "SBO",
        "file_name": "./emls/output/648478_0_closes.pdf"
    },
    :param data:
    :param pivot_value:
    :return:
    """
    flattened_data = []
    for record in data:
        spot_date = parser.parse(record["date"])  # convert 'date' to datetime format
        for sub_record in record["records"]:
            try:
                month = int(sub_record["month"])
            except ValueError:
                # invalid record
                continue
            # Check if 'month' in record is less than 'month' in spot_date,
            # If yes, it implies the record is for next year
            year = spot_date.year if month >= spot_date.month else spot_date.year + 1
            sub_record["year"] = str(year)
            sub_record["file_name"] = record["file_name"]
            sub_record["spot date"] = spot_date.strftime(
                "%B %d, %Y"
            )  # convert back to string format
            flattened_data.append(sub_record)

    # Create DataFrame
    df = pd.DataFrame(flattened_data)

    # Convert 'year' and 'month' to string to create 'year-month' column
    df["year"] = df["year"].astype(str)
    df["month"] = df["month"].astype(str)
    df["file_name"] = df["file_name"].astype(str)

    # Creating 'year-month' column
    df["year-month"] = df["year"] + "-" + df["month"]

    df_original = df.copy()
    df = df.drop_duplicates(subset=["spot date", "year-month"], keep="first")

    # Pivot table, 'spot date' as index, 'year-month' as columns, 'Seller' as values
    pivot_df = df.pivot(index="spot date", columns="year-month", values=pivot_value)
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df = pivot_df.sort_index()

    # Fill missing values with '0'
    pivot_df = pivot_df.fillna("0")

    return pivot_df, df_original
