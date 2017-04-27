# localisation_code
This code organises cells based on data gathered from volocity software with regards to fluorescence intensity.

A few set up items:  
- you have the option to analyse pre-formatted .csv files containing cell data
- you also have the option to analyse raw .csv (comma separated option) or .txt (tab separated option) files (from volocity 6.3 software); these files must be saved per cell, must have columns pertaining to fluorescence intensity and normalised (spelt "Normalized Distance") distance, and must be grouped in a single folder above the current working directory from where the code is run

As for the code:  
- the code will use python 3 and requires the matplotlib and numpy libraries
- recommend installing anaconda so that these are already installed
- should work for windows and linux OS

## FOR WINDOWS
1. Go to the folder above where your cell files are saved or go to the folder where your pre-formatted .csv file is saved.
2. Download the two files: Localisation_code.py and run_localisation.py to this location.
3. Open cmd (command prompt). You can find this program by pressing the windows button and typing "command prompt".
4. Using cmd, go to the folder where the code is saved (the one above the cell folder files or the one containing pre-formatted .csv files). For help on navigating file systems using cmd, see CMD Notes below.
5. Type "python run_localisation.py"
6. Reply to prompts, images should autogenerate.  

## FOR LINUX
1. Go to the directory above where your cell files are saved or go to the directory where your pre-formatted .csv file is saved.
2. Download the two files: Localisation_code.py and run_localisation.py to this location.
3. Open the terminal.
4. Go to the folder where the code is saved (the one above the cell folder files or the one containing pre-formatted .csv files). For help on navigating the terminal, see Terminal Notes below.
5. Type "python run_localisation.py"
6. Reply to prompts, images should autogenerate.

## Prompts
The code will prompt for a few things:  
1. whether to analyse a folder containing raw cell data or a pre-formatted .csv file.  
2. The folder identifier. Note the folder identifier is only necessary if you are analysing folders of raw cell data.   
3. Once the data has been found, whether or not to organise by localisation. Localisation here means that the fluorescence intensity appears more intense at the ends of the cell. 
4. Enter the distance from the ends of the cells that are considered for having
  higher intensity. This number should be between 0 and 0.5. The code will return errors if any cells are missing values in the start, middle, or end segments. Usually these errors are due to choosing a cut-off distance that is too low (i.e. < 0.1) or too high (i.e. > 0.45).  
5. Enter the percent that the ends have to be higher than the middle average
  such that these are considered localised fluorescence.

## CMD Notes
To navigate the filesystem on windows, you first need to know where you files are located, and on which drive they are located. The drive name is usually C:, but if you are using a USB stick, it can be other letters (F:, E:, D:, etc.). To figure out what drive you want, you can look up the letter in My Computer.   
  The next step is to figure out the path to the files. The path starts with the drive letter, followed by the folders that are needed to pass through to get to the localisation code.  
  To use the cmd to travel through the computer, you can use the "dir" command to list all of the files and folders in the given directory. To go to a different folder, type "cd foldername". To go up one level, type "cd..". Note that the cmd is case-insensitive (cd means the same as CD) and accepts "/" or "\".

## Terminal Notes
To navigate the terminal on linux, use commands such as "cd directoryname" to change directory, "ls" to list the contents of a directory, and "cd .." to go up one level. The terminal is case-sensitive (cd does not mean the same thing as CD) and accepts "/" or "\".
