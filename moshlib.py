#!/usr/bin/env python
from PIL import Image
import subprocess
import os, sys
import string
import random
import ConfigParser

#Very early implementation
#This script will take an image file and glitch amount (as an integer)
#It will then write a new bmp file that has been databent

baseimage = sys.argv[1] 
glitchamount = int(raw_input("Glitch Amount: "))
saturation = int(raw_input("Saturation: "))
anim_delay = int(raw_input("Animation Delay: "))

try:
    frames = int(raw_input("Frames: "))
except IndexError:
    frames = 16

Config = ConfigParser.ConfigParser()
Config.read('conf.ini')

def configmap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

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


class ImageWitch():                                 # handles ImageMagick-based glitches
    
    def color_jitter(self, filename, hue_range):
        frame_saturation = saturation + random.randint(-15,65)
        hue = random.randint(100-hue_range, 100+hue_range)
        IM_command = "mogrify -quiet -modulate 100,%i,%i %s" % (frame_saturation, hue, filename)
        subprocess.call(IM_command, shell=True)

    def flashing_lights(self, filename, light_range):
        light = random.randint(110-light_range/2, 110+light_range)
        IM_command = "mogrify -quiet -modulate %i,100,100 %s" % (light, filename)
        subprocess.call(IM_command, shell=True)
        


class StreamEditor():                               # handles sed-based effects

    def __init__(self, image):
        self.filelength = filelen(image)
        print ("File length is %s lines" % self.filelength)
        #basic implementation of the config file below
        #we can discuss which params we want to offload to the ini file later
        self.headerdifferential = configmap('Settings')['headerdifferential']
        self.endheader = int(self.filelength * float(self.headerdifferential))
        print "End of header approximated at line %s" % self.endheader

    def rgb_wiggle(self, filename, outfile, cutcount):
        targets = [44, 66, 42, 88, 'xx', 55, 99, 77, 'dd', 'ef', 'aa']
        for i in range(cutcount):
            target = random.choice(targets)
            start = random.randint(self.endheader, int(self.filelength * float(self.headerdifferential))
            end = random.randint(start + 1, self.filelength)
            payload = ''.join(random.choice(string.hexdigits) for i in range(random.randint(1,8)))
            
            if i == 0:
                sedcommand = "sed '%i,%i s/%s/%s/g' %s > %s" % (start, end, target, payload, filename, outfile)
            else:
                sedcommand = "sed -i '%i,%i s/%s/%s/g' %s" % (start, end, target, payload, filename)
            
            print "On lines %s through line %s, '%s' will be replaced with '%s'" % (start, end, target, payload)
            subprocess.call(sedcommand, shell=True)
            filename = outfile

    # makes viewable BMPs but both PIL and Imagemagick seem to think they're broken
    def del_chunks(self, filename, outfile, chunkcount):
        for i in range(chunkcount):
            start = random.randint(self.endheader+100, int(self.filelength * 0.90))
            end = random.randint(start + 1, start+40)
            if i == 0:
                sedcommand = "sed -e '%i,%id' %s > %s" % (start, end, filename, outfile)
            else:
                sedcommand = "sed -i -e '%i,%id' %s" % (start, end, outfile)
            print sedcommand
            subprocess.call(sedcommand, shell=True)

def glitchbmp(infile, outfile, amount):
    """
    infile is an image file
    outfile is the name of the bent output file (can include .bmp or be a single word)
    """
    outfile = outfile.split('.')[0] + '.bmp'

    sed = StreamEditor(infile)
    sed.rgb_wiggle(infile, outfile, amount)
    #sed.del_chunks(infile, outfile, amount)

    witch = ImageWitch()
    witch.color_jitter(outfile, 25)
    witch.flashing_lights(outfile, 50)

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

    print "\nAnimating GIF... (this may take a while)"
    animatecommand = "convert -delay %i -loop 0 -quiet *bmp %s-animated.gif" % (anim_delay, baseimage.split('.')[0])
    subprocess.call(animatecommand, shell=True)

    print "Done! Cleaning up...."
    rm_bmps = "rm glitch*.bmp convert*.bmp"
    subprocess.call(rm_bmps, shell=True)


animateglitch(baseimage, frames)




