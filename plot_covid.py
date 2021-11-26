#!/usr/bin/python
import sys, argparse
parser = argparse.ArgumentParser()     
parser.add_argument('-u',action="store_true",help=r'Update the database. If set, it does:  wget -r https://covid.ourworldindata.org/data/owid-covid-data.csv')
parser.add_argument('--clist',nargs='+',metavar="Countryname",help="List of countries to show, default: Romania Poland Germany Netherlands",default=['Romania','Poland','Germany','Netherlands']
)
parser.add_argument('--ylim',nargs=1,metavar='float',help="Upper bound of y left axis, default is 1",default=[1.],type=float)
parser.add_argument('--of',nargs=1,metavar="Filename.xyz",default="plot_covid.png",help="Output filename (*.png, *.pdf etc.), default: plot_covid.png")
parselist = parser.parse_args(sys.argv[1:])

country_list = parselist.clist 
upper_ylim = float(parselist.ylim[0])
ofilename = parselist.of
if parselist.u:
	import os
	try:
		os.system('wget -r https://covid.ourworldindata.org/data/owid-covid-data.csv')
	except Exception as e:
		print(e)
import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import datetime as dt

try:
	tab = ascii.read("owid-covid-data.csv",format='csv') 
except Exception as e:
	print("No data file found, try -u option")
	sys.exit(e)
col_title_1 = "new_deaths_smoothed"
col_title_2 = "new_cases_smoothed"
col_operator = "/"

col_title_a_1 = 'people_vaccinated_per_hundred'

fig,ax = plt.subplots()
ax2 = ax.twinx()
entries=0
for country in country_list:
	temp_tab = tab[tab['location']==country]
	if len(temp_tab) > 0:
		entries+=1
		xx = [dt.datetime.strptime(_,'%Y-%m-%d') for _ in temp_tab['date']]
		yy_1 = temp_tab[col_title_1]
		yy_2 = temp_tab[col_title_2]
		yy_a = eval('yy_1'+col_operator+'yy_2')
		p1, = ax.plot(xx,yy_a,label=country,linestyle='solid')
		yy_b = temp_tab[col_title_a_1]
		ax2.plot(np.array(xx)[yy_b.mask==False],np.array(yy_b)[yy_b.mask==False],color = p1.get_color(),linestyle = 'dashed')
	else:
		print("Country "+country+" not found!\ni")
		pass
if entries == 0:
	sys.exit('No countries found!')

ax.set_ylim(-0.05,upper_ylim)
ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
lin1, = plt.plot([],[],linestyle='solid',label='Left y-axis',color='black')
y_legend_left = plt.legend(handles = [lin1],loc='upper left')
plt.gca().add_artist(y_legend_left)
lin2, = plt.plot([],[],linestyle='dashed',label='Right y-axis',color='black')
plt.legend(handles = [lin2],loc='upper right')
#ax.add_artist(y_legend)
#plt.plot([],[],linestyle='dashed',label='Right y-axis',color='black')
#legend2 = plt.legend(loc='upper right')
#ax.add_artist(y_legend)
ax.set_ylabel(col_title_1.replace("_"," ").capitalize()+" "+col_operator+"\n"+col_title_2.replace("_"," ").capitalize())
ax2.set_ylabel(col_title_a_1.replace("_"," ").capitalize())
fig.autofmt_xdate()
plt.tight_layout()
try:
	plt.savefig(ofilename)
except Exception as e:
	print(e)
plt.show()
plt.close()

