from PIL import Image
import subprocess
import os, sys
import string
import random

#Very early implementation
#This script will take an image file and glitch amount (as an integer)
#It will then write a new bmp file that has been databent

baseimage = sys.argv[1] 
glitchamount = int(raw_input("Glitch Amount: "))
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

def color_jitter(filename, hue_range):
    global saturation
    frame_saturation = saturation + random.randint(-20,80)
    hue = random.randint(100-hue_range, 100+hue_range)
    IM_command = "mogrify -quiet -modulate 100,%i,%i %s" % (frame_saturation, hue, filename)
    subprocess.call(IM_command, shell=True)

#def sed_edit(filename, outfile, cutcount):
#    filelength = filelen(filename)
#    print ("File length is %s lines" % filelength)
#    targets = [44, 66, 42, 88, 'xx', 55, 99, 77]
#    endheader = int(filelength * 0.4)
#    print "End of header approximated at line %s" % endheader
#    for i in range(cutcount):
#        target = random.choice(targets)
#        start = random.randint(endheader, int(filelength * 0.8))
#        end = random.randint(start + 1, filelength)
#        payload = ''.join(random.choice(string.hexdigits) for i in range(2))
#        sedcommand = "sed '%i,%i s/%s/%s/g' %s > %s" % (start, end, target, payload, filename, outfile)
#        print "Starting at line %s and ending at line %s all instances of '%s', will be replaced with '%s'" % (start, end, target, payload)
#        subprocess.call(sedcommand, shell=True)
#        filename = outfile

#    return outfile


def glitchbmp(infile, outfile, amount):
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
    endheader = lines * 0.1
    payload = ''.join(random.choice(string.hexdigits) for i in range(4))
    target = [random.choice(string.hexdigits), random.choice(string.punctuation)]

    #TODO implement ability to specify multiple targets when called
    #TODO implement ability to specify target as a regular expression
    
    
    sedcommand = "sed '%i,%i s/[%s%s]/%s/g' %s > %s" % (endheader, lines, target[0], target[1], payload, infile, outfile)
   
    print "String: '%s' will be replaced with '%s' \n" % (target, payload)
    print "Command to be run is: %s \n" % sedcommand

    #sed_edit(infile, outfile, amount)
    subprocess.call(sedcommand, shell=True)
    color_jitter(outfile, 30)

    return outfile


def animateglitch(infile, frames):

    convertedimage = convertbmp(baseimage, 'converted-%s' % baseimage)

    print "%s converted to %s \n" % (baseimage, convertedimage)

    i = frames

    while i > 0:
        glitchedimage = glitchbmp(convertedimage, 'glitched-' + baseimage.split('.')[0] + str(i) + '.bmp', glitchamount)
        print "%s glitched to %s \n" % (convertedimage, glitchedimage)
        print "----------------------------------------"
        i -= 1

    animatecommand = "convert -delay 05 -loop 0 -quiet *bmp animated.gif"

    subprocess.call(animatecommand, shell=True)

animateglitch(baseimage, frames)




