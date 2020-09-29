import time

from django.test import TestCase

# Create your tests here.
from bs4 import BeautifulSoup
import requests
import csv
mylist = []
import pandas
#
#
def moblie_links( phone_name, count):
    url = "https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=" + phone_name + ""

    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    headers = {'User-Agent': user_agent}

    html_page = requests.get(url, headers=headers)
    html = html_page.text

    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.findAll('div', class_="makers")

    for links in soup:
        links = links.find_all('a')

        print(len(links))
        for link in links:
            count = count - 1
            if count >= 0:
                url = "https://www.gsmarena.com/" + link['href']
                time.sleep(1)
                all_opinions(url)
                print("check")


def all_opinions(url):
        user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        headers = {'User-Agent': user_agent}

        html_page = requests.get(url, headers=headers)
        html = html_page.text
        soup = BeautifulSoup(html, 'html.parser')
        #############        The below code scrap the mobile features        #############
        mobile_image = soup.find_all("div", class_="specs-photo-main")
        mobile_name = soup.find_all("h1", class_="specs-phone-name-title")
        mobile_os = soup.select("span[data-spec=os-hl]")
        mobile_storage = soup.select("span[data-spec=storage-hl]")
        mobile_display1 = soup.select("span[data-spec=displaysize-hl]")
        mobile_display2 = soup.select("div[data-spec=displayres-hl]")
        mobile_camer = soup.find_all("li", class_="help accented help-camera")

        for m_img,m_name, m_os, m_storage, m_display1, m_display2, m_camera in zip(mobile_image,mobile_name,mobile_os, mobile_storage, mobile_display1,mobile_display2, mobile_camer):

            mobile_featuers = {}

            links= m_img.find_all('img')
            for link in links:
                mobile_featuers["Mobile_image"] = link["src"]
            mobile_featuers["Mobile_Name"] = m_name.text
            mobile_featuers["Operating_System"] = m_os.text
            mobile_featuers["Storage"] = m_storage.text
            mobile_featuers["Display"] = m_display1.text + " " + m_display2.text
            camera= m_camera.text
            mobile_featuers["Camera"] = " ".join(camera.split())
            mylist.append(mobile_featuers)
        #############             Scraping mobile featuer code end            #############
moblie_links(phone_name = "oppo", count = 2)
print(mylist)
with open('mobilefeatuer4.csv','w',newline='') as f:
    fieldnames = ["Mobile_image","Mobile_Name","Operating_System","Storage","Display","Camera"]
    thewriter = csv.DictWriter(f,fieldnames=fieldnames)
    thewriter.writeheader()
    for data in mylist:
        print(data)

        m_name=data["Mobile_Name"]
        m_os=data["Operating_System"]
        m_stroage=data["Storage"]
        m_display=data["Display"]
        m_camera=data["Camera"]
        thewriter.writerow(data)






""""""""""
user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
headers = {'User-Agent': user_agent}
url= 'https://www.gsmarena.com/samsung_galaxy_a72-10469.php'
html_page = requests.get(url, headers=headers)
html = html_page.text

soup = BeautifulSoup(html, 'html.parser')
mobile_name = soup.find_all("h1",class_="specs-phone-name-title")
mobile_os = soup.select("span[data-spec=os-hl]")
mobile_storage = soup.select("span[data-spec=storage-hl]")
mobile_display1 = soup.select("span[data-spec=displaysize-hl]")
mobile_display2 = soup.select("div[data-spec=displayres-hl]")
mobile_camer = soup.find_all("li",class_="help accented help-camera")


for m_name,m_os,m_storage,m_display1,m_display2,m_camera in zip(mobile_name,mobile_os,mobile_storage,mobile_display1,mobile_display2,mobile_camer):
    print("Mobile Name = " + m_name.text)
    print("Operating System = "+m_os.text)
    print("Storage = "+m_storage.text)
    print("Display = "+m_display1.text+" "+m_display2.text)
    print("Camera = "+m_camera.text.strip())
"""""