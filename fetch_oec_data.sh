#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="$DIR/data"

# Check if data directory exists, if not create it
if [ ! -d "$DATA_DIR" ]; then
  echo "creating $DATA_DIR"
  mkdir $DATA_DIR
fi

cd $DATA_DIR

# Download data dump from OEC site (if it doesn't already exist)
if [ ! -f year_origin_hs92_4.tsv ]; then
  curl http://atlas.media.mit.edu/static/db/raw/year_origin_hs92_4.tsv.bz2 > year_origin_hs92_4.tsv.bz2
  bunzip2 year_origin_hs92_4.tsv.bz2
else
  echo "Not downloading, file already exists in..."
  echo "$DATA_DIR"
fi