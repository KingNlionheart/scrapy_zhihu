import scrapy
from datetime import datetime
import json

class zhihuTestSpider(scrapy.Spider):
    
    name = 'zhihu_test'
    
    custom_settings = {'LOG_LEVEL': 'ERROR',}
    
    start_urls = ['https://httpbin.org/get?show_env=1']
    
    def __init__(self, question_id=405043851, *args, **kwargs):
        super(zhihuTestSpider, self).__init__(*args, **kwargs)
#         self.start_urls = ['http://193.112.32.22:5010/get',]

        self.answers_limit = 20
        self.answers_offset = 0
        self.answers_url_open = "https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bsettings.table_of_content.enabled%3B&limit={1}&offset={2}&platform=desktop&sort_by=default"
        self.answers_url_collapsed = "https://www.zhihu.com/api/v4/questions/{0}/collapsed-answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bsettings.table_of_content.enabled%3B&limit={1}&offset={2}&sort_by=defaul"

        self.comments_limit = 20
        self.comments_offset = 0
        self.comments_url_open = "https://www.zhihu.com/api/v4/answers/{0}/comments?limit={1}&offset={2}&order=reverse&status=open"
        self.comments_url_collapsed = "https://www.zhihu.com/api/v4/answers/{0}/comments?limit={1}&offset={2}&order=reverse&status=collapsed"

        self.start_urls = ['https://www.zhihu.com/api/v4/questions/{0}'.format(question_id),]


    def parse(self, response):
        response_json = response.json()
        # dict_keys(['type', 'id', 'title', 'question_type', 'created', 'updated_time', 'url', 'relationship'])
        #
        # with open('question_id.json','w')as f:
        #     f.write(json.dumps(response_json,indent=4,ensure_ascii=False))
        #
        # print(response_json.keys())

        # print(json.dumps(response_json,indent=4,ensure_ascii=False))
        # print(response_json['origin'])

        yield scrapy.Request(self.answers_url_open.format(response_json['id'], self.answers_limit, self.answers_offset),callback=self.parse_answers)
        yield scrapy.Request(self.answers_url_collapsed.format(response_json['id'], self.answers_limit, self.answers_offset),callback=self.parse_answers)


    def parse_answers(self,response):
        response_json = response.json()
        # dict_keys(
        #     ['id', 'type', 'answer_type', 'question', 'author', 'url', 'is_collapsed', 'created_time', 'updated_time',
        #      'extras', 'is_copyable', 'is_normal', 'voteup_count', 'comment_count', 'is_sticky', 'admin_closed_comment',
        #      'comment_permission', 'can_comment', 'reshipment_settings', 'content', 'editable_content', 'excerpt',
        #      'collapsed_by', 'collapse_reason', 'annotation_action', 'mark_infos', 'relevant_info', 'suggest_edit',
        #      'is_labeled', 'reward_info', 'relationship', 'ad_answer'])
        #
        # if len(response_json['data'])>0:
        #     with open('answers.json','w')as f:
        #         f.write(json.dumps(response_json['data'][0],indent=4,ensure_ascii=False))

        for i in response_json['data']:
            print('|'+'-'*15,i['excerpt'])
            # print(i.keys())
            if i['comment_count']>0:
                yield scrapy.Request(self.comments_url_open.format(i['id'],self.comments_limit,self.comments_offset),callback=self.parse_comments)
                yield scrapy.Request(self.comments_url_collapsed.format(i['id'],self.comments_limit,self.comments_offset),callback=self.parse_comments)

        if response_json['paging']['is_end'] != True :
            yield scrapy.Request(response_json['paging']['next'],callback=self.parse_answers)
    
    def parse_comments(self,response):
        response_json = response.json()
        # dict_keys(
        #     ['id', 'type', 'url', 'content', 'featured', 'top', 'collapsed', 'is_author', 'is_delete', 'created_time',
        #      'resource_type', 'reviewing', 'allow_like', 'allow_delete', 'allow_reply', 'allow_vote', 'can_recommend',
        #      'can_collapse', 'attached_info', 'author', 'is_parent_author', 'vote_count', 'voting', 'liked',
        #      'disliked'])
        #
        # if len(response_json['data'])>0:
        #     with open('comment.json','w')as f:
        #         f.write(json.dumps(response_json['data'][0],indent=4,ensure_ascii=False))

        for i in response_json['data']:
            print('|'+'-'*30,i['content'])
            # print(i.keys())
        if response_json['paging']['is_end'] != True :
            yield scrapy.Request(response_json['paging']['next'],callback=self.parse_comments)