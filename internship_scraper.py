import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

a=input("enter the internship position:")
def get_soup(a, pageno="1"):
    url = "https://internshala.com/internships/keywords-"
    l = a.split()
    for n, i in enumerate(l):
        if n != len(l) - 1:
            url += i + "%20"
        else:
            url += i + "/"
    url += f"page-{pageno}/"


    
    req = requests.get(url)
    
    stat=req.status_code
    
    if stat==200:
        soup = BeautifulSoup(req.content, "html.parser")
        return soup
    else:
        print("there was an error not able to load page")
        return None


def get_pageno():
    try:
        num=get_soup(a).find("div",class_="page_number heading_6").find_all("a")[-1].text.strip()
        return num
    except:
        return False






def get_info(no):
    info={"company":[],"role":[],"location":[],"stipend":[],"duration":[],"link":[]}
    container="internship_list_container_"+str(no)
    
    hlo=get_soup(a,pageno=no).find(id=container)
    if hlo!=None:
        internships=hlo.find_all(class_="container-fluid individual_internship view_detail_button visibilityTrackerItem")
        for i in internships:
            company=i.find("p",class_="company-name").text.strip()
            role=i.find("a",class_="job-title-href").text.strip()
            location=i.find("div",class_="row-1-item locations").find("a").text.strip()
            stipend=i.find("span",class_="stipend").text.strip()
            duration=i.find_all("div",class_="row-1-item")[2].find("span").text.strip()
            link="https://internshala.com"+i.get("data-href")
            info["company"].append(company)
            info["role"].append(role)
            info["location"].append(location)
            info["stipend"].append(stipend)
            info["duration"].append(duration)
            info["link"].append(link)

        df=pd.DataFrame(info)
        return df
    else:
        return None
 
def main():
    if get_pageno()!=False:
        info={"company":[],"role":[],"location":[],"stipend":[],"duration":[],"link":[]}
        dfm=pd.DataFrame(info)
        for i in range(1,int(get_pageno())+1):
            if not get_info(i).empty:
                    dfm=pd.concat([dfm,get_info(i)],ignore_index=True)
                    time.sleep(1)
        print(dfm)
        dfm.to_excel("internships.xlsx")
    else:
        print("no result found")
        
        

if __name__=="__main__":
    main()
    


