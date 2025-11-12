import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from word2number import w2n
import csv

#Choosing files and creating data frames
data=pd.read_csv("unclean_job_data.csv")
df=pd.DataFrame(data)
 #print(df.to_string()) 
print(df.info())

#removing empty phone numbers
df.dropna(subset=["Phone Number"],inplace=True)
print(df.info())

#Changing Age to Numbers
def agenum(value):
    if pd.isna(value):
        return value
    try:
        return pd.to_numeric(value)
    except:
        try:
           return w2n.word_to_num(value.strip().lower())
        except:
            return pd.NA
df["Age"]=df["Age"].apply(agenum)

#filling null age with Mean
x=df["Age"].mean()
df.fillna({"Age":x},inplace=True)
print(df.info())

#Filling empty emails with N/A
df.fillna({"Email":"None"},inplace=True)
print(df.info())

#Changing DataTypes In Salary To Numeric
def numbizer(value):
    if pd.isna(value):
        return value
    try:
        return pd.to_numeric(value)
    except:
        try:
            return w2n.word_to_num(value.strip().lower())
        except:
            return pd.NA


df["Salary"]=df["Salary"].apply(numbizer)
print(df["Salary"].to_string())
print(df.info())

#Removing People Without Salary
df.dropna(subset=["Salary"],inplace=True)
print(df.info())

#Removing No-entry & Blank Phone Numbers
mask=df["Phone Number"].notna() & (df["Phone Number"].str.strip()!= "")
df=df[mask]
print(df["Phone Number"].to_string())

#Removing Duplicates
df.drop_duplicates(inplace=True)




#Changing DataType in Salary
df["Salary"]=df["Salary"].astype(int)

#Saving Cleaned Data In New Csv
with open("cleandata.csv","w",newline="") as file:
    writer=csv.writer(file)
    writer.writerow(df.columns)
    writer.writerows(df.values)

#Checking for correlation between Salary and Age
correlation=(df.corr(numeric_only=True))
correlation=pd.DataFrame(correlation)
print(correlation)

correlation.to_csv("Age_Salary_Correlation.csv")

#Creating Visualizations
Tfont={"family":"serif","color":"blue","size":20}
axfont={"family":"fantasy","color":"darkred","size":15}
plt.plot(correlation)

plt.ylabel("Correlation Values",loc="center",fontdict=axfont)
plt.title("AGE vs SALARY CORRELATION",loc="left",fontdict=Tfont)
plt.grid(color="green",ls="--",lw=0.5)
plt.show()