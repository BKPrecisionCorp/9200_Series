# This is example code for the BK Precision 9200 Series Power Supplies
# A programming manual for the BK Precision 9200 Series can be found in chapter 5 of:
# https://bkpmedia.s3.amazonaws.com/downloads/manuals/en-us/9200_Series_manual.pdf

# Lets make a list
# List mode allows the power supply to store a list, which is a series of up to 150 steps. This list (up to 10) can be stored in the supply's memory. 
# Each step can have it's own voltage, current, and time. The list is traversed when the power supply receives a trigger signal.
# In order to enter list mode you must first enable it. Then you can simply run one of the lists or edit one of them. We will create a simple list now.


import visa
import time     #This is used for the sleep function (Delay)


print("This Script is made for the BK9200 Series Multi-Range DC Power Supplies")
manager = visa.ResourceManager()
li = manager.list_resources()
for index in range(len(li)):
    print(str(index)+" - "+li[index])
choice = input("Which Device?: ")
powerSupply_9200=manager.open_resource(li[int(choice)]) #creates an alias (variable) for the VISA resource name of a device
# we do this so we don't have to call that constantly. This is unique to a unit and changes depending on USB port used and serial number of a unit. 
# This will automatically detect connected devices and allows you to select the one you want to run the script on.




powerSupply_9200.write("List:Func 1")       # We enable list mode, 0 is off, 1 is on
time.sleep(0.1)
powerSupply_9200.write("LIST:LOAD 0")       # Loads one of the 10 lists, input value is from 0 to 9. We load the 0th list.

powerSupply_9200.write("list:volt 1,10")
powerSupply_9200.write("list:volt 2,21")
powerSupply_9200.write("list:volt 3,3.33")
powerSupply_9200.write("list:volt 4,7")
powerSupply_9200.write("list:volt 5,60")

powerSupply_9200.write("list:curr 1,0.5")
powerSupply_9200.write("list:curr 2,2.3")
powerSupply_9200.write("list:curr 3,6")
powerSupply_9200.write("list:curr 4,6.5")
powerSupply_9200.write("list:curr 5,9.9999")

powerSupply_9200.write("list:time 1,0.5")
powerSupply_9200.write("list:time 2,2")
powerSupply_9200.write("list:time 3,1")
powerSupply_9200.write("list:time 4,0.8")   # Not some of these random values may trigger the power supplies power limit of 200W, which means the power supply will limit the values
powerSupply_9200.write("list:time 5,6")     # Here we fulfill the first 5 slots of the list with their respective voltage, current, and time values


powerSupply_9200.write("List:save 0")       # We save the list to slot 0
powerSupply_9200.write("List:time? 2")      # To make sure the list saved we look at slot 2 to see if it is consistant with what we wanted
print(powerSupply_9200.read())

time.sleep(0.2)

# Now we want to run our list

powerSupply_9200.write("list:rep 3")        # Because our list is only 5 slots, we'll set it to repeat itself 3 times (0 - 65535)      
powerSupply_9200.write("trig:sour bus")     # We set the trigger mode to BUS. This way the power supply will be looking for a trigger signal from the computer rather than the trigger button.
powerSupply_9200.write("trig")              # We send the trigger signal.
