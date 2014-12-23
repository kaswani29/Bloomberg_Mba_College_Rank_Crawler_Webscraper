#20th Dec'2014
#Note: 1> This should not be used for commercial purpose
#      2> The website might have some restrictions for crawling, read it and adhere to it.

#importing urllib, beautifulsoup and csv
import urllib 
from bs4 import BeautifulSoup
import csv

count =0 
#creating a file
with open('grad_mba_rank.csv','wb') as f1:
    writer=csv.writer(f1, delimiter=',', lineterminator = '\n')
    #Header Row
    writer.writerow(["University","College","Avg_Gmat", "Yield", "Selectivity", "Job_Offers", "Average_Salary", "Top_Industry","Workex","Workex_minmax", "Program_Cost", "Living", "No_Full_Sch" ,"Average_Sch", "Avg_sch_student%","Interntl_Stdnt","Feml_Stdnt" "Link" ])
    #Starting Url to grab all the links
    htmltext = urllib.urlopen("http://www.businessweek.com/bschools/rankings").read()
    soup = BeautifulSoup(htmltext)
    
    #To get a better readability
    print(soup.prettify())

    # Crawling all the college links and names from starting page
    g_data = soup.find_all("td", {"class":"school"})
    for item in g_data:
        count = count + 1
        #Using tag "a" and data-category class to extract information
        link = item.find_all('a', {"data-category":"Business School Rankings"})
        #Extracting link for each college for more information
        full_link = [x.get("href") for x in link]
        #College Name- from tag span and class businees_school_name
        college = item.find('span', {"class":"business_school_name"}).text.strip()
        #University Name- tag span and class school_name
        university = item.find('span', {"class":"school_name"}).text.strip()
        #print   college, university,full_link[0]
    
    # For each college link, again parse html page
        htmltext1 = urllib.urlopen(full_link[0]).read()
        soup1 = BeautifulSoup(htmltext1)
        
    #Build a dictionary for table 1 as the number details keep changing for each collge
    #Check "row =" line to understand use of dictionary
        
        stat = {}
        #detail is the value
        detail = soup1.find_all('span', {"class":"detail"} )
        #label is the name of category
        label = soup1.find_all('div', {"class":"label"} )
        for i in xrange(len(detail)):
            stat [label[i-1].text] =  detail[i-1].text
           
         # Post Grad Work     
        try:  # Similarly using the appropriate class to get work ex
            for feature in soup1.find_all('div', {"class":"list_feature alpha"}):
                workex = feature.em.text #Using em tag after the above condition, then extracting text
                #using first element from list
                minmax = feature.find_all('em', {"class":"lengthy"})[0].text
                print minmax, workex
        except:
         minmax = "NA"
         workex = "NA"
         
            #Tution Fee
        a = soup1.find_all('div', {"class":"tf_container"})[1]
        try:
            Program_Cost = a.find_all('em')[0].text
        except:
            Program_Cost = "NA"
        try:
            Budget = a.find_all('em')[1].text
        except:
            Budget = "NA"            
        
        try:            
            #Full Tution Scholarship
            for a in soup1.find_all('div', {"class":"middle_align"}):
                No_Ft = a.em.text
                print No_Ft
        except:
            No_Ft = "NA"    
        
            #Scholarship Amount 
        for a in soup1.find_all('td', {"class":"one_sixth last"}):
            try:
                Average_Scholarship = a.em.text
            except:
                Average_Scholarship = "NA"
            try:
                avg_sch_student = a.find('em', {"class":"divider"}).text
            except:
                avg_sch_student = "NA"
           #print Average_Scholarship,avg_sch_student
        # %International Students and %Female Students
        student = soup1.find_all('div', {"class":"topic_module"})
        try:
            int_st = student[4].find('em',{"class":"divider"}).text
        except:
            int_st = "NA"
        try:
            fem = student[4].find_all('td',{"class":"one_sixth"})[1].em.text
        except:
            fem = "NA"
  
         #Making a list of tupules             
        row = [(university),(college),(stat.get("Avg GMAT (Admitted Students)","NA")),(stat.get("Yield","NA")),(stat.get("Selectivity","NA")),(stat.get("Job Offers","NA")),(stat.get("Average Salary","NA")),(stat.get("Top Industry","NA")),(workex),(minmax),(Program_Cost), (Budget), (No_Ft), (Average_Scholarship),(avg_sch_student),(int_st),(fem),( full_link[0]) ]
        print row
        #writing to file
        writer.writerow(row)
        print count
        if count == 85:
            break 
