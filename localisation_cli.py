# utf-8 encoding

import sys
import os
from shutil import copyfile
from localisation import *
from copy import deepcopy

#############################################################################
# functions for both folders and pre-formatted csv files
#############################################################################

def print_intro():
    print(
        66 * "*",
        "Welcome to Jen's cell localisation data analysis.",
        "Please have python version 3 installed on your home computer.",
        "You will also need the following libraries installed: matplotlib, numpy.",
        "These libraries will come installed by default if using Anaconda python.",
        "At any point, you can stop this program by pressing \"ctrl Z\".",
        66 * "*\n", sep="\n"
    )

# determine OS
def det_OS():
    if sys.platform == "linux":
        print("The operating system is Linux.\n")
        print()
        return "linux"
    elif sys.platform == "win32":
        print("The operating system is Windows.\n")
        return "windows"
    elif sys.platform == "darwin":
        print(
            "The operating system is Mac OS X.",
            "The code will try to run using linux commands.\n"
        )
        return "linux"
    else:
        print(
            "The operating system is not linux or windows.",
            "Program may not run successfully.\n"
        )
        return "unknown"
    
def do_analysis(input_name, operating_system):
    """ makes a new member of the Localisation object, writes
        data to csv files, and plots this data
        
        NEW: also makes a Localisation object for cells that
        have one or two poles for localisation called polar
    """    
    g = str(input_name[:-4])
    
    meow = Localisation(input_name, operating_system, {},{},1,False,{},{},{},0,0)
    meow.open_input()          # open input file, complete dict1
    meow.ask_organise()        # ask whether to organise files by localisation
    meow.choose_NL_split()     # determine NL_split value using dict1
    meow.make_dict_main()      # initialise dict_main using NL_split
    meow.analyse_dict()        # sort dict1 into dict_main
    if meow.write_dict_main() != "onecell": # write data into output file
        meow.plot_data()           # plot data
    else: return               # if only one cell in dataset, cannot organise
                               # by localisation
    # sort/plot extra data if files are set to be organised by localisation
    # note: each of the three cases is made as a new version of the 
    # Localisation class
    # note that since dict1 has already been created for these instances
    # of the Localisation class, the input name is a placeholder and is
    # only used to write the name of the output file. Aka these instances
    # do not call open_input()
    if meow.sorter == True:
        if len(meow.local0) != 0:
            nopole = Localisation(g+"_no_local.csv", operating_system, meow.local0, {},1,False,{},{},{},0,0)
            nopole.choose_NL_split()     # determine NL_split value using dict1
            nopole.make_dict_main()      # initialise dict_main using NL_split
            nopole.analyse_dict()        # sort dict1 into dict_main
            if nopole.write_dict_main() != "onecell": # write data into output file
                nopole.plot_data()           # plot data
        
        if len(meow.local1) != 0:
            onepole = Localisation(g+"_one_local.csv", operating_system, meow.local1, {},1,False,{},{},{},0,0)
            onepole.choose_NL_split()     # determine NL_split value using dict1
            onepole.make_dict_main()      # initialise dict_main using NL_split
            onepole.analyse_dict()        # sort dict1 into dict_main
            if onepole.write_dict_main() != "onecell": # write data into output file
                onepole.plot_data()           # plot data
        
        if len(meow.local2) != 0:
            twopole = Localisation(g+"_two_local.csv", operating_system, meow.local2, {},1,False,{},{},{},0,0)
            twopole.choose_NL_split()     # determine NL_split value using dict1
            twopole.make_dict_main()      # initialise dict_main using NL_split
            twopole.analyse_dict()        # sort dict1 into dict_main
            if twopole.write_dict_main() != "onecell": # write data into output file
                twopole.plot_data()           # plot data 

        # combine one pole and two pole into polar category
        if len(meow.local1) * len(meow.local2) != 0:
            p1 = deepcopy(meow.local1)
            p2 = deepcopy(meow.local2)
            for item in p2:
                p1[item] = p2[item][:]
            polar = Localisation(g+"_polar.csv", operating_system,p1,{},1,False,{},{},{},0,0)
            polar.choose_NL_split()
            polar.make_dict_main()
            polar.analyse_dict()
            if polar.write_dict_main() != "onecell":
                polar.plot_data()

#############################################################################
# functions for folders only
#############################################################################

def get_dir_ID(current_OS):
    """ gets folder identifier for finding text or csv files
        then finds if the folders matching that identifier
        returns "empty" if there are no folders matching
        the identifier in the current directory
    """
    print("Make sure you are in the folder or directory above where you files are stored.")
    print("Choose an identifier (a piece of text) that is present in all folders that contain cell data.")
    print("Based on the identifier, the code will enable you to select the folders you wish to analyse.")
    print("For example, if my folders were \"bluecells\", \"red_cells\", and \"green-cells\", I would choose \"cells\" as my identifier.")
    print("If you only have one folder of files, your identifier should be the name of that folder.")
    print("Do not leave the identifier blank. If there are no common identifiers, either close this program and change the folder names or enter each folder separately.")
    print()
    
    dir_ID = input("Enter your folder identifier: ")
    
    if dir_ID == "": return "error"
    elif dir_ID in "__pycache__": 
        print("Identifier cannot be part of \"__pycache__\". Please try again.")
        return "error"
    make_list = make_group_list(dir_ID, current_OS)
    if make_list == "empty":
        return "error"
    else: return make_list

def make_group_list(dir_ID, current_OS):    
    make_list = []     # category of files based on directory (folder) name
    # save all files and folders to list, pull the ones matching dir_ID
   
    if current_OS == "windows":
	    start_dir = sys.path[0]
    elif current_OS == "linux":
	    start_dir = os.getcwd()
    
    ls_all = os.listdir(start_dir)
    for ff in ls_all:
        if dir_ID in ff:
            # try to open the folder, otherwise it"s a file
            try:
                os.chdir(ff)        # try to cd to folder
                os.chdir(start_dir) # if successful, return to start_dir
                make_list.append(ff+".csv")
            except (NotADirectoryError, FileNotFoundError) as e:
                print(ff+" is not a directory. Skipping.")
    # if no folders are found, return error
    if len(make_list) == 0:
        print("No folders found with identifier "+str(dir_ID)+". Please try again.")
        return "empty"
    else: # loop through folders to make sure all are for analysis
        print("Looking for folders in: "+str(start_dir))
        print()
        print("Folders are: "+str([x[:-4] for x in make_list]))
        print()
        make_list2 = make_list[:]   # make sure that looping removes from   
        for group in make_list:     # a hard copied list 
            print()
            print("Would you like to analyse data in folder "+str(group[:-4])+"? The options are:")
            print("Y = yes to ALL folders in list above")
            print("y = yes to this folder")
            print("N = no to ALL folders in the list above")
            print("n = no to this folder")    
            check = input()
            if check == "N":
                print("Please give another identifier.")
                return "empty"
            elif check == "n":
                make_list2.remove(group)
            elif check == "Y":
                break
        return make_list2

def prep_for(current_OS, make_list):
    """ WORKING HERE
    
    
        am currently fixing an issue whereby items from
        a list become deleted while iterating through
        said list
    """
    if current_OS == "windows":
	    start_dir = sys.path[0]
    elif current_OS == "linux":
	    start_dir = os.getcwd()
    
    # loop through items in make_list 
    for i, group in enumerate(make_list):
        group_files_txt = []                    # initialize names list
        group_files_csv = []
        new_dir = start_dir+"/"+str(group[:-4]) # get rid of .csv
        os.chdir(new_dir)                       # go to group directory
        g = str(group[:-4])      # group name with .csv removed
        
        # prevents adding new data to old dataset
        # prevents trying to read in csv data that is not for a cell
        print("Removing old instances of csv files.")
        if os.path.isfile(new_dir+"/"+str(group)) == True:
            os.remove(new_dir+"/"+str(group))
        if os.path.isfile(new_dir+"/"+g+"_output.csv") == True:
            os.remove(new_dir+"/"+g+"_output.csv")
        if os.path.isfile(new_dir+"/"+g+"_localisation_data.csv") == True:
            os.remove(new_dir+"/"+g+"_localisation_data.csv")
        if os.path.isfile(new_dir+"/"+g+"_no_local_output.csv") == True:
            os.remove(new_dir+"/"+g+"_no_local_output.csv")
        if os.path.isfile(new_dir+"/"+g+"_one_local_output.csv") == True:
            os.remove(new_dir+"/"+g+"_one_local_output.csv")
        if os.path.isfile(new_dir+"/"+g+"_two_local_output.csv") == True:
            os.remove(new_dir+"/"+g+"_two_local_output.csv")
        if os.path.isfile(new_dir+"/"+g+"_polar_output.csv") == True:
            os.remove(new_dir+"/"+g+"_polar_output.csv")
                    
        # set all files to a list, collect subset of text files (.txt)
        print("Analysing files in: "+str(group[:-4]))
        print("If there are any unrelated ".txt" or ".csv" files in this folder, this may cause errors. Open files may also cause errors.")
        print()
        ls_all_subdir = os.listdir(start_dir+"/"+str(group[:-4]))
        for ff_subdir in ls_all_subdir:
            if ".txt" in ff_subdir:
                group_files_txt.append(ff_subdir)
            elif ".csv" in ff_subdir:
                group_files_csv.append(ff_subdir)
        
        # debug list of text files
        #print("*")
        #print(group_files_txt)
        #print("*")
        
        # sort all files in group_files using sort_file
        print("Found "+str(len(group_files_txt))+" text files in "+str(group[:-4])+".")
        print("Found "+str(len(group_files_csv))+" csv files in "+str(group[:-4])+".", "\n")
        
        # check to make sure there are files available for analysis
        if len(group_files_txt) == 0 and len(group_files_csv) == 0:
            print("No cell file data found in "+g+". Going to next folder.")
            continue
        
        group_files = group_files_txt + group_files_csv # catenate two lists
        
        # try to read in the cell data
        # if there is any error in reading the file, file is removed
        # from the master list and is not analysed.
        cell_count = 0 # initialise cell count
        poopy_cells = [] # cell names that could not be analysed
        
        for cell_data in group_files:
            try: 
                sort_file(cell_data, group, cell_data[-4:])
            except ValueError as e: 
                print("Unable to process file: "+str(cell_data)+" from group "+str(group[:-4]))
                print(e.args[0])
                poopy_cells.append(cell_data)
            else:
                cell_count += 1 # if sorting of file is successful, increment
        
        print("\n", "Cells processed: ", cell_count, sep="")
        if len(poopy_cells) != 0:
            print("Cells not processed: ", end="")
            print(", ".join(poopy_cells), "\n")
        if not cell_count:      # no cells were successfully sorted
            print("Unable to process any of the cell files.")
        else:  
            # plot data using Localisation_code
            do_analysis(group, current_OS)
            print()
    
    # after all groups have been analysed, return to original directory
    os.chdir(start_dir) 

def sort_file(filename, group, file_ext):
    """ this is the sort_file.py code from earlier code analysis
        there is a special encoding for these files:
        solution found on stack overflow
        http://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
        
        note: fixing an issue where Normalized Distance is not pulled
        from the line. This is caused when the ND is the last column.
        Aka the column header ends in /n and is not picked up by the 
        indexing system.
        
        WORKING HERE
    """
    intensity = []
    norm_dist = []
    #print("Sorting file "+str(filename)+" from group "+str(group)+".")
    
    headers = False
    with open(filename, "r", encoding = "ISO-8859-15") as ftxt: 
        for line in ftxt: 
            if "Normalized Distance" in line and "Intensity" in line:
                headers = True
                # make line comma separated and a list
                if file_ext == ".txt":
                    line = line.replace("\t",",").split(",")
                elif file_ext == ".csv":
                    line = line.split(",")
                
                # check to make sure neither of the important
                # columns include /n by removing it
                if line[-1][-1:] == "\n":
                    line[-1] = line[-1][:-1]
                
                # find where intensity data is
                int_values = line.index("Intensity")
                # find where Normalised distance data is
                ndist_values = line.index("Normalized Distance")
                break

        if not headers:     # couldn"t find ND or I in the file
            print("File "+str(filename)+" may not contain columns for Normalized Distance and Intensity.")
            raise ValueError("Missing Columns")        
                
    with open(filename, "r", encoding = "ISO-8859-15") as f:        
        for line in f:
            if line.replace("\t", ",").split(",") == ["\n"]:
                continue                # ignore empty lines
            elif "Normalized Distance" in line:
                continue                # ignore header
            elif file_ext == ".txt":
                line = line.replace("\t", ",").split(",")
            elif file_ext == ".csv":
                line = line.split(",")
            
            intensity.append(float(line[int_values]))
            norm_dist.append(float(line[ndist_values]))  
    
    # check to make sure normalised distance goes from 0-1 not 1-0
    if norm_dist[0] == 1 and norm_dist[-1] == 0:
        norm_dist = norm_dist[::-1]
        intensity = intensity[::-1]        
              
    ipiece = str(filename[:-4])+",I,"
    stringI = ipiece + str(intensity).strip("[]")+"\n"
    ndpiece = ",ND,"
    stringND = ndpiece + str(norm_dist).strip("[]")+"\n"
           
    with open(group, "a") as f2:        
        f2.write(stringI)
        f2.write(stringND)   

#############################################################################
# functions for pre-formatted csv files only
#############################################################################
        
def get_input_file(operating_system):
    # get starting directory
    print("Formatted csv file should be in the current folder (directory).")
    print("Make sure to include the ".csv" file extension when entering your filename.")
    if operating_system == "windows":
	    sdir = sys.path[0]
    elif operating_system == "linux":
	    sdir = os.getcwd()
    else:
        try: 
            sdir = os.getcwd()
        except OSError: 
            sdir = sys.path[0]
        except: 
            print("Unable to resolve current working directory.")
            return "error"
 
    while True:
        fname = input("Enter the name of your formatted csv file, or enter "q" to quit: ")
        print()
        if fname == "q":
            return "quit"
        elif os.path.isfile(sdir+"/"+fname) == True:
            return fname
        else: print("No such file in current directory. Please try again.")


def make_folder(ifile, current_OS):
    """ first make a folder with same name as parent file
        move file to that folder
        cd to that folder
        do analysis
        return to parent directory
    """
    if current_OS == "windows":
	    sdir = sys.path[0]
    elif current_OS == "linux":
	    sdir = os.getcwd()
    counter = ""
    dirname = str(ifile[:-4])
    while True:
        if os.path.exists(sdir+"/"+dirname+str(counter)) == True:
            if counter == "":
                counter = 1
            else: 
                counter+=1
        else:
	        dirname = dirname+str(counter)
	        os.makedirs(sdir+"/"+dirname)
	        print("Moving data to new folder called "+str(dirname))
	        copyfile(sdir+"/"+ifile, sdir+"/"+dirname+"/"+ifile)
	        os.chdir(sdir+"/"+dirname)
	        print("Analysing "+str(ifile))
	        do_analysis(ifile, current_OS)
	        os.chdir(sdir)
	        return        
        
#############################################################################
# main program execution
#############################################################################

print_intro()
current_OS = det_OS()
choice = input("Analyse folders of files (1) or pre-formatted csv files (2) ? ")
print()
while choice != "1" and choice != "2":
    choice = input("Enter (1) or (2): ")

if choice == "1":
    if current_OS == "linux" or current_OS == "windows":    
        make_list = get_dir_ID(current_OS)
        while make_list == "error":
            make_list = get_dir_ID(current_OS)
        prep_for(current_OS, make_list)
    else: 
        try: 
            make_list = get_dir_ID(current_OS)
            while make_list == "error":
                make_list = get_dir_ID()
            prep_for("linux", make_list)
        except: 
            make_list = get_dir_ID(current_OS)
            while make_list == "error":
                make_list = get_dir_ID()            
            prep_for("windows", make_list)   

elif choice == "2":
    while True:
        ifile = get_input_file(current_OS)
        if ifile == "error" or ifile == "quit":
            break
        make_folder(ifile, current_OS)

print("Done")
    
    
    
    
    
