import sys
import math
import os
import re
from math import sqrt, pow
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def get_difference(rgb1,rgb2):
    rgb1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2])
    rgb2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2])
            
    lab1 = convert_color(rgb1, LabColor)
    lab2 = convert_color(rgb2, LabColor)
    
    delta = delta_e_cie2000(lab1, lab2)
    
    return delta

def to_stretch(rgbs):
    height = 100
    block_width = 20
    image = Image.new("RGBA", (len(rgbs)*block_width, height), (0,0,0,0))
    yrange = list(range(0,height))

    for i in range(0,len(rgbs)):    
        rgb = rgbs[i]

        xrange = list(range(i*block_width, i*block_width+block_width))
        
        for x in xrange:
            for y in yrange:
                image.putpixel((x,y), rgb)

    return image

def perfect_sqr(n):  
    nextN = math.floor(math.sqrt(n)) + 1
    return nextN * nextN

def largest_prime_factor(n):
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    return n

def to_grid(rgbs, block_size = 200):
    gridy = int(perfect_sqr(len(rgbs))**0.5)

    if gridy**2 != len(rgbs):
        gridy = largest_prime_factor(len(rgbs))

    # print(gridy)
    
    grid = list()
    row = list()
    count = 0
    for i in range(0, len(rgbs)):
        rgb = rgbs[i]
        row.append(rgb)
        count += 1
        if count % gridy == 0 or i == len(rgbs)-1:
            grid.append(row)
            row = list()
    
    image = Image.new("RGBA", (len(grid[0])*block_size, len(grid)*block_size), (0,0,0,0))
    draw = ImageDraw.Draw(image)
    font_size = int(block_size / 10)
    font = ImageFont.truetype("Roboto.ttf", font_size)

    for i in range(0, len(grid)):
        row = grid[i]
        yrange = list(range(i*block_size, i*block_size+block_size))
        for j in range(0,len(row)):
            rgb = row[j]
            xrange = list(range(j*block_size, j*block_size+block_size))

            for x in xrange:
                for y in yrange:
                    image.putpixel((x,y), rgb)

            h = "#%02x%02x%02x" % rgb
            padding = int(block_size / 20)

            diff_to_white = get_difference(rgb, WHITE)

            font_color = WHITE if diff_to_white > 40 else BLACK
            
            draw.text((j*block_size+padding, i*block_size+padding), "RGB({0[0]}, {0[1]}, {0[2]})\n{1}".format(rgb, h), font_color, font=font)

    return image

def get_colors(image, maxcolors=4, max_tolerance=6):
    mc = 256
    image_colors = image.getcolors(maxcolors=mc)
    while image_colors is None:
        image_colors = image.getcolors(maxcolors=mc)
        mc *= 2

    image_colors = sorted(image_colors, reverse=True, key=lambda c: c[0])

    count = 0
    colors = list()
    rgbs = list()
    backup_colors = list()
    for color in image_colors:
        rgb = (color[1][0], color[1][1], color[1][2])
        
        if rgb in rgbs:
            continue

        is_white = rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255
        is_black = rgb[0] == 0 and rgb[1] == 0 and rgb[2] == 0

        if is_white or is_black:
            backup_colors.append(color)
        else:
            min_diff = sys.maxsize
            for c in colors:
                rgb2 = (c[1][0], c[1][1], c[1][2])
                diff = get_difference(rgb, rgb2)
                if diff < min_diff:
                    min_diff = diff

            if min_diff < max_tolerance:
                continue
            
            colors.append(color)
            
        rgbs.append(rgb)
        count += 1
        
        if count == maxcolors:
            break

    loop_max = min(maxcolors - len(colors), len(backup_colors))
    for i in range(0, loop_max):
        color = backup_colors[i]
        colors.append(color)

    colors = sorted(colors, reverse=True, key=lambda c: c[0])
    rgbs = [(color[1][0], color[1][1], color[1][2]) for color in colors]

    return rgbs
