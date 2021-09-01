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
print("EDEM Displacement Calculate Program for Paraview ")
print("Hideharu Sugimoto")
print("Ver1.0")
print("2020/12/10")
print("-------------------------------------------------------")


# Check exsistance of vtk file
for file in os.listdir():
    if file.endswith("vtk"):
        print ("-------------------------------------------------------")
        print("vtk file is exits. Please delete old vtk files!")
        print ("-------------------------------------------------------")
        sys.exit()


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
            
            # Reading in Setting file
            if os.path.exists(os.path.join(root,'Setting.txt')): 
                with open(os.path.join(root,'Setting.txt'), 'r') as file:
                    preferences=file.readlines()
                    sim_end=float(preferences[3])
                    ini_time=float(preferences[5])
                    final_time=float(preferences[7])
                    interval=float(preferences[9])
                    Number_of_output_data=int(preferences[11])
                    Larger_value_delete=str(preferences[13])
                    Threshold = float(preferences[15])
                    Particle_IDs = float(preferences[17])
                    file.close()
                    settings=True
                    
            else:
                settings=False
                sim_end=0
                
                
            #Defining timestep
            ini_timestep=ini_time / interval
            
            
            #Get number of particle IDs
            ids_ini = deck.timestep[ini_timestep].particle[Particle_IDs].getIds()
            
                
            #Declearing arrays
            particle_X_ini=np.zeros([len(ids_ini),1])
            particle_Y_ini=np.zeros([len(ids_ini),1])
            particle_Z_ini=np.zeros([len(ids_ini),1])
            particle_disp_temp_unit=np.zeros([len(ids_ini),4])
            
            particle_disp_temp = np.zeros([len(ids_ini),3])
            
            particle_disp_old = np.zeros([len(ids_ini),3])
            
            
                
            #Declearing arrays for total mass and volume of difference particle type
            
            Particle_Mass=np.zeros([deck.numTypes])
            Particle_Volume=np.zeros([deck.numTypes])
            Particle_volume_confine=np.zeros([deck.numTypes])
            parcicle_coordinateX=np.zeros([deck.numTypes])
            particle_coordinateY=np.zeros([deck.numTypes])
            particle_coordinateZ=np.zeros([deck.numTypes])
            
            D_temp=np.zeros([deck.numTimesteps])


    
            #Check if prefrence file is found
                
            if(sim_end-np.amax(deck.timestepValues)<0.001 and settings==True):
                    
                    print ("-------------------------------------------------------")
                    print ("Processing_1: "+str(name)+".dem")
                    print ("-------------------------------------------------------")
                    
                 
                    

                    #Defining timestep & interval for calculation
                    
                    ini_time_part = ini_time
                    
                    time_sim = final_time - ini_time
                    Num_step = time_sim / interval
                    Each_num_step = Num_step / Number_of_output_data
                    
                    i_cal = ini_time_part / interval
                    
                    
                    #Start loop-----------------------------------------------------------------------------------------
                    #Calculating displacement
                
                    for i in range(Number_of_output_data):
                        if(i<Number_of_output_data):
                           print (i_cal)
                           i_cal_next = i_cal + Each_num_step
                           print(i_cal_next)
               
                        
                           particle_disp_before = deck.timestep[i_cal].particle[Particle_IDs].getPositions()
                           print(particle_disp_before)
                           particle_disp_after = deck.timestep[i_cal_next].particle[Particle_IDs].getPositions()
                           print(particle_disp_after)
                           ids_ini = deck.timestep[i_cal].particle[Particle_IDs].getIds()
                           ids_ini_next = deck.timestep[i_cal_next].particle[Particle_IDs].getIds()
                          
                   
                          
                           elapsed_time1 = time.time() - start
                           print ("-------------------------------------------------------")
                           print("elapsed_time:{0}".format(elapsed_time1) + "[sec]")
                           print ("-------------------------------------------------------")      
                          
                           print ("-------------------------------------------------------")
                           print ("Processing_2: "+str(name)+".dem")
                           print ("-------------------------------------------------------")
                    
                    
                           #Convert unit(mm)
                           particle_disp_before = particle_disp_before * 1000
                           particle_disp_after = particle_disp_after * 1000
                           
                           # Extract Component
                           particle_X_ini = particle_disp_before[:,0]
                           particle_Y_ini = particle_disp_before[:,1]
                           particle_Z_ini = particle_disp_before[:,2]
                           
                           particle_X_old = particle_disp_after[:,0]
                           particle_Y_old = particle_disp_after[:,1]
                           particle_Z_old = particle_disp_after[:,2]
                           
                           
              
                    
                           print(ids_ini)
                           print(particle_disp_before)
                           
                           #Connecting Displacement data and particle ids
                           particle_disp_before_rot = np.rot90(particle_disp_before)
                           particle_disp_before_unit = (np.vstack([ids_ini , particle_disp_before_rot]))
                           particle_disp_before_unit = np.rot90(particle_disp_before_unit,-3)
                           
                 
                           
                           particle_disp_after_rot = np.rot90(particle_disp_after)
                           particle_disp_after_unit = (np.vstack([ids_ini_next , particle_disp_after_rot]))
                           particle_disp_after_unit = np.rot90(particle_disp_after_unit,-3)
                           
                           array_size = len(particle_disp_after_unit)
     
                           
                           common_element = np.intersect1d(particle_disp_before_unit[:,0],particle_disp_after_unit[:,0])
                           
                           particle_disp_before = particle_disp_before_unit[np.isin(particle_disp_before_unit[:,0],common_element)]
                           particle_disp_after  = particle_disp_after_unit[np.isin(particle_disp_after_unit[:,0],common_element)]
                           
   
    
   
                           col_num = 0
                           argsort_before=np.argsort(particle_disp_before[:,col_num])
                           particle_disp_before = particle_disp_before[np.argsort(particle_disp_before[:,col_num])]
                           
                           argsort_before=np.argsort(particle_disp_after[:,col_num])
                           particle_disp_after = particle_disp_after[np.argsort(particle_disp_after[:,col_num])]
            
                           
                           particle_disp_before = particle_disp_before[:,1:4]
                           particle_disp_after  = particle_disp_after[:,1:4]
  
                           
                           
                           particle_disp = particle_disp_after - particle_disp_before
                           
                           particle_disp_scl = np.linalg.norm([particle_disp], axis=-1)
                           particle_disp_scl = np.rot90(particle_disp_scl,3)
                           
                           # Check Threshold
                           if(Larger_value_delete == "Yes\n"):
                               Threshold_vec = np.sqrt(Threshold/3)
                               particle_disp = np.where(particle_disp > Threshold_vec, 0, particle_disp)
                               particle_disp_scl = np.where(particle_disp_scl > Threshold, 0, particle_disp_scl)
                               
                               
                               
                           #Calculate simulation time
                          
                           Time1 = i_cal * interval
                           Time2 = i_cal_next * interval
     
                           
                           #Making vtk file
                           with open('Displacement' + str(i+1) + '.vtk', mode='a', encoding='ASCII') as vtk:
                               
                               
                               
                               vtk.write('# vtk DataFile Version 4.1\n')

                               vtk.write('Displacement   Time = ' + str(Time1) + '~' + str(Time2) + ' {s}\n')
                               vtk.write('ASCII\n')
                               vtk.write('DATASET POLYDATA\n')
                               vtk.write('POINTS ' + str(len(ids_ini_next)) + ' float\n')
                           
                               np.savetxt(vtk, particle_disp_after,delimiter=" ", fmt = '%.5f')
                               
                               vtk.write('POINT_DATA ' + str(len(ids_ini_next))+ '\n')
                               vtk.write('VECTORS point_vectors float\n')
                               
                               np.savetxt(vtk, particle_disp, delimiter=" ",  fmt = '%.5f')
                               
                               vtk.write('SCALARS displacement float\n')
                               vtk.write('LOOKUP_TABLE default\n')
                               np.savetxt(vtk,particle_disp_scl, fmt='%.5f')
                               

                               
                           vtk.close()
                               
                           
                           #Calculate i_cal for next  step
                           i_cal = i_cal + Each_num_step
                               
                           
                           
                           print ("-------------------------------------------------------")
                           print ("Next step")
                           print ("-------------------------------------------------------")

                           
                           
                    #End loop---------------------------------------------------------------------------------------------

    
            else:
                if (settings == False):
                    print ("----------------------------------------------------------------------")
                    print (str(name)+".dem"+" : Settings file not found. Moving to next simulation")
                    print ("----------------------------------------------------------------------")
                else:
                    print ("--------------------------------------------------------------------")
                    print (str(name)+".dem"+" : Simulation unfinished. Moving to next simulation")
                    print ("--------------------------------------------------------------------")
                    
# Calculate total time
elapsed_time3 = time.time() - start
print ("-------------------------------------------------------")
print("elapsed_time:{0}".format(elapsed_time3) + "[sec]")
print ("-------------------------------------------------------")

print ("----------------------------------------------------------------------------------")
print ("Complete! By Hideharu Kevin Sugimoto")        
print ("----------------------------------------------------------------------------------") 
    

                      
                      
                            
                            