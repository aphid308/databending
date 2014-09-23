from PIL import Image
import subprocess
import os, sys
import string
import random

#Very early implementation
#This script will take an image file and glitch amount (as an integer)
#It will then write a new bmp file that has been databent

baseimage = raw_input("Base Image: ")
glitchamount = int(raw_input("Glitch Amount: "))
offset = int(raw_input("Offset: "))
saturation = int(raw_input("Saturation: "))

try:
    frames = int(raw_input("Frames: "))
except IndexError:
    frames = 16

def filelen(infile):
    with open(infile) as f:
        for i, l in enumerate(f):
            pass
        return i + 1

def convertbmp(infile, outfile):
    outfile = outfile.split('.')[0] + '.bmp'
    image = Image.open(infile)

    try:
        image.save(outfile, 'BMP')
        return outfile

    except IOError:
        return ("Cannot process", infile)


def glitchbmp(infile, outfile, amount, offset):
    """
    infile is an image file
    outfile is the name of the bent output file (can include .bmp or be a single word)
    amount is how many lines you would like to affect of the file (if this exceeds 
    file limits or is likely to break the image, it will be error corrected.)
    offset is how far into the file to begin bending (if this is too far in to do 
    anything or too early to miss the header it will be error corrected.)
    """
    outfile = outfile.split('.')[0] + '.bmp'
    lines = filelen(infile)
    print "%s is %i lines long. \n" % (infile, lines)
    minoffset = lines * 0.05
    maxoffset = lines - 50

    if offset < minoffset:
        offset = minoffset
        
        print "Offset is too low and may corrupt the header."
        print "Setting offset to minimum working value: %i" % minoffset

    elif offset > maxoffset:
        offset = maxoffset

        print "Offset is too high and may not create desired affect."
        print "Setting offset to maximum working value: %i" % maxoffset

    print "Substitution will start at %i \n" % offset
    end = offset + amount
    
    if end > lines:
        end = lines
    else:
        pass

    print "Substitution will end at %i \n" % end
    
    payload = ''.join(random.choice(string.hexdigits) for i in range(4))
    target = [random.choice(string.hexdigits), random.choice(string.punctuation)]

    #TODO implement ability to specify multiple targets when called
    #TODO implement ability to specify target as a regular expression
    
    global saturation
    saturation = saturation + random.randint(-10,90)
    hue = random.randint(85,115)
    IM_command = "mogrify -quiet -modulate 100,%i,%i %s" % (saturation, hue, outfile)
    
    sedcommand = "sed '%i,%i s/[%s%s]/%s/g' %s > %s" % (offset, end, target[0], target[1], payload, infile, outfile)
    
    print "String: '%s' will be replaced with '%s' \n" % (target, payload)
    print "Command to be run is: %s \n" % sedcommand

    subprocess.call(sedcommand, shell=True)
    subprocess.call(IM_command, shell=True)

    return outfile


def animateglitch(infile, frames):

    convertedimage = convertbmp(baseimage, 'converted-%s' % baseimage)

    print "%s converted to %s \n" % (baseimage, convertedimage)

    i = frames

    while i > 0:
        glitchedimage = glitchbmp(convertedimage, 'glitched-' + baseimage.split('.')[0] + str(i) + '.bmp', glitchamount, offset)
        print "%s glitched to %s \n" % (convertedimage, glitchedimage)
        print "----------------------------------------"
        i -= 1

    animatecommand = "convert -delay 05 -loop 0 -quiet *bmp animated.gif"

    subprocess.call(animatecommand, shell=True)

animateglitch(baseimage, frames)




