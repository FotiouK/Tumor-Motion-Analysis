# Tumor Motion Analysis
Welcome to the Tumour Motion Analysis Repository! This repository is dedicated to the in-depth motion analysis of mobile lung cancer tumours. The project encompasses various algorithms and techniques to quantify motion, including Centre of Mass Displacement, Image Deformation, Volume Tracking, and a Voxel-Wise Motion Analysis. The algorithms can be implemented for any applications where motion is described by sequential timed snapshots representations. In our example we analyse tumour motion from 4D Computed-Tomography (4D-CT) scans of the thorax region. This repository provides valuable tools and insights for the comprehensive analysis of tumor motion in the context of radiation therapy and radiation treatment planning.

</br>
<p align="center">
  <img height = 400 src="https://github.com/FotiouK/Motion_Analysis_Python_code/assets/108896534/bf3cb2ae-d1c0-4f3d-b9e0-37ddf711553c">
</p>

## Centre of Mass Displacement


The primary focus of this method is to quantify the motion of the tumour based on the position of the Centre of Mass (CoM) of the tumor for each phase of the respiratory cycle. It employs Euclidean geometry to determine the maximum and average displacement, providing essential insights into tumor motion.
<br>
<img height = "330" width = "400"  align ="left" src="Images/Centre_of_Mass.png">
 The CoM coordinate of the tumour volume is calculated for each phase, assuming uniform tumor density. This information is then utilised to generate a 3D scatter plot, visualising the motion of the tumor throughout the breathing cycle.
<br> To quantify the displacement between tumor phases, the Euclidean distance between the CoM coordinates is scaled with the voxel dimensions and then iterate between all phase combinations. The maximum and average CoM displacement is thus computed and utilised to quantify the motion of the tumour. These displacement values provide valuable information for characterising tumour motion and are instrumental in the context of radiation therapy treatment planning.
</br>
</br>
</br>
</br>


## Image Deformation
The image deformation algorithm is designed to assess tumour motion amplitude through the process of image registration. It involves aligning the tumour regions from different phases to quantify their motion characteristics. This approach relies on calculating deformation vectors to enumerate the motion between two phases relative to an origin point. The reference point used for image registration is the CoM of the ICTV (Internal Clinical Target Volume), which corresponds to the isocentre position commonly used for radiotherapy treatment planning. Additionally, the scan voxel dimensions are incorporated to ensure that the calculated displacements are in millimetres. The implementation of this algorithm leverages the multi-dimensional image analysis Python library, SimpleITK.
<br> The key steps of the image deformation approach are as follows:
- _Transformation Model_: The algorithm utilises a translation transform to represent motion along each axis.
-  _Optimisation_: The goal is to find the optimal transformation aligning tumour regions in reference and current frames. The mean squares metric measures dissimilarity by averaging the squared differences of corresponding pixels while a regular step gradient descent is employed to iteratively refine transformation parameters.
- _Deformation Vector_: After optimisation, the final transform reveals the deformation between two tumour frames. Deformation vectors are then extracted, signifying tumor region displacement.
- _Displacement Analysis_: Deformation vectors from all frames are accumulated to infer maximum tumor displacement by interpolating vector magnitudes. Directional tumor displacement is also determined by assessing peak-to-peak differences along each of the three axes.
<img height="150" align="right" src="Images/Deformation_Vector.png">
</br>
In summary, the image deformation approach achieves its goal through the iterative optimisation of a transformation model to align tumor regions from different phases. Tumor displacement is quantified through deformation vectors, allowing for the extraction of directional motion amplitude and maximum directional displacement. This process is iterated between all possible tumour phase combinations to identify the maximum overall and directional displacement over the whole breathing phase.


## Volume Tracking
The Volume Tracking section focuses on monitoring changes in tumour size throughout the respiratory cycle. This is achieved by quantifying the tumour volume within the delineations of the Gross Tumor Volume (GTV), with volumes expressed in cubic centimetres (cc), the standard clinical format for tumour volume measurement. The approach involves evaluating the volume of the GTV for all phases of the breathing cycle, providing a comprehensive understanding of tumour volume variations.
<br> To account for varying tumour sizes found in a clinical environment, we introduce the Percentage Volume Variation (PVV) metric. PVV enables the comparison of volume variations among different patients and is defined as follows:
<br>

$$
PVV = (V_{max} - V_{min}) * 100 / V_{mean} 
$$

The PVV metric facilitates the comparison of tumor expansion and contraction relative to the average volume, allowing for comparisons between tumors of varying sizes. The volume tracking analysis provides valuable insights into how tumour size changes during the respiratory cycle, which is essential information for radiation therapy treatment planning.
<p align="center">
  <img height = 300 src="Images/vol_var.png">
</p>

## Voxel-Wise Motion Analysis (Tumour Location Probability Map)
The Voxel-Wise Motion Analysis section introduces the Tumour Location Probability (TLP) map, a crucial metric for understanding tumour motion within the thorax. The TLP map encapsulates both tumour displacement and volumetric variations by representing the likelihood of finding the tumour at each voxel throughout the entire breathing cycle. Each voxel in the TLP map corresponds to a specific location within the imaging volume, with voxel values denoting the probability of the tumour’s presence at that particular voxel at any point in the respiratory cycle.
<br> The Tumor Location Probability (TLP) map is generated by first transforming input arrays, where tumour presence pixels are assigned a value of 1/N (N being the number of phases) and tumor absence pixels are set to 0. Geometric summation of these transformed arrays identifies pixels with tumour presence across multiple phases. Extrapolating this methodology over all motion snapshot representations (this case the 10 breathing phases), results in the TLP map. Voxel values in this map range from 0 to 1, with 1 indicating constant tumor presence. Analysis of the TLP voxels allows for a comprehensive understanding of tumor motion, incorporating both movement mechanisms and providing insights into the progression of tumour motion in a single variable.
<p align="center">
<img src="Images/Probability_Map.png" alt="p100_gif" style="height: 300px;" /> <img src="Images/vox_freq.png" alt="Image 2" style="height: 300px;" />
</p>
While volume variation and tumour movement metrics focus on extreme measurements from individual phases, the Tumour Location Probability (TLP) map offers a comprehensive perspective by evenly considering motion across all phases. It amalgamates both movement mechanisms and presents a unified view of tumour motion progression. In additions, the TLP map proves invaluable for comparing patients which exhibit similar motion characteristics.
<br> The TLP map utilises  colour coding to represent voxel probabilities, providing insights into tumour motion. For a more detailed understanding, cross-sectional representations at the iso-centre position can be examined, covering axial, coronal, and sagittal planes, with axes labelled in voxel numbers as illustrated below. The visualisation below was extracted at the isocentre plane where the isocentre coordinate is denoted with a blue X 
<p align="center">
  <img  src="Images/pm_planes.png">
</p>
