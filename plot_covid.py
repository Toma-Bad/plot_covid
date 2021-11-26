#!/usr/bin/python

countrylist = ["Afghanistan","Africa","Albania","Algeria","Andorra","Angola","Anguilla","Antigua and Barbuda","Argentina","Armenia","Aruba","Asia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bonaire Sint Eustatius and Saba","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Curacao","Cyprus","Czechia","Democratic Republic of Congo","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Europe","European Union","Faeroe Islands","Falkland Islands","Fiji","Finland","France","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","High income","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","International","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Low income","Lower middle income","Luxembourg","Macao","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia (country)","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","North America","North Macedonia","Northern Cyprus","Norway","Oceania","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn","Poland","Portugal","Qatar","Romania","Russia","Rwanda","Saint Helena","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Sint Maarten (Dutch part)","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South America","South Korea","South Sudan","Spain","Sri Lanka","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor","Togo","Tokelau","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","United States","Upper middle income","Uruguay","Uzbekistan","Vanuatu","Vatican","Venezuela","Vietnam","Wallis and Futuna","World","Yemen","Zambia","Zimbabwe"]
import sys, argparse
parser = argparse.ArgumentParser()     
parser.add_argument('-u',action="store_true",help=r'Update the database. If set, it does:  wget -r https://covid.ourworldindata.org/data/owid-covid-data.csv')
parser.add_argument('--clist',nargs='+',metavar="Countryname",help="List of countries to show, default: Romania Poland Germany Netherlands",default=['Romania','Poland','Germany','Netherlands']
)
parser.add_argument('--ylim',nargs=1,metavar='float',help="Upper bound of y left axis, default is 1",default=[1.],type=float)
parser.add_argument('--of',nargs=1,metavar="Filename.xyz",default="plot_covid.png",help="Output filename (*.png, *.pdf etc.), default: plot_covid.png")
parser.add_argument('--list',action="store_true",help='List all available countries')
parselist = parser.parse_args(sys.argv[1:])
if parselist.list:
	for _ in countrylist:
		print(_)
	sys.exit()

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
parselist.list = True
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

