import sys
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
import re
#2748
#3143 (+1)

payload = {'from':'/bbs/Beauty/M.1514740613.A.FF1.html',
		   'yes': 'yes'
		  }
rs = requests.session()
res = rs.post("https://www.ptt.cc/ask/over18", data=payload)


def crawl():
	begin=2740
	end=3146
	alittlerange=50
	soup_list=[]


	f = open("all_articles.txt", "w",encoding="utf-8")
	popular_f = open("all_popular.txt", "w",encoding="utf-8")


	url_Beauty = "https://www.ptt.cc/bbs/Beauty/"
	for crawling in range(begin,end+1):
		
		#使用soup的一些東西
		url = url_Beauty+'index'+str(crawling)+'.html'
		res = rs.get(url)
		content = res.text
		soup = BeautifulSoup(content,'html.parser')
		soup_list.append(soup)
		
		
		#結束的flag
		finish=False
		
		
		for individual in soup.find_all(class_="r-ent"):
			#文章沒有被刪除的話
			num=individual.find_all(class_="nrec")[0].string
			#確認文章不是公告
			ind_title=individual.find_all(class_="title")[0].find_all("a")[0].string
			if ind_title.find('[公告]')==-1:
				
				#設定日期
				date=individual.find_all(class_="date")[0].string
				#確定是2019的1月1號，如果是2020的1月1號就結束
				if date == ' 1/01':
					if crawling>(end-alittlerange):
						finish=True
						break
				
				if date[0]==' ':
					dt = datetime.strptime(date, " %m/%d")
				else:
					dt = datetime.strptime(date, "%m/%d")
				if dt.month>=11 and crawling<begin+alittlerange:
					continue
					
					
				
				#找網址及印出
				ind_url=individual.find_all(class_="title")[0].find_all("a")[0].get('href')
				print_string=str(dt.month)
				if dt.day<10 :  
					print_string+='0'
				print_string+=str(dt.day)+","+ind_title+","+'https://www.ptt.cc'+ind_url
				print(print_string)
				f.write(print_string+'\n')
				
				if num == '爆':
					popular_f.write(print_string+'\n')
						
		if finish:
			break
		time.sleep(0.1)
	f.close()
	popular_f.close()

def push(ssday,eeday):	
	f = open("all_articles.txt", "r",encoding="utf-8")
	Lines = f.readlines() 
	count = 0
	# Strips the newline character 
	for line in Lines: 
		x = re.split(",", line, 1)
		print(x[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")
		print(url_post)








	push_user_list=[]
	push_number_list=[]

	boo_user_list=[]
	boo_number_list=[]

	all_push=0
	all_boo=0
	finish_find=False

	start_find_date=int(ssday)
	end_date=int(eeday)
	for line in Lines: 
		nows_date = int(re.split(",", line, 1)[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")

		
		if nows_date>=start_find_date and nows_date<=end_date:


			#開始爬文章
			print(nows_date)
			print(url_post) 
			res_post = rs.get(url_post)
			content_post = res_post.text
			soup_post = BeautifulSoup(content_post,'html.parser')

			#沒發信站不算
			fffffffa_mail=''
			for div in soup_post.find_all("span", {'class':'f2'}): 
				fffffffa_mail+=str(div.string)
			if fffffffa_mail.find('發信站')==-1:
				continue					
			
			
			
			for individual_post in soup_post.find_all(class_="push"):
				reply=individual_post.find_all(class_="push-tag")[0].string
				user=individual_post.find_all(class_="push-userid")[0].string

				if reply=='推 ':
					all_push+=1
					print('推',end='')
					print(user)

					try:
						push_number_list[push_user_list.index(user)]-=1

					except ValueError:
						push_user_list.append(user)
						push_number_list.append(-1)
				if reply=='噓 ':
					all_boo+=1
					print('噓',end='')
					print(user)

					try:
						boo_number_list[boo_user_list.index(user)]-=1

					except ValueError:
						boo_user_list.append(user)
						boo_number_list.append(-1)
			
			time.sleep(0.1)
	print(len(push_user_list))
	print(len(push_number_list))
	print(len(boo_user_list))
	print(len(boo_number_list))	
	push_number_list, push_user_list = zip(*sorted(zip(push_number_list, push_user_list)))
	boo_number_list, boo_user_list = zip(*sorted(zip(boo_number_list, boo_user_list)))




	push_f = open("push ["+str(start_find_date)+"-"+str(end_date)+"].txt", "w",encoding="utf-8")


	print('all like:',all_push)
	push_f.write('all like: '+str(all_push)+'\n')
	print('all boo:',all_boo)
	push_f.write('all boo: '+str(all_boo)+'\n')
	for i in range (0,10):
		like_string='like #'+str(i+1)+': '+push_user_list[i]+' '+str(-push_number_list[i])
		print(like_string)
		push_f.write(like_string+'\n')
	for i in range (0,10):
		boo_string='boo #'+str(i+1)+': '+boo_user_list[i]+' '+str(-boo_number_list[i])
		print(boo_string)
		push_f.write(boo_string+'\n')
	push_f.close()

def popular(ssday,eeday):
	f = open("all_popular.txt", "r",encoding="utf-8")
	Lines = f.readlines() 
	count = 0
	# Strips the newline character 
	for line in Lines: 
		x = re.split(",", line, 1)
		print(x[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")
		print(url_post)










	import os
	boom_number=0
	picture_list=[]

	finish_find=False
	start_find_date=int(ssday)
	end_date=int(eeday)
	url_Beauty = "https://www.ptt.cc/bbs/Beauty/"


	for line in Lines: 
		nows_date = int(re.split(",", line, 1)[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")

		
		if nows_date>=start_find_date and nows_date<=end_date:


			#開始爬文章
			print(nows_date)
			print(url_post) 
			res_post = rs.get(url_post)
			content_post = res_post.text
			soup_post = BeautifulSoup(content_post,'html.parser')

			
			#沒發信站不算

			fffffffa_mail=''
			for div in soup_post.find_all("span", {'class':'f2'}): 
				fffffffa_mail+=str(div.string)
			if fffffffa_mail.find('發信站')==-1:
				continue		

			
			for individual_post in soup_post.find_all("a"):
				image_file=individual_post.get('href')
				extension = os.path.splitext(image_file)[1]
				if extension =='.jpg' or extension =='.jpeg' or  extension =='.png' or extension =='.gif' :
					print(image_file)
					picture_list.append(image_file)


			boom_number+=1
			time.sleep(0.1)
			

	Popular_f = open("popular ["+str(start_find_date)+"-"+str(end_date)+"].txt", "w",encoding="utf-8")

	num_art='number of popular articles: '+str(boom_number)
	print(num_art)
	Popular_f.write(num_art+'\n')
	for i in range(0,len(picture_list)):
		print(picture_list[i])
		Popular_f.write(picture_list[i]+'\n')
	Popular_f.close()
def keyword(keykey,ssday,eeday):
	f = open("all_articles.txt", "r",encoding="utf-8")
	Lines = f.readlines() 
	count = 0
	# Strips the newline character 
	for line in Lines: 
		x = re.split(",", line, 1)
		print(x[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")
		print(url_post)
		
		
	picture_list=[]
	import os
	keyword=keykey


	finish_find=False
	start_find_date=int(ssday)
	end_date=int(eeday)
	url_Beauty = "https://www.ptt.cc/bbs/Beauty/"




	for line in Lines: 
		nows_date = int(re.split(",", line, 1)[0])
		url_post=re.search("(?P<url>https?://[^\s]+)", line).group("url")

		
		if nows_date>=start_find_date and nows_date<=end_date:


			#開始爬文章
			print(nows_date)
			print(url_post) 
			res_post = rs.get(url_post)
			content_post = res_post.text
			soup_post = BeautifulSoup(content_post,'html.parser')

			check_true_flag=False
			for individual_post in soup_post.find_all(class_='bbs-screen bbs-content'):
				for div in individual_post.find_all("div", {'class':'push'}): 
					div.decompose()
				
				fffffffa_mail=''
				for div in individual_post.find_all("span", {'class':'f2'}): 
					fffffffa_mail+=str(div.string)
			
				if fffffffa_mail.find('發信站')==-1:
					break
				

				stttr=''
				for divvvv in individual_post.find_all("div", {'class':'article-metaline'}): 
					for tttttt in divvvv.children:
						stttr+=tttttt.string
					divvvv.decompose()
				for divvvv in individual_post.find_all("div", {'class':'article-metaline-right'}): 
					for tttttt in divvvv.children:
						stttr+=tttttt.string
					divvvv.decompose()         
				for divvvv in individual_post.find_all("div", {'class':'richcontent'}): 
					divvvv.decompose()
				for divvvv in individual_post.find_all("div", {'class':'bbs-screen bbs-content'}):
					for tttttt in divvvv.children:
						stttr+=tttttt.string                            
					divvvv.decompose()


				for divvvv in individual_post.find_all("a"): 
					divvvv.decompose()

				stttr+=str(individual_post.contents)
				

				stttr = str(re.split("發信站", stttr, 1)[0])
				find_ing=stttr.find(keyword)
				if find_ing !=None and find_ing!=-1:
					check_true_flag=True





			res_post = rs.get(url_post)
			content_post = res_post.text
			soup_post = BeautifulSoup(content_post,'html.parser')

			if check_true_flag:
				for individual_post in soup_post.find_all("a"):
					#print(individual_post.get('href'))
					image_file=individual_post.get('href')
					extension = os.path.splitext(image_file)[1]
					if extension =='.jpg' or extension =='.jpeg' or  extension =='.png' or extension =='.gif' :
						print(image_file)
						picture_list.append(image_file)

			time.sleep(0.1)
			
	keyword_file = open("keyword("+keyword+')['+str(start_find_date)+"-"+str(end_date)+"].txt", "w",encoding="utf-8")
	for i in range(0,len(picture_list)):
		print(picture_list[i])
		keyword_file.write(picture_list[i]+'\n')
	keyword_file.close()

	

if sys.argv[1]=='crawl':
	crawl()
elif sys.argv[1]=='push':
	push(sys.argv[2],sys.argv[3])
elif sys.argv[1]=='popular':
	popular(sys.argv[2],sys.argv[3])
elif sys.argv[1]=='keyword':
	keyword(sys.argv[2],sys.argv[3],sys.argv[4])




'''
print ("This is the name of the script: ", sys.argv[0])
print ("Number of arguments: ", len(sys.argv))
print ("The arguments are: " , str(sys.argv))
'''