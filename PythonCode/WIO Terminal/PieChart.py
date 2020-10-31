from machine import LCD, Sprite
import time, math

DEG2RAD = 0.0174532925
lcd = LCD()
lcd.fillScreen(lcd.color.BLACK)

# DRAW CIRCLE SEGMENTS
# x,y == coords of centre of circle
# start_angle = 0 - 359
# sub_angle   = 0 - 360 = subtended angle
# r = radius
# colour = 16 bit colour value

def fillSegment(x, y, startAngle, subAngle, r, color):
    # Calculate first pair of coordinates for segment start
    sx = math.cos((startAngle - 90) * DEG2RAD)
    sy = math.sin((startAngle - 90) * DEG2RAD)
    x1 = sx * r + x
    y1 = sy * r + y
    
    # Draw colour blocks every inc degrees
    for i in range(startAngle, startAngle+subAngle, 1):
        # Calculate pair of coordinates for segment end
        x2 = math.cos((i + 1 - 90) * DEG2RAD) * r + x
        y2 = math.sin((i + 1 - 90) * DEG2RAD) * r + y
        
        lcd.fillTriangle(int(x1), int(y1), int(x2), int(y2), x, y, color)
        
        # Copy segment end to segment start for next segment
        x1 = x2
        y1 = y2
        
def main():
    # Draw 4 pie chart segments
    fillSegment(160, 120, 0, 60, 100, lcd.color.RED)
    fillSegment(160, 120, 60, 30, 100, lcd.color.GREEN)
    fillSegment(160, 120, 60 + 30, 120, 100, lcd.color.BLUE)
    fillSegment(160, 120, 60 + 30 + 120, 150, 100, lcd.color.YELLOW)
    time.sleep(1)
    fillSegment(160, 120, 0, 360, 100, lcd.color.BLACK)
    
if __name__ == "__main__":
    while True:
        main()
        