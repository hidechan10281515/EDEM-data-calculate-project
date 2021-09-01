# created 2020/06/15
# author: Hideharu Sugimoto
# script for post-processing EDEM of a triaxial test

#Importing libraries
from edempy import Deck
import numpy as np
import matplotlib.pyplot as plt
import math
import os 
import csv

#Reading in simulation data
for root, dirs, files in os.walk(os.curdir):
    for file in files:
        if file.endswith(".dem"):
            name=file.replace(".dem","")
            print ("-------------------------------------------------------")
            print ("Loading: "+str(name)+".dem")
            print ("-------------------------------------------------------")
            deck=Deck(os.path.join(root,file))
            
            # Reading in preference
            if os.path.exists(os.path.join(root,'triaxial_setting.txt')): 
                with open(os.path.join(root,'triaxial_setting.txt'), 'r') as file:
                    preferences=file.readlines()
                    sim_end=float(preferences[3])
                    D=float(preferences[5])
                    Initial_Piston_Height=float(preferences[7])
                    Confine_Value=float(preferences[9])
                    report=str(preferences[11])
                    summary=str(preferences[13])
                    plots=str(preferences[15])
                    file.close()
                    settings=True
            else:
                settings=False
                sim_end=0
                
            #Counter for detecting first contact between the sample and the piston
                
            first_contact = 0
                
            #Holder for the number of the timestep at first cotact between piston and sample
                
            Timestep_First_Contact=deck.numTimesteps
                
            #Defining conter for key Timesteps
                
            Timestep_First_Contact=deck.numTimesteps;
                
            Timestep_End_Confined_Compression=0;
                
            #Declearing arrays for axial stress and strain
                
            Stress=np.zeros([deck.numTimesteps])
            Deviatoric_stress=np.zeros([deck.numTimesteps])
            Speed=np.zeros([deck.numTimesteps])
            lx_front=np.zeros([deck.numTimesteps])
            lx_back=np.zeros([deck.numTimesteps])
            ly_left=np.zeros([deck.numTimesteps])
            ly_right=np.zeros([deck.numTimesteps])
            lz_bottom=np.zeros([deck.numTimesteps])
            lz_confining=np.zeros([deck.numTimesteps])
            
            strainX=np.zeros([deck.numTimesteps])
            strainY=np.zeros([deck.numTimesteps])
            StrainZ=np.zeros([deck.numTimesteps])
            strainVol=np.zeros([deck.numTimesteps])
            
            wx=np.zeros([deck.numTimesteps])
            wy=np.zeros([deck.numTimesteps])
            Piston_Area=np.zeros([deck.numTimesteps])
            
            # x_ini=np.zeros([deck.numTimesteps])
            # y_ini=np.zeros([deck.numTimesteps])
                
            #Declearing arrays for total mass and volume of difference particle type
                
            Particle_Mass=np.zeros([deck.numTypes])
            Particle_Volume=np.zeros([deck.numTypes])
            Particle_volume_confine=np.zeros([deck.numTypes])
            
            D_temp=np.zeros([deck.numTimesteps])
                
            #Check if prefrence file is found
                
            if(sim_end-np.amax(deck.timestepValues)<0.001 and settings==True):
                    
                    print ("-------------------------------------------------------")
                    print ("Processing: "+str(name)+".dem")
                    print ("-------------------------------------------------------")
                
                    #Calculating area of the piston for stress calculation
                
                    Piston_Area = D
                
                    #Looping through timesteps
                
                    for i in range(deck.numTimesteps):
                    
                    
                        
                        #Get position of geometry to calculate volumetric strain
                        
                        lx_front[i]=sum(deck.timestep[i].geometry["wall_front"].getXCoords())
                        lx_back[i]=sum(deck.timestep[i].geometry["wall_back"].getXCoords())
                        ly_left[i]=sum(deck.timestep[i].geometry["wall_left"].getYCoords())
                        ly_right[i]=sum(deck.timestep[i].geometry["wall_right"].getYCoords())
                        lz_bottom[i]=sum(deck.timestep[i].geometry["bottom"].getZCoords())
                        lz_confining[i]=sum(deck.timestep[i].geometry["confining"].getZCoords())
                        
                        wx[i]=lx_front[i]-lx_back[i]
                        wy[i]=ly_left[i]-ly_right[i]
                        
                        #Piston_Area[i]= (wx[i]) * (wy[i])
                        
                        #Calculating axial stress
                        Stress[i] = sum(deck.timestep[i].geometry["confining"].getZForce())/Piston_Area/1000
                        Deviatoric_stress[i]=Stress[i]-Confine_Value
                        #Speed[i] = sum(deck.timestep[i].particle["New Particle 1"].getXVelocities())
                        
                        # wx[i]=lx_front[i]-lx_back[i]
                        # wy[i]=ly_left[i]-ly_right[i]
                        
                        x_ini=wx[1]
                        y_ini=wy[1]
                        
                        
                        
                    
                        #Detecting first contact between sample and piston
                        
                        if Stress[i]>0 and first_contact==0:
                            
                            #Changing counter for first contact
                            
                            first_contact=1
                            
                            #Saving timestep number for first contact
                            
                            Timestep_First_Contact=i
                            
                            #Calculating the initial sample height
                            
                            Initial_Sample_Height = max(deck.timestep[i].contact.surfSurf.getZPositions())
                            
                            
                            
                        #Detecting the end of the confined compresion stage
                        
                        if Stress[i]>(Confine_Value+15) and first_contact==1 and Timestep_End_Confined_Compression==0:
                            
                            #Saving timestep number for end of confined compression stage
                            
                            Timestep_End_Confined_Compression = i-1
                            
                        #Calculating axial strain in the sample
                        
                        if i>Timestep_First_Contact:
                            
                            StrainZ[i]=1-max(deck.timestep[i].contact.surfSurf.getZPositions())/Initial_Sample_Height
                            
                            
                        
                            #Calculating volumetric strain
                        
                            strainX[i]=(wx[i]-x_ini)/x_ini
                            strainY[i]=(wy[i]-y_ini)/y_ini
                            
                            strainVol[i]=strainX[i] + strainY[i] -StrainZ[i]
                            
                            #calculate D
                            
                        D_temp = wx * wy /10
                        
                        D_temp_100 = D_temp[100]
                        
                        D_temp_200 = D_temp[200]
                            
                            

                            
                    #Reading material parameteres and interaction
                    
                    Material_Parameters=deck.creatorData.materials.getMaterials()
                    Interaction_Parameters=deck.creatorData.interactions.getInteractions()
                    
                    #Get sample height under confine condition
                    
                    Sample_height_confine = max(deck.timestep[200].contact.surfSurf.getZPositions())
                    
                    #Check if simulation has been run
                    
                    if Timestep_End_Confined_Compression>0:
                        
                        #Determination of total particle mass and volume by particle type
                        
                        for j in range(deck.numTypes):
                            
                            Particle_Mass[j]=sum(deck.timestep[Timestep_First_Contact].particle[j].getScales()**3)*deck.timestep[Timestep_First_Contact].particle[j].getRawMass()
                        
                            Particle_Volume[j]=sum(deck.timestep[Timestep_First_Contact].particle[j].getScales()**3)*deck.timestep[Timestep_First_Contact].particle[j].getRawVolume()
                            
                            Particle_volume_confine[j]=sum(deck.timestep[200].particle[j].getScales()**3)*deck.timestep[200].particle[j].getRawVolume()
                            
                        #Determination of the total particle mass and picle volume in the simulation
                        
                        Total_particle_Mass = sum(Particle_Mass)
                        Total_Particle_Volume = sum(Particle_Volume)
                        Total_particle_volume_confine=sum(Particle_volume_confine)
                        
                        #Determination of the initiall fill density and porosity
                        
                        Initial_Fill_Density = Total_particle_Mass/(D*Initial_Sample_Height)
                        Initial_Fill_Porosity = 1-Total_Particle_Volume/(D_temp_100*Initial_Sample_Height)
                        Confine_Fill_porosity = 1-(Total_particle_volume_confine/(D_temp_200*Sample_height_confine))
                        #Determination of peak consolidation stress
                        
                        Peak_Consolidation_stress=max(Stress[0:Timestep_End_Confined_Compression])
                        
                        #Determination of the minimum sample height
                        
                        Minimum_Sample_Height = max(deck.timestep[np.argmax(Stress[0:])].contact.surfGeom.getZPositions())
                        
                        #Determination of the consolidated sample height
                    
                        Consolidated_Sample_Height= max(deck.timestep[Timestep_End_Confined_Compression-1].contact.surfGeom.getZPositions())
                    
                        #Determination of the consolidated aspect ration
                    
                        Aspect_Ratio= Consolidated_Sample_Height/D
                    
                        #Determination of the elastic strain
                    
                        Elastic_Strain = (Consolidated_Sample_Height-Minimum_Sample_Height)/Initial_Sample_Height
                    
                        #Determination of the plastic strain
                    
                        Plastic_Strain = 1-Consolidated_Sample_Height/Initial_Sample_Height
                    
                        #Determination of the unconfined yield strength (UYS)
                    
                        UYS=max(Stress[Timestep_End_Confined_Compression:])
                        
                    
                      
                        #Writing data
                        
                        Names = ["Initial fill denisity","Initial fill porosity","Confine_Fill_porosity","Maximum consolidation stress","Unconfined yield strength","Consolidated aspect ratio","Elastic axial strain","Plastic axial strain"]
                        Values = [Initial_Fill_Density,Initial_Fill_Porosity,Confine_Fill_porosity,Peak_Consolidation_stress,UYS,Aspect_Ratio,Elastic_Strain,Plastic_Strain]
                        Units = ["kg/m^3"," ","kPa","kPa"," "," "" "]
                        Empty_Column=["","","","","",""]
                        
                        if(report=="Yes\n"):
                            
                            with open(str(name)+"_Report"+".csv",'w',newline='') as csvFile:
                                writer = csv.writer(csvFile)
                                writer.writerow(["Material parameters"])
                                writer.writerow(["Material","Poisson ratio","Shear modulus(Pa)","Density(kg/m^2","Work function","Type"])
                                writer.writerow(Material_Parameters)
                                writer.writerow(["Interaction parameters"])
                                writer.writerow(["Interaction","Restitution","Static friction","Rolling friction"])
                                for line in Interaction_Parameters:
                                    writer.writerow(line)
                                writer.writerow(["Results"])                                
                                #for line in np.column_stack([Names,Values,Units,Empty_Column]):
                                   # writer.writerow(line)
                                writer.writerow(["Simulation time","Axial strain","Deviatoric stress(kPa)","Volumetric strain"])
                                for line in np.transpose([deck.timestepValues,StrainZ,Deviatoric_stress,strainVol]):
                                    writer.writerow(line)
                            csvFile.close()

                        if (summary=="Yes\n"):
                            if os.path.exists("Summary.csv"):
                                with open("Summary.csv", 'a', newline='') as csvFile:  
                                    writer = csv.writer(csvFile)
                                    writer.writerow(np.concatenate((str(name),Values),axis=None))
                                    csvFile.close()

                            else:
                                with open("Summary.csv", 'w', newline='') as csvFile:
                                    writer = csv.writer(csvFile)
                                    writer.writerow(["Simulation name","Initial fill density(kg/m3)","Initial fill porosity","Confine_Fill_porosity","Maximum Consolidation stress(kPa)","Unconfined yield strength(kPa)","Consolidated aspect ratio","Elastic axial strain","Plastic axial strain"])
                                    writer.writerow(np.concatenate((str(name),Values),axis=None))
                                    csvFile.close()
                            
                        #Expoting figures
                        if (plots=="Yes\n"):
                            
                            # fig1=plt.figure(1)
                            # plt.plot(Strain[(Timestep_First_Contact-1):Timestep_End_Confined_Compression], Stress[(Timestep_First_Contact-1):Timestep_End_Confined_Compression], 'g-')
                            # plt.xlabel('Axial strain', fontsize=14, color='black')
                            # plt.ylabel('Axial stress (kPa)', fontsize=14, color='black')
                            # plt.title("Confined compression response for " + str(name))
                            # plt.grid(True)
                            # plt.show(block=False)
                            # fig1.savefig(str(name)+'_Confined_Compression.png',dpi=150)
                        
                            fig2=plt.figure(2)
                            plt.plot(StrainZ[Timestep_End_Confined_Compression:], Deviatoric_stress[Timestep_End_Confined_Compression:], 'g-')
                            plt.xlabel('Axial strain', fontsize=14, color='black')
                            plt.ylabel('Deviatoric stress (kPa)', fontsize=14, color='black')
                            plt.title("Deviatoric stress VS Axial strain " + str(name))
                            plt.grid(True)
                            plt.show(block=False)
                          #  fig2.savefig(str(name)+'_Deviatoric stress_VS_Axial strain.png',dpi=150)
                            plt.close('all')
                            
                            fig3=plt.figure(3)
                            plt.plot(StrainZ[Timestep_End_Confined_Compression:], strainVol[Timestep_End_Confined_Compression:], 'g-')
                            plt.xlabel('Axial strain', fontsize=14, color='black')
                            plt.ylabel('Volumetoric_strain', fontsize=14, color='black')
                            plt.title("Volumetoric strain VS Axial strain " + str(name))
                            plt.grid(True)
                            plt.show(block=False)
                           # fig2.savefig(str(name)+'_Volumetoric strain_VS_Axial strain.png',dpi=150)
                            plt.close('all')
    
            else:
                if (settings == False):
                    print ("----------------------------------------------------------------------")
                    print (str(name)+".dem"+" : Settings file not found. Moving to next simulation")
                    print ("----------------------------------------------------------------------")
                else:
                    print ("--------------------------------------------------------------------")
                    print (str(name)+".dem"+" : Simulation unfinished. Moving to next simulation")
                    print ("--------------------------------------------------------------------")
    
print ("----------------------------------------------------------------------------------")
print ("Complete! By Hideharu Kevin Sugimoto")        
print ("----------------------------------------------------------------------------------") 
    

                      
                      
                            
                            