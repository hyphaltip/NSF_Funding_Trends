Download and process NSF XML for funding trends

Run the download script once to get files by year (right now just limited it to 2000-2020)
`bash pipeline/00_download.sh`

This will save the files in `download` folder.

Then run this script to generate a per-year summary of values
`python3 scripts/summarize_funding.py`

This will create file in `reports` folder
