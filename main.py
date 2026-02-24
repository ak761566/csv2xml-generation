import pandas as pd

# import re

# Read the Excel/CSV file
# df = pd.read_csv('/Users/gkalwala/Documents/_Portico/AMDIGITAL/EAST-INDIA-5/amd-eastindiacompany-mod5full.csv')

# df = pd.read_csv('C:\\portico-project\\work\\amdigital\\Hindi_Cinema\\Posters indexing.csv', low_memory=False)

df = pd.read_csv('C:\\portico-project\\work\\amdigital\\COLCARIBBEAN\\Colonial Caribbean Document Metadata Import.csv', low_memory=False)
# df = pd.read_csv('/Users/gkalwala/Downloads/ACS Taxonomy for Portico.csv')

# Rename columns with underscores
df.columns = [c.replace(' ', '_').replace('/','_').replace('(','').replace(')','').replace(':', '_')
              .replace('?','').replace(',','_').replace('[','_').replace(']','') for c in df.columns]
# df.columns = [re.sub(r'[\s/\\():]', '_', c) for c in df.columns]

# Remove leading and trailing spaces from column headers
df.columns = df.columns.str.strip()

# Convert the DataFrame to XML
xml_data = df.to_xml()

# Save the XML data to a file
with open('C:\\portico-project\\work\\amdigital\\COLCARIBBEAN\\colcaribbean-excel2xml.xml', 'w') as f:
    f.write(xml_data)
# with open('/Users/gkalwala/Downloads/mhe.xml', 'w') as f:
#    f.write(xml_data)
