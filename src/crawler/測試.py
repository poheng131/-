import requests
import time
import random
import pandas as pd
from datetime import datetime 
import os  
import ast

#先F12開啟開發者模式，確認參數
keywords="數據分析"
page=1

url="https://www.104.com.tw/jobs/search/api/jobs"

params={
    "jobsource":"m_joblist_search",
    "keyword":keywords,
    "mode":"s",
    "order":15,
    "page":page,
    "pagesize":20,
}

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer":"https://www.104.com.tw/",
}


# ✅ 白名單：只保留這些職缺名稱關鍵字的職缺
WHITELIST_KEYWORDS = [
    "數據分析", "資料分析", "data analyst", "data analysis", 
    "data analytic", "資料科學", "data scientist",
    "資料工程", "data engineer", "商業分析", "bi", 
    "bi工程師", "bi analyst", "powerbi", "business intelligence",
    "business analyst", "machine learning", "AI分析"
]

# ❌ 黑名單：排除這些明顯不相關的職缺
EXCLUDE_WORDS = ["助理", "客服", "門市", "儲備幹部", "工讀", "講師", "作業員", "行政", "業務", "外包", "設計"]

def is_relevant_job(title):
    title=title.lower()
    return any(good in title for good in WHITELIST_KEYWORDS) and not any(bad in title for bad in EXCLUDE_WORDS)

#---第二層爬蟲---所需參數與函數
detail_headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Referer":"", #先留空
    "X-Requested-With": "XMLHttpRequest",
}
def fetch_job_detail(first_layer_data):
    link_data = first_layer_data["link"]
    print(f"Link data: {link_data}")  # 確認link_data的原始格式

    # 如果 link_data 已經是字典格式，直接使用它；如果是字串，則解析它
    if isinstance(link_data, str):
        try:
            link_data = ast.literal_eval(link_data)
        except Exception as e:
            print(f"解析連結資料錯誤: {e}")
            return None
    
    job_url = link_data["job"]
    job_no = job_url.strip("/").split("/")[-1]
    detail_url = f"https://www.104.com.tw/job/ajax/content/{job_no}"

    detail_headers_current = detail_headers.copy()
    detail_headers_current["Referer"] = link_data["job"]

    try:
        response = requests.get(url=detail_url, headers=detail_headers_current, timeout=15)
        response.raise_for_status()  # 如果status不是200，會拋出HTTPError
        detail_data = response.json()
        print(f"Returned detail_data: {detail_data}")  # 打印返回的資料，看看它的結構

        if isinstance(detail_data["data"], list):  # 檢查是否是列表
            print("Returned 'data' is a list, processing first item...")
            return detail_data["data"][0]  # 如果是列表，取第一個項目
        elif isinstance(detail_data["data"], dict):  # 如果是字典
            return detail_data["data"]
        else:
            print("Unexpected structure of 'data' field")
            return None
    except requests.exceptions.RequestException as e:
        print(f"請求錯誤: {e}")
        print(f"回應內容: {response.text}")  # 打印出回應的原始文本
        return None
    except ValueError as e:
        print(f"解析JSON錯誤: {e}")
        print(f"回應內容: {response.text}")  # 打印出回應的原始文本
        return None



#開始請求回傳資料

all_data=[]  #將蒐集的資料存在這個空list當中
max_page=10
while page <= max_page:
    try:
        params["page"]=page
        print(f"🔍 抓取「{keywords}」第 {page} 頁")
        response=requests.get(url=url,params=params,headers=headers)
        print(response.text)
        data=response.json()
        filter_jobs=[job for job in data["data"] if is_relevant_job(job["jobName"])] 
        detail_data_all=[]
        for job_item in filter_jobs:
            detail_info = fetch_job_detail(job_item) # 獲取單一職位的詳細資料
            if detail_info:
                merged_record = {**job_item, **detail_info} # 將兩個字典合併
                all_data.append(merged_record) # 加入總列表
            else:
                all_data.append(job_item) # 若無詳細資料，則只加入第一層數據
        time.sleep(random.uniform(1.5,3.5)) #模擬人操作，隨機時間間隔換頁
        page+=1
    except Exception as e:
        print(e)
        print("錯誤，解析json失敗!!")
        break

#將回傳內容儲存成檔案
df=pd.DataFrame(all_data)  
today=datetime.today().strftime("%Y-%m-%d")
filename=f"104_rawdata_{today}.csv"
folder=r"C:\Users\FM_pc\Desktop\jobs_analysis_project\data"
os.makedirs(folder,exist_ok=True)  #確保資料夾存在，無則建立
df.to_csv(os.path.join(folder,filename),index=False,encoding="utf-8-sig",quoting=1)
print(f"爬蟲完成，儲存成{filename}")
