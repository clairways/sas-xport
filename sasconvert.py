import pandas as pd
import xport
import xport.v56

# Load data as DataFrame
csv = 'sample.csv'
df  = pd.read_csv(csv)


# Writing XPT
out = 'output.xpt'
ds  = xport.Dataset(df,name='DATA',label='Detected Cough Events')

# Rename columns to upper case, limited to 8 characters
ds = ds.rename(columns={k: k.upper()[:8] for k in ds})

# Libraries can have multiple datasets.
library = xport.Library({'DATA': ds})

with open(out,'wb') as f:
    xport.v56.dump(library,f)

