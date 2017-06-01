from time import gmtime, strftime
from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw, ImageFont
from subprocess import call 
import numpy as np
import os

print("Viz script has started")

def createViz(pin):
    src = "audio3.mp3"
    
    questions = {23: "What's your motto?", 24: "Give us your best laugh!", 25:"Make a wish!", 8:"What are you grateful for today?"}

    audio = AudioSegment.from_file(src)
    data = np.fromstring(audio._data, np.int16)
    fs = audio.frame_rate

    BARS = 500
    BAR_HEIGHT = 300
    LINE_WIDTH = 5

    length = len(data)
    RATIO = length/BARS

    count = 0
    maximum_item = 0
    max_array = []
    highest_line = 0

    for d in data:
        if count < RATIO:
            count = count + 1

            if abs(d) > maximum_item:
                maximum_item = abs(d)
        else:
            max_array.append(maximum_item)

            if maximum_item > highest_line:
                highest_line = maximum_item

            maximum_item = 0
            count = 1

    line_ratio = highest_line/BAR_HEIGHT

    fnt = ImageFont.truetype('vcr.ttf', 50)

    im = Image.new('RGB', (BARS * LINE_WIDTH, BAR_HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((0,0), questions[pin] , font=fnt, fill=(0,0,0,255))

    current_x = 1
    for item in max_array:
        item_height = item/line_ratio

        current_y = (BAR_HEIGHT - item_height)/2
        draw.line((current_x, current_y, current_x, current_y + item_height), fill=(0, 0, 0), width=4)

        current_x = current_x + LINE_WIDTH

    im.show()

    filename = "audioViz_" + strftime("%Y_%m_%d%H-%M-%S", gmtime()) + ".bmp"
    im.save("images/" + filename)
    
    call(["lpr","-o","fit-to-page","images/" + filename])
