import pandas as pd
import numpy as np
from datetime import date

################################################################################
# parses raw data in data/Section_By_Section_Analysis_.csv to a seprate csv 
################################################################################

TRACE_BACK = 5 # only look at 5 years of records

if __name__ =="__main__": 

    raw_data = pd.read_csv("Section_By_Section_Analysis_.csv", index_col=False) 
    raw_data = raw_data.loc[ raw_data['Year'] >=  date.today().year - TRACE_BACK ]

    # get only selected columns 
    short_data = raw_data[['Year', 'Sem', 'College', 'Dept', 'Num', 'Section', 
                           'Instructor', 'Course Name', 'Hrs Per Week', 'Overall course rate']] 

    # organize records by course number and instructor
    output = short_data.groupby(by=["Num", "Instructor", "Course Name"]) \
                       .aggregate({
                                    'Num': 'max', 
                                    'Instructor': 'max',
                                    'Course Name': 'max', 
                                    'Hrs Per Week': 'mean', 
                                    'Overall course rate': 'mean' 
                                   })
    output.index = np.arange(len(output))
    output = output.rename(columns={'Num': 'cnum', 
                                    'Instructor': 'instructor',
                                    'Course Name': 'cname', 
                                    'Hrs Per Week': 'hours',
                                    'Overall course rate': 'rating'})
    
    output.to_csv("FCE_data.csv", index=False) 
    print("File saved to FCE_data.csv")

