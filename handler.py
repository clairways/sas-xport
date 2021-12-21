import boto3
import urllib.parse
import logging
from pathlib import Path
import pandas as pd
import xport
import xport.v56

s3  = boto3.client('s3')
s3r = boto3.resource('s3')
bkt = 'clairways-xport-convert'

logging.basicConfig(level=logging.INFO, force=True)
log = logging.getLogger()


def convert(event, context):
    # Get bucket & object from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],
                                    encoding='utf-8')
    log.info("⚠️ Detected new csv file.")
    log.info(f"⚙️ Executing xport-conversion function for: {key}.")

    # Load csv file from S3
    try :
        obj = s3r.Object(bucket,{key})
        df  = pd.read_csv(obj.get()['Body'])
    except Exception as e:
        log.info(f"Error getting object {key} from bucket {bucket}.")
        raise e

    # Generating XPT dataset
    ds = xport.Dataset(df, name='DATA', label='Detected Cough Events')

    # Rename columns to upper case, limited to 8 characters
    ds = ds.rename(columns={k: k.upper()[:8] for k in ds})

    # Libraries can have multiple datasets.
    library = xport.Library({'DATA': ds})

    dst = f"{Path(key).stem}.xpt"
    with open(dst,'wb') as f:
        xport.v56.dump(library,f)

    # Upload to S3
    s3.upload_file(Filename=dst,
                   Bucket=bucket,
                   Key=f'output/{dst}')
    log.info(f"✅ Execution complete. Files uploaded to s3 path: output/{dst}.")
    return
