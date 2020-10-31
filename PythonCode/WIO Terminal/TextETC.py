from machine import LCD

tft = LCD()
tft.fillScreen(tft.color.BLACK)
tft.drawPixel(50,50,tft.color.WHITE)
tft.drawLine(10,1,100,10,tft.color.WHITE)
tft.drawRoundRect(110,70,100,100,10,tft.color.GREEN)
tft.fillRoundRect(220,100,10,20,2,tft.color.GREEN)
tft.drawTriangle(160,70,60,170,260,170,tft.color.BLUE)

tft.drawNumber(70,20,100)
tft.drawFloat(3.1415,300,400)

tft.drawChar(10,10,2,64)
tft.setTextColor(tft.color.RED)
tft.setTextSize(1)
tft.drawString("Hello world!", 230, 210)
tft.setTextSize(2)
tft.drawString("H", 200, 210)

tft.drawCircle(100,100,50,tft.color.WHITE)
