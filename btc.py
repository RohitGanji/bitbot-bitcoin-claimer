import requests
import time
import hashlib
from bs4 import BeautifulSoup
import pymongo
from random import randint
from datetime import datetime

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
headers = {
  'User-Agent':
      USER_AGENT,
  'Cookie':
      '_ga=GA1.2.1506161081.1587364019; have_account=1; cookieconsent_dismissed=yes; btc_address=1CZ8AgZy1a8duZt4VRyXMqzzu5ZzfvHKQn; password=eda74144c1a1d46c78e2fcbc5075f3bf5085039f8b943b0e21a0c3cd166aa34a; login_auth=a3c0b9b56029ed43ce4d3c19d39d8849186334008655d9ee5da394428fbb174b; __cfduid=d9762eb8e808d2dc89b9b7a35f971a2c01592649691; last_play=1593077988; csrf_token=n8V5wsQnaqy6; _gid=GA1.2.2052395072.1594307843; hide_push_msg=1; _gat=1'
}
proxies = {}
client = pymongo.MongoClient("mongodb+srv://Rohit:Rohit.2001@cluster0-1g6nx.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client.BTC
csrf_token = 'n8V5wsQnaqy6'
status = True
rv2 = False
rolltime = "0"

def fingerprint():
    md5 = hashlib.md5()
    md5.update(('###'.join([USER_AGENT,
                            'x'.join(['1024', '1280', '24']),'-420','true','true',
                            '::'.join(['BookReader', '', 'application/epub+zip~epub,application/x-fictionbook+xml~fb2,application/x-zip-compressed-fb2~fb2.zip;Chromium PDF Plugin',
                                        'Portable Document Format', 'application/x-google-chrome-pdf~;Chromium PDF Viewer', '', 'application/pdf~pdf;Native Client',
                                        '', 'application/x-nacl~,application/x-pnacl~;Shockwave Flash', 'Shockwave Flash 32.0 r0::application/x-shockwave-flash~swf,application/futuresplash~spl'
                                        ])])).encode('utf-8'))

while True:
    try:
        with requests.Session() as s:
            r = s.get("https://freebitco.in/?op=home", headers = headers, proxies = proxies)
            now = int(datetime.now().timestamp())
            soup = BeautifulSoup(r.content, 'lxml')
        client_seed = soup.find(id='next_client_seed')['value']
        rpb_status = bool(soup.find(id='bonus_container_free_points'))
        fbb_status = bool(soup.find(id='bonus_container_fp_bonus'))
        captcha_status = bool(soup.find(id='play_without_captchas_button'))
        email = soup.find(id="edit_profile_form_email")['value']
        deposit_address = soup.find(id='main_deposit_address')['value']
        with requests.Session() as s:
            cab = s.get('https://freebitco.in/?op=get_current_address_and_balance&csrf_token='+csrf_token, headers = headers)
            withdraw_address = cab.text.split(':')[1]
            BTC = cab.text.split(':')[2]
            slow_fee = cab.text.split(':')[3]
            instant_fee = cab.text.split(':')[4]
        try:
            BONUS = soup.find(id='bonus_account_balance').text.replace(' ','').replace('BTC','')
        except:
            BONUS = 0
        rp = int(soup.find('div', attrs={'class':'reward_table_box br_0_0_5_5 user_reward_points font_bold'}).text.replace(',', ""))
        try:
            rend = int(r.text[r.text.find('title_countdown (')+17:r.text.find(');});</script>')])+3
        except:
            rend = 0
        try:
            p = str(soup.find(id='bonus_container_free_points'))
            rpend = int(p[p.rfind('free_points')+13:p.rfind(')})')])+3
        except:
            rpend = 0
        try:
            q = str(soup.find(id='bonus_container_fp_bonus'))
            fbend = int(q[q.rfind('fp_bonus')+10:q.rfind(')})')])+3
        except:
            fbend = 0
        if float(BTC) > (float(0.0003000) + float(slow_fee)):
            red = True
        else:
            red = False
        if rpb_status == False:
            if rp > 11:
                rpbnos = [1,10,25,50,100]
                for rpn in range(len(rpbnos)):
                    if int(rp/12) >= rpbnos[rpn]:
                        rpbno = rpn
                try:
                    if (rpbnos[rpbno+1]*12)-rp <= 24:
                        rpbno = rpbnos[rpbno+1]
                    else:
                        rpbno = rpbnos[rpbno]     
                except:
                    rpbno = rpbnos[rpbno]
                if rp >= rpbno*12:
                    with requests.Session() as s:
                        rpb = s.get(f'https://freebitco.in/?op=redeem_rewards&id=free_points_{rpbno}&points=&csrf_token={csrf_token}', headers = headers, proxies = proxies)
                        if rpb.text[0] == 's':
                            pass
                        else:
                            rpb = s.get(f'https://freebitco.in/?op=redeem_rewards&id=free_points_10&points=&csrf_token={csrf_token}', headers = headers, proxies = proxies)
        with requests.Session() as s:
            r = s.get("https://freebitco.in/?op=home", headers = headers, proxies = proxies)
            rp = int(soup.find('div', attrs={'class':'reward_table_box br_0_0_5_5 user_reward_points font_bold'}).text.replace(',', ""))
            soup = BeautifulSoup(r.content, 'lxml')
            rpb_status = bool(soup.find(id='bonus_container_free_points'))
            fbb_status = bool(soup.find(id='bonus_container_fp_bonus'))
#        if fbb_status == False:
#            if rpb_status:
#                if (rp-3200)+(int((rpend%(24*3600))/3600)*104)>1199:
#                        with requests.Session() as s:
#                            fbb = s.get(f'https://freebitco.in/?op=redeem_rewards&id=fp_bonus_1000&points=&csrf_token={csrf_token}', headers = headers, proxies = proxies)
        db.three.update_many({"_id":1},
        { "$set": {
            "BTC":float(BTC),
            "BONUS": float(BONUS), 
            "RP":rp,
            "RPB": rpb_status,
            "FBB": fbb_status,
            "RED": red,
            "RV2": rv2,
            "SLOW": float(slow_fee),
            "INSTANT": float(instant_fee),
            "STATUS": status,
            "DEPOSIT": deposit_address,
            "WITHDRAW": withdraw_address,
            "EMAIL": email,
            "NROLL": now+rend,
            "NRPB": now+rpend,
            "NFBB": now+fbend },} )
        time.sleep(rend)
        with requests.Session() as s:
            data = {'csrf_token': csrf_token, 'op': 'free_play', 'fingerprint': fingerprint(), 'client_seed': client_seed, 'fingerprint2': randint(1000000000,9999999999), 'pwc': '0', 'd5c2233cd15f': '1594322467:ed5b7da67d20be0ff3925e62e818f5557208bf00d1e1c8c6f770e9f9b29df50c', 'f53d8b816e9d': hashlib.sha256(s.get(f'https://freebitco.in/cgi-bin/fp_check.pl?s=f53d8b816e9d&csrf_token={csrf_token}', headers={'x-csrf-token': csrf_token, 'X-Requested-With': 'XMLHttpRequest'}).text.encode('utf-8')).hexdigest()}
            roll = requests.post('https://www.freebitco.in/', data = data, headers = headers, proxies = proxies)
        rolltime = int(datetime.now().timestamp())
        db.three.update_one({"_id":1},
        { "$set": {
            "TIME":rolltime}})
        if roll.text[0] == 's':
            print(datetime.fromtimestamp(rolltime).strftime('[%d] %H:%M:%S')+' --- Roll Played')
            status = True
            rv2 = False
        else:
            print(datetime.fromtimestamp(rolltime).strftime('[%d] %H:%M:%S')+'--- Roll Not Played')
            rv2 = True
    except:
        pass
        time.sleep(60)
