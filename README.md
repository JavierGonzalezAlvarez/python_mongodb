
## create virtualenv on linux
virtualenv entorno_virtual -p python3

## activate virtualenv on linux
source entorno_virtual/bin/activate

## install dependencies
python -m pip install pymongo
python -m pip install datetime
python -m pip install pandas

## run script
python3 getSql.py

