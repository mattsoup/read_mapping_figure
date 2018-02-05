"""
A Processing script (in python mode) to draw contigs and where their reads map
to. Reads for which the mates are more than 2kb apart are shown in a
different color to highlight them.
"""

add_library('pdf')

# The file resulting from 'read_mapping_sam.py'
file = loadStrings("./CHOCRA.out")

# The desired output file name (in pdf format)
beginRecord(PDF, "CHOCRA_only_alts.pdf")
size(2500, 600)
background(255)
strokeCap(SQUARE)
noFill()

# size_scale determines size of the circles.
size_scale = 600
drawn_list = []
xcenter = 10
prevx = 0
prevradius = 0
prevx2 = 0
prevy2 = 0

# Sets a few settings for drawing
stroke(55, 55, 55)
strokeWeight(2)
ellipseMode(RADIUS)
file = sort(file)
prev_scaffold = ""

# Reads through the input file and draws the circles and lines connecting the
# reads.
for item in file:
    if item.startswith("Scaffold\t"):
        pass
    else:
        temp = item.split("\t")
        scaffold = temp[0]
        scaffold_length = int(temp[1])
        radius = scaffold_length / float(size_scale)
        pos1 = int(temp[2])
        pos2 = int(temp[3])
        # If the contig hasn't been drawn yet, draw it.
        if scaffold not in drawn_list:
            stroke(55, 55, 55, 50)
            strokeWeight(.5)
            nt_size = float(360) / scaffold_length
            xcenter = (prevx + radius + 10)
            prevradius = radius
            prevx = xcenter + prevradius
            stroke(55, 55, 55)
            strokeWeight(2)
            drawn_list.append(scaffold)
            ellipse(xcenter, height / 2, radius, radius)
        stroke(55, 55, 55, 50)
        strokeWeight(0.5)
        # Determines the coordinates of where the lines (bezier curves, really)
        # will start, and where the control points will be.
        x1 = (xcenter) + ((radius - 1) * cos(radians(nt_size) * float(pos1)))
        y1 = (height / 2) + ((radius - 1) * sin(radians(nt_size) * float(pos1)))
        cont1 = (xcenter) + ((radius - 15) * cos(radians(nt_size) * float(pos1)))
        cont2 = (height / 2) + ((radius - 15) * sin(radians(nt_size) * float(pos1)))
        cont3 = (xcenter) + ((radius - 15) * cos(radians(nt_size) * float(pos2)))
        cont4 = (height / 2) + ((radius - 15) * sin(radians(nt_size) * float(pos2)))
        x2 = (xcenter) + ((radius - 1) * cos(radians(nt_size) * float(pos2)))
        y2 = (height / 2) + ((radius - 1) * sin(radians(nt_size) * float(pos2)))
        prevx2 = x2
        prevy2 = y2
        x = int(random(10))
        x = 1
        # If x == 1, draws the bezier curve. If the above line is not commented
        # out, it will draw every curve.
        if x == 1:
            # If the reads are more than 2kb apart, draws the curve in a
            # different color to stand out.
            if abs(pos1 - pos2) > 2000:
                stroke(15, 137, 160, 50)
                bezier(x1, y1, cont1, cont2, cont3, cont4, x2, y2)

endRecord()
print "All done"
