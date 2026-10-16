#!/usr/bin/bash

ID=$1

start=$2
end=$3


for ((i=start; i<=end; i++))
do
echo "${ID}_${i}"
echo "Setting IDEAL image path"
if ((i < 100)); then
subj=${ID}_0${i}
else
subj=${ID}_$i
fi

Input_path="/MRRCdata/PlantarFasciitis/Data/$subj/WATER__Ax_3D_IDEAL_IQ_Calf_A/WATER_Ax_3D_IDEAL_IQ_Calf_A.nii.gz"

echo "Creating Output Directory $Input_path"

Output_Directory="/MRRCdata/PlantarFasciitis/Data/$subj/MuscleMap"

if [ -e "$Input_path" ]; then
echo "Path exists"
mkdir -p "$Output_Directory"

cd "scripts"

pwd

echo "LoadingMuscleMap"


python mm_segment.py -i "$Input_path" -o "$Output_Directory" -r "wholebody" 

else 
echo "Path does not exist"
fi

done

