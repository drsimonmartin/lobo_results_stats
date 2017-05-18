#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:09:32 2017

@author: simonmartin
"""
import pandas as pd # Pandas use here for easy manipulation of data files
import numpy as np

def Geometry(nmodules,rowmax=6):
    """
    calculates plot grid dimensions – limited to rowmax rows
    returns tuple of nrows,ncols needed to fit all histograms (there may be blank spaces)
    uses integer division to work out number of columns
    """
    if nmodules<=rowmax:
        return (nmodules,1)#rows,columns
    else:
        # aim to make a grid that looks as full as possible
        # 
        # number of columns will be (nfiles/rowmax)+1(if (nfiles%rowmax)>=1)
        # number of rows: (nfiles/ncolumns)+1(if (nfiles%rowmax)>=1)
        ncolumns=nmodules/rowmax
        if (nmodules%rowmax)>=1:
            ncolumns=ncolumns+1
        nrows=nmodules/ncolumns
        if (nmodules%ncolumns)>=1:
            nrows=nrows+1
        return (nrows,ncolumns)

def StatFrame(filename='Module Marks.xls',programme_list=[],module_list=[],debug=False):
    """Creates dataframe of the marks for a module or set of modules
    Inputs:
        filename is an excelfile from LUSI system includes Module marks and programmes
        module_code is the code for the module of interest e.g. '15MPA201'
        programme_code (optional) returns data just for given programme e.g. MPUB01
        invalid codes will result in (nan,nan,0)
        """
# Method: build up dataframe of matching modules, then output this dataframe using df.to_latex()     
    # Create dataframe to put the required data in.
        # this dataframe will have len(programme_list)+3 columns
    #build a columns list
    col_list=['Module','All cohorts','StDev']
    if (programme_list != []):
        col_list=col_list+programme_list
    if debug==True: print('col_list='+str(col_list[:]))
    # read in the LUSI spreadsheet
    df=pd.read_excel(filename,skiprows=[0,1]) # have the LUSI file in df
    # some of the column names (may) have spaces. This is a problem in Pandas. Replace space with underscore
    cols = df.columns
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str)) else x) # code based on: https://github.com/pandas-dev/pandas/issues/6508
    df.columns = cols
    if debug==True : print (df.columns.tolist())
    #if debug==True : print(df.head())
    # check to see if module list has values, otherwise go over all modules
    if (module_list==[]):
        # Now pull out list of modules – search "Module Code" column for unique values.
        module_list=df.Module_Code.unique()
    if debug==True : print ((module_list) )
    if debug==True : print (len(module_list) )
    datadf = pd.DataFrame(index=np.arange(0, len(module_list)), columns=col_list) # define size of dataframe for storing results
    for idx,module in enumerate(module_list):
        if debug==True : print (idx,module)
        # build up a list with the required info then append to the dataframe
        line=[module]
        line.append(df["Module_Mark"][(df["Module_Code"] == module)].mean())
        line.append(df["Module_Mark"][(df["Module_Code"] == module)].std())
        #datadf.loc[idx:idx,'Module':]=line # put line into dataf
        for programme in programme_list:
            line.append(df["Module_Mark"][(df["Module_Code"] == module)& (df["Programme_Code"] == programme)].mean())
        if debug==True : print (line) 
        datadf.loc[idx:idx,'Module':]=line # put line into dataf
        
    return (datadf)
"""     
"""  

def ModuleDF(filename='Module Marks.xls',module_name='',elements=False,debug=False): 
    """returns a dataframe of the results of module_name
        Inputs: Lusi results filename"""
    if module_name=='':
        print('Module name must be supplied')
        return
    df=pd.read_excel(filename,skiprows=[0,1]) # have the LUSI file in df
    # some of the column names (may) have spaces. This is a problem in Pandas. Replace space with underscore
    cols = df.columns
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str)) else x) # code based on: https://github.com/pandas-dev/pandas/issues/6508
    df.columns = cols
    if debug==True : print (df.columns.tolist())
    # get results for module_name
    if elements==False:
        ResultList=[]
        ResultList=df["Module_Mark"][(df["Module_Code"] == module_name)]
        if debug: print (ResultList)
        #datadf=pd.DataFrame(ResultList)
        ResultFrame=pd.DataFrame({'Module':df["Module_Mark"][(df["Module_Code"] == module_name)]})
        if debug: print(ResultFrame)       
    else:
        ResultFrame=pd.DataFrame({'Module': df["Module_Mark"][(df["Module_Code"] == module_name)],'Cswk': df["Cswk_Mark"][(df["Module_Code"] == module_name)],'Exam':df["Exam_Mark"][(df["Module_Code"] == module_name)]})       
    return (ResultFrame)
    
    

def HistoModule(filename='Module Marks.xls',module_name='',bins=20,elements=False,debug=False):
    """creates a pandas histogram of the results for specified module
        Inputs: 
            filename is an excelfile from LUSI system includes Module marks and programmes
        module_name is the code for the module of interest e.g. '15MPA201'
        bins=number of bins for the data
        elements=True causes the results for both exam and CW to be displayed 
        """
    # method
    # get results for given module
    # display as histogram
    #
    # get dataframe for module_name
    DataF=ModuleDF(filename,module_name,elements,debug)
    # get results for module_name
    if elements==False:
        if debug: print(DataF)
        DataF.plot.hist(alpha=0.5,range=(0,100),bins=bins,color='b')
    else:
        DataF.plot.hist(alpha=0.25,bins=bins,stacked=False,sort_columns=False,color=['r','g','b'],range=(0,100))
    return

def HistoArray(filename='Module Marks.xls',module_list=[],bins=20,elements=False,rowmax=6,debug=False):
    """creates a pandas histogram of the results for specified module
        Inputs: 
            filename is an excelfile from LUSI system includes Module marks and programmes
        module_list is a list of the modules of interest e.g. '15MPA201'
        bins=number of bins for the data
        elements=True causes the results for both exam and CW to be displayed 
        """
        
    """need to sort out code to follow list of modules"""
    
    # method
    # read in data
    # get results for given modules
    # display as array of histograms
    #
    # read in the LUSI spreadsheet
    df=pd.read_excel(filename,skiprows=[0,1]) # have the LUSI file in df
    # some of the column names (may) have spaces. This is sometimes a problem in Pandas. Replace space with underscore
    cols = df.columns
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str)) else x) # code based on: https://github.com/pandas-dev/pandas/issues/6508
    df.columns = cols
    if debug==True : print (df.columns.tolist())
    #if debug==True : print(df.head())
    # check to see if module list has values, otherwise go over all modules
    if (module_list==[]):
        # Now pull out list of modules – search "Module Code" column for unique values.
        module_list=df.Module_Code.unique()
    if debug==True : print ((module_list) )
    if debug==True : print (len(module_list) )
    nModules=len(module_list)
    # now work out dimensions of array
    nRows,nCols=Geometry(nModules,rowmax)
    #f, axarr = plt.subplots(nrows=nRows,ncols=nCols, sharex=True) # setup an array in which to put the plots
    #build a dataframe of result data frames then plot array using by keyword
    df2=pd.DataFrame()
    #for idx,module in enumerate(module_list):
        #df2=df2.append({'Module':df["Module_Mark"][(df["Module_Code"] == module)]})
    df['Module_Mark'].hist(by=df['Module_Code'])
    return