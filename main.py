import requests
import wget
from tqdm import tqdm
import os
if __name__ == '__main__':
    baseUrl = "https://www.yuque.com/api"
    knowledgeBaseUrl = baseUrl + "/mine/personal_books"


    headers = {
        "Cookie": "_yuque_session=; _uab_collina=; tfstk=; yuque_ctoken=;",
        "X-Csrf-Token": ""}
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
