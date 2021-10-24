#Webscraping Trulia.com
##########################################################################################################
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import time
import csv

driver = webdriver.Firefox(executable_path=r'C:\Users\KADAVADK\Documents\geckodriver-v0.30.0-win64\geckodriver.exe')

#Agent listing
dv1_url='https://www.trulia.com/for_sale/Oklahoma_City,OK/foreclosure_lt/'
driver.get(dv1_url)
time.sleep(3)

#address
address_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-address"]')
for i in element :
    address_list.append(i.text)

#price
element = driver.find_elements_by_xpath('//div[@data-testid="property-price"]')
price_list=[]
for i in element :
    price_list.append(i.text)

#beds
beds_list =[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-beds"]')
for i in element :
    beds_list.append(i.text)


#bath
bath_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-baths"]')
for i in element :
    bath_list.append(i.text)


#Lotsize/SqFt
prop_floorspace_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-floorSpace"]')
for i in element :
    prop_floorspace_list.append(i.text)


ownership_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-tags"]')
for i in element :
    ownership_list.append(i.text)


list =[address_list,price_list,beds_list,bath_list,prop_floorspace_list,ownership_list]
df =pd.DataFrame(list)
df_trans = df.transpose()
df_trans.rename(columns={0 : 'Address', 1 : 'Price',2:'Bed',3: 'Bath',4:'LotSize/SqFt',5:'Ownership',}, inplace=True)
df_trans.to_csv(r'C:\Users\KADAVADK\Documents\trulia_v1.csv',index =False,sep=',')

#########################################################################################################################
#OtherListing

dv2_url='https://www.trulia.com/for_sale/Oklahoma_City,OK/foreclosure_lt/1_als/'
driver.get(dv2_url)
time.sleep(3)
#price
price_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-price"]')
for i in element :
    price_list.append(i.text)

#address
address_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-address"]')
for i in element :
    address_list.append(i.text)

#beds
beds_list =[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-beds"]')
for i in element :
    beds_list.append(i.text)

#bath
bath_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-baths"]')
for i in element :
    bath_list.append(i.text)


#Lotsize/SqFt
prop_floorspace_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-floorSpace"]')
for i in element :
    prop_floorspace_list.append(i.text)

#ownership
ownership_list=[]
element = driver.find_elements_by_xpath('//div[@data-testid="property-tags"]')
for i in element :
    ownership_list.append(i.text)

list =[address_list,price_list,beds_list,bath_list,prop_floorspace_list,ownership_list]
df =pd.DataFrame(list)
df_trans = df.transpose()
df_trans.rename(columns={0 : 'Address', 1 : 'Price',2:'Bed',3: 'Bath',4:'LotSize/SqFt',5:'Ownership',}, inplace=True)
df_trans.to_csv(r'C:\Users\KADAVADK\Documents\trulia_v1_otherlisting.csv',index =False,sep=',')

#############################################################################################################
#Listed for sale or sold
dv3_url='https://www.trulia.com/p/ok/oklahoma-city/5808-nw-109th-st-oklahoma-city-ok-73162--2108409814'
driver.get(dv3_url)
time.sleep(2)
address1='5808-nw-109th-st-oklahoma-city-ok-73162'
listedsalesold1=[]
element= driver.find_elements_by_xpath('//table[@class="Table-latbb5-3 lomxvq"]')
for i in element :
    listedsalesold1.append(i.text)

sold1=listedsalesold1[-2][788:811]
listed_for_sale1=listedsalesold1[-2][354:389]
################################################################################################################
dv4_url='https://www.trulia.com/p/ok/oklahoma-city/5324-se-134th-st-oklahoma-city-ok-73165--2354121667'
driver.get(dv4_url)
time.sleep(3)
address2='5324-se-134th-st-oklahoma-city-ok-73165'
listedsalesold2=[]
for i in driver.find_elements_by_xpath('//table[@class="Table-latbb5-3 lomxvq"]') :
    listedsalesold2.append(i.text)

sold2=listedsalesold2[-2][118:142]
listed_for_sale2=listedsalesold2[-2][67:102]
##################################################################################################################
dv5_url='https://www.trulia.com/p/ok/bethany/3605-n-donna-ave-bethany-ok-73008--2108135806'
driver.get(dv5_url)
time.sleep(3)
address3='3605-n-donna-ave-bethany-ok-73008'
listedsalesold3=[]
for i in driver.find_elements_by_xpath('//table[@class="Table-latbb5-3 lomxvq"]') :
    listedsalesold3.append(i.text)

sold3=listedsalesold3[-2][165:188]
listed_for_sale3=listedsalesold3[-2][115:149]
###############################################################################################################
dv6_url='https://www.trulia.com/p/ok/newalla/17061-winding-creek-dr-newalla-ok-74857--2065408801'
driver.get(dv6_url)
time.sleep(3)
address4='17061-winding-creek-dr-newalla-ok-74857'
listedsalesold4=[]
for i in driver.find_elements_by_xpath('//table[@class="Table-latbb5-3 lomxvq"]') :
    listedsalesold4.append(i.text)

sold4=listedsalesold4[-2][24:48]
listed_for_sale4=listedsalesold4[-2][120:156]

##################################################################################################################
dv7_url='https://www.trulia.com/property/5057867900-NW-178th-St-Piedmont-OK-73078'
driver.get(dv7_url)
time.sleep(3)
address5='NW-178th-St-Piedmont-OK-73078'
listedsalesold5=[]
for i in driver.find_elements_by_xpath('//table[@class="Table-latbb5-3 lomxvq"]') :
    listedsalesold5.append(i.text)

sold5=""
listed_for_sale5=listedsalesold5[-1][24:60]
#####################################################################################################################
#dataFrame
addresslist=[address1,address2,address3,address4,address5]
soldlist=[sold1,sold2,sold3,sold4,sold5]
listedforsale=[listed_for_sale1,listed_for_sale2,listed_for_sale3,listed_for_sale4,listed_for_sale5]
list=[addresslist,soldlist,listedforsale]

df =pd.DataFrame(list)
df_trans = df.transpose()
df_trans.rename(columns={0 : 'Address', 1 : 'Sold',2:'listed for sale',}, inplace=True)
df_trans.to_csv(r'C:\Users\KADAVADK\Documents\trulia_v1_sold_listedforsale.csv',index =False,sep=",")
###########################################################################################################
driver.quit()