import requests
import time
import json

headers = {'accept-language': 'zh-CN,zh;q=0.9',
            'Host': 'www.zhihu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
            }

def get_all_comments(answers_id = 15108995 ,limit = 20,offset=0):
#     s=requests.Session()
    comments=[]
    comments_url_open = "https://www.zhihu.com/api/v4/answers/{0}/comments?limit={1}&offset={2}&order=reverse&status=open"
    comments_url_collapsed = "https://www.zhihu.com/api/v4/answers/{0}/comments?limit={1}&offset={2}&order=reverse&status=collapsed"
    comments_totals=0
    comments_get=0
    start_time=time.time()

    url=comments_url_open.format(answers_id,limit,offset)
    while(True):
        comments_response = requests.get(url=url,headers=headers,)#verify=False)
        comments_response_json=comments_response.json()
        
        comments.extend(comments_response_json['data'])
        url=comments_response_json['paging']['next']
        comments_totals=comments_response_json['paging']['totals']
        comments_get+=len(comments_response_json['data'])
        
        if comments_response_json['paging']['is_end'] or comments_totals == 0 or len(comments_response_json['data']) == 0:
            print("|  |----comments:open      answers_id:{0},总共:{1},耗时:{2}s".format(answers_id,comments_totals,time.time()-start_time))
            break
        print("|  |----comments:open      总共:{0},进度:{1}%,已耗时:{2}s".format(comments_totals,round((comments_get) * 100 / comments_totals),time.time()-start_time), end="\r")
        time.sleep(1)
    
    comments_totals=0
    comments_get=0
    start_time=time.time()
    
    url=comments_url_collapsed.format(answers_id,limit,offset)
    while(True):
        comments_response = requests.get(url=url,headers=headers,)#verify=False)
        comments_response_json=comments_response.json()
        
        comments.extend(comments_response_json['data'])
        url=comments_response_json['paging']['next']
        comments_totals=comments_response_json['paging']['totals']
        comments_get+=len(comments_response_json['data'])
        
        if comments_response_json['paging']['is_end'] or comments_totals == 0 or len(comments_response_json['data']) == 0:
            print("|  |----comments:collapsed answers_id:{0},总共:{1},耗时:{2}s".format(answers_id,comments_totals,time.time()-start_time))
            break
        print("|  |----comments:collapsed 总共:{0},进度:{1}%，已耗时:{2}s".format(comments_totals,round((comments_get) * 100 / comments_totals),time.time()-start_time), end="\r")
        time.sleep(1)
        
    return comments

def get_all_answers(question_id = 20427672 ,limit = 20,offset=0):
#     s=requests.Session()
    answers=[]
    answers_url_open = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bsettings.table_of_content.enabled%3B&limit={1}&offset={2}&platform=desktop&sort_by=default"
    answers_url_collapsed = "https://www.zhihu.com/api/v4/questions/{0}/collapsed-answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bsettings.table_of_content.enabled%3B&limit={1}&offset={2}&sort_by=defaul"
    answers_totals=0
    answers_get=0
    start_time=time.time()
    
    url=answers_url_open.format(question_id,limit,offset)
    while(True):
        answers_response = requests.get(url=url,headers=headers,)#verify=False)
        answers_response_json=answers_response.json()
        
        for answer in answers_response_json['data']:
            answer['comments'] = get_all_comments(answer['id'])
        answers.extend(answers_response_json['data'])
        
        url=answers_response_json['paging']['next']
        answers_totals=answers_response_json['paging']['totals']
        answers_get+=len(answers_response_json['data'])
        
        if answers_response_json['paging']['is_end'] or answers_totals==0 or len(answers_response_json['data'])==0:
            print("|--answers:open      question_id:{0},总共:{1},耗时:{2}s".format(question_id,answers_totals,time.time()-start_time))
            break
        print("|--answers:open      总共:{0},进度:{1}%，已耗时:{2}s".format(answers_totals,round((answers_get) * 100 / answers_totals),time.time()-start_time), end="\r")
        time.sleep(1)

    answers_totals=0
    answers_get=0
    start_time=time.time()
        
    url=answers_url_collapsed.format(question_id,limit,offset)
    while(True):
        answers_response = requests.get(url=url,headers=headers,)#verify=False)
        answers_response_json=answers_response.json()
        
        for answer in answers_response_json['data']:
            answer['comments'] = get_all_comments(answer['id'])
        answers.extend(answers_response_json['data'])
        
        url=answers_response_json['paging']['next']
        answers_totals=answers_response_json['paging']['totals']
        answers_get+=len(answers_response_json['data'])
        
        if answers_response_json['paging']['is_end'] or answers_totals==0 or len(answers_response_json['data'])==0:
            print("|--answers:collapsed question_id:{0},总共:{1},耗时:{2}s".format(question_id,answers_totals,time.time()-start_time))
            break
        print("|--answers:collapsed 总共:{0},进度:{1}%，已耗时:{2}s".format(answers_totals,round((answers_get) * 100 / answers_totals),time.time()-start_time), end="\r")
        time.sleep(1)
    
    return answers
if __name__ == "__main__":
    question_id = 20427672 #修改此 id 爬取不同答案20427672
#     question_id = 405043851 
    answers = get_all_answers(question_id)
    with open(str(question_id)+'.json','w') as f:
        json.dump(answers,f)
    