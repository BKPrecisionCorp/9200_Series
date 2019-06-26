# This is example code for the BK Precision 9201
# A programming manual for the BK Precision 9201 can be found in chapter 5 of:
# https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/9200_Series_manual.pdf



import visa
import time     #This is used for the sleep function (Delay)



print("This Script is made for the BK9201 Multi-Range DC Power Supply")
manager = visa.ResourceManager()
li = manager.list_resources()
for index in range(len(li)):
    print(str(index)+" - "+li[index])
choice = input("Which Device?: ")
powerSupply_9201=manager.open_resource(li[int(choice)]) #creates an alias (variable) for the VISA resource name of a device
# we do this so we don't have to call that constantly. This is unique to a unit and changes depending on USB port used and serial number of a unit. 
# This will automatically detect connected devices and allows you to select the one you want to run the script on.


#####_________________________________________________________#####     Initial
print("\n")
print("_____Test Code Initialized..._____")
time.sleep(1)                                       # Delay in seconds
powerSupply_9201.write("List:Func 0")
powerSupply_9201.write("OUTP:STATE OFF")            # Disables Output
print("_____Output Disabled_____")

powerSupply_9201.write("syst:rwlock")               # Disables Local Button and Sets Power supply to remote mode
print("Remote Mode Enabled, Local Button Locked")
print("\n")


#####_________________________________________________________#####     Set Voltage and Current, Measure Voltage and Current (Output Off)


powerSupply_9201.write("CURR:level 0.5")            # Sets current output to 0.5 A
print("Output Current:", end=' ')
powerSupply_9201.write("CuRr:level?")               # Prints the current the Power Supply is set to
print(powerSupply_9201.read())
print("\n")
time.sleep(1)
print("Measured Current:", end=' ')
powerSupply_9201.write("measure:current?")          # Prints current the internal ammeter of the supply measures    (Should always be 0)
print(powerSupply_9201.read())
print("\n")

time.sleep(1)
print("Output Voltage: ")
powerSupply_9201.write("VOLT:level 12")             # Sets voltage output to 12 V
powerSupply_9201.write("voLT:LEV?")
print(powerSupply_9201.read())                      # Prints voltage the Power Supply is set to
print("\n")

time.sleep(1)
print("Measured Voltage:", end=' ')        
powerSupply_9201.write("meas:volt?")                # Prints voltage the internal voltmeter of the supply measures  (Should always be 0)
print(powerSupply_9201.read())
print("\n")
print("\n")


#####_________________________________________________________#####     Measure Voltage and Current (Output On)


time.sleep(3)
powerSupply_9201.write("OUTP:STATE ON")             # Enables Output
print("_____Output Enabled_____")
print("\n")
time.sleep(2)

print("Measured Current:", end=' ')
powerSupply_9201.write("measure:current?")          # Prints current the internal ammeter of the supply measures
print(powerSupply_9201.read())
print("\n")

print("Measured Voltage:", end=' ')
powerSupply_9201.write("meas:volt?")                # Prints voltage the internal voltmeter of the supply measures
print(powerSupply_9201.read())
print("\n")
print("\n")

  
#####_________________________________________________________#####         Disable Output  


time.sleep(1)
powerSupply_9201.write("OUTP:STATE OFF")            # Disables Output
print("_____Output Disabled_____")    
print("\n")
print("\n")


#####_________________________________________________________#####         Test Range


print("_____Range Testing..._____")    

powerSupply_9201.write("curr:step 0.1;lev 5")       # Sets step size of current to 0.1 Amps
powerSupply_9201.write("volt:step 1;lev 30")        # Sets step size of voltage to 1 Volt
time.sleep(0.2)


for x in range(0, 80):                              # a FOR loop interating 80 times
    if x < 20:
       powerSupply_9201.write("curr:level up") 
       powerSupply_9201.write("volt:level down") 
       time.sleep(0.2)                              # increases voltage and current 20 steps
    elif x < 60:
       powerSupply_9201.write("curr:level down") 
       powerSupply_9201.write("volt:level up") 
       time.sleep(0.2)                              # decreases voltage and current 40 steps
    else:
       powerSupply_9201.write("curr:level up") 
       powerSupply_9201.write("volt:level down") 
       time.sleep(0.2)                              # increases voltage and current 20 steps

print("_____Range Testing Complete_____")  
print("\n")
print("\n")


#####_________________________________________________________#####         Create List


time.sleep(1)
powerSupply_9201.write("OUTP:STATE OFF")            # Disables Output    
powerSupply_9201.write("curr:level 0")              # Resets Voltage and Current levels
powerSupply_9201.write("volt:level 0") 
time.sleep(1)

print("_____Creating List..._____")       
powerSupply_9201.write("List:Func 1")               # Set unit to list mode
time.sleep(0.1)
powerSupply_9201.write("LIST:LOAD 1")               # Loads one of the 10 lists, input value is from 0 to 9. This loads list 1 to be edited

voltageCenter = 30
currentCenter = 5
voltageOutput = 0
currentOutput = 0

print(1)
print(voltageOutput)
print(currentOutput)
print("\n")

for x in range(1, 152):                             # a FOR loop iterating 150 times (the max length of a list who's indices are from 1 to 151)
    if x < 21:
       powerSupply_9201.write("list:time %d,0.2" % (x))     # Writes a time value to X slot in the list. Notice how we write a variable to the list.
       voltageOutput = voltageCenter + (x - 1)
       powerSupply_9201.write("list:volt %d,%.3f" % (x, voltageOutput))     # Writes a voltage value to X slot in the list
       currentOutput = round((currentCenter - (x - 1)*0.1), 1)
       powerSupply_9201.write("list:curr %d,%.3f" % (x, currentOutput))     # Writes a current value to X slot in the list
    elif x < 61:
       powerSupply_9201.write("list:time %d,0.2" % (x))
       voltageOutput = (voltageCenter + 20) - (x - 21)
       powerSupply_9201.write("list:volt %d,%.3f" % (x, voltageOutput))
       currentOutput = round(((currentCenter - 2) + (x - 21)*0.1), 1)
       powerSupply_9201.write("list:curr %d,%.3f" % (x, currentOutput)) 
    elif x < 82:
       powerSupply_9201.write("list:time %d,0.2" % (x))
       voltageOutput = (voltageCenter - 20) + (x - 61)
       powerSupply_9201.write("list:volt %d,%.3f" % (x, voltageOutput))
       currentOutput = round(((currentCenter + 2) - (x - 61)*0.1), 1)
       powerSupply_9201.write("list:curr %d,%.3f" % (x, currentOutput)) 
    else:
       powerSupply_9201.write("list:time %d,0" % (x))
       voltageOutput = 0
       powerSupply_9201.write("list:volt %d,0" % (x))
       currentOutput = 0
       powerSupply_9201.write("list:curr %d,0" % (x)) 
    print(x)
    print(voltageOutput)
    print(currentOutput)
    print("\n")                                     # This FOR loop does the same as the range testing FOR loop, except it edits a list and stores the values in the list
    print("_____List Complete_____")  


#####_________________________________________________________#####     Save List and Read List Steps


time.sleep(2)
powerSupply_9201.write("List:save 1")               # We save the list to slot 1
powerSupply_9201.write("List:volt? 1")              # To make sure the list saved we look at slot 1 to see if it is consistant with what we wanted
print(powerSupply_9201.read())
powerSupply_9201.write("List:curr? 1") 
print(powerSupply_9201.read())
powerSupply_9201.write("List:time? 1") 
print(powerSupply_9201.read())
  
print("_____List Saved_____") 
print("\n")
print("\n")


#####_________________________________________________________#####     Read List


time.sleep(0.2)

print("_____Running List 1..._____") 
powerSupply_9201.write("trig:sour bus")     # We set the trigger mode to BUS. This way the power supply will be looking for a trigger signal from the computer rather than the trigger button.
powerSupply_9201.write("trig")              # We send the trigger signal, when in list mode, the supply waits for a trigger signal to navigate the loaded list.

time.sleep(25)                              # We have to wait until the list finishes so we can send more instructions
print("_____List Complete_____") 
print("\n")
print("\n")


#####_________________________________________________________#####     End


print("_____Test Complete... Clearing_____") 
powerSupply_9201.write("List:Func 0")
powerSupply_9201.write("OUTP:STATE OFF")    # Disables and Resets    
powerSupply_9201.write("curr:level 0") 
powerSupply_9201.write("volt:level 0") 
powerSupply_9201.write("syst:LOC")          # Sets system to local mode


print("_____Goodbye_____")

