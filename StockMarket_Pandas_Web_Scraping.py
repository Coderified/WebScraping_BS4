import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import re





def NSE_PriceList(stock_name):
    
    url="https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol="+str(stock_name)
    
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'}
    
    response=requests.get(url,headers=headers)
    
    soup=BeautifulSoup(response.text,features="html.parser")
    
    data = soup.find(id='responseDiv').getText().strip().split(":")
    
    for items in data:
        if 'lastPrice' in items:
            ind=data.index(items)+1
            latpri=data[ind].split('"')[1]
            lp=float(latpri.replace(',',''))
        
        elif 'open' in items:
            ind=data.index(items)+1
            openpri=data[ind].split('"')[1]
            op=float(openpri.replace(',',''))
        
        elif 'high52' in items:
            ind=data.index(items)+1
            yearlyhigh=data[ind].split('"')[1]
            yh=float(yearlyhigh.replace(',',''))
            
        elif 'low52' in items:
            ind=data.index(items)+1
            yearlylow=data[ind].split('"')[1]
            yl=float(yearlylow.replace(',',''))
        
        elif 'previousClose' in items:
            ind=data.index(items)+1
            prevclose=data[ind].split('"')[1]
            pc=float(prevclose.replace(',',''))
        
        elif 'dayHigh' in items:
            ind=data.index(items)+1
            dayhigh=data[ind].split('"')[1]
            dh=float(dayhigh.replace(',',''))
        
        elif 'dayLow' in items:
            ind=data.index(items)+1
            daylow=data[ind].split('"')[1]
            dl=float(daylow.replace(',',''))
            
        elif 'totalTradedVolume' in items:
            ind=data.index(items)+1
            tottradvol=data[ind].split('"')[1]
            ttv=float(tottradvol.replace(',',''))
    
    return lp, op, yh, yl, pc, dh, dl, ttv


nifty_50_url='https://www1.nseindia.com/content/indices/ind_nifty50list.csv'

df_n50=pd.read_csv(nifty_50_url)


LP=[]
OP=[]
YH=[]
YL=[]
PC=[]
DH=[]
DL=[]
TTV=[]

for index,row in df_n50.iterrows():
    stock_key=row['Symbol']
    
    if re.compile("&").search(stock_key)!=None:
        stock_key = stock_key.replace("&","%26")
        
    lastpri, openpri, yearh, yearl, prevclo, dailyh, dailyl, totradvol = NSE_PriceList(stock_key)
    
    OP.append(str(openpri))
    LP.append(str(lastpri))
    YH.append(str(yearh))
    YL.append(str(yearl))
    PC.append(str(prevclo))
    DH.append(str(dailyh))
    DL.append(str(dailyl))
    TTV.append(str(totradvol))

dd=pd.DataFrame(columns=['Company Name','Symbol','Open Price','Last Price','Yearly High','Yearly Low','Previous Close','Day High','Day Low','Total Traded Volume'])


for index,row in df_n50.iterrows():
    stock_key=row['Symbol']
    
    dd=dd.append({'Company Name':str(row['Company Name']),'Symbol':row['Symbol'],'Open Price':OP[index],'Last Price':LP[index],'Yearly High':YH[index],'Yearly Low':YL[index],'Previous Close':PC[index],'Day High':DH[index],'Day Low':DL[index],'Total Traded Volume':TTV[index]},ignore_index=True)

date=datetime.date.today()
date=str(date)
dd.to_excel(r'E:\oldBackups\Projects & Courses\nifty_data'+date+'.xlsx', index = False)

#Email to the recipients
    

# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication



# subject=" NIFTY_50 Stats"
# body =" NIFTY 50 data scraped from NSE "
# sender = 'bharath2396@gmail.com'
# reciever = 'bharath2396@gmail.com'
# pwd=input("Please type in your Password and Hit Enter : ")

# message=MIMEMultipart()
# message["From"]=sender
# message["To"]=reciever
# message["Subject"]=subject
# message["Bcc"]=reciever

# message.attach(MIMEText(body))

# file='nifty_data.xlsx'

# with open(file,"rb") as attachment:
#     part=MIMEBase("application","vnd.ms-excel")
#     part.set_payload(attachment.read())
    
# encoders.encode_base64(part)

# part.add_header(
#     "Content-Disposition",
#     f"attachment; filename= {file}",
# )

# message.attach(part)

# # s = smtplib.SMTP('localhost')
# # s.sendmail(sender, reciever, message.as_string())
# # s.quit()


# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#      smtp.ehlo()
#      smtp.starttls()
#      smtp.login(sender, pwd)
#      smtp.send_message(message)
#      smtp.quit()

# smtp = smtplib.SMTP(server, port)
# if isTls:
#     smtp.starttls()
# smtp.login(username,password)
# smtp.sendmail(send_from, send_to, msg.as_string())
# smtp.quit()
