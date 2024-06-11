**How to use**
_To re-create master_imwut.csv:_
1. Download .bib files of each volume and issue, and populate the directory bibtex-files. 
2. Run bibtex-parse.py. This script will:
    1. Iterate through all files in bibtex-files and parse it into a .csv in bibtex-csvs.  
    2, Merge all .csv files in bibtex-csvs into master_imwut.csv

_To implement search using queries:_
1. Put keywords and search locations in acm-queries, a Google Sheet. (https://docs.google.com/spreadsheets/d/1pR_V-9CGaHZgG1ChMKjFw7x7V-ffk-9ktJ5DrJY4H0Q/edit#gid=788660334)
2. Download the sheet as a .csv, and rename the file to acm-queries.csv.
3. Put the new file in the repo directory, allowing the previous acm-queries.csv file to be replaced.
4. Open PyLitReview_v4.ipynb, and run all cells. This script will:
    1. Move all files in acm-query-dl and move them to acm-query-archive — if a file already exists in the same name, this will override it in acm-query-archive.
    2. Read acm-queries.csv, iterate and execute through them based on their searchwhere.
    3. Populate acm-query-dl with screenshots of each query, and .bib files from each query. → Use these to check that none of the search queries had more than 1000 search results. If so, those queries need to be manually accounted for; using “All Citations” downloads maximally 1000 citations.
    4. Iterate through all .bib files in acm-query-dl and add them as boolean columns to master_imwut.csv, returning a modified master_imwut.csv file in query-modified-masters directory containing the date and a copy of the corresponding acm-queries csv file. 

**Troubleshooting**
* 'Timeout Error' and 'Element not clickable' errors can be resolved by increasing the wait time for the file to download. On the line after the comment "# Wait for the popup and the new download button to be visible", increase the wait time in 'export_div = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="exportDownloadReady"]/div[2]')))' from 60 until the error is no longer present.  
