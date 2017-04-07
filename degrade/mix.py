import colour as c
#CMYK
cyanExtruder=2
magentaExtruder=0
yellowExtruder=1

def cambiacolor(color,v_ext=0):
    cyan,magenta,yellow=color
    result = "M163 S%s P%s\n" % (cyanExtruder,cyan)
    result += "M163 S%s P%s\n" % (magentaExtruder,magenta)
    result += "M163 S%s P%s\n" % (yellowExtruder,yellow)
    result += "M164 S%s\n" % v_ext
    result += "T%s" % v_ext
    return result

while True:
    try:
        line=raw_input()
    except EOFError:
        break
    if ";LAYER_COUNT:" in line:
        layers = int(line[len(";LAYER_COUNT:"):])
        scale = c.color_scale((0, 0, 1), (0, 1, 0), int(layers/2))+c.color_scale((0, 1, 0), (1, 0, 0), int(layers/2))
    elif ";LAYER:" in line:
        print (line)
        print(cambiacolor(scale.pop(0)))
    else:
        print(line)


