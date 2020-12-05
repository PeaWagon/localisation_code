
# localisation

This code organises cells based on data gathered from volocity software with regards to fluorescence intensity.

[Go back to the code.](https://github.com/peawagon/localisation)

## Features

* analyse pre-formatted .csv files containing cell data
* analyse raw .csv (comma separated option) or .txt (tab separated option) files (from Volocity 6.3 software)

## Requirements

The input files (from Volocity software) must:

* be saved per cell,
* have columns pertaining to fluorescence intensity and normalised (spelt "Normalized Distance") distance, and
* be grouped in a single folder above the current working directory from where the code is run

## Dependencies

* python>=3.5
* matplotlib
* numpy

## Instructions

### Windows

1. Go to the folder above where your cell files are saved or go to the folder where your pre-formatted .csv file is saved.
2. Download the two files: localisation.py and localisation_cli.py to this location.
3. Open cmd (command prompt). You can find this program by pressing the windows button and typing "command prompt".
4. Using cmd, go to the folder where the code is saved (the one above the cell folder files or the one containing pre-formatted .csv files). For help on navigating file systems using cmd, see CMD Notes below.
5. Type `python localisation_cli.py`
6. Reply to prompts, images should autogenerate.  

### Linux

1. Go to the directory above where your cell files are saved or go to the directory where your pre-formatted .csv file is saved.
2. Download the two files: localisation.py and localisation_cli.py to this location.
3. Open the terminal.
4. Go to the folder where the code is saved (the one above the cell folder files or the one containing pre-formatted .csv files). For help on navigating the terminal, see Terminal Notes below.
5. Type `python localisation_cli.py`
6. Reply to prompts, images should autogenerate.

## Prompts

The code will prompt for a few things:

1. Whether to analyse a folder containing raw cell data or a pre-formatted .csv file.  
2. The folder identifier. Note the folder identifier is only necessary if you are analysing folders of raw cell data.
3. Once the data has been found, whether or not to organise by localisation. Localisation here means that the fluorescence intensity appears more intense at the ends of the cell.
4. Enter the distance from the ends of the cells that are considered for having higher intensity. This number should be between 0 and 0.5. The code will return errors if any cells are missing values in the start, middle, or end segments. Usually these errors are due to choosing a cut-off distance that is too low (i.e. < 0.1) or too high (i.e. > 0.45).  
5. Enter the percent that the ends have to be higher than the middle average such that these are considered localised fluorescence.

## CMD Notes

To navigate the filesystem on Windows, you first need to know where you files are located, and on which drive they are located. The drive name is usually C:, but if you are using a USB stick, it can be other letters (F:, E:, D:, etc.). To figure out what drive you want, you can look up the letter in My Computer.

The next step is to figure out the path to the files. The path starts with the drive letter, followed by the folders that are needed to pass through to get to the localisation code.  

To use the cmd to travel through the computer, you can use the `dir` command to list all of the files and folders in the given directory. To go to a different folder, type `cd foldername`. To go up one level, type `cd ..`. Note that the cmd is case-insensitive (cd means the same as CD) and accepts `/` or `\`.

## Terminal Notes

To navigate the terminal on linux, use commands such as `cd directoryname` to change directory, `ls` to list the contents of a directory, and `cd ..` to go up one level. The terminal is case-sensitive (cd does **not** mean the same thing as CD) and accepts `/`.

## Notes About GitHub Pages

You can use the [editor on GitHub](https://github.com/PeaWagon/localisation/edit/master/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

This Pages site uses the layout and styles from the selected Jekyll theme (see [repository settings](https://github.com/PeaWagon/localisation/settings)). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

For help with Github Pages, see the [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact).
