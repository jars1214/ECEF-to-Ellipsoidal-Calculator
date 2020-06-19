__author__ = "Justine"
from pyproj import _datadir, datadir
import tkinter as tk
from functools import partial
import math
from math import cos
from math import sin
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



def store_val(sel_convert):
    global convertVal
    convertVal = sel_convert


def call_result(rl1, rl2, rl3, rl4, rl5, rl6, input1, input2, input3, input4, input5, input6):
    xval = float(input1.get())
    yval = float(input2.get())
    zval= float(input3.get())
    latval = float(input4.get())
    longval = float(input5.get())
    heightval = float(input6.get())

    print(latval)
    print(longval)
    print(heightval)
    print(xval)
    print(yval)

    if convertVal == "ECEF":
         global a
         a = 6378137
         #f = 1/298.257224
         global esqured
         esqured= 6.694*(1*pow(10, -3))
         global xcord, ycord, zcord
         v = (a / (math.sqrt(1 - (esqured * (sin(latval)) ** 2))))
        # n = 6378137 / math.sqrt((1 - (esqured*(math.sin(latval))**2)))
         xcord = float((v+heightval)*(cos(latval))*(cos(longval)))
         ycord = float((v+heightval)*(cos(latval))*(sin(longval)))
         zcord = float(((v*(1-esqured))+heightval)*(sin(latval)))
        # print(n)
         print(xcord)

         rl1.config(text="X: %f " % xcord)
         rl2.config(text="Y: %f " % ycord)
         rl3.config(text="Z: %f " % zcord)

    if convertVal == "Ellipsoidal":
        esqured = 6.694 * (1 * pow(10, -3))
        a = 6378137
        eprime_squared = esqured/(1-esqured)
        p= math.sqrt((xval**2)+(yval**2))
        latitude = math.atan((zval*(1+eprime_squared))/p)
        v = (a/(math.sqrt(1-(esqured*(sin(latitude))**2))))
        height = float((p/math.cos(latitude))-v)
        longitude = float(math.atan(yval/xval))

        print(p)
        print(eprime_squared)
        print(latitude)
        print(v)
        print(height)
        print(longitude)

        rl4.config(text="Latitude: %f " % latitude)
        rl5.config(text="Longitude: %f " % longitude)
        rl6.config(text="Height: %f " % height)
        global latdegree
        global longdegree
        latdegree = (latitude * 180) / math.pi
        longdegree = (longitude * 180) / math.pi

        return


def show_map():
    if convertVal == "Ellipsoidal":

        fig = plt.figure(figsize=(12, 9))

        m = Basemap(projection='mill',
                    llcrnrlat=-90,
                    urcrnrlat=90,
                    llcrnrlon=-180,
                    urcrnrlon=180,
                    resolution='c')

        m.drawcoastlines()

        m.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False])
        m.drawmeridians(np.arange(-180, 180, 30), labels=[0, 0, 0, 1])

        m.scatter(longdegree, latdegree, latlon=True, s=200, c='red', marker='*', alpha=1, edgecolor='k', linewidth=1,
                  zorder=1)

        plt.title('Map Showing Latitude and Longitude', fontsize=20)

        plt.show()

    if convertVal == 'ECEF':
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # Define lower left, uperright lontitude and lattitude respectively
        extent = [-180, 180, -90, 90]
        # Create a basemap instance that draws the Earth layer
        bm = Basemap(llcrnrlon=extent[0], llcrnrlat=extent[2],
                     urcrnrlon=extent[1], urcrnrlat=extent[3],
                     projection='cyl', resolution='l', fix_aspect=False, ax=ax)
        # Add Basemap to the figure
        ax.add_collection3d(bm.drawcoastlines(linewidth=0.25))
        ax.add_collection3d(bm.drawcountries(linewidth=0.35))
        ax.view_init(azim=230, elev=50)
        ax.set_xlabel('Longitude (°E)', labelpad=20)
        ax.set_ylabel('Latitude (°N)', labelpad=20)
        ax.set_zlabel('Altitude (km)', labelpad=20)

        # Add meridian and parallel gridlines
        lon_step = 30
        lat_step = 30
        meridians = np.arange(extent[0], extent[1] + lon_step, lon_step)
        parallels = np.arange(extent[2], extent[3] + lat_step, lat_step)
        ax.set_yticks(parallels)
        ax.set_yticklabels(parallels)
        ax.set_xticks(meridians)
        ax.set_xticklabels(meridians)
        ax.set_zlim(0., 1000.)

        ax.bar3d(xcord/100000, ycord/100000, zcord/100000, 5, 5, 100, color='red')

        plt.show()

root = tk.Tk()

numberInput1 = tk.StringVar()
numberInput2 = tk.StringVar()
numberInput3 = tk.StringVar()
numberInput4 = tk.StringVar()
numberInput5 = tk.StringVar()
numberInput6 = tk.StringVar()

var = tk.StringVar()
input_labelx = tk.Label(root, text="Enter X-Coordinate")
x_entry = tk.Entry(root, textvariable=numberInput1)
input_labelx.grid(row=0)
x_entry.grid(row=0, column=1)

input_labely = tk.Label(root, text="Enter Y-Coordinate")
y_entry = tk.Entry(root, textvariable=numberInput2)
input_labely.grid(row=1)
y_entry.grid(row=1, column=1)

input_labelz = tk.Label(root, text="Enter Z-Coordinate")
z_entry = tk.Entry(root, textvariable=numberInput3)
input_labelz.grid(row=2)
z_entry.grid(row=2, column=1)

input_latitude = tk.Label(root, text="Enter Latitude")
lat_entry = tk.Entry(root, textvariable=numberInput4)
input_latitude.grid(row=3)
lat_entry.grid(row=3, column=1)

input_longitude = tk.Label(root, text="Enter Longitude")
long_entry = tk.Entry(root, textvariable=numberInput5)
input_longitude.grid(row=4)
long_entry.grid(row=4, column=1)

input_height = tk.Label(root, text="Enter Height")
height_entry = tk.Entry(root, textvariable=numberInput6)
input_height.grid(row=5)
height_entry.grid(row=5, column=1)

# ECEFresult_button = tk.Button(root, text="Ellipsoidal")
# ECEFresult_button.grid(row=6, columnspan=1)

resultLabel1 = tk.Label(root, text="X:")
resultLabel1.grid(row=8, columnspan=4)
resultLabel2 = tk.Label(root, text="Y:")
resultLabel2.grid(row=9, columnspan=4)
resultLabel3 = tk.Label(root, text="Z:")
resultLabel3.grid(row=10, columnspan=4)
resultLabel4 = tk.Label(root, text="Latitude:")
resultLabel4.grid(row=11, columnspan=4)
resultLabel5 = tk.Label(root, text="Longitude:")
resultLabel5.grid(row=12, columnspan=4)
resultLabel6 = tk.Label(root, text="Height:")
resultLabel6.grid(row=13, columnspan=4)

call_result = partial(call_result, resultLabel1, resultLabel2, resultLabel3, resultLabel4, resultLabel5, resultLabel6,
                      numberInput1, numberInput2, numberInput3, numberInput4, numberInput5, numberInput6)
result_button = tk.Button(root, text="Convert", command=call_result)
result_button.grid(row=6, column=2)

mapshow_button = tk.Button(root, text="Show", command=show_map)
mapshow_button.grid(row=7, column=2)


# Drop down Menu
dropdownList = ["ECEF", "Ellipsoidal"]
dropdown= tk.OptionMenu(root, var, *dropdownList, command=store_val)
var.set(dropdownList[0])
dropdown.grid(row=0, column=2)

root.mainloop()


