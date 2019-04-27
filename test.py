import rgb
import rgb_new
import os
from datetime import datetime
from os import listdir
from os.path import isfile, join
from PIL import Image

def save_result(path):
    print("Evaluating {}...".format(path))
    time_started = datetime.now()
    
    image = Image.open(path)

    filename = os.path.splitext(path)[0].split("/")[-1:][0]

    # time_started_rgbs = datetime.now()
    # rgbs_new = rgb_new.get_colors(image, 4)
    # print("Getting RGBs with new script: {}".format(datetime.now() - time_started_rgbs))

    time_started_rgbs = datetime.now()
    rgbs = rgb.get_colors(image, 4)
    print("Getting RGBs with original script: {}".format(datetime.now() - time_started_rgbs))
    
    stretch = rgb.to_stretch(rgbs)
    stretch.save("results/{}_stretch.png".format(filename))

    # time_started_grid = datetime.now()
    # new_grid = rgb.to_grid(rgbs_new)
    # print("Getting grid with new script: {}".format(datetime.now() - time_started_grid))

    time_started_grid = datetime.now()
    grid = rgb.to_grid(rgbs)
    print("Getting grid with original script: {}".format(datetime.now() - time_started_grid))
    
    # new_grid.save("results/{}_grid_new.png".format(filename))
    grid.save("results/{}_grid.png".format(filename))

    print("Total time: {}\n".format(datetime.now() - time_started))

files = [join("sources/", f) for f in listdir("sources") if isfile(join("sources/", f))]

for filepath in files:
    save_result(filepath)

