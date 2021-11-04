## this is a very poorly written piece of code by worms_sg. It is still hardcoded while i mess around with features

## v0.1 (04 Nov 21)

## Import Matplotlib & Related Modules ##

import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
from matplotlib.patches import Polygon

##Import Misc Modules ##

import pandas as pd
from datetime import datetime

## Optional Modules ##

#from functools import cache
import numpy as np
import math

## Set Color parameters ##

clist = ['cornsilk', 'moccasin', 'mistyrose', 'honeydew', 'lightpink', 'aliceblue','lightgoldenrodyellow', 'thistle','lightcyan', 'lavenderblush', 'mintcream', 'oldlace', 'gainsboro']

## Set pyplot parameters ##

plt.rcParams.update({'font.size': 18})
plt.rcParams['figure.figsize'] = 16, 9
plt.rcParams['figure.dpi']=100

## Function to create lines ##

def CreateLines(num):
    
    createdlines = []

    for x in range(0,num):
        createdlines.append([])

    return createdlines

## Function to extend information to fill blank rows ##

def ExtendBlanks(*args):
    for y in args:
        for i in range(len(y)):
            if (y[i]==0):
                y[i]=y[i-1]

## Function to clear text lists ##

def DeleteTexts(*args):
    for axis in args:
        axis.texts.clear()

## Function to set x axis ##

def Set_xWindow(tmin, tmax, *args):
    for axis in args:
        axis.set_xlim(tmin, tmax)

## Read csv & Format data ##

df=pd.read_csv('Covid.csv', header = 0)
df = df.fillna(0)

df['Swab Test Positivity Rate (%)'] = df['Swab Test Positivity Rate (%)'].astype(float)
#df['CFR (all cases)'] = df['CFR (all cases)'].str.rstrip('%')
df['CFR (all cases)'] = df['CFR (all cases)'].astype(float)

## Assign column data to variables ##

t = []

y = CreateLines(10)

for index, row in df.iterrows():

    t.append(datetime.strptime(row['Date'],'%d-%b-%Y'))
    y[0].append(row['Local cases']) 
    y[1].append(row['Hospitalized'])
    y[2].append(row['ICU'])
    y[3].append(row['Deaths'])
    y[4].append(row['Swab Test Positivity Rate (%)'])
    y[5].append(row['CFR (all cases)'])
    y[6].append(row['Weekly case ratio'])
    y[7].append(row['%Full Regimen'])
    y[8].append(row['Note'])
    y[9].append(row['Status'])

## extend information to fill blank rows ##


ExtendBlanks( y[4] , y[6] , y[7] ,y[8], y[9])



## Scale down values for presentation ##

y4b = y[4]
y5b = y[5]
y6b = y[6]

y[4] = [x*10 for x in y[4]]
y[5] = [x*100 for x in y[5]]
y[6] = [x*10 for x in y[6]]

## Create blank plots ##

fig, ((ax1, ax2, ax3)) = plt.subplots(3,sharex=True)

fig.tight_layout(pad=5,h_pad=0.5, w_pad = 0.5)

fig.patch.set_facecolor('floralwhite')
ax1.set_facecolor('snow')
ax2.set_facecolor('snow')
ax3.set_facecolor('snow')

ax1.grid(b=True,which='major',axis='x')
ax2.grid(b=True,which='major',axis='x')
ax3.grid(b=True,which='major',axis='y')

## PLot Lines ##

line0, = ax1.plot(t, y[0], color = "r", label = 'Daily Local transmission ', linewidth=2)
line1, = ax1.plot(t, y[1],color = "olive", label = 'Hospitalized', linewidth=2)

line2, = ax2.plot(t, y[2], color = "g", label = 'Warded in ICU', linewidth=2)
line3, = ax2.plot(t, y[3], color = "b", label = 'Cumulative Deaths', linewidth=2)

line4, = ax3.plot(t, y[4], color = "y", label = 'Test Positivity Rate', linewidth=2)
line5, = ax3.plot(t, y[5], color = "tab:purple", label = 'CFR (all cases)', linewidth=2)
line6, = ax3.plot(t, y[6], color = "tab:grey", label = 'Weekly Case Ratio', linewidth=2)
line7, = ax3.plot(t, y[7], color = "tab:pink", label = 'Full Regimen', linewidth=2)

## Set additional y margins

axis1_margin = 10
axis2_margin = 10
axis3_margin = 1.1

## Set x window size

x_window = 90

def update(num,t):

    ax1_y_limit= max(max(y[0][0:num+1]),max(y[1][0:num+1]))+axis1_margin
    ax1.set_ylim(-1, ax1_y_limit)
    #ax1.set_yscale('log')

    ax2_y_limit = max(max(y[2][0:num+1]),max(y[3][0:num+1]))+axis2_margin
    ax2.set_ylim(-1, ax2_y_limit)
    #ax2.set_yscale('linear')

    ax3_y_limit = min(100,max(max(y[4][0:num+1]) , max(y[5][0:num+1]) , max(y[6][0:num+1]) , max(y[7][0:num+1]))*axis3_margin)
    ax3.set_ylim(0, ax3_y_limit)
    #ax3.set_yscale('linear')

    DeleteTexts(ax1, ax2, ax3)

    nIndex = len(set(y[9][0:num]))

    if(num<x_window+1):

        Set_xWindow(min(t), t[num], ax1, ax2, ax3)

        line0.set_data(t[0:num], y[0][0:num])
        line1.set_data(t[0:num], y[1][0:num])
        line2.set_data(t[0:num], y[2][0:num])
        line3.set_data(t[0:num], y[3][0:num])
        line4.set_data(t[0:num], y[4][0:num])
        line5.set_data(t[0:num], y[5][0:num])
        line6.set_data(t[0:num], y[6][0:num])
        line7.set_data(t[0:num], y[7][0:num])

        ax1.text(t[0],ax1_y_limit*1.1, "Current Phase: " + str(y[9][num]))

        if (str(y[9][num]) != str(y[9][num-1])):

            ax1.axvspan(t[num],t[len(t)-1], color = clist[nIndex], zorder = nIndex-99)
            #ax1.boxplot()


    else:

        Set_xWindow(t[num-x_window], t[num], ax1, ax2, ax3)

        PlotMin = num - x_window

        line0.set_data(t[PlotMin:num], y[0][PlotMin:num])
        line1.set_data(t[PlotMin:num], y[1][PlotMin:num])
        line2.set_data(t[PlotMin:num], y[2][PlotMin:num])
        line3.set_data(t[PlotMin:num], y[3][PlotMin:num])
        line4.set_data(t[PlotMin:num], y[4][PlotMin:num])
        line5.set_data(t[PlotMin:num], y[5][PlotMin:num])
        line6.set_data(t[PlotMin:num], y[6][PlotMin:num])
        line7.set_data(t[PlotMin:num], y[7][PlotMin:num])

        ax1.text(t[PlotMin],ax1_y_limit*1.1, "Current Phase: " + str(y[9][num]))
   
        if (str(y[9][num]) != str(y[9][num-1])):

            ax1.axvspan(t[num],t[len(t)-1], color = clist[nIndex % 4], zorder = nIndex-99)
            #ax1.boxplot()

   ## Diplay data on each axis

    ax1.text(t[num], ax1_y_limit*0.25, t[num].strftime("%d %b %y") + "\n" + str(int(y[0][num])) + " Local Cases", fontsize=14, color = "r")
    ax1.text(t[num], ax1_y_limit*0, str(int(y[1][num])) + " Hospitalized", fontsize=14, color = "olive")

    ax2.text(t[num], ax2_y_limit*0.25, str(int(y[2][num])) + " in ICU", fontsize=12, color = "g")
    ax2.text(t[num], ax2_y_limit*0.5, str(int(y[3][num])) + " dead", fontsize=12, color = "b")

    ax3.text(t[num], ax3_y_limit*0.5, str(round(y4b[num],3)) + "% Test Positivity Rate\n(Display 10x)", fontsize=12, color = "y")
    ax3.text(t[num], ax3_y_limit*0.75, str(round(y5b[num],3)) + "% CFR (Display 100x)", fontsize=12, color = "tab:purple")
    ax3.text(t[num], ax3_y_limit*0.25, "Weekly Case Ratio: " + str(y6b[num]), fontsize=12, color = "tab:grey")
    ax3.text(t[num], ax3_y_limit*0, str(y[7][num]) + "% Fully Vacinnated", fontsize=12, color = "tab:pink")

    return []
    
def main():

    ani = animation.FuncAnimation(fig, update, len(t), fargs=[t],
                      interval=1,repeat = False)

    plt.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1)

    fig.autofmt_xdate()

    plt.suptitle("Covid-19 Pandemic in Singapore")
    fig.legend(loc= 'upper right', fontsize=10,borderpad=0.1)

    plt.minorticks_on()
    plt.xlabel('Dates')
    plt.grid(which = 'major')

    ## Switch between display and save gif modes ##

    ani.save("CovidPlot.gif", fps=15)      
    #plt.show()

main()

