from __future__ import print_function
from __future__ import division
import vigra
import nifty
import h5py
import fastfilters as ffilt
import numpy

def watersheds(raw, sigma):
    edgeIndicator = ffilt.hessianOfGaussianEigenvalues(raw, sigma)[:,:,0]
    seg, nseg = vigra.analysis.watersheds(edgeIndicator)
    #seg -= 1
    #vigra.segShow(raw, seg)
    #vigra.show()
    return seg,nseg




class PatchExtractor(object):

    def __init__(self, raw, seg, rag, patchSize = (200,200)):
        self.raw = raw
        self.seg = seg
        self.rag = rag
        self.patchSize = patchSize

        #compute bounding boxes and center of mass
        f = vigra.analysis.extractRegionFeatures(raw, seg, features=['Coord<Minimum >','Coord<Maximum >','RegionCenter'])
        self.coordMin  = f['Coord<Minimum >']
        self.coordMax  = f['Coord<Maximum >']
        self.coordMean = f['RegionCenter']




    def getBoundingBox(self, nodeId):
        return self.coordMin[nodeId,:], self.coordMax[nodeId, :]


    def uvBoundingBox(self, u, v):
        minU, maxU = self.getBoundingBox(u)
        minV, maxV = self.getBoundingBox(v)


        minUV = numpy.minimum(minU, minV)
        maxUV = numpy.maximum(maxU, maxV)

        return minUV, maxUV



    def getPatch(self, u,v):

        # bounding box
        bb = self.uvBoundingBox(u,v)
        bbSize  = bb[1] - bb[0] 
        #print(bb, bbSize)

        ps = self.patchSize

        if(bbSize[0] <= ps[0] and bbSize[1] <= ps[1]):
            enlargeSize = (ps - bbSize)//2
            bbLow = bb[0] - enlargeSize
            enlargeSize = (ps - (bb[1] - bbLow))
            bbHigh = bb[1] + enlargeSize
            
            #size = bbHigh - bbLow

            rawPatch = self.raw[bbLow[0]:bbHigh[0],bbLow[1]:bbHigh[1]]
            segPatch = self.seg[bbLow[0]:bbHigh[0],bbLow[1]:bbHigh[1]].astype('int32')

            maskU = numpy.zeros(ps)
            maskV = numpy.zeros(ps)
            edge  = numpy.zeros(ps)

            maskU[segPatch == u ] = 1
            maskV[segPatch == v ] = 1
            
            edge = maskU- maskV
            g = vigra.filters.gaussianGradientMagnitude(edge,0.1)
            vigra.imshow(g)
            vigra.show()

            vigra.segShow(rawPatch, maskU.astype('uint32'))
            vigra.show()
            #sys.exit()

        else:
            assert False


# cremi data
f = "/home/tbeier/Downloads/sample_A_20160501.hdf"
f = h5py.File(f)
raw = f['volumes/raw'][0,:,:].astype('float32')[0:400,0:400].squeeze()
gt  = f['volumes/labels/neuron_ids'][0,:,:].astype('uint32')[0:400,0:400]
print(gt.min())


patchSize = [200,200]
padding = [200,200,200,200]




# compute simple watersheds
# supervoxels start at 1 !!!!
seg, nseg = watersheds(raw,  3.0)

# do the padding
paddedRaw = numpy.pad(raw, patchSize, mode='reflect')
paddedSeg = numpy.pad(seg, patchSize, mode='constant', constant_values=0)


#vigra.segShow(paddedRaw, paddedSeg)
#vigra.show()


# compute rag
rag = nifty.graph.rag.gridRag(seg)
print(rag)

# patch extractor
patchExtractor = PatchExtractor(raw=paddedRaw, seg=paddedSeg, rag=rag)


for e in rag.edges():
    uv = rag.uv(e)

    patchExtractor.getPatch(*uv)