
"""
@author: Kyriakos Fotiou
"""

import SimpleITK as sitk
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from scipy.spatial import distance
import statistics
import itertools
from collections import Counter
from scipy import ndimage




"""
Functions for Tumor Motion Analysis
"""

def center_of_mass_displacement(tumor_list, voxel_dimenstions):
    """
    Parameters
    ----------
    tumor_list : List containing tumour coordinates in numpy arrays
    voxel_size : Dimensions of voxel in mm [SI,AP,RL]
    Returns
    -------
    max_displacement : Tumour maximum displacement over the breathing cycle in mm calculate from CoM displacement
    com_list         : List of all CoM coordinates 
    average_com      : The average CoM coordinate 
    """
    com_list = []
    displacement_list = []
    print('Calculating CoM Displacement')
    def center_of_mass(arr):
        indices = np.where(arr == 1)
        RL_cm = np.mean(indices[2])
        AP_cm = np.mean(indices[1])
        SP_cm = np.mean(indices[0])
        return (SP_cm, AP_cm, RL_cm)
    
    ### Calculate CoM Position for all Phases
    for tumor_array in tumor_list:
        com = center_of_mass(tumor_array)
        com_list.append(com)
    
    
    average_com = np.mean(com_list, axis=0)
    print("Average center of mass:", average_com)
    itv_com = center_of_mass(itv)
    print("ITV center of mass:", itv_com)
    ictv_com = center_of_mass(ictv)
    print("ICTV center of mass:", ictv_com)
    ptv_com = center_of_mass(ptv)
    print("PTV center of mass:", ptv_com)
    
    # Calculate All Pairwise Distances Between CoM Points
    for pair in itertools.combinations(com_list, 2):
        point1 = [a * b for a, b in zip(pair[0], voxel_dimenstions)]
        point2 = [a * b for a, b in zip(pair[1], voxel_dimenstions)]
        displacement = distance.euclidean(point1, point2)
        displacement_list.append(displacement)
    
    max_displacement = max(displacement_list)
    avg_displacement = np.mean(displacement_list)
    print("CoM Maximum displacement:", max_displacement)
    return max_displacement, avg_displacement ,com_list, average_com, itv_com,ictv_com



def prob_hist(prob_map):
    """
    Parameters
    ----------
    prob_map : Array describing the Probability Map
    Returns
    -------
    prob_hist : Percentage Frequency of Voxel Probability
    """
    print('Generating Probability Histogram')
    prob_hist = prob_map[np.nonzero(prob_map)]
    mean_hist = np.mean(prob_hist) 
    sigma_hist = statistics.stdev(prob_hist,mean_hist)
    print('The average pixel probability is',mean_hist)
    print ('Standard deviation of the distribution is', sigma_hist)
    # Create a dictionary that contains the frequency of each value in the prob_hist array
    # Create a list of tuples with the value and its frequency
    value_freq = Counter(prob_hist)
    
    # Extract the values and frequencies from the Counter object
    fig, ax = plt.subplots()
    #plt.title('Probability Map Frequency')
    values = [val for val in value_freq.keys()]
    freq = [value_freq[val] for val in values]
    freq = [value_freq[val]/len(prob_hist)*100 for val in values]
    ax.bar(values, freq, width=0.08, align='center') 
    plt.xticks(np.linspace(0,1,11))
    ax.yaxis.set_major_formatter(ticker.PercentFormatter())
    #plt.gca().set_yticklabels(['{:,%}'.format(x) for x in freq])
    plt.title('Voxel Probability Frequency')
    plt.xlabel('Voxel Probability Value')
    plt.ylabel('Frequency')
    plt.grid(axis ='y')
    plt.show()
    return (mean_hist,sigma_hist)

def tumor_volume(tumor_list, voxel_volume):
    """
    Parameters
    ----------
    tumor_list : List containing tumor coordinates in numpy arrays
    voxel_volume : Volume of Each Voxel in mm^3 (use converion *0.001 to convert to cc)
    Returns
    -------
    tumor_volume : List of tumor volumes
    """
    print('Tracking tumour volume')
    tumor_volumes = []
    for i, tumor in enumerate(tumor_list):
        non_zero_voxels = np.count_nonzero(tumor)
        tumor_volume = non_zero_voxels * voxel_volume
        tumor_volumes.append(tumor_volume)
    mean_vol = np.mean(tumor_volumes)
    volume_var = 100*(np.max(tumor_volumes) - np.min(tumor_volumes))/mean_vol
    print('mean tumor volume is',mean_vol)
    print('perc volume variation is', volume_var)
    print(np.min(tumor_volumes))
    print(np.max(tumor_volumes))
    return ( tumor_volumes, volume_var)

def generate_tumor_maps(tumor_array):
    """    
    Parameters
    ----------
    tumor_array : A list of Arrays containign tumor coordinates in numpy array format
    Returns
    -------
    Prob_map : Voxel value represents the probability of tumor location within the timescale of the input arrays 
    itv : Geometric summation of all tumor coordinates
    """
    print('Generate ITV and TLP')
    # calculate the probability map
    tumors_lists = []
    for tumor in tumor_array:
        tumor[tumor > 0.1] = 1
        tumors_lists.append(tumor)
    
    itv = np.sum(tumors_lists, axis=0)
    #generate the PM
    Prob_map = np.copy(itv)/10
    # generate the ITV
    itv[itv>=1]=1
    return Prob_map, itv


def generate_ctv(tumor_list, voxel_size, expansion_magnitude):
    print('generate ctv')
    ctv_list =[]
    i= 0
    for tumor in tumor_list:
        i = i +1
        print(i)
        # Calculate the dilation radius for the x-y plane only
        dilation_radius = tuple(expansion_magnitude / np.array(voxel_size))
        new_array = np.zeros_like(tumor)
        ctv = np.zeros_like(tumor)
        # Find the tumor indices
        tumor_indices = np.argwhere(tumor)
        # Get the min and max indices for the tumor in the z-axis
        z_min = np.min(tumor_indices[:, 0])
        z_max = np.max(tumor_indices[:, 0])
    
        # Iterate over the z-axis where there is tumor
        for z in range(z_min, z_max+1):
            # Get the x-y slice of the tumor for this z-index
            tumor_slice = tumor[z,:,:]
    
            # Expand the tumor in the x-y plane using binary dilation
            dilated_array = ndimage.binary_dilation(tumor_slice, structure=np.ones(shape=(3,3),dtype=float),iterations=int(np.floor(np.max(dilation_radius[1]))))
    
            # Update the tumor array with the dilated array for this z-index
            new_array[z,:,:] = dilated_array
            
        dilated_array_z = ndimage.binary_dilation(new_array, structure= np.ones(shape=(3,1,1),dtype=float), iterations=int(np.floor(dilation_radius[0])))
        ctv[:,:,:] =  dilated_array_z
        ctv_list.append(ctv)
    ictv = np.sum(ctv_list, axis=0)
    ictv_pm = np.copy(ictv)/10
    ictv[ictv>=1]=1
    return ctv_list, ictv,ictv_pm

def generate_ptv(ictv, voxel_size, margin):
    print('Generate PTV')
    # Calculate the dilation radius for the x-y plane only based on the margin
    dilation_radius = tuple(margin / np.array(voxel_size))
    
    # Create a new array for the PTV
    ptv = np.zeros_like(ictv)
    
    # Expand the iCTV in the x-y plane using binary dilation
    for z in range(ictv.shape[0]):
        ictv_slice = ictv[z, :, :]
        # dilated_slice = ndimage.binary_dilation(x_y_slice, structure=np.ones(shape=(3, 3), dtype=float), iterations=int(np.floor(np.max(dilation_radius[1])))
        dilated_slice = ndimage.binary_dilation(ictv_slice, structure=np.ones(shape=(3,3), dtype=float), iterations=int(np.floor(np.max(dilation_radius[1]))))
        ptv[z, :, :] = dilated_slice
    
    # Expand the iCTV in the z-axis using binary dilation
    dilated_z = ndimage.binary_dilation(ptv, structure=np.ones(shape=(3, 1, 1), dtype=float), iterations=int(np.floor(dilation_radius[0])))
    ptv[:,:,:] = dilated_z

    return ptv




def motion_image_deformation(tumor_list, itv):
    """
    Parameters
    ----------
    tumor_list : List containing tumor coordinates in numpy arrays.
    itv : Array describing the itv. (tumor voxels = 1)
    Returns
    -------
    max_displacement : Tumor maximum displacement over the breathing cycle in mm calculate form image deformation
    directinal_displacement : Displacement of Tumor in each direction.

    """
    print('Generate Image Deformation')
    # Generate a ROI as the itv bounding box (add some margins)
    itv_bb = itv.nonzero()
    z_min, z_max = np.min(itv_bb[0]) + 5, np.max(itv_bb[0]) + 5
    y_min, y_max = np.min(itv_bb[1]) + 5, np.max(itv_bb[1]) + 5
    x_min, x_max = np.min(itv_bb[2]) + 5, np.max(itv_bb[2]) + 5

    # Create an empty list to store the deformation vectors
    deformation_vectors = []

    # Loop over all pairs of frames
    for reference_index, current_index in itertools.combinations(range(len(tumor_list)), 2):
        reference_frame = tumor_list[reference_index]
        reference_roi = reference_frame[z_min:z_max, y_min:y_max, x_min:x_max]
        reference_image = sitk.GetImageFromArray(reference_roi)

        # Define the image spacing and origin (in mm) - adjust these values to match your data
        spacing = voxel_dimenstions
        origin = itv_com
        reference_image.SetSpacing(spacing)
        reference_image.SetOrigin(origin)

        current_frame = tumor_list[current_index]
        current_roi = current_frame[z_min:z_max, y_min:y_max, x_min:x_max]
        current_image = sitk.GetImageFromArray(current_roi)

        # Define the image spacing and origin (in mm) - adjust these values to match your data
        current_image.SetSpacing(spacing)
        current_image.SetOrigin(origin)

        # Register the current frame to the reference frame
        registration = sitk.ImageRegistrationMethod()
        registration.SetMetricAsMeanSquares()
        registration.SetOptimizerAsRegularStepGradientDescent(4.0, .01, 200)
        registration.SetInitialTransform(sitk.TranslationTransform(current_image.GetDimension()))
        registration.SetInterpolator(sitk.sitkLinear)
        registration.AddCommand(sitk.sitkIterationEvent, lambda: print(".", end='', flush=True))
        final_transform = registration.Execute(reference_image, current_image)

        # Extract the deformation vector from the final transform
        deformation_vector = np.array(final_transform.GetParameters())

        # Add the deformation vector to the list
        deformation_vectors.append(deformation_vector)
        
    final_deformation_vectors = np.array(deformation_vectors)
    # Compute the peak-to-peak (ptp) along axis 0, 1, and 2
    ptp_axis_SI = np.ptp(final_deformation_vectors[:, 0], axis=0)
    ptp_axis1_AP = np.ptp(final_deformation_vectors[:, 1], axis=0)
    ptp_axis2_RL = np.ptp(final_deformation_vectors[:, 2], axis=0)

    # Compute the maximum displacement
    max_displacement = np.max(np.linalg.norm(final_deformation_vectors, axis=1))

    directinal_displacement = [ptp_axis_SI, ptp_axis1_AP, ptp_axis2_RL]

    # Print the peak-to-peak values for each axis
    print(f"Peak-to-peak deformation along axis SI: {ptp_axis_SI}")
    print(f"Peak-to-peak deformation along axis AP: {ptp_axis1_AP}")
    print(f"Peak-to-peak deformation along axis RL: {ptp_axis2_RL}")
    print(f"Max deformation displacement: {max_displacement}")
    
    
    # Calculate pairwise distances between deformation vectors
    distances = []
    for pair in itertools.combinations(final_deformation_vectors, 2):
        displacement = distance.euclidean(pair[0], pair[1])
        distances.append(displacement)

    max_displacement2 = max(distances)
    print("Maximum displacement:", max_displacement2)
    
    return (deformation_vectors,max_displacement, directinal_displacement)




def prob_planes(prob_map):
    """
    Parameters
    ----------
    prob_map : Input Probability Aap Array

    Returns
    Plots Each Plane of The Probability Map at The Average Centre of Mass Point 
    -------
    """
    zc, yc, xc = np.round(average_com)
    pz = prob_map [int((zc))]
    py = prob_map [:,int(yc),:]
    px = prob_map [:, :,int(xc)]
    fig, ax = plt.subplots(nrows = 1 , ncols=3,figsize=(12, 8))
    y,x = pz.nonzero()
    z1,x1 = py.nonzero()
    z2,y2 = px.nonzero()
    sc0= ax[0].scatter(y,x, c =pz[y,x], marker = 's', cmap ='tab10')
    ax[0].scatter(yc,xc,marker = 'x', c ='b')
    ax[0].set_xlabel('AP')
    ax[0].set_ylabel('RL')
    sc1 = ax[1].scatter(z1,x1, c =py[z1,x1], marker = 's', cmap ='tab10')
    ax[1].scatter(zc,xc,marker = 'x', c ='b')
    ax[1].set_xlabel('SI')
    ax[1].set_ylabel('RL')  
    sc2= ax[2].scatter(z2,y2, c =px[z2,y2], marker = 's', cmap ='tab10')
    ax[2].scatter(zc,yc,marker = 'x', c ='b')
    ax[2].set_xlabel('SI')
    ax[2].set_ylabel('AP') 
    num1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']
    handles = [plt.plot([],[],color=sc0.cmap(sc0.norm(float(num))), ls="", marker="s")[0] for num in num1]
    # Add legend
    fig.legend(handles, num1, loc='center right')
    
    plt.show()

"""
Functions End
"""
    
    
"""
Load Tumor Arrays 
"""
tumor_list = []
# giving directory name
dirname = 'tumor_p101'
# giving file extension
ext = '.npy'
for files in os.listdir(dirname):
    if files.endswith(ext):
        print(files)
        filepath = dirname + '/' + files
        tum = np.load(filepath)
        tumor_list.append(tum)


"""
Patient Specific CT Information in mm
"""
voxel_dimenstions = [3.0,1.0527,1.0527]
voxel_volume = np.prod(voxel_dimenstions)

    
"""
Call the Functions. 
"""
### Generate ITV and Tumour Location Probability Map. ###
prob_map, itv = generate_tumor_maps(tumor_list)

### Generate CTV For All Phases and ICTV. ###
ctv_list , ictv, ictv_pm = generate_ctv(tumor_list, voxel_dimenstions, 5)

### Generate PTV ###
ptv = generate_ptv(ictv, voxel_dimenstions, 5)

### Generate Tumour Location Probability Map Histogram. ###
mean_hist,sigma_hist = prob_hist(prob_map)

### Volume Tracking ###
tumor_volumes, volume_var = tumor_volume(tumor_list, voxel_volume= (voxel_volume*0.001)) #convert to cc

### Centre of Mass Tracking and Maximum CoM Motion Amplitude. ###
max_displacement, avg_displacement ,com_list, average_com, itv_com,ictv_com= center_of_mass_displacement(tumor_list, voxel_dimenstions)

### Vector Deformation Maximum Motion Amplitude. ###
deformation_vectors,max_displacement, directinal_displacement = motion_image_deformation(tumor_list,itv)

### Visualise Probability Planes at Average CoM. ###
prob_planes = prob_planes(prob_map)


