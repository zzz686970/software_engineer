from skimage import data 
from skimage.exposure import histogram 
from skimage.feature import canny 
from scipy import ndimage as ndi 
from skimage.filters import sobel
from skimage.segmentation import watershed

coins = data.coins()
hist, hist_centers = histogram(coins)

## if the background is very smooth
## edge-based segmentation 
edges = canny(coins/255.)
fill_coins = ndi.binary_fill_holes(edges)

## remove background of objects smallers than a threshold
label_objects, nb_labels = ndi.label(fill_coins)
sizes = np.bincount(label_objects.ravel())
mask_sizes = sizes > 20 
mask_sizes[0] = 0 
coins_cleaned = mask_sizes[label_objects]


## determine markers of the coins and the background
## watershed transfrom floods an image of elevation starting from markers
## watershed lines separate these catchment basins and correspond to desired segmentation 


markers = np.zeros_like(coins)
markers[coins < 30] = 1
markers[coins > 150] = 2

elevation_map = sobel(coins)

segmentation = watershed(elevation_map, markers)

segmentation = ndi.binary_fill_holes(segmentation - 1)

labeled_coins, _ = ndi.label(segmentation)

