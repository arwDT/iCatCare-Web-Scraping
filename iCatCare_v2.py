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
clinic_address_1 = []
clinic_address_2 = []
clinic_address_3 = []
clinic_address_4 = []
clinic_address_5 = []
clinic_address_6 = []

#Create list of number of pages
pages = np.linspace(1,146,146, dtype=int)

#Iterate over each web page
for page in pages:
    #make request from CatFriendlyClinic.org
    url = "https://catfriendlyclinic.org/cat-owners/find-a-clinic/"#page/"+str(page)+"/"
    webpage = rq.get(url)

    #Create BeautifulSoup object to traverse the webpage
    soup = BeautifulSoup(webpage.content, "html.parser")

    #Find all clinics on page
    all_clinic_elements = soup.find_all(attrs={"class": "clinic"})

    #Retrieve all clinic names and addresses
    for container in all_clinic_elements:
        '''Clinic Names'''
        clinic_name = container.h2.get_text()
        clinic_names.append(clinic_name)
        '''Clinic Accreditation'''
        accreditation = container.div['class'][1]
        if accreditation == "rating--gold":
            accreditations.append("Gold")
        elif accreditation == "rating--silver":
            accreditations.append("Silver")
        elif accreditation == "rating--bronze":
            accreditations.append("Bronze")
        '''Clinic Addresses'''
        clinic_address = container.section.get_text()
        #split clinic addresses
        clinic_address_split = re.split("\t+", clinic_address)
        #remove first and last values
        clinic_address_filt = clinic_address_split[1:(len(clinic_address_split)-1)]
        # add blank spaces to the end of the list till it has a length of 6
        while len(clinic_address_filt) < 6:
            clinic_address_filt.append(" ")
        #Append address lines to lists
        clinic_address_1.append(clinic_address_filt[0])
        clinic_address_2.append(clinic_address_filt[1])
        clinic_address_3.append(clinic_address_filt[2])
        clinic_address_4.append(clinic_address_filt[3])
        clinic_address_5.append(clinic_address_filt[4])
        clinic_address_6.append(clinic_address_filt[5])

#create dataframe
data = {"Name":clinic_names, "Clinic Rating Level":accreditations, "Address 1":clinic_address_1, "Address 2":clinic_address_2, "Address 3":clinic_address_3, "Address 4":clinic_address_4, "Address 5":clinic_address_5, "Address 6":clinic_address_6}
df = pd.DataFrame.from_dict(data)
print(df)

#Get current datetime
now = datetime.now()
dt_string = now.strftime("%Y%m%d%H%S")

#Export
df.to_excel("C:\Python\Web Scraping\Output\iCatCareAccredited_{}.xlsx".format(dt_string))
