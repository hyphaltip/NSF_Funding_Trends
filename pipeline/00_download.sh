#!/usr/bin/bash
#SBATCH -p short -N 1 -n 1 --out logs/download.log

URL="https://www.nsf.gov/awardsearch/download?DownloadFileName=%s&All=true"
OUTDIR=download
mkdir -p $OUTDIR
for year in $(seq 2000 2020)
do
	url=$(printf $URL $year)
	outfile=$OUTDIR/$year.zip
	if [ ! -s $outfile ]; then
		curl -o $outfile "$url"
	fi
done
