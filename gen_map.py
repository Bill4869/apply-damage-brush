import numpy
import skimage
import skimage.io, skimage.filters

# the bigger sigma is, the less edges detected
# the bigger threshold is, the bigger area in map gets
def generate_map(tar_dir, sigma, threshold):
    org = skimage.io.imread(tar_dir)

    # gaussian filter
    blurred = skimage.filters.gaussian(org, sigma=(sigma, sigma), multichannel=True)
    blur_rgb = [ blurred[:, :, i] for i in range(3) ]

    # sobel filter
    edges = numpy.sqrt(sum([skimage.filters.sobel(i)**2 for i in blur_rgb]))
    max_val = numpy.amax(edges)
    max_preferred_val = max_val * threshold / 100

    map = 255 * numpy.ones([edges.shape[0], edges.shape[1]],dtype=numpy.uint8)
    
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            p = edges[i, j]
            if p < max_preferred_val and p > 0:
                pix = round(p * 255 / max_val)
                map[i, j] = pix

    return map

