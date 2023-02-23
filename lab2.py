import requests
import json
import boto3
import matplotlib.pyplot as plt


def get_curs_json(valcode="usd"):
    return requests.get(f"https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode={valcode}&json").json()


s3 = boto3.client('s3')


val = "eur"

with open(f"exchange_{val}","w") as file:
    for i in get_curs_json(val):
        file.write(f"{i['exchangedate']},{i['rate']}\n")
    
with open(f"exchange_{val}", "rb") as f:
    s3.upload_fileobj(f, "cloudtechbucket123", f"exchange_{val}")


filename = f'exchange_{val}'

with open('temp', 'wb') as f:
    s3.download_fileobj('cloudtechbucket123', filename, f)
    
data = {}
with open('temp') as file:
    for i in file.read().split("\n"):
        if "," in i:
            data[i.split(",")[0]] = float(i.split(",")[1])


fig, ax = plt.subplots()

ax.bar(data.keys(), data.values())

ax.set_title(val.upper())
ax.set_xlabel('X Axis Label')
ax.set_ylabel('Y Axis Label')

ax.set_ylim([26, None])

plt.savefig(filename+'.png')
with open(filename+'.png', "rb") as f:
    s3.upload_fileobj(f, "cloudtechbucket123", filename+'.png')