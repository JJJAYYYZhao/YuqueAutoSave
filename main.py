import requests
import wget
from tqdm import tqdm
import os
if __name__ == '__main__':
    baseUrl = "https://www.yuque.com/api"
    knowledgeBaseUrl = baseUrl + "/mine/personal_books"


    headers = {
        "Cookie": "_yuque_session=GjmDSBKgdOqFpJrwqFMTeVx0lUWVjytlOs0Ih300v7JTAuIoMUvPRFBek13m3bCaPoYMX4KvoRJCFcKKl1Rukg==; _uab_collina=170960582359858110786178; tfstk=eRn2ns1j_nK2l0WIuzqa8lz1NfZYjkdB0cN_IADghSVcci1izxMUhZ9xI5lZN7E_Gmgj7tnrTGsXMEHGblZMOBtBAxHbXlAB0PzBGxh_w9-XAHMxn8-zHItBHsPO_MrsKTTeuzOnp7mSf8I6AIzbaGjFp-4DOYb1AMib3roin7kq30y4uWjz_1elffntu1bao8ezOLJrzzY89wKioSQOWzqLUW9bhNQTo82zOKUFWNUuU8PBhGf..; yuque_ctoken=-LxSLkr_xMTNf6mzxm3nOQbU;",
        "X-Csrf-Token": "-LxSLkr_xMTNf6mzxm3nOQbU"}
    knowledgeBaseData = requests.get(knowledgeBaseUrl, headers=headers).json()['data']

    problem_doc_list=[]

    for item in tqdm(knowledgeBaseData):
        knowledgeBaseId = item['id']
        knowledgeBaseName = item['name']

        docUrl = baseUrl + "/docs/?book_id=" + str(knowledgeBaseId)
        docData = requests.get(docUrl, headers=headers).json()['data']

        # "options": "{\"latexType\": 2,\"enableAnchor\": 0,\"enableBreak\": 0}"
        # latexType：1、导出LaTeX公式图片2、导出LaTeX公式为Markdown语法
        # enableAnchor：导出保持语雀的锚点
        # enableBreak：导出保持语雀的换行
        setting = {
            "type": "markdown",
            "force": 0,
            "options": "{\"latexType\":2}"
        }
        for doc in tqdm(docData):
            if not os.path.exists(knowledgeBaseName):
                os.makedirs(knowledgeBaseName)
            docId = doc['id']
            exportURL = baseUrl + "/docs/" + str(docId) + "/export"
            exportResponse = requests.post(exportURL, headers=headers, json=setting)
            if exportResponse.status_code!=200:
                problem_doc_list.append(f"{knowledgeBaseName}:{doc['title']}")
                continue
            downloadUrl = exportResponse.json()['data']['url']
            with open(f"output/{knowledgeBaseName}/{'_'.join(doc['title'].replace(':',' ').split())}.md", 'w',encoding='utf-8') as f:
                f.write(requests.get(downloadUrl,headers=headers).text)

    print("======以下文档存在问题，请亲自查看======")
    for i in problem_doc_list:
        print(i)