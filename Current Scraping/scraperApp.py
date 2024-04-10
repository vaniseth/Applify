#Make sure you run chrome in remote debugging protocol first 
#google-chrome --remote-debugging-port=9222


import time
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask,request
# from datetime import date
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('applify-9f7a9-firebase-adminsdk-xbaza-bfa99362c4.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)
# Date_app=date.today()
Date_app=datetime.datetime.now()
# def scrape_naukri():
#     options = Options()
#     options.add_argument('--headless')
#     driver = webdriver.Chrome(options=options)

def scrape_LinkedIn(jobUrl):

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver=webdriver.Chrome(options=options)
    driver.get(url=jobUrl)
    if(jobUrl.startswith("https://www.linkedin.com/jobs/collections/")): 
        job_title=driver.find_element(By.XPATH,"//h2[@class='t-24 t-bold job-details-jobs-unified-top-card__job-title']")

        company_name=driver.find_element(By.XPATH,"//div[@class='job-details-jobs-unified-top-card__primary-description-without-tagline mb2']//a[@class='app-aware-link ']")
        
        dict={'jobTitle':job_title.text,'companyName': company_name.text, 'date':Date_app, 'uid':1001 }
        return(dict)

    elif(jobUrl.startswith("https://www.linkedin.com/jobs/view/")):
        time.sleep(5)
        job_title=driver.find_element(By.XPATH,"//h1[@class='t-24 t-bold job-details-jobs-unified-top-card__job-title']")

        company_name=driver.find_element(By.XPATH,"//div[@class='job-details-jobs-unified-top-card__primary-description-without-tagline mb2']//a[@class='app-aware-link ']")
        # driver.quit()
        p1=job_title.text
        print(type(p1))
        dict={'jobTitle':job_title.text,'companyName': company_name.text, 'date':Date_app, 'uid':1001 }
        return(dict)
    
# def scrape_LinkedIn(jobUrl):

#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("debuggerAddress", "localhost:9222")
#     driver=webdriver.Chrome(options=options)
#     driver.get(url=jobUrl)
#     if(jobUrl.startswith("https://www.linkedin.com/jobs/collections/")): 
#         job_title=driver.find_element(By.XPATH,"//h2[@class='t-24 t-bold job-details-jobs-unified-top-card__job-title']")

#         company_name=driver.find_element(By.XPATH,"//div[@class='job-details-jobs-unified-top-card__primary-description-without-tagline mb2']//a[@class='app-aware-link ']")
        
#         dict={'jobTitle':job_title.text,'companyName': company_name.text, 'date':Date_app, 'uid':1001 }
#         return(dict)

#     elif(jobUrl.startswith("https://www.linkedin.com/jobs/view/")):
#         time.sleep(5)
#         job_title=driver.find_element(By.XPATH,"//h1[@class='t-24 t-bold job-details-jobs-unified-top-card__job-title']")

#         company_name=driver.find_element(By.XPATH,"//div[@class='job-details-jobs-unified-top-card__primary-description-without-tagline mb2']//a[@class='app-aware-link ']")
#         # driver.quit()
#         p1=job_title.text
#         print(type(p1))
#         dict={'jobTitle':job_title.text,'companyName': company_name.text, 'date':Date_app, 'uid':10001 }
#         return(dict)

def scrape_indeed(jobUrl):

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver=webdriver.Chrome(options=options)
    driver.get(url=jobUrl)
    job_title=driver.find_element(By.XPATH,"//h2[@class='jobsearch-JobInfoHeader-title css-jf6w2g e1tiznh50']")

    company_name=driver.find_element(By.XPATH,"//span[@class='css-1saizt3 e1wnkr790']")
        
    dict={'jobTitle':job_title.text,'companyName': company_name.text, 'date':Date_app, 'uid':10001 }
    return(dict)


@app.route('/scrape', methods=['GET','POST'])
def scrape_job_details():
    data = request.get_json()
    website = data['link']
    # userID=data['uid']
   
    if website.startswith("https://www.linkedin.com"):
        job_details = scrape_LinkedIn(website)
        # return(job_details)
        db.collection("applify01").document(str(job_details["uid"])).set(job_details)
        return {"status":"200 OK"}
        
    elif website.startswith("https://in.indeed.com/"):
        job_details = scrape_indeed(website)
        # return(job_details)
        db.collection("applify01").document(str(job_details["uid"])).set(job_details)
    # else:
    #     return jsonify({'error': 'Invalid website'})
if __name__ == '__main__':
    app.run(debug=True, port=2000)