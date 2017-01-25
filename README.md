# localisation_code
organises cells based on data gathered from volocity software with regards to fluorescence intensity

# cells must be organised by folder
# cells can be exported from volocity version 6.3 as .csv or .txt files

# the code will use python 3 and requires the matplotlib and numpy libraries
# recommend installing anaconda so that these are already installed

# TO RUN
# should work for windows and linux OS

# FOR WINDOWS
# open cmd
# go to the folder above where your cell data is saved.
# download the two files: Localisation_code.py and bashreplace5.py to this location
# type "python bashreplace5.py"
# reply to prompts, images should autogenerate

# FOR LINUX
# open terminal
# go to the folder above where your cell data is saved.
# download the two files: Localisation_code.py and bashreplace5.py to this location
# type "python bashreplace5.py"
# reply to prompts, images should autogenerate

# the code will prompt for 2-4 things:
(1) folder identifier
(2) whether or not to organise by localisation
  if yes:
  (a) enter the distance from the ends of the cells that are considered for having
  higher localisation
  (b) enter the percent that the ends have to be higher than the middle average
  such that these are considered localised fluorescence
