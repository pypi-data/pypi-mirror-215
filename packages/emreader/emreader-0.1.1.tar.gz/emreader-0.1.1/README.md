# EMReader

Streamlit showcase app for extracting data from emails.
- Extracts pdfs from attachments.
- Saves to storage folder.
- Runs OCR on pdfs.
- Displays extracted data in a table.
- Saves extracted data to csv.

## How to run this project

1. Add emails to the `storage/source/emails` folder

### Conda environment
```bash

conda create -n extract python=3.7

conda activate extract

pip install -r requirements.txt

```

### Run the app
```bash

streamlit run app.py

```
