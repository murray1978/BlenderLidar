# BlenderLidar
 Blender Plugin/script to import point data from a basic lidar using an LDS006, or other lidar.
 
## Using the script.
  In order to use the script you need to install pySerial into blender.
  1. download pyserial-3.5.tar.gz
  2. unzip the contents to a temp folder
  3. copy the folder serial to your Blender 2.91\2.91\scripts\modules folder
  4. run blender
  5. open the blender python terminal
  6. type import serial and hit return
  7. if there is an error then pyserial has not been installed correct or I have missed a step for you :)
 
  Currently the script will import a 2D slice of data, rotated on the y axis
 
## Using other Lidar Units
  The current script read's directly from the lidar unit, in the function getRange() there is a statemachine to read the lidar data, you will need to modify this bit
  if your lidarunit has two bytes for the header, gives you a different angle and range format.
 
## Future Plans
  Use an Arduino or Rpi to control the ascention angle, and add that to the data from the lidar.
  Create a UI for blender to control the lidar
  Web interface for remote access
  
## Help with Lidar
 For help with lidar unit's I have followed this discord channel https://discord.com/channels/647756128058605581/861328431932768296
 For help with this script use the github Issues function for this project.
 If you do modify the above code expect frequent blender crash's
