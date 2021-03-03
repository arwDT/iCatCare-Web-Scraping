#import libraries
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import numpy as np
import re
from datetime import datetime

#Initiate Storage
clinic_names = []
accreditations = []
clinic_addresses = []
#Create list of number of pages
#pages = np.linspace(1,146,146, dtype=int)

#Iterate over each web page
#for page in pages:
    #make request from CatFriendlyClinic.org
url = "https://catfriendlyclinic.org/cat-owners/find-a-clinic/"#page/"+str(page)+"/"
webpage = rq.get(url)

#Create BeautifulSoup object to traverse the webpage
soup = BeautifulSoup(webpage.content, "html.parser")

#Find all clinics on page
all_clinic_elements = soup.find_all(attrs={"class": "clinic"})

#Retrieve all clinic names and addresses
for container in all_clinic_elements:
    #clinic names
    clinic_name = container.h2.get_text()
    clinic_names.append(clinic_name)
    #clinic accreditation
    accreditation = container.div['class'][1]
    if accreditation == "rating--gold":
        accreditations.append("Gold")
    elif accreditation == "rating--silver":
        accreditations.append("Silver")
    elif accreditation == "rating--bronze":
        accreditations.append("Bronze")
    #clinic addresses
    clinic_address = container.section.get_text()
    #split clinic addresses
    clinic_address_split = re.split("\t+", clinic_address)
    #remove first and last values
    clinic_address_filt = clinic_address_split[1:(len(clinic_address_split)-1)]
    #turn address into string
    address_string = ""
    for line in clinic_address_filt:
        address_string += " "+line
    clinic_addresses.append(address_string)


#create dataframe
data = {"Name":clinic_names, "Clinic Rating Level":accreditations, "Address":clinic_addresses}
df = pd.DataFrame.from_dict(data)
print(df)

#Get current datetime
now = datetime.now()
dt_string = now.strftime("%Y%m%d%H%S")

#Export
df.to_excel("C:\Python\Web Scraping\Output\iCatCareAccredited_{}.xlsx".format(dt_string))
