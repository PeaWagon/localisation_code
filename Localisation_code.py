# object orientated programming version of analysis code for cells

# JEN
# January 27th, 2017

############################################################################

from statistics import stdev, mean
from matplotlib import pyplot as pl
import numpy as np
from math import sqrt

class Localisation(object):
    
    def __init__(self, input_name, operating_system, dict1, dict_main, NL_split, sorter, local0, local1, local2, dcutoff, pdiff):
        self.input_name = input_name    # name of csv file with cell data
        self.operating_system = operating_system # running on windows/linux
        self.dict1 = dict1              # dictionary containing all cell data
        self.dict_main = dict_main      # dict for bins containing each cell
        self.NL_split = NL_split        # number of data points for graph
        self.sorter = sorter        # True (do localisation), False (don't)
        self.local0 = local0        # dict of cells with no localisation
        self.local1 = local1        # dict of cells with 1 pole localisation
        self.local2 = local2        # dict of cells with 2 pole localisation
        self.dcutoff = dcutoff      # distance cutoff
        self.pdiff = pdiff          # percent difference from middle
    
    def normalise(self, values):
        """ input is a non-normalised list
            output is a normalised list
            formula is:
                (x-min)/(max-min)
        """
        result = []
        for item in values:
            result.append((item-min(values))/(max(values)-min(values)))
        return result
    
    def open_input(self):
        """ collects the data from the csv input file for each cell
            write the data to a dictionary (self.dict1)
            the dictionary keys are the names of the cells
            the dictionary value is a list of lists, with two parts
            the first part of the list of lists is the normalized
            intensity values
            the second part of the list of lists is the normalized
            distance values
            
            i.e. dict1 = { cell1: [[NI_list],[ND_list]] }
            all values are floating point numbers
        """
        with open(self.input_name, "r") as f:
            for line in f:
                line = line.strip()                         #get rid of \n
                if line[0] != ',':                          #Intensity
                    name = line[:line.index(',')]       #assign ProP cell name 
                    intensity = line[line.index("I")+2:]    #get rid of header
                    intensity_list = intensity.split(",")   #list by comma
                    try:                                #remove blanks/newlines
                        intensity_list = intensity_list[0:intensity_list.index('')]
                    except ValueError:
                        pass
                    NI_list = self.normalise([float(i) for i in intensity_list])
                    self.dict1[name] = [NI_list,'']    #add floats to dictionary
                elif line[0] == ',':                      #normalised distances
                    dist = line[line.index('0'):]           #get rid of header
                    dist_list = dist.split(",")             #list by comma
                    try:
                        dist_list = dist_list[0:dist_list.index('')]
                    except ValueError:
                        pass
                    ND_list = [float(i) for i in dist_list]
                    self.dict1[name][1] = ND_list    
    
    def ask_organise(self):
        """ asks whether to sort each file in the group via 
            localisation (aka at one pole, two poles, or evenly
            distributed)
            returns False if no sorting is requested.
            executes organise_cells(self) if sorting is requested
        """
        query = 'blank'
        while query != "Y" and query != "n":
            query = input("Sort files by their localisation patterns? (Y/n) ")
        if query == 'Y':
            self.sorter = True
            self.get_local_values()         # determine pdiff and dcutoff
            q1 = self.organise_cells()      # sort cells by localisation
            while q1 == 'error':            # if ill-defined ends
                self.local0 = {}            # reset dictionaries
                self.local1 = {}
                self.local2 = {}
                self.get_local_values()     # reset pdfiff and dcutoff
                q1 = self.organise_cells()  # try again
            self.write_cell_local()         # write data to a csv file
            return True
        elif query == 'n':
            self.sorter = False
            return False
    
    def get_local_values(self):
        """ gets dcutoff and pdiff from user. reprompts for input
            if the user inputs something wrong
        """
        # set dcutoff
        while True:
            self.dcutoff = input("Choose a distance cut-off: ")
            try: self.dcutoff = float(self.dcutoff)
            except ValueError:
                print("Please enter numbers only. No special characters or letters.")
                continue
            if 0.5 <= self.dcutoff <= 0:
                print("Value must be larger than 0 and smaller than 0.5. Please try again.")
                continue
            break
        # set pdiff    
        while True:
            self.pdiff = input("Choose a percentage difference from average: ")
            try: self.pdiff = float(self.pdiff)
            except ValueError:
                print("Please enter numbers only. No special characters or letters.")
                continue
            if self.pdiff <= 0:
                print("Value must be larger than 0. Please try again.")
                continue
            break
    
    def organise_cells(self):
        """ designates localisation patterns for each cell within 
            a folder/group
        """      
        for key in self.dict1:
            """ (1) get distance values between DC and 1-DC
                (2) get the average of the intensity value
                    between DC, 1-DC
                (3) determine if any intensity values between
                    0, DC and/or 1-DC, 1 are higher than 100% +
                    PD of average intensity value in center
                (4) group accordingly (no pole, one pole, two pole)
            
            """
            middle_values = self.sort_middle(key)
            if middle_values == 'error':
                return 'error'
           
            det_localisation = self.sort_cell(key, middle_values)
           
            if det_localisation == 0:
                self.local0[key] = self.dict1[key]
            elif det_localisation == 2:
                self.local2[key] = self.dict1[key]
            # add all right localised cells to dict local1
            elif det_localisation == 'r1':
                self.local1[key] = self.dict1[key]
            # reverse cells if they are left localised and add to local1
            elif det_localisation == 'l1':
                # reverse intensity values
                self.dict1[key][0] = self.dict1[key][0][::-1]
                # reverse distance values
                self.dict1[key][1] = self.dict1[key][1][::-1]
                # add to local1
                self.local1[key] = self.dict1[key]
                
    def write_cell_local(self):
        """ (5) write data to .csv file for reference
            (6) print number of cells in each group
        """
        g = str(self.input_name[:-4])
        
        with open(g+'_localisation_data.csv', 'w') as l:
            l.write("Chosen distance cutoff, "+str(self.dcutoff)+'\n')
            l.write("Chosen percent difference, "+str(self.pdiff)+'\n')
            l.write(g+" delocalised count, "+str(len(self.local0))+'\n')
            l.write(g+" one pole count, "+str(len(self.local1))+'\n')
            l.write(g+" two pole count, "+str(len(self.local2))+'\n')
            l.write('\n')
            l.write(g+" delocalised cells, "+', '.join(str(key0) for key0 in sorted(self.local0))+'\n')
            l.write(g+" one pole cells, "+', '.join(str(key1) for key1 in sorted(self.local1))+'\n')
            l.write(g+" two pole cells, "+', '.join(str(key2) for key2 in sorted(self.local2))+'\n')
            l.write('\n')
        
        print()
        print('Found '+str(len(self.local0))+' delocalised cells in '+str(self.input_name)+'.')   
        print('Found '+str(len(self.local1))+' cells with polar localisation at one pole in '+str(self.input_name)+'.') 
        print('Found '+str(len(self.local2))+' cells with polar localisation at both poles in '+str(self.input_name)+'.')  
        print()
    
    
    def sort_middle(self, key):
        """ determines the distance values of within the
            cut-off points (dcutoff, 1-dcutoff)
            returns a list containing:
            [0] starting middle value index
            [1] ending middle value index
            [2] average of the middle intensity values 
        """
        key_dists = self.dict1[key][1]
        key_intens = self.dict1[key][0]
        
        if key_dists[1] > self.dcutoff:
            print("Error. Cell "+str(key)+" only has one data point to define its end. Please increase the value for distance cut-off.")
            return 'error'
        elif key_dists[-2] < 1-self.dcutoff:
            print("Error. Cell "+str(key)+" only has one data point to define its end. Please increase the value for distance cut-off.")
            return 'error' 
  
        # key's normalised distances go from 0-1
        elif key_dists[0] == 0 and key_dists[-1] == 1.0:
            for i, value in enumerate(key_dists):
                if value > self.dcutoff:
                    middle_start_index = i
                    break
            for i2, value2 in enumerate(key_dists):
                if value2 > 1-self.dcutoff:
                    middle_end_index = i2-1
                    break        
        
        middle_int_values = key_intens[middle_start_index:middle_end_index+1]
        
        # make sure the number of values in the middle is non-zero
        # otherwise, will have to start the process again for filling
        # localisation dictionaries
        try:
            av_middle = sum(middle_int_values)/len(middle_int_values)
        except ZeroDivisionError:
            print("The cell "+str(key)+' has an empty set of middle values, which has caused a division by zero. Please re-enter the distance cut-off.')
            return 'error'
        
        return [middle_start_index, middle_end_index, av_middle]
        
    def sort_cell(self, key, middle_values):
        """ returns 0 if no localisation at poles is found
            returns l1 if localisation is found at left pole ONLY
            returns r1 if localisation is found at right pole ONLY
            returns 2 if localisation is found at both poles
            note: localisation means that the AVERAGE value at 
            either pole is higher (by pdiff %) than the average 
            value in the middle of the cell
        """
        counter = ''
        av_int = middle_values[2]
        middle_start = middle_values[0]
        middle_end = middle_values[1]
        int_to_beat = (1+(self.pdiff/100))*av_int
        
        # check beginning of cell for intensity values higher 
        # than average intensity value from middle values
        # times 100+pdiff%
        for value in self.dict1[key][0][:middle_start]:
            if value > int_to_beat:
                counter+='l'
                break
       
        # check end of cell for intensity values as before
        for value2 in self.dict1[key][0][middle_end+1:]:
            if value2 > int_to_beat:
                counter+='r'
                break
        
        if counter == 'lr':
            return 2
        elif counter == 'l':
            return 'l1'
        elif counter == 'r':
            return 'r1'
        elif counter == '':
            return 0
        
    def choose_NL_split(self):
        """ determines how many times the normalised distance can
            be split such that there is at least one data point
            in each "bin" for each cell
        """
        max_bins_list = []
        counter = 1
        for key in self.dict1:
            while self.compare_checklist(key, counter) == True:
                counter += 1
            else:
                counter -= 1
                max_bins_list.append(counter)
                counter = 1
        self.NL_split = min(max_bins_list)
        return min(max_bins_list)
                
    def make_checklist(self, NL_split):
        """ uses NL_split to divide 1.0 evenly into pieces
            returns a list with these values
            each value has max 3 decimal places
        """        
        check_list = [ "%.3f" % ((1.0/NL_split)*x) for x in range(1,NL_split+1) ]
        return [ float(i) for i in check_list ]
    
    
    def compare_checklist(self, key, counter):
        """ uses counter to determine how many bins to use
            then checks if the key contains one value per bin
            returns true if there is at least one value for each
            bin from the key
            returns false if a bin is empty from one key
            note: not necessary step, but each time a value is 
            found to be in a given range, it is replaced (in a copy
            list) with -1.
        """
        checklist = self.make_checklist(counter)
        comp_list = self.dict1[key][1][:]
        passed_checks = 0
        for num, check in enumerate(checklist):
            for num2, value in enumerate(comp_list):
                if num == 0:
                    if 0 <= value <= checklist[num]: 
                        passed_checks += 1
                        comp_list[num2] = -1
                        break
                elif checklist[num-1] < value <= checklist[num]:
                    passed_checks += 1
                    comp_list[num2] = -1
                    break
        if passed_checks == len(checklist):
            return True
        else:
            return False
            
    def make_dict_main(self):
        """ keys in dictionary correspond to 1-NL_split value
            eg dict_1 dict_2 ... dict_NL_split
            each is written to contain two empty lists
        """
        for i in range(1,self.NL_split+1):
            self.dict_main["dict_"+str(i)] = [[],[]]  #initialise main dictionary
        return self.dict_main
    
    def analyse_dict(self):
        check_list = self.make_checklist(self.NL_split)
        for key in self.dict1:
            for counter1, value in enumerate(self.dict1[key][1]):
                for counter2, check in enumerate(check_list):
                    if value <= check:
                        self.dict_main['dict_'+str(counter2+1)][0].append(self.dict1[key][0][counter1])
                        self.dict_main['dict_'+str(counter2+1)][1].append(value)
                        break          
        return self.dict_main
    
    def write_dict_main(self):
        """ writes a file containing rows, where each row is intensity average
            followed by distance average for each segment in 1-NL_split
            output name is input name with _output added
        """
        # statistics will throw an error if there are not at least 
        # two datapoints for standard deviation and mean calculations
        if len(self.dict1) == 1:
            key_name = str([key for key in self.dict1]).strip("'[]'")
            print("Only one cell ("+key_name+")"+" available in "+str(self.input_name)+". Unable to plot.")
            print()
            return 'onecell'
            
        output_name = self.input_name[:-4]+'_output.csv'
        with open(output_name, "w") as g:
            g.write("av_intensity,stdev_intensity,av_distance,stdev_distance\n")
            for i in range(1, self.NL_split+1):
                key_name = "dict_"+str(i)
                av_intensity = mean(self.dict_main[key_name][0])
                stdev_intensity = stdev(self.dict_main[key_name][0])
                #av_error_int = stdev_intensity/sqrt(len(self.dict_main[key_name][0]))
                av_dist = mean(self.dict_main[key_name][1])
                stdev_dist = stdev(self.dict_main[key_name][1])
                #av_error_dist = stdev_dist/sqrt(len(self.dict_main[key_name][1]))
                line = str(av_intensity)+','+str(stdev_intensity)+','+str(av_dist)+','+str(stdev_dist)+'\n'
                g.write(line)
    


            
    
    def plot_data(self):
        """ uses matplotlib to make pictures with shading for y-error
            from http://stackoverflow.com/questions/12957582/matplotlib-plot-
            yerr-xerr-as-shaded-region-rather-than-error-bars
        """
        y = []
        x = []
        y_error = []

        # try to fix plot layout issues
        # on my windows machine, the computer crops off the axis labels
        # works fine without this fix for ubuntu
        # http://stackoverflow.com/questions/6774086/why-is-my-xlabel-cut-off-in-my-matplotlib-plot
        if self.operating_system == 'windows':    
            pl.rcParams.update({'figure.autolayout': True})        

        for i in range(1, self.NL_split+1):
            key_name = "dict_"+str(i)
            y.append(mean(self.dict_main[key_name][0]))# average intens. values
            y_error.append(stdev(self.dict_main[key_name][0])) #stdev ints.
            #y_error.append((stdev(self.dict_main[key_name][0]))/sqrt(len(self.dict_main[key_name][0]))) # standard error of intensity
            x.append(mean(self.dict_main[key_name][1])) # average distance vls
        
        y_upper=[]
        y_lower=[]
        for index,value in enumerate(y):
            y_upper.append(y[index]+y_error[index])
            y_lower.append(y[index]-y_error[index])
        # pl.figure(figsize=(10,8))
        pl.rc('font', family='arial')
        pl.tick_params(axis='y',which='major', labelsize = 18)
        pl.tick_params(axis='x',which='major',labelsize=18)
        #if self.input_name in ["cls-polar.csv", "cls+twopole.csv"]:
        #    pl.tick_params(axis='x',which='major',labelsize=18)
        #else:
        #    pl.tick_params(axis='x',which='major',labelbottom='off')
        pl.yticks(np.arange(-0.2,1.4,0.2))    
        pl.ylim(ymin=-0.2,ymax=1.2)
        pl.plot(x, y, 'k-', lw = 5, color = 'red')
        pl.fill_between(x, y_lower, y_upper, facecolor='red', edgecolor = 'none', alpha = 0.2)
        oname = self.input_name[:-3]+"png"
        if self.operating_system == 'linux':            
            csfont = {'fontname':'Arial','size': 20, 'weight':'bold'}
            tifont = {'fontname':'Arial','size': 16, 'weight':'bold'}
        else:
            csfont = {'fontname':'Arial','size': 16, 'weight':'bold'}
            tifont = {'fontname':'Arial','size': 12, 'weight':'bold'}            
        #pl.title(self.input_name[:-4],**tifont)
        #if self.input_name in ["cls-polar.csv", "cls+twopole.csv"]:
        #    pl.xlabel("Normalized Cell Length",**csfont)
        pl.xlabel("Normalized Cell Length",**csfont)
        pl.ylabel("Normalized Fluorescence Intensity",**csfont)
        pl.savefig(oname,dpi=300)
        pl.close()
        
#############################################################################



        
