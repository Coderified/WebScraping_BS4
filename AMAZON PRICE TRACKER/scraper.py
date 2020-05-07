import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL="https://www.amazon.in/Apple-iPad-Tablet-Wi-Fi-Space/dp/B07C4YKR3J/ref=sr_1_2?keywords=ipad&qid=1576426272&sr=8-2"

headers={"user_agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

def checkprice():
    page = requests.get(URL, headers=headers)

    soup= BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id ="productTitle").get_text()
    price = soup.find(id ="priceblock_ourprice").get_text()
    price_in_int=int(price[2:8].replace(",",""))
    
    print(price_in_int)
    
    print(title.strip())

    if price_in_int < int(28000) :
        sendmail()

    

def sendmail():
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('bharath2396@gmail.com','lreygrvmpayvulnj')

    subject="Wanna buy it now ??"

    body= " Check the link https://www.amazon.in/Apple-iPad-Tablet-Wi-Fi-Space/dp/B07C4YKR3J/ref=sr_1_2?keywords=ipad&qid=1576 "

    msg=f"Subject:{subject}\n\n\n\n{body}"

    server.sendmail("bharath2396@gmail.com","sathyamohan68@gmail.com",msg)

    server.quit()

checkprice()