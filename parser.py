
state = {"x":0,"y":0,"z":0, "e":0}
printing = []
absolute = True

class Line(object):
    def __init__(self,x0,y0,z0,e0,x1,y1,z1,e1,f,t):
        self.start = (x0,y0,z0,e0)
        self.end = (x1,y1,z1,e1)
        self.feed = f
        self.type = t
        
    def to_gcode(self):
        result=["G%s" % self.type]
        if self.end[0] is not None:
            result.append("X%s" % self.end[0])
        if self.end[1] is not None:
            result.append("Y%s" % self.end[1])
        if self.end[2] is not None:
            result.append("Z%s" % self.end[2])
        if self.end[3] is not None:
            result.append("E%s" % self.end[3])
        if self.feed is not None:
            result.append("F%s" % self.feed)
        return " ".join(result)
        
    def divide(self):
        d=[]
        for i in self.end:
            if i is not None:
                d.append(i/2)
            else:
                d.append(i)
        xd,yd,zd,ed=d
        
        return (Line(self.start[0],self.start[1],self.start[2],self.start[3],xd,yd,zd,ed,self.feed,self.type),
                Line(xd,yd,zd,ed,self.end[0],self.end[1],self.end[2],self.end[3],self.feed,self.type))
        

def parseg(line):
    #G1 X91.406 Y157.951 E0.10057
    values = line.split()
    assert values[0][0] == "G"
    number = int(values.pop(0)[1:])
    assert number in [0,1]
    x0 = state["x"]
    y0 = state["y"]
    z0 = state["z"]
    e0 = state["e"]
    x1 = None
    y1 = None
    z1 = None
    e1 = None
    f = None

    while values:
        value = values.pop(0)
        try:
            arg,value=value[0],value[1:]
        except:
            print value
            assert False
        if arg == "X":
            x1 = float(value)
        elif arg == "Y":
            y1 = float(value)
        elif arg == "Z":
            z1 = float(value)
        elif arg == "E":
            e1 = float(value)
        elif arg == "F":
            # TODO seguro que el feed es solo entero?
            f = int(value)
            assert value == str(f)
            
        else:
            assert False
    return Line(x0,y0,z0,e0,x1,y1,z1,e1,f,number)

while True:
    try:
        line=raw_input().split(";")[0].strip()
    except EOFError:
        break
    if not line:
        print("")
        continue
    if line.startswith("G90"):
        absolute = True
        print(line)
    elif line.startswith("G91"):
        absolute = False
        print(line)
    elif "G0 " in line or "G1 " in line:
        parsed = parseg(line)
        if absolute:
            for i in parsed.divide():
                print(i.to_gcode())
        else:
            print(parsed.to_gcode())
    else:
        pass
        print(line)

