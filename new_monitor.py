import csv
import psychopy.monitors.calibTools as T

# Constructs and saves a new monitor to the given pathname based on the
# given photometer data. Photo data file should be in tab delimited form:
# "input level", "grayscale lum", "red gun lum", green gun lum", "blue gun lum"

# Note: When you want to access a monitor saved into a custom path, must
# change the monitorFolder variable inside of the calibTools module, then 
# get the monitor using <module>.Monitor(monitorName)

# Set runtime parameters for monitor:
path = './calibration/'     # where monitors will be stored
# Make sure to change monitorFolder in this module for custom save location
T.monitorFolder = path

monitors = {
'CRT_NEC_FE992': 
dict(monitor_name = 'CRT_NEC_FE992', # name of the new monitor
     calib_file = '%sCRT_NEC_FE992.csv'%path, # photometer data
     width = 35, # width of the screen (cm)
     distance = 50, # distance from the screen (cm)
     size = [800, 600], # size of the screen (px)
     # We can also save notes to our monitor:
     notes = """This is the CRT in 582D, used for psychophysical experiments"""),

'582D_multisync': 
dict(monitor_name = '582J_multisync', # name of the new monitor
     calib_file = '%s582J_multisync_gamma.csv'%path, # photometer data
     width = 40.8, # width of the screen (cm)
     distance = 120, # distance from the screen (cm)
     size = [800, 600], # size of the screen (px)
     # We can also save notes to our monitor:
     notes = """ This monitor is the LCD in the psychophysical testing room
     582D and supposedly resembles the monitor in the scanner"""),

'BIC3T_avotec':
dict(monitor_name = 'BIC3T_avotec', # name of the new monitor
     calib_file = '%sBIC3T_avotec_gamma.csv'%path, # photometer data
     width = 16 , # width of the screen (cm)
     distance = 35.5, #  distance from the screen (cm)
     size = [800, 600], # size of the screen (px)
     # We can also save notes to our monitor:
     notes = """ This is the Acotec LCD projector located in the scanner"""),

#Just for testing:
'testMonitor':
    dict(monitor_name = 'testMonitor', # name of the new monitor
		 calib_file = '%sBIC3T_avotec_gamma.csv'%path, # dummy photometer data
    width = 32, # width of the screen (cm)
    distance = 80, # (virtural) distance from the screen (cm)
    size = [800, 600], # size of the screen (px)
    # We can also save notes to our monitor:
    notes = """ Rough estimate of parameters on a laptop, just for testing""")
}

for m in monitors.keys():
    monitor = monitors[m]
    # Initialize our intermediary variables and open the text file
    fileobj = open(monitor['calib_file'], 'rU') 
    csv_read = csv.reader(fileobj)
    input_levels = [];
    lums = {'R' : [], 'G' : [], 'B' : [] } 

    gamma_vals = lums.copy()
    # Read input levels and luminescence values from file
    for row in csv_read:
        input_levels.append(float(row[0]))
        lums['R'].append(float(row[1]))
        lums['G'].append(float(row[2]))
        lums['B'].append(float(row[3]))

    # Calculate the gamma grid based on given lums
    gammaGrid = []
    for val in ['R','G','B']:
        calculator = T.GammaCalculator(inputs = input_levels, lums = lums[val])
        gamma_vals[val] = [calculator.a,calculator.b, calculator.gamma]
        gammaGrid.append(gamma_vals[val])
    
    # Create the new monitor, set values and save
    newMon = T.Monitor(monitor['monitor_name'],
                       monitor['width'],
                       monitor['distance'])
    newMon.setSizePix(monitor['size'])
    newMon.setNotes(monitor['notes'])
    newMon.setGammaGrid(gammaGrid)
    newMon.setCalibDate()
    newMon.saveMon()
