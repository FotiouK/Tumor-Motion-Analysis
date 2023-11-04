# Tumor Motion Analysis
Welcome to the Tumour Motion Analysis Repository! This repository is dedicated to the in-depth motion analysis of mobile lung cancer tumours. The project encompasses various algorithms and techniques to quantify motion, including Centre of Mass Displacement, Image Deformation, Volume Tracking, and a Voxel-Wise Motion Analysis. The algorithms can be implemented for any applications where motion is described by sequential timed snapshots representations. In our example we analyse tumour motion from 4D Computed-Tomography (4D-CT) scans of the thorax region. This repository provides valuable tools and insights for the comprehensive analysis of tumor motion in the context of radiation therapy and radiation treatment planning.

</br>
<p align="center">
  <img height = 400 src="https://github.com/FotiouK/Motion_Analysis_Python_code/assets/108896534/bf3cb2ae-d1c0-4f3d-b9e0-37ddf711553c">
</p>

### Centre of Mass Displacement


The primary focus of this method is to quantify the motion of the tumour based on the position of the Centre of Mass (CoM) of the tumor for each phase of the respiratory cycle. It employs Euclidean geometry to determine the maximum and average displacement, providing essential insights into tumor motion.
<br>
<img height = "330" width = "400"  align ="left" src="Images/Centre_of_Mass.png">
 The CoM coordinate of the tumour volume is calculated for each phase, assuming uniform tumor density. This information is then utilised to generate a 3D scatter plot, visualising the motion of the tumor throughout the breathing cycle.
<br> To quantify the displacement between tumor phases, the Euclidean distance between the CoM coordinates is scaled with the voxel dimensions and then iterate between all phase combinations. The maximum and average CoM displacement is thus computed and utilised to quantify the motion of the tumour. These displacement values provide valuable information for characterising tumour motion and are instrumental in the context of radiation therapy treatment planning.
</br>
</br>
</br>
</br>


### Image Deformation
The image deformation algorithm is designed to assess tumour motion amplitude through the process of image registration. It involves aligning the tumour regions from different phases to quantify their motion characteristics. This approach relies on calculating deformation vectors to enumerate the motion between two phases relative to an origin point. The reference point used for image registration is the CoM of the ICTV (Internal Clinical Target Volume), which corresponds to the isocentre position commonly used for radiotherapy treatment planning. Additionally, the scan voxel dimensions are incorporated to ensure that the calculated displacements are in millimetres. The implementation of this algorithm leverages the multi-dimensional image analysis Python library, SimpleITK.
<br> The key steps of the image deformation approach are as follows:
- _Transformation Model_: The algorithm utilises a translation transform to represent motion along each axis.
-  _Optimisation_: The goal is to find the optimal transformation aligning tumour regions in reference and current frames. The mean squares metric measures dissimilarity by averaging the squared differences of corresponding pixels while a regular step gradient descent is employed to iteratively refine transformation parameters.
- _Deformation Vector_: After optimisation, the final transform reveals the deformation between two tumour frames. Deformation vectors are then extracted, signifying tumor region displacement.
- _Displacement Analysis_: Deformation vectors from all frames are accumulated to infer maximum tumor displacement by interpolating vector magnitudes. Directional tumor displacement is also determined by assessing peak-to-peak differences along each of the three axes.
<img height="150" align="right" src="Images/Deformation_Vector.png">
</br>
In summary, the image deformation approach achieves its goal through the iterative optimisation of a transformation model to align tumor regions from different phases. Tumor displacement is quantified through deformation vectors, allowing for the extraction of directional motion amplitude and maximum directional displacement. This process is iterated between all possible tumour phase combinations to identify the maximum overall and directional displacement over the whole breathing phase.


### Volume Tracking
The Volume Tracking section focuses on monitoring changes in tumour size throughout the respiratory cycle. This is achieved by quantifying the tumour volume within the delineations of the Gross Tumor Volume (GTV), with volumes expressed in cubic centimetres (cc), the standard clinical format for tumour volume measurement. The approach involves evaluating the volume of the GTV for all phases of the breathing cycle, providing a comprehensive understanding of tumour volume variations.
<br> To account for varying tumour sizes found in a clinical environment, we introduce the Percentage Volume Variation (PVV) metric. PVV enables the comparison of volume variations among different patients and is defined as follows:
<br>

$$
PVV = (V_{max} - V_{min}) * 100 / V_{mean} 
$$

The PVV metric facilitates the comparison of tumor expansion and contraction relative to the average volume, allowing for comparisons between tumors of varying sizes. The volume tracking analysis provides valuable insights into how tumour size changes during the respiratory cycle, which is essential information for radiation therapy treatment planning.
