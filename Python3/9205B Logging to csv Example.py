# BK PRECISION 
#Sample script to establish communication with a USBTMC instrument"

import pyvisa
import xlsxwriter
import csv
import time
from datetime import datetime

manager = pyvisa.ResourceManager()
li = manager.list_resources()
for index in range(len(li)):
   print(str(index)+" - "+li[index])
choice = input ("Which Device?: ")
powerSupply_9200 = manager.open_resource(li[int(choice)])

DATE_TIME = "%s"%datetime.now() 

#####_____ Command ______#####
ID = "*IDN?\n"
print(powerSupply_9200.query(ID))
IDE= "%s"%(powerSupply_9200.query("*IDN?\n"))

#create file workbook and worksheet 

name = input("Enter a name for the Excel File: ")
outWorkbook = xlsxwriter.Workbook(name + ".xlsx")
Sheet1 = outWorkbook.add_worksheet("Sheet1")
cell_format = outWorkbook.add_format()
cell_format.set_num_format("0.00E+00")

# Create a format to use in the merged range.  
merge_format = outWorkbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'})

centerbold_format = outWorkbook.add_format({
    'bold': 1,
    'border': 0,
    'align': 'center',
    'valign': 'vcenter'})
cell_format.set_num_format(11)
Sheet1.set_column(0, 1, 16)

# Merge 6 columns for ID 
Sheet1.merge_range('A1:F1', IDE, merge_format)

#Basic information of acquired data 
Sheet1.write('A3', 'Date and Time', centerbold_format)
Sheet1.merge_range('B3:D3', DATE_TIME,centerbold_format)
Sheet1.write('A5', "Voltage", centerbold_format)
Sheet1.write('B5', "Current", centerbold_format)
Sheet1.write('C5', "Power", centerbold_format)

print("\n")
print("_____Test Code Initialized..._____")
time.sleep(1)                                       # Delay in seconds
powerSupply_9200.write("List:Func 0")
time.sleep(0.05)
powerSupply_9200.write('OUTP:STATE ON')            # enables Output
print("_____Output ON_____")

powerSupply_9200.write("syst:rwlock")               # Disables Local Button and Sets Power supply to remote mode
print("Remote Mode Enabled, Local Button Locked")


print("_____Range Testing..._____")

powerSupply_9200.write("curr:step 0.1;lev 10.0")            # Sets step size of current to 0.1 Amps
time.sleep(0.05)
powerSupply_9200.write("volt:step 0.1;lev 10.0")            # Sets step size of voltage to 1 Volt
time.sleep(1)

# Add variable for specifying the row and colum
k = 6
l = 6
m = 6

for x in range(0, 10):                                     # a FOR loop interating 600 times
        if x < 3:
            for j in range(0, 10):
                powerSupply_9200.write("MEAS:POWer?")
                time.sleep(0.05)
                a = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:VOLt?")
                time.sleep(0.05)
                b = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:CURr?")
                time.sleep(0.05)
                c = str(powerSupply_9200.read())
                time.sleep(0.05)
                Volt_line = "A%d"%k
                Curr_line = "B%d"%l
                Power_line = "C%d"%m
                Sheet1.write(Volt_line, a, cell_format)
                Sheet1.write(Curr_line, b, cell_format)
                Sheet1.write(Power_line, c, cell_format)
                print(" Watts " + a + " Volts " + b + " Amps " + c)  # Prints the current the Power Supply is set to
                time.sleep(0.05)
                k += 1    
                l += 1
                m += 1
            powerSupply_9200.write("volt:level up")
            time.sleep(1.5)                             # increases voltage 200 steps

        elif x < 6:
            for j in range(0, 10):
                powerSupply_9200.write("MEAS:POWer?")
                time.sleep(0.05)
                a = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:VOLt?")
                time.sleep(0.05)
                b = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:CURr?")
                time.sleep(0.05)
                c = str(powerSupply_9200.read())
                time.sleep(0.05)
                print(" Watts " + a + " Volts " + b + " Amps " + c)  # Prints the current the Power Supply is set to
                time.sleep(0.05)
                k += 1    
                l += 1
                m += 1
            powerSupply_9200.write("volt:level down")

            time.sleep(1.5)                              # decreases voltage 400 steps
            for j in range(0, 10):
                powerSupply_9200.write("MEAS:POWer?")
                time.sleep(0.05)
                a = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:VOLt?")
                time.sleep(0.05)
                b = str(powerSupply_9200.read())
                time.sleep(0.05)
                powerSupply_9200.write("MEAS:CURr?")
                time.sleep(0.05)
                c = str(powerSupply_9200.read())
                time.sleep(0.05)
                print(" Watts " + a + " Volts " + b + " Amps " + c)  # Prints the current the Power Supply is set to
                k += 1    
                l += 1
                m += 1
print("Data Acquired")

outWorkbook.close()

powerSupply_9200.close()