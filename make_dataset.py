import requests
import json
from datetime import datetime,timedelta
from tqdm import tqdm
import re

def clean(s):
    return re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|\\<.*?>|\\《.*?》|\\（.*?）", "", s)

def dateRange(startDate,endDate):
    dates = []
    date_tmp = datetime.strptime(startDate,"%Y-%m-%d")
    end_date = datetime.strptime(endDate,"%Y-%m-%d")
    while date_tmp <= end_date:
        dates.append(date_tmp.strftime("%Y-%m-%d"))
        date_tmp += timedelta(days=1)
    return dates

def make_dataset(url,dates):
    content = []
    note = []

    for date in tqdm(dates):
        param = {'date':date}
        r = requests.get(url,params=param)
        data = json.loads(r.text)

        if clean(data["content"]) in content:
            pass
        else:
            content.append(clean(data["content"]))
            note.append(clean(data["note"]))


    with open("aciba_en_zh.txt",'a') as f:
        for i, _ in enumerate(content):
            f.write(content[i]+'\t\t'+note[i])
            f.write('\n')

def load_dataset(file):
    EN = []
    CN = []
    with open(file, 'r') as f:
        line = f.readline()
        line = line.strip('\n')
        en, cn= line.split(sep='\t\t')
        EN.append(en)
        CN.append(cn)
    return EN,CN

if __name__ == '__main__':
    url = 'http://open.iciba.com/dsapi/'
    dates = dateRange('2012-01-01', '2019-3-21')
    make_dataset(url,dates)
    EN, CN = load_dataset('aciba_en_zh.txt')
    print(EN[0],CN[0])

