# -*- coding:utf-8 -*-
from reportlab.graphics.shapes import *
from reportlab.lib import colors
from reportlab.graphics import renderPDF

data=[
    (2007,8, 113.2, 114.2, 112.2),
    (2007,9, 112.8, 115.8, 108.8),
    (2007,10, 111.0, 116.0, 106.0),
    (2007,11, 109.8, 116.8, 102.8),
    (2007,12, 107.3,115.3, 99.31 ),
    (2008,1, 102.2, 114.2, 112.2),
    (2008,2, 104.8, 115.8, 88.8),
    (2008,3, 99.0, 116.0, 92.0),
    (2008,4, 98.8, 116.8, 82.8),
    (2008,5, 91.3,115.3, 78.31 )
]

drawing=Drawing(200,150)
pred=[row[2]-40 for row in data]
high=[row[3]-40 for row in data]
low=[row[4]-40 for row in data]
times=[200*((row[0]+row[1]/12.0)-2007)-110 for row in data]


drawing.add(PolyLine(list(zip(times,pred)),strokeColor=colors.blue))
drawing.add(PolyLine(list(zip(times,high)),strokeColor=colors.red))
drawing.add(PolyLine(list(zip(times,low)),strokeColor=colors.green))
drawing.add(String(65,115,'Sunspot',fontsize=18,fileColor=colors.red))

renderPDF.drawToFile(drawing,'reports.pdf','Sunports')