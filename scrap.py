import tabula as tb
import pandas as pd
import re
import csv

file = 'select-guide.pdf'
data = tb.read_pdf(file, pages=[5,6,7,9])

i=0
for dataframe in data:
    dataframe.to_csv('file_select-guide_' + str(i) + '.csv')
    i+=1
    

