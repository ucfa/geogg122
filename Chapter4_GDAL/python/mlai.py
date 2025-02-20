import gdal
import numpy as np
import numpy.ma as ma
from glob import glob

year = '2012'
tile = 'h17v03'

def hooray(year,tile):

	file_pattern = 'files/data/MCD15A2.A%s*.%s.*'%(year,tile)

	filenames = np.sort(glob(file_pattern))


	selected_layers = [  "Lai_1km", "FparLai_QC", "LaiStdDev_1km" ]
	file_template = 'HDF4_EOS:EOS_GRID:"%s":MOD_Grid_MOD15A2:%s'


	lai_all    = []
	lai_sd_all = []

	for filename in filenames:
		data = {}
		for i, layer in enumerate ( selected_layers ):
		    this_file = file_template % ( filename, layer )
		    g = gdal.Open ( this_file )
		    
		    if g is None:
		        raise IOError
		    data[layer] = g.ReadAsArray() 
		lai = data['Lai_1km'] * 0.1
		lai_sd = data['LaiStdDev_1km'] * 0.1
		mask = data['FparLai_QC'] & 1
		laim = ma.array(lai,mask=mask)
		laim_sd = ma.array(lai_sd,mask=mask)

		lai_all.append(laim)
		lai_sd_all.append(laim_sd)

	lai_all    = ma.array(lai_all)
	lai_sd_all = ma.array(lai_sd_all)
	return lai_all, lai_sd_all
