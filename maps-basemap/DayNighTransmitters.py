import csv

# Open the earthquake data file.
filename = 'transmitter_info.csv'
# Create empty lists for the latitudes and longitudes.
lats, lons, labels, tunlon, tunlat = [], [], [], [], []

# Read through the entire file, skip the first line,
#  and pull out just the lats and lons.
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)
    
    # Ignore the header row.
    next(reader)
    
    # Store the latitudes and longitudes in the appropriate lists.
    for row in reader:
        labels.append(row[0])
        lats.append(float(row[2]))
        lons.append(float(row[3]))
        tunlon.append(float(row[5]))
        tunlat.append(float(row[6]))
#Tunis coordinate
tunis_lat=36.5
tunis_lon=10.08
# --- Build Map ---
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#from matplotlib.widgets import Cursor
import numpy as np
from datetime import datetime
map = plt.figure(figsize=[10,7]) 
map = Basemap(projection='mill', area_thresh = 1000.0,
              lat_0=0, lon_0=10, resolution = 'l', suppress_ticks=True)      #resolution : 'l' for low and 'h' for hight and 'c'


map.drawcoastlines(color='#A3A3A3')
map.drawcountries(color='#A3A3A3')
map.drawmapboundary(fill_color='lightblue')
map.fillcontinents(color='#FFFFFF',lake_color='lightblue')
map.drawparallels(np.arange(-90,100,30),labels=[1,0,0,0],color='#A1A866', linewidth=.2)
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,30),labels=[0,0,0,1],color='#A1A866', linewidth=.2)
 
x,y = map(lons, lats)
v,w = map(tunis_lon, tunis_lat)
map.plot(x, y, 'ro', markersize=10, label='VLF Transmitter')
map.plot(v, w, 'bo', markersize=10, label='VLF Reciever')
for label, xpt, ypt in zip(labels, x, y):
    plt.text(xpt+10000, ypt+5000, label, color='k',fontsize=12, fontweight='bold')

for wpt, vpt, xpt, ypt in zip(tunlon, tunlat, lons, lats):
    # draw great circle route between tunisia and vlf trx
   
    map.drawgreatcircle(wpt,vpt,xpt,ypt,linewidth=2, linestyle='--',color='k')
    
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
#date = datetime.today()
date=datetime(2016,6, 21,12)
CS=map.nightshade(date)
#plt.title('Day/Night Map for %s (UT)' % date.strftime("%d %b %Y %H:%M:%S"))

#to show long/lat coordination under the curosor
ax = plt.gca()
def format_coord(x, y):
    return 'Longitude=%.4f, Latitude=%.4f'%(map(x, y, inverse = True))
ax.format_coord = format_coord

#cursor
## set useblit = True on gtkagg for enhanced performance
#cursor = Cursor(ax, useblit=True, color='yellow', linewidth=1 )

#make legend
legend = plt.legend(loc='lower left',fontsize=8,frameon=True,title='Legend',markerscale=1,prop={'size':10})
legend.get_title().set_fontsize('20')
plt.savefig("carte_vlf_dn.pdf", dps=50)
plt.show()
