from pymoshlib import Mosh

baseimage = Mosh('4EObFe8.jpg')

length = baseimage.filelen

bmpconvert = baseimage.convert('bmp')

print length

print bmpconvert.filelen
