#!/usr/bin/python3

import newplotter as np
import analyzer as ana
import extractor as ex
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Housing Analysis Started")


km_distance = 1
logging.info("Kilometre distance set to {k} km".format(k=km_distance))

ex.updateExtracts()
logging.info("Updating extracts")

plot_list = ana.measure(ana.getPropertyCoordinates(), ana.getStoreCoordinates(), ana.getStopCoordinates(), km_distance)
logging.info("Generating plot coordinates")

np.allPlotter(plot_list, km_distance)
logging.info("Map creation completed")

logging.info("Housing Analysis Completed")
