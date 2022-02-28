#At some point will need to break this up into __init__.py, import_lidar.py and lds006.py

import sys
import serial
import time
from enum import Enum
import math

class State(Enum):
    START1 = 0
    START2 = 1
    HEADER = 2
    DATA = 3

class LDS006:
    def __init__(self, serialPort = "com10", baudRate = 115200):
        self.serialPort = serialPort
        self.baudRate = baudRate
        self.connected = False
        self.scanning = False

    def connect(self):
        if self.connected == False:
            try:
                self.ser = serial.Serial(self.serialPort, self.baudRate, timeout=0.1)
            except:
                print("Cound not connect to device")
                exit()
        self.connected = True
        self.ser.write(b'$')
        self.ser.write(b"stoplds$")
        self.scanning = False
        print("LDS Connected")

    def disconnect(self):
        self.ser.close()
        self.connected = False
        self.scanning = False

    def readBytes(self, count):
        data = self.ser.read(count)
        if len(data) != count:
                    return False
        return data

    def startLDS(self):

        if self.connected == False:
            self.connect();
        self.ser.write(b'$')
        self.ser.write(b"startlds$")
        self.scanning = True

    def stopLDS(self):
        if self.connected == False:
            return
        self.ser.write(b"stoplds$")
        self.scanning = False
        
    def getRange(self):
        if self.connected == False:
            self.connect()
        if self.scanning == False:
            self.startLDS()

        run = True
        
        angle = 0xFB
        rpm = 0
        distance = 0

        state = State.START1
        while run:
            if state == State.START1:
                data = self.readBytes(1)
                if data == False:
                    break;
                if data[0] == 0xFA:
                    state = State.DATA
                else:
                    state = State.START1
                continue
            elif state == State.DATA:
                data = self.readBytes(21)
                if data == False:
                    break
                if data[0] == 0xFB:
                    angle = 0xFB
                    rpm = 0xFB
                    return angle, rpm, distance
                angle = 4 * (data[0] - 0xA0)
                
                rpm = int(data[2] << 8) + int(data[1])

                distance += int(data[4] << 8) + int(data[3])
                #distance += int(data[8] << 8) + int(data[7])
                #distance += int(data[13] << 8) + int(data[12])
                #distance += int(data[17] << 8) + int(data[16])
                
                #distance = distance / 4
                #print("getRange " + str(angle) + " " + str(rpm/100) + " " + str(distance))
                run = False
            else:
                print("error")

        return angle, rpm, distance


class ImportLidar():
    bl_idname = "object.ImportLidar"
    bl_label = "Import Lidar Data"
    
    #https://blender.stackexchange.com/questions/23086/add-a-simple-vertex-via-python
    def point_cloud(self, ob_name, coords, edges=[], faces=[]):
        """Create point cloud object based on given coordinates and name.

        Keyword arguments:
        ob_name -- new object name
        coords -- float triplets eg: [(-1.0, 1.0, 0.0), (-1.0, -1.0, 0.0)]
        """

        # Create new mesh and a new object
        me = bpy.data.meshes.new(ob_name + "Mesh")
        ob = bpy.data.objects.new(ob_name, me)

        # Make a mesh from a list of vertices/edges/faces
        me.from_pydata(coords, edges, faces)

        # Display name and update the mesh
        ob.show_name = True
        me.update()
        return ob
    
    def degToRad(self,deg):
        PI = 3.14
        return deg * (PI / 180.0)
        
    
    def createPointCloud(self, offset=[]):
    
        
        scanner = LDS006()
        scanner.connect()
        
        posDec = 0
        posAsc = 90
        pointCloud = list()

        #howmany points to capture
        pointsDec = 360
        pointsAsc = 36
        
        while pointsDec > 0 :
            pointsDec -= 1
            posDec, rpm, range = scanner.getRange()
            if posDec != 0xFB:
                #Range is in mm, convert to mm
                range = range  / 1000
                _x = (range * math.sin(self.degToRad(posDec) * math.cos(self.degToRad(posAsc)))) + offset[0]
                _y = (range * math.sin(self.degToRad(posDec) * math.sin(self.degToRad(posAsc)))) + offset[1]
                _z = (range * math.cos(self.degToRad(posDec))) + offset[2]
                pointCloud += [(_x,_y,_z)]
                #debug string
                #print(str(posDec) + ',' + str(_x) + ',' + str(_y) + ' ' + str(_z))
                
        scanner.stopLDS()
        
        # Create the object
        #pc = self.point_cloud("point-cloud", [(0.0, 0.0, 0.0)])
        pc = self.point_cloud("point-cloud", pointCloud)
        # Link object to the active collection
        bpy.context.collection.objects.link(pc)

# Alternatively Link object to scene collection
#bpy.context.scene.collection.objects.link(pc)
    
    def execute(self):
        print("Import Lidar")
        offset = [0.0, 0.0, 0.0]
        self.createPointCloud(offset)
        return {'FINISHED'}
        
#def register():
#   bpy.utils.register_class(ImportLidar)

#def unregister():
#    bpy.utils.unregister_class(ImportLidar)

if __name__ == "__main__":
    #register()
    il = ImportLidar()
    il.execute()
    
#--------------- Not Real code below -------------------------------------------------------
#create a new mesh
#mesh = bpy.data.meshes.new(name="MyMesh")
#print(mesh) #just to check






