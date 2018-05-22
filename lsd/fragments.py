import mahotas
import numpy as np
import logging
from scipy.ndimage.filters import gaussian_filter

logger = logging.getLogger(__name__)

def watershed(lsds, sigma, return_distances=False, return_seeds=False):
    '''Extract initial fragments from local shape descriptors ``lsds`` using a
    watershed transform. This assumes that the first three entries of
    ``lsds`` for each voxel are vectors pointing towards the center.'''

    boundary_distances = np.sum(lsds[0:3,:]**2, axis=0)
    boundary_distances = gaussian_filter(boundary_distances, sigma)
    minima = mahotas.regmin(boundary_distances)
    seeds, n = mahotas.label(minima)

    logger.info("Found %d fragments", n)

    ret = mahotas.cwatershed(boundary_distances, seeds).astype(np.uint64)

    if return_distances or return_seeds:

        ret = (ret,)
        if return_distances:
            ret = ret + (boundary_distances,)
        if return_seeds:
            ret = ret + (seeds.astype(np.uint64),)

    return ret
