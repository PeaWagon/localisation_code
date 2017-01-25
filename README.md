# localisation_code
This code organises cells based on data gathered from volocity software with regards to fluorescence intensity.

A few set up items:  
- cells must be grouped in a single folder
- the data for each cell can be exported from volocity version 6.3 as a .csv or .txt file

As for the code:  
- the code will use python 3 and requires the matplotlib and numpy libraries
- recommend installing anaconda so that these are already installed
- should work for windows and linux OS

## FOR WINDOWS
1. Go to the folder above where your cell files are saved.
2. Download the two files: Localisation_code.py and bashreplace.py to this location.
3. Open cmd (command prompt)
4. Go to the folder where the code is saved (the one above the cell files). For help on navigating the cmd, see CMD Notes below.
5. Type "python bashreplace5.py"
6. Reply to prompts, images should autogenerate

## FOR LINUX
1. Go to the folder above where your cell files are saved.
2. Download the two files: Localisation_code.py and bashreplace.py to this location.
3. Open the terminal
4. Go to the folder where the code is saved (the one above the cell files). For help on navigating the terminal, see Terminal Notes below.
5. Type "python bashreplace.py"
6. Reply to prompts, images should autogenerate

## Prompts
The code will prompt for 2-4 things:  
1. folder identifier  
2. whether or not to organise by localisation  
3. Enter the distance from the ends of the cells that are considered for having
  higher localisation  
4. Enter the percent that the ends have to be higher than the middle average
  such that these are considered localised fluorescence  

## CMD Notes
To navigate the filesystem on windows, you first need to know where you files are located, and on which drive they are located. The drive name is usually C:, but if you are using a USB stick, it can be other letters (F:, E:, D:, etc.). To figure out what drive you want, you can look up the letter in My Computer.   
  The next step is to figure out the path to the files. The path starts with the drive letter, followed by the folders that are needed to pass through to get to the localisation code.  
  To use the cmd to travel through the computer, you can use the "dir" command to list all of the files and folders in the given directory. To go to a different folder, type "cd foldername". To go up one level, type "cd..".

## Terminal Notes
To navigate the terminal on linux, use commands such as "cd directoryname" to change directory, "ls" to list the contents of a directory, and "cd .." to go up one level. 
