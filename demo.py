from pymongo import MongoClient
import urllib.request
import os
import sys
import re


while 1:
	file_place =input("Please input the file dir : ")
	if file_place is "exit":
		sys.exit()
	elif os.path.isfile(file_place)==True:
		f = open(file_place,'r')
		target_url = f.readline()
		f.close()
		break;	


fp = urllib.request.urlopen(target_url)
mybytes = fp.read()
pure_data = mybytes.decode("Big5")
fp.close()

#print(mystr)

deal_data = re.sub("&nbsp;", '', pure_data)
deal_data = re.sub("<!--[\s\S]*?-->", '', deal_data)
deal_data = re.sub("<script[\d\D]*?>[\d\D]*?</script>;", '', deal_data)
deal_data = re.sub("<noscript[\d\D]*?>[\d\D]*?</noscript>;", '', deal_data)

pure_list = re.findall("((<tr>\s*(<td.*>.*<\/td>\s*){2}<\/tr>\s*?){3})", deal_data)

#print(type(pure_list))

client = MongoClient("mongodb://localhost:27017/")
db = client['nctu_bot']
collect = db['school_bulletin']

for tmp in pure_list:
	tmp = re.search("<td.*?alt=\"(.*?)\"[\s\S]*?<td.*?href=\"(.*?)\".*?title=\"(.*?)\"[\s\S]*?<td.*?<\/td>[\s\S]*?<td.*?>(.*?)<\/td>[\s\S]*?<td.*?<\/td>[\s\S]*?<td.*?>(.*?)<\/td>",tmp[0])
	if tmp is not None:
		#print(tmp.group(0)+"\n")
		tmp_post = { "type" : tmp.group(1),
					 "url" : tmp.group(2),
					 "title" : tmp.group(3),
					 "time" : tmp.group(4),
					 "place" : tmp.group(5)}
		post_id = collect.insert_one(tmp_post).inserted_id
		print(" _id : ", end="", flush=True)
		print(post_id)
		print("類別 : "+tmp.group(1))
		print("網址 : "+tmp.group(2))
		print("名稱 : "+tmp.group(3))
		print("時間 : "+tmp.group(4))
		print("地點 : "+tmp.group(5)+"\n\n")
		
client.close()
#print(pure_list)
