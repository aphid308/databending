from PIL import Image
import subprocess
import os, sys
import string
import random

class StreamEditor():                               # handles sed-based effects

    def __init__(self, image):
        self.filelength = filelen(image)
        print ("File length is %s lines" % self.filelength)
        self.endheader = int(self.filelength * 0.05)
        print "End of header approximated at line %s" % self.endheader

    def rgb_wiggle(self, filename, outfile, cutcount):
        targets = [44, 66, 42, 88, 'xx', 55, 99, 77, 'dd', 'ef', 'aa']
        for i in range(cutcount):
            target = random.choice(targets)
            start = random.randint(self.endheader, int(self.filelength * 0.8))
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
