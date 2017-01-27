#!/usr/bin/python3.5

# this code will replace bashhelp.bash
# it will be used for getting the names of the files for analysis
# using python.
# it will hopefully work on Windows OS and Linux OS

#############################################################################

import sys
import os
from Localisation_code import *
from textwrap import wrap

#############################################################################

def print_intro():
    print("******************************************************************")
    print("Welcome to Jen's cell localisation data analysis.")
    print("Please have python version 3 installed on your home computer.")
    print("You will also need the following libraries installed: matplotlib, numpy.")
    print("These libraries will come installed by default if using Anaconda python.")
    print("At any point, you can stop this program by pressing \'ctrl Z\'.")
    print("******************************************************************")
    print()

# determine OS
def det_OS():
    if sys.platform == "linux":                     # linux
        print("The operating system is linux.")
        print()
        return 'linux'
    elif sys.platform == 'win32':                   # windows
        print("The operating system is windows.")
        print()
        return 'windows'
    elif sys.platform == 'darwin':                  # Mac OS X
        print("The operating system is Mac OS X. The code will try to run using linux commands.")
        print()
        return 'linux'
    else:
        print("The operating system is not linux or windows. Program may not run successfully.")
        print()
        return 'unknown'

def get_dir_ID(current_OS):
    """ gets folder identifier for finding text or csv files
        then finds if the folders matching that identifier
        returns 'empty' if there are no folders matching
        the identifier in the current directory
    """
    print("Make sure you are in the folder or directory above where you files are stored.")
    print("Choose an identifier (a piece of text) that is present in all folders that contain cell data, but NOT present in any other folder.")
    print("For example, if my folders were \"bluecells\", \"red_cells\", and \"green-cells\", I would choose \"cells\" as my identifier.")
    print("If you only have one folder of files, your identifier should be the name of that folder.")
    print("Do not leave the identifier blank. If there are no common identifiers, please close this program and change the folder names.")
    print()
    
    dir_ID = input("Enter your folder identifier: ")
    
    if dir_ID == '': return 'error'
    elif dir_ID in '__pycache__': 
        print("Identifier cannot be part of \"__pycache__\". Please try again.")
        return 'error'
    make_list = make_group_list(dir_ID, current_OS)
    if make_list == 'empty':
        return 'error'
    else: return make_list

def make_group_list(dir_ID, current_OS):    
    make_list = []     # category of files based on directory (folder) name
    # save all files and folders to list, pull the ones matching dir_ID
   
    if current_OS == 'windows':
	    start_dir = sys.path[0]
    elif current_OS == 'linux':
	    start_dir = os.getcwd()
    
    ls_all = os.listdir(start_dir)
    for ff in ls_all:
        if dir_ID in ff:
            # try to open the folder, otherwise it's a file
            try:
                os.chdir(dir_ID)
                make_list.append(ff+'.csv')
            except FileNotFoundError:
                print(ff+" is not a directory. Skipping.")
    # if no folders are found, return error
    if len(make_list) == 0:
        print("No folders found with identifier "+str(dir_ID)+". Please try again.")
        return 'empty'
    else: return make_list
   
#############################################################################
# for windows or linux
#############################################################################

def prep_for(operating_system, make_list):
    """
    """
    if operating_system == 'windows':
	    start_dir = sys.path[0]
    elif operating_system == 'linux':
	    start_dir = os.getcwd()
    print("Looking for folders in: "+str(start_dir))
    print()
    print('Groups are: '+str([x[:-4] for x in make_list]))
    print()
    
    # loop through items in make_list 
    for i, group in enumerate(make_list):
        group_files_txt = []                    # initialize names list
        group_files_csv = []
        new_dir = start_dir+'/'+str(group[:-4]) # get rid of .csv
        os.chdir(new_dir)                       # go to group directory
        g = str(group[:-4])      # group name with .csv removed
        
        # prevents adding new data to old dataset
        # prevents trying to read in csv data that is not for a cell
        print("Removing old instances of csv files.")
        if os.path.isfile(new_dir+'/'+str(group)) == True:
            os.remove(new_dir+'/'+str(group))
        if os.path.isfile(new_dir+'/'+g+'_output.csv') == True:
            os.remove(new_dir+'/'+g+'_output.csv')
        if os.path.isfile(new_dir+'/'+g+'_localisation_data.csv') == True:
            os.remove(new_dir+'/'+g+'_localisation_data.csv')
        if os.path.isfile(new_dir+'/'+g+'_no_local_output.csv') == True:
            os.remove(new_dir+'/'+g+'_no_local_output.csv')
        if os.path.isfile(new_dir+'/'+g+'_one_local_output.csv') == True:
            os.remove(new_dir+'/'+g+'_one_local_output.csv')
        if os.path.isfile(new_dir+'/'+g+'_two_local_output.csv') == True:
            os.remove(new_dir+'/'+g+'_two_local_output.csv')
                    
        # set all files to a list, collect subset of text files (.txt)
        print("Analysing files in: "+str(group[:-4]))
        print("If there are any unrelated '.txt' or '.csv' files in this folder, this may cause errors. Open files may also cause errors.")
        ls_all_subdir = os.listdir(start_dir+'/'+str(group[:-4]))
        for ff_subdir in ls_all_subdir:
            if '.txt' in ff_subdir:
                group_files_txt.append(ff_subdir)
            elif '.csv' in ff_subdir:
                group_files_csv.append(ff_subdir)
        
        # sort all files in group_files using sort_file
        print('Found '+str(len(group_files_txt))+' text files in '+str(group[:-4])+'.')
        print('Found '+str(len(group_files_csv))+' csv files in '+str(group[:-4])+'.')
        
        group_files = group_files_txt + group_files_csv # catenate two lists
        
        # try to read in the cell data
        # if there is any error in reading the file, file is removed
        # from the master list and is not analysed.
        for cell_data in group_files:
            try: 
                sort_file(cell_data, group, cell_data[-4:])
            except: 
                print("Unable to process file: "+str(cell_data)+' from group '+str(group[:-4]))
                group_files.remove(cell_data)
            
        # plot data using Localisation_code
        do_analysis(group, operating_system)
        print()
    
    # after all groups have been analysed, return to original directory
    os.chdir(start_dir) 

def get_input_file(operating_system):
    # get starting directory
    print("Formatted csv file should be in the current folder (directory).")
    print("Make sure to include the '.csv' file extension when entering your filename.")
    if operating_system == 'windows':
	    sdir = sys.path[0]
    elif operating_system == 'linux':
	    sdir = os.getcwd()
    else:
        try: 
            sdir = os.getcwd()
        except OSError: 
            sdir = sys.path[0]
        except: 
            print("Unable to resolve current working directory.")
            return 'error'
 
    while True:
        fname = input("Enter the name of your formatted csv file, or enter 'q' to quit: ")
        print()
        if fname == 'q':
            return 'quit'
        elif os.path.isfile(sdir+'/'+fname) == True:
            return fname
        else: print("No such file in current directory. Please try again.")
    
#############################################################################
# Cross-platform code
#############################################################################

def sort_file(filename, group, file_ext):
    """ this is the sort_file.py code from earlier code analysis
        there is a special encoding for these files:
        solution found on stack overflow
        http://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
    """
    intensity = []
    norm_dist = []
    #print("Sorting file "+str(filename)+' from group '+str(group)+'.')
    
    found = False
    with open(filename, 'r', encoding = "ISO-8859-15") as ftxt: 
        for line in ftxt: 
            if 'Normalized Distance' in line and 'Intensity' in line:
                found = True
                # make line comma separated and a list
                if file_ext == '.txt':
                    line = line.replace('\t',',').split(',')
                elif file_ext == '.csv':
                    line = line.split(',')
                
                # find where intensity data is
                int_values = line.index("Intensity")
                # find where Normalised distance data is
                ndist_values = line.index("Normalized Distance")
                
        if found == False:
            print("File "+str(filename)+" may not contain columns for Normalized Distance and Intensity.")
            return ValueError        
                
    with open(filename, 'r', encoding = "ISO-8859-15") as f:        
        for line in f:
            if line.replace("\t", ",").split(',') == ['\n']:
                continue                # ignore empty lines
            elif 'Normalized Distance' in line:
                continue                # ignore header
            elif file_ext == '.txt':
                line = line.replace("\t", ",").split(',')
            elif file_ext == '.csv':
                line = line.split(',')
            
            intensity.append(float(line[int_values]))
            norm_dist.append(float(line[ndist_values]))    
    ipiece = str(filename[:-4])+',I,'
    stringI = ipiece + str(intensity).strip("[]")+'\n'
    ndpiece = ",ND,"
    stringND = ndpiece + str(norm_dist).strip("[]")+'\n'
           
    with open(group, 'a') as f2:        
        f2.write(stringI)
        f2.write(stringND)    

def do_analysis(input_name, operating_system):
    """ makes a new member of the Localisation object, writes
        data to csv files, and plots this data
    """    
    g = str(input_name[:-4])
    
    meow = Localisation(input_name, operating_system, {},{},1,False,{},{},{},0,0)
    meow.open_input()          # open input file, complete dict1
    meow.ask_organise()        # ask whether to organise files by localisation
    meow.choose_NL_split()     # determine NL_split value using dict1
    meow.make_dict_main()      # initialise dict_main using NL_split
    meow.analyse_dict()        # sort dict1 into dict_main
    meow.write_dict_main()     # write data into output file
    meow.plot_data()           # plot data
    
    # sort/plot extra data if files are set to be organised by localisation
    # note: each of the three cases is made as a new version of the 
    # Localisation class
    # note that since dict1 has already been created for these instances
    # of the Localisation class, the input name is a placeholder and is
    # only used to write the name of the output file. Aka these instances
    # do not call open_input()
    if meow.sorter == True:
        nopole = Localisation(g+'_no_local.csv', operating_system, meow.local0, {},1,False,{},{},{},0,0)
        nopole.choose_NL_split()     # determine NL_split value using dict1
        nopole.make_dict_main()      # initialise dict_main using NL_split
        nopole.analyse_dict()        # sort dict1 into dict_main
        nopole.write_dict_main()     # write data into output file
        nopole.plot_data()           # plot data
        
        onepole = Localisation(g+'_one_local.csv', operating_system, meow.local1, {},1,False,{},{},{},0,0)
        onepole.choose_NL_split()     # determine NL_split value using dict1
        onepole.make_dict_main()      # initialise dict_main using NL_split
        onepole.analyse_dict()        # sort dict1 into dict_main
        onepole.write_dict_main()     # write data into output file
        onepole.plot_data()           # plot data
        
        twopole = Localisation(g+'_two_local.csv', operating_system, meow.local2, {},1,False,{},{},{},0,0)
        twopole.choose_NL_split()     # determine NL_split value using dict1
        twopole.make_dict_main()      # initialise dict_main using NL_split
        twopole.analyse_dict()        # sort dict1 into dict_main
        twopole.write_dict_main()     # write data into output file
        twopole.plot_data()           # plot data  
        
#############################################################################


print_intro()
current_OS = det_OS()
choice = input("Analyse folders of files (1) or pre-formatted csv files (2) ? ")
while choice != '1' and choice != '2':
    choice = input("Enter (1) or (2): ")

if choice == '1':
    if current_OS == 'linux' or current_OS == 'windows':    
        make_list = get_dir_ID(current_OS)
        while make_list == 'error':
            make_list = get_dir_ID(current_OS)
        prep_for(current_OS, make_list)
    else: 
        try: 
            make_list = get_dir_ID(current_OS)
            while make_list == 'error':
                make_list = get_dir_ID()
            prep_for('linux', make_list)
        except: 
            make_list = get_dir_ID(current_OS)
            while make_list == 'error':
                make_list = get_dir_ID()            
            prep_for('windows', make_list)   

elif choice == '2':
    while True:
        ifile = get_input_file(current_OS)
        if ifile == 'error' or ifile == 'quit':
            break
        print("Analysing "+str(ifile))
        do_analysis(ifile, current_OS)
    
print('Done')
    
    
    
    
    
