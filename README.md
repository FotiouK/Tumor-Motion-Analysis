# Tumor Motion Analysis
Welcome to the Tumour Motion Analysis Repository! This repository is dedicated to the in-depth motion analysis of mobile lung cancer tumours. The project encompasses various algorithms and techniques to quantify motion, including Centre of Mass Displacement, Image Deformation, Volume Tracking, and a Voxel-Wise Motion Analysis. The algorithms can be implemented for any applications where motion is described by sequential timed snapshots representations. In our example we analyse tumour motion from 4D Computed-Tomography (4D-CT) scans of the thorax region. This repository provides valuable tools and insights for the comprehensive analysis of tumor motion in the context of radiation therapy and radiation treatment planning.

</br>
<p align="center">
  <img height = 400 src="https://github.com/FotiouK/Motion_Analysis_Python_code/assets/108896534/bf3cb2ae-d1c0-4f3d-b9e0-37ddf711553c">
</p>

### Centre of Mass Displacement
The primary focus of this method is to quantify the motion of the tumour based on the position of the Centre of Mass (CoM) of the tumor for each phase of the respiratory cycle. It employs Euclidean geometry to determine the maximum and average displacement, providing essential insights into tumor motion.
<br> The CoM coordinate of the tumour volume is calculated for each phase, assuming uniform tumor density. This information is then utilised to generate a 3D scatter plot, visualising the motion of the tumor throughout the breathing cycle.
<br> To quantify the displacement between tumor phases, the Euclidean distance between the CoM coordinates is scaled with the voxel dimensions and then iterate between all phase combinations. The maximum and average CoM displacement is thus computed and utilised to quantify the motion of the tumour. These displacement values provide valuable information for characterising tumour motion and are instrumental in the context of radiation therapy treatment planning.


