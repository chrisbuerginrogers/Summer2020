from machine import LCD
import time, math

M_SIZE = 1.3333
LOOP_PERIOD = 35

ltx = 0
osx = M_SIZE * 120
osy = M_SIZE * 120
updateTime = 0
old_analog = -999
d = 0

tft = LCD()
tft.fillScreen(tft.color.BLACK)

def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
    
def plotNeedle(value, ms_delay):
    global old_analog
    global osx, osy, ltx
    tft.setTextColor(tft.color.BLACK, tft.color.WHITE)
    if (value < -10):
        value = -10   # Limit value to emulate needle end stops
        
    if (value > 110):
        value = 110
        
    while(value != old_analog):
        if (old_analog < value):
            old_analog+=1
        else:
            old_analog-=1
            
        if (ms_delay == 0):
            old_analog = value
            
        sdeg = valmap(old_analog, -10, 110, -150, -30) # Map value to angle
        # Calculate tip of needle coords
        sx = math.cos(sdeg * 0.0174532925)
        sy = math.sin(sdeg * 0.0174532925)
        
        # Calculate x delta of needle start (does not start at pivot point)
        tx = math.tan((sdeg + 90) * 0.0174532925)
        
        # Erase old needle image
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx - 1)), int(M_SIZE * (140 - 20)), int(osx - 1), int(osy), tft.color.WHITE)
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx)), int(M_SIZE * (140 - 20)), int(osx), int(osy), tft.color.WHITE)
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx + 1)), int(M_SIZE * (140 - 20)), int(osx + 1), int(osy), tft.color.WHITE)
        
        # Re-plot text under needle
        tft.setTextColor(tft.color.BLACK);
        tft.drawCentreString("%RH", int(M_SIZE * 120), int(M_SIZE * 70), 4); # Comment out to avoid font 4
        
        # Store new needle end coords for next erase
        ltx = tx
        osx = M_SIZE * (sx * 98 + 120)
        osy = M_SIZE * (sy * 98 + 140)
        
        # Draw the needle in the new postion, magenta makes needle a bit bolder
        # draws 3 lines to thicken needle
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx - 1)),int( M_SIZE * (140 - 20)), int(osx - 1), int(osy), tft.color.RED)
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx)), int(M_SIZE * (140 - 20)), int(osx), int(osy), tft.color.MAGENTA)
        tft.drawLine(int(M_SIZE * (120 + 20 * ltx + 1)), int(M_SIZE * (140 - 20)), int(osx + 1), int(osy), tft.color.RED)
        
        if(math.fabs(old_analog - value) < 10):
            ms_delay += ms_delay / 5
            
        time.sleep(ms_delay)
        
def analogMeter():
    tft.fillRect(0, 0, int(M_SIZE * 239), int(M_SIZE * 126), tft.color.LIGHTGREY)
    tft.fillRect(5, 3, int(M_SIZE * 230), int(M_SIZE * 119), tft.color.WHITE)
    
    tft.setTextColor(tft.color.BLACK)
    
    # Draw ticks every 5 degrees from -50 to +50 degrees (100 deg. FSD swing)
    for i in range(-50, 51, 5):
        # Long scale tick length
        tl = 15
        
        # Coordinates of tick to draw
        sx = math.cos((i - 90) * 0.0174532925)
        sy = math.sin((i - 90) * 0.0174532925)
        x0 = sx * (M_SIZE * 100 + tl) + M_SIZE * 120
        y0 = sy * (M_SIZE * 100 + tl) + M_SIZE * 140
        x1 = sx * M_SIZE * 100 + M_SIZE * 120
        y1 = sy * M_SIZE * 100 + M_SIZE * 140
        
        # Coordinates of next tick for zone fill
        sx2 = math.cos((i + 5 - 90) * 0.0174532925)
        sy2 = math.sin((i + 5 - 90) * 0.0174532925)
        x2 = sx2 * (M_SIZE * 100 + tl) + M_SIZE * 120
        y2 = sy2 * (M_SIZE * 100 + tl) + M_SIZE * 140
        x3 = sx2 * M_SIZE * 100 + M_SIZE * 120
        y3 = sy2 * M_SIZE * 100 + M_SIZE * 140
        
        # Yellow zone limits
        if (i >= -50 and i < 0):
            tft.fillTriangle(int(x0), int(y0), int(x1), int(y1), int(x2), int(y2), tft.color.GREEN)
            tft.fillTriangle(int(x1), int(y1), int(x2), int(y2), int(x3), int(y3),tft.color.GREEN)
            
        # Green Zone limits
        if (i >= 0 and i < 25):
            tft.fillTriangle(int(x0), int(y0), int(x1), int(y1), int(x2), int(y2), tft.color.YELLOW)
            tft.fillTriangle(int(x1), int(y1), int(x2), int(y2), int(x3), int(y3), tft.color.YELLOW)
            
        # Orange zone limits
        if (i >= 25 and i < 50):
            tft.fillTriangle(int(x0), int(y0), int(x1), int(y1), int(x2), int(y2), tft.color.ORANGE)
            tft.fillTriangle(int(x1), int(y1), int(x2), int(y2), int(x3), int(y3), tft.color.ORANGE)
            
        # Short scale tick length
        if (i % 25 != 0):
            tl = 8
        # Recalculate coords incase tick length changed
        x0 = sx * (M_SIZE * 100 + tl) + M_SIZE * 120
        y0 = sy * (M_SIZE * 100 + tl) + M_SIZE * 140
        x1 = sx * M_SIZE * 100 + M_SIZE * 120
        y1 = sy * M_SIZE * 100 + M_SIZE * 140
        
        # Draw tick
        tft.drawLine(int(x0), int(y0), int(x1), int(y1), tft.color.BLACK)
        
        # Check if labels should be drawn, with position tweaks
        if (i % 25 == 0):
            x0 = sx * (M_SIZE * 100 + tl + 10) + M_SIZE * 120
            y0 = sy * (M_SIZE * 100 + tl + 10) + M_SIZE * 140
            
            if(i/25 == -2 ):
                tft.drawCentreString("0", int(x0), int(y0) - 12, 2)
            elif (i/25 == -1 ):
                tft.drawCentreString("25", int(x0), int(y0) - 9, 2)
            elif (i/25 == -0 ):
                tft.drawCentreString("50", int(x0), int(y0) - 7, 2)
            elif (i/25 == 1 ):
                tft.drawCentreString("75", int(x0), int(y0) - 9, 2)
            elif (i/25 == 2 ):
                tft.drawCentreString("100", int(x0), int(y0) - 12, 2)
                
            # Now draw the arc of the scale
            # sx = math.cos((i + 5 - 90) * 0.0174532925)
            # sy = math.sin((i + 5 - 90) * 0.0174532925)
            # x0 = sx * M_SIZE * 100 + M_SIZE * 120
            # y0 = sy * M_SIZE * 100 + M_SIZE * 140
            # # Draw scale arc, don't draw the last part
            # if (i < 50):
            #     tft.drawLine(int(x0), int(y0), int(x1), int(y1), tft.color.BLACK)
            
        tft.drawString("%RH", int(M_SIZE * (5 + 230 - 40)), int(M_SIZE * (119 - 20)), 2); # Units at bottom right
        tft.drawCentreString("%RH", int(M_SIZE * 120), int(M_SIZE * 70), 4); # Comment out to avoid font 4
        tft.drawRect(5, 3, int(M_SIZE * 230), int(M_SIZE * 119), tft.color.BLACK); # Draw bezel line
        
        plotNeedle(0, 0)
        
        
def initial():
    analogMeter()
    updateTime = time.ticks_ms()
    
def main():
    global updateTime, d
    if (updateTime <= time.ticks_ms()):
        updateTime = time.ticks_ms() + 100
        d += 4
        if (d >= 360):
            d = 0
            
        value = 50 + 50 * math.sin((d+0)*0.0174532925)
        print(value)
        plotNeedle(value, 0)
        
        
if __name__ == "__main__":
    initial()
    while True:
        main()
        
        
        
        
        
        
        