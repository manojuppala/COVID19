from bs4 import BeautifulSoup
import os
import numpy as np
import requests
import pandas as pd
import csv
import datetime as dt
from matplotlib import pyplot as plt
os.chdir("Desktop\python\covid19")
#using requests.get() and the link of the website that is to be souped we can retrieve the html code used the website.
source=requests.get('https://www.google.com/covid19-map/').text
#using the BeautifulSoup function imported we can assign the retrieved code to a variable. the second attribute of the function is the type of html code.
soup=BeautifulSoup(source,'lxml')
#the data we need is situated in the body-tag of the script.
body=soup.find('body')
#now movin further into the body tag. the data is situated in a script tag with an id='Yp9gcL11JbUBXK0ETflCBw'
#script=body.find('script',id="Yp9gcL11JbUBXK0ETflCBw")
script=body.find_all('script')[5]
#the prettify function properly arranges the code that is retrieved.
file1=open("script.txt",'w')
file1.write(str(script))
file1.close()
file2=open("script.txt",'r')
data=file2.read()
file2.close()
#cleaning the retrieved data to get the number of deaths globally   
def clean(d):
    v=[]
    a=d.split('"Worldwide"')
    b=a[0].split("null")
    val=b[1].split(",")
    v.append(val[1].split("[")[2].split("]")[0])
    v.append(val[4].split("]")[0].split("[")[1])
    return v
 
val=clean(data)
val=[int(i) for i in val]
aff=val[0]
rec=val[1]
rate=round((rec/aff)*100,2)
date1=str(dt.date.today())
rows_=[[date1,rate]]
#working with csv file
def datecheck(csv1,date1):
    rows=[]
    for row in csv.reader(csv1):
        rows.append(row)   
    for j in rows:
        if(j[0]==date1):
            return False
    return True        
csv_=open("data.csv",'r')    
k=datecheck(csv_,date1)
csv_.close()        
if(k):
    csv1=open('data.csv','a')
    csv.writer(csv1).writerows(rows_)
    csv1.close()
csv1=open('data.csv','r')
row_=[]
x=[]
y=[]
for row in csv.reader(csv1):
    row_.append(row)   
for j in range(1,len(row_)-1):
    if(str(dt.date.today())==row_[j][0]):
        x.append('Today')
    else:
        x.append(row_[j][0][:5])
    y.append(float(row_[j][1]))

#plotting graph using matplotlib
plt.title("% of people recovered from COVID19")
plt.xlabel("date")
plt.ylabel("% people")
plt.xticks(np.arange(0,len(x)+1))
plt.yticks(np.arange(20,100,0.5))
plt.scatter(x,y)
plt.grid(color="r")
plt.plot(x,y)
plt.show()  