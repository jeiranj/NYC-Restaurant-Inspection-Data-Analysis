# 
# Python ass9.py 
# 

import numpy as np
import matplotlib.pyplot as plt
import pandas as p
from scipy import stats
from checks import *
import time
import sys
    
def main():
#Questions 1: reads inspection.csv
    print '****Starting question 1****'
    try:
        print 'inspection data loading...'
        global inspection
        inspection = p.read_csv('inspection.csv',low_memory=False,engine='c',index_col=0,usecols=['CAMIS','DBA','STREET','BORO','ZIPCODE','CUISINE DESCRIPTION','INSPECTION DATE','GRADE','RECORD DATE','GRADE DATE'])#,parse_dates=['INSPECTION DATE','RECORD DATE'])
        print 'inspection data loaded.'
    except:
        print 'Unexpected error:', sys.exc_info()[0]
        sys.exit()

#Questions 2: Keep only records with grades of either A, B or C. Drop duplicated 
#             (same restaurant and same date) inspection records. Fix Missing Boro data. 
    print '****Starting question 2****'
    inspection = inspection[inspection.GRADE.isin(['A','B','C'])]
    #inspection.insert(0, 'CAMIS', inspection.index)
    inspection.reset_index(inplace=True)
    inspection.drop_duplicates(['CAMIS','INSPECTION DATE','GRADE'], take_last=True, inplace=True)
    #del inspection['CAMIS']
    # Now fill in for missing boroughs using zip codes:
    # construct zip code dictionary:
    inspection = inspection[inspection.ZIPCODE != 7005]
    zips = {}
    zips = {'112': 'BROOKLYN', '104':'BRONX', '100':'MANHATTAN','103':'STATEN ISLAND'}
    for key in ['110', '111', '113','114','116']:
        zips[key] = 'QUEENS'
    missing_boro = inspection[inspection.BORO == 'Missing']
    first3_zip = map(lambda x:x[0:3],map(str,missing_boro.ZIPCODE))  # first 3 numbers of the zipcode
    missing_boro['first3_zip'] = p.Series(first3_zip,index=missing_boro.index)
    missing_boro['BORO'] = missing_boro['first3_zip'].map(zips)
    inspection.ix[missing_boro.index.values] = missing_boro
    del missing_boro, first3_zip, zips
    # convert dates to datetime object and sort
    inspection['GRADE DATE'] = p.to_datetime(inspection['GRADE DATE'])
    inspection['INSPECTION DATE'] = p.to_datetime(inspection['INSPECTION DATE'])
    inspection.sort('INSPECTION DATE',inplace=True)
    print 'cleaned data.'

#Question 4(continued) and 5: Check restaurant grade trend for each of the 5 boroughs 
#                             and grade trend for all restaurants.
#                             Produce figs of grade trends versus time in each borough and in all NYC.
    print '****Starting question 4****'
    inspection_grouped = inspection.groupby(['BORO','CAMIS'])
    boros = list(p.unique(inspection.BORO))
    vec_test_restaurant_grades = np.vectorize(test_restaurant_grades)
    sum_trends = p.DataFrame(np.zeros(len(boros)).reshape(1,len(boros)),index=['sum trends'],columns=boros)
    for b in boros:
        # trend calculations:
        inspection_boro = inspection[inspection.BORO==b]
        boro_ids = p.unique(inspection_boro.CAMIS)
        sum_trends[b] = sum(vec_test_restaurant_grades(boro_ids))
        print 'Sum of all trends in {} is {}'.format(b,int(sum_trends[b]))
        # trend plots:
        
        
        
        
        del inspection_boro, boro_ids
    sum_all_trends = sum_trends.sum(axis=1)
    print 'Sum of all trends in all boroughs is {}'.format(int(sum_all_trends))       


    
    
    
#Question 3:
def test_grades(grade_list):
    """Compares the list of grades, sorted temporally, and reports whether grades have 
   improved over time or not.
    Args:
        -- grade_list: user-supplied grades, already sorted temporally.
    Returns:
        -- result: 1, if grades improved. -1, if grades declined. 0, if no change."""
    if (check_grades(grade_list)==False):
        raise ValueError('Grades should be one of A, B or C.')    
    # convert string grades (A,B,C) to numeric grades (3,2,1). The higher grade is better.
    grades = {'A': 3, 'B': 2, 'C': 1} 
    numeric_grades = [grades[g] for g in grade_list]
    # If only one grade is available, set result=0.
    # If more than one grade is available, fit a line a+b.x to numeric_grades... 
    # If slope b>0, grades improved. If b~0, grades are the same. If b<0, grades declined.
    if len(grade_list)>1:
        x = np.array(range(len(numeric_grades)))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,numeric_grades)
        if abs(slope) < 1e-12:
            result = 0
        elif slope>0:
            result = 1
        elif slope<0:
            result = -1
        else:
            raise ValueError('Make sure grades are provided correctly. Invalid slope estimated: {}'.format(slope))   
    else:
        result = 0
    return result
        
        
# Question 4:
def test_restaurant_grades(camis_id):
    """Determines if grades of the restaurant corresponding to camis_id improve over time or not.
    Args:
        -- inspection: dataframe containing all the restaurant grading info.
        -- camis_id: user-supplied restaurant id.
    Returns:
        -- result: 1, if grades improved. -1, if grades declined. 0, if no change."""
    camis_id = int(camis_id)
    allowed_ids = np.unique(inspection.CAMIS)
    if (check_camis_id(allowed_ids,camis_id)==False):
        raise ValueError('CAMIS ID is not among the existing CAMIS IDs. Please check it.')
    grades = list(inspection[inspection.CAMIS==camis_id].GRADE)
    try:
        result = test_grades(grades)
        return result
    except ValueError:
        print 'Unexpected Error at CAMIS ID {}'.format(camis_id)
        sys.exit()
            

if __name__ == '__main__':
    main()
    
    
    