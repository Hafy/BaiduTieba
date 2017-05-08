#encoding:utf-8
import sys   
reload(sys)  
import requests
from bs4 import BeautifulSoup
import re
import os
sys.setdefaultencoding('utf8')
#修改系统默认编码格式 
class BDTB:
    def __init__(self,baseurl,see_lz):
        self.baseurl=baseurl
        self.see_lz='?see_lz='+str(see_lz)
    def get_Page(self,pageNum): #获取得到某个页面的response
        try:
            url=self.baseurl+self.see_lz+'&pn='+str(pageNum)
            resp=requests.get(url)
            self.soup=BeautifulSoup(resp.text,'html')
        except requests.exception.RequestsException,msg:
            print '错误原因:'.msg
            
    def get_Title(self):
        self.title=self.soup.find('h3', class_='core_title_txt').text
        
    def get_reply_num(self):
        #re_soup=self.get_Page(1)
        self.pages=self.soup.find('li',class_='l_reply_num').find_all('span')[1].text #总共页数
        self.reply_items=self.soup.find('li',class_='l_reply_num').find_all('span')[0].text #总回复数
        #print self.pages,self.reply_items
        
    def get_id_content(self):               #获取层主ID 和层主发布的正文内容
        #id_soup=self.get_Page(1)
        id_list=self.soup.find_all('li',class_='d_name')
        content_list=self.soup.find_all(id=re.compile("post_content_.*?")) #搜索id=post_content_
        id_list=zip(id_list,content_list)
        fd=open(self.title+'.txt','wa')  #打开文件
        for iclist in id_list:
                contents= '-'*50+'\n'+'层主ID：' +iclist[0].text+'\n'+'回复内容:'+'\n'+iclist[1].text+'\n'
                fd.write(contents)
        fd.close()
    def entrance(self):
        self.get_Page(1)  #获取soup  
        self.get_Title() #获取帖子标题 title
        self.get_reply_num()
        print '帖子标题是:%s'%self.title
        print '帖子总共页数:%s'%self.pages
        print '正在写入第1页内容...\n'
        self.get_id_content()
        for page in range(2,int(self.pages)+1):
            print '正在写入第%s页内容...\n' % page
            self.get_Page(page)
            self.get_id_content()
            
            
        print "帖子内容已写完"
        
         

        
baseurl=raw_input('请输入你要获取的帖子的URL...')
issee_lz=raw_input('是否只看楼主..\n 1:是\t0:不是')
bdtb=BDTB(baseurl,issee_lz)
bdtb.entrance()
