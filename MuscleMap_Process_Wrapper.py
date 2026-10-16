import sys
import os
import numpy as np
import pandas as pd
import ants
from scipy.stats import kurtosis, skew
sys.path.append('/user/iibi/ztlong/Desktop/Code/GitHub/PlantarFasciitis/ROI_Processing')
from QUANTIFY_Process import Q_Read,Extract_Process,Calc_Row_idx,Resample_ROI,Param_Stats
from Read_Maps import Read_Maps
from Q_Process_Wrapper import Q_Process_Wrapper

def Read_Maps(MRRCdata_Root,QY_ID):

    #Define the wT2 map
    wT2_Calf_Path = os.path.join(MRRCdata_Root,QY_ID,"Results/Calf_EPG_T2MapFatCal_Water.nii.gz")


    #Define PDFF path
    PDFF_Calf_Path = os.path.join(MRRCdata_Root,QY_ID,"FatFrac__Ax_3D_IDEAL_IQ_Calf_A/FatFrac_Ax_3D_IDEAL_IQ_Calf_A.nii.gz")

    wT2_Calf = ants.image_read(wT2_Calf_Path)
    PDFF_Calf = ants.image_read(PDFF_Calf_Path)
    return wT2_Calf,PDFF_Calf

def MuscleMap_Read(MRRCdata_Root,QY_ID):

    

    #Define the MuscleMap segmentation path
    Calf_Path = os.path.join(MRRCdata_Root,QY_ID,"MuscleMap/WATER_Ax_3D_IDEAL_IQ_Calf_A_dseg.nii.gz")


    Calf = ants.image_read(Calf_Path)

    MedGas = ((Calf==8141) + (Calf ==8142)) > 0
    LatGas = ((Calf==8151) + (Calf==8152)) > 0
    MedSol = ((Calf==8131) + (Calf ==8132)) > 0


    return MedGas,LatGas,MedSol

def Resample_Calf(MRRCdata_Root,QY_ID,ROI,Param,ROI_ID):

    #Define the Resampled output path
    Calf_re_Root_path = os.path.join(MRRCdata_Root,QY_ID,"MuscleMap")
    
    ROI2 = ants.from_numpy(ROI.numpy().astype(np.float32),origin=ROI.origin,spacing=ROI.spacing,direction=ROI.direction)

    ROI_re = ants.resample_image_to_target(
        ROI2,
        Param,
        interp_type="nearestNeighbor"
    )
    ROI_ID = ROI_ID + 'Global.nii.gz'
    Out_Path = os.path.join(Calf_re_Root_path,ROI_ID)
    ants.image_write(ROI_re,Out_Path)
    ROI_arr =ROI_re.numpy()

    return ROI_arr

def MuscleMap_Measure(ROI_arr,Param,ROI_dict,Output_File,QY_ID,Param_ID,ROI_ID):

    row_idx = Calc_Row_idx(QY_ID,ROI_ID,Param_ID,ROI_dict,Output_File)

    Compartment = Param[ROI_arr!=0]

    ROI_Size_GT = np.count_nonzero(ROI_arr)


    Param_Stats(QY_ID,Compartment,ROI_Size_GT,Compartment,Param_ID,row_idx,Output_File)

    return 


MRRCdata_Root = r'/var/tmp/windowsdir/ztlong_MRRCdata/PlantarFasciitis/Data'
QY_ID = 'QY_ID'

wT2_Calf,PDFF_Calf = Read_Maps(MRRCdata_Root,QY_ID)

MedGas,LatGas,MedSol = MuscleMap_Read(MRRCdata_Root,QY_ID)

MedGas_re = Resample_Calf(MRRCdata_Root,QY_ID,MedGas,wT2_Calf,'MedGas')


MuscleMap_Measure(MedGas_re,wT2_Calf,ROI_dict,Output_File,QY_ID,'wT2_EPG','MedGas')





