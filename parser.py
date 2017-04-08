
state = {"x":0,"y":0,"z":0}
printing = []
absolute = True

class Line(object):
    def __init__(self,x0,y0,z0,x1,y1,z1,e,f):
        self.start = (x0,y0,z0)
        self.end = (x1,y1,z1)
        self.extrude = e
        self.feed = f
    def to_gcode(self):
        result = ""
        #TODO

def parseg(line):
    #G1 X91.406 Y157.951 E0.10057
    values = line.split()
    assert values[0][0] == "G"
    number = int(values.pop(0)[1:])
    assert number in [0,1]
    x0 = state["x"]
    y0 = state["y"]
    z0 = state["z"]
    x1 = x0
    y1 = y0
    z1 = z0
    e = 0
    f = None

    while values:
        value = values.pop(0)
        try:
            arg,value=value[0],value[1:]
        except:
            print value
            assert False
        if arg == "X":
            x1 = value
        elif arg == "Y":
            y1 = value
        elif arg == "Z":
            z1 = value
        elif arg == "E":
            e = value
        elif arg == "F":
            f = value
        else:
            assert False
    return Line(x0,y0,z0,x1,y1,z1,e,f)

while True:
    try:
        line=raw_input().split(";")[0].strip()
    except EOFError:
        break
    if not line:
        continue
    if "G90 " in line:
        absolute = True
    elif "G91 " in line:
        absolute = False
    elif "G0 " in line or "G1 " in line:
        parseg(line)
    else:
        print(line)


