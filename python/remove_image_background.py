from skimage import io as skio
from skimage import filters, morphology
import matplotlib.pyplot as plt 
import numpy as np 
from scipy import ndimage as ndi 


"""steps

detect edges
seed the obtained image to separate background from foreground 
perform a watershed transformation
"""

## read image
url = 'http://i.stack.imgur.com/SYxmp.jpg'
img = skio.imread(url)

## print out basic info 
print(img.shape)
print(img.dtype)

## 1. detect edges
sobel = filter.sobel(img)

## display image
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmpa'] = 'gray'
plt.rcParams['figure.dpi'] = 200

## thicker the edges
blurred = filters.gaussian(sobel, sigma = 2.0)
plt.imshow(blurred)


## 2. assign classes to the fore and background 
### use dark and light zone properties of the image
### use local peaks from the distance transformed image
light_spots = np.array((img > 245).nonzero()).T
plt.plot(light_spots[:, 1], light_spots[:, 0], 'o')

dark_spots = np.array((img < 3).nonzero()).T
plt.plot(dark_spots[:, 1], dark_spots[:, 0], 'o')


## make a seed mask 
bool_mask = np.zeros(img.shape, dtype=np.bool)
bool_mask[tuple(light_spots.T)] = True
bool_mask[tuple(dark_spots.T)] = True

seed_mask, num_seeds = ndi.label(bool_mask)

ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)

def draw_group_as_background(ax, group, watershed_result, original_image)::
    "Draws a group from the watershed result as red background."
    background_mask = (watershed_result == group)
    cleaned = original_image * ~background_mask
    ax.imshow(cleaned, cmap='gray')
    ax.imshow(background_mask.reshape(background_mask.shape + (1,)) * np.array([1, 0, 0, 1]))

## remove background, which would be the class with the most pixels in the image
background = max(set(ws.ravel(), key = lambda g: np.sum(ws == g)))

background_mask = (ws == background)

plt.imshow(~background_mask)

cleaned = img * ~background_mask 
plt.imshow(cleaned)



## mannually inputting seeds
seed_mask = np.zeros(img.shape, dtype = np.int)
seed_mask[0, 0] = 1 ## background
seed_mask[600, 400] = 2 # foreground 
seed_mask[1000, 150] = 2 # left arm 
ws = morphology.watershed(blurred, seed_mask)
plt.imshow(ws)

fig, ax = plt.subplots(1, 2)
ax[0].imshow(img)

draw_group_as_background(ax[1], 1, ws, img)


