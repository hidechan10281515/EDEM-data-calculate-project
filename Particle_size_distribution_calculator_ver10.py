# created 2020/12/10
# author: Hideharu Sugimoto
# script for post-processing EDEM for Calculating Displacement

#Importing libraries
from edempy import Deck
import numpy as np
import sys
import os 
import time


#Say Hallo
print("-------------------------------------------------------")
print("Particle size distribution calculator ")
print("Hideharu Sugimoto")
print("Ver1.0")
print("2020/12/10")
print("-------------------------------------------------------")



# Start mesuaring program execution time
start = time.time()


np.set_printoptions(suppress=True)
#Reading in simulation data
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        if file.endswith(".dem"):
            name=file.replace(".dem","")
            print ("-------------------------------------------------------")
            print ("Loading: "+str(name)+".dem")
            print ("-------------------------------------------------------")
            deck=Deck(os.path.join(root,file))
            
            
            print ("-------------------------------------------------------")
            print ("Time? and interval?")
            print ("-------------------------------------------------------")
            
            DEMtime = input()
            interval = input()
            
            print ("-------------------------------------------------------")
            print (time)
            print (interval) 
            print ("-------------------------------------------------------")
            
            print ("-------------------------------------------------------")
            print ("Particle ID?")
            print ("-------------------------------------------------------")
            
            Particle_ID = input()
            
            timestep = float(DEMtime) / float(interval)
            
            
            
            
            num = deck.timestep[timestep].particle[Particle_ID].getNumParticles()
            radi = np.zeros([num,1])
            radi = deck.timestep[timestep].particle[Particle_ID].getSpherePhysicalRadius()
            
            radi_sort = np.sort(radi, axis = 0)
            
            radi_sum = np.sum(radi_sort)
            
            percent = radi_sort / radi_sum
            
            percent_sum = np.zeros([num,1])
            
              
            percent_sum =  np.cumsum(percent)
            
            # percent_sum = percent_sum.reshape()percent_sum
            
            radi_sort = radi_sort.flatten()
            
            data = np.stack([percent_sum,radi_sort])
            
            data = np.rot90(data, -1)
            
            
            
            # Making csv file
            with open('Particle_size_distribution' + '.csv', mode='a',encoding='ASCII') as csv:
                
                np.savetxt(csv,data ,delimiter=", ", fmt = '%.5f')
                

            csv.close()
                

# Calculate total time
elapsed_time3 = time.time() - start
print ("-------------------------------------------------------")
print("elapsed_time:{0}".format(elapsed_time3) + "[sec]")
print ("-------------------------------------------------------")

print ("----------------------------------------------------------------------------------")
print ("Complete! By Hideharu Kevin Sugimoto")        
print ("----------------------------------------------------------------------------------") 
    
            
            
