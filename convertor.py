# importing the libraries
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import codecs
import csv
import re
import json

mypath="newtest/"
configFile="config.json"

def readConfig(papper_name):
	with open(configFile) as f:
		data = json.load(f)
	return data.get(papper_name)

def write_dataFile(paper_data):
	# html_file.replace('.html','.csv')
	with open('dataDump.csv', mode='w') as csv_file:
		fieldnames = ['papper_name','date','headding','data','link', 'comments']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		for headding, data in paper_data.items():
			headding=headding.split('__')
			papper_name=headding[1]
			date_name=headding[2]
			headding=headding[0]
			data=data.split('__')
			link=data[1]
			data=data[0]
			writer.writerow({'papper_name':papper_name,'date':date_name,'headding':headding,'data':data,'link':link})

def extract_dataFile(soup,element,class_name,papper_name,date_name):
	data_array={}
	if class_name=='':
		coverpage_news = soup.find_all(element)
	else:
		coverpage_news = soup.find_all(element, class_=class_name)
	# Empty lists for content, links and titles
	for n in range(len(coverpage_news)):
		if coverpage_news[n].find('a') is not None and "href" in str(coverpage_news[n].find('a')):
			link=coverpage_news[n].find('a')["href"]
			title = coverpage_news[n].find('a').get_text()
		else:
			link=''
			if coverpage_news[n].find('span') is not None:
				title = coverpage_news[n].find('span').get_text()
			else:
				title = coverpage_news[n].get_text()
		if( len(title.split())>3 ):
			data_array.update({element+'__'+papper_name+'__'+date_name+'__'+str(n) : re.sub(r"[\n\r\t]+", ' ', title)+'__'+link})
	return data_array

def filter_duplicate_data(data):
	result = {}
	for key,value in data.items():
		if value not in result.values():
			result[key] = value
	return result

tempPaperData=[]

html_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for html_file in html_files:
	if html_file == '.DS_Store':
		continue
	papper_name=html_file.split('_')[-1].replace('.html','')
	date_name=html_file.split('_')[0]

	# for html_file in html_files:
	file = codecs.open(mypath+html_file, "r", "utf-8")
	html_content=file.read()
	# Parse the html content
	soup = BeautifulSoup(html_content, "lxml")
	tempData=[]
	for data in readConfig(papper_name):
		for html_tag, classname in data.items():
			tempData.append(extract_dataFile(soup,html_tag,classname,papper_name,date_name))

	tempPaperData.append({i:j for x in tempData for i,j in x.items()})

merged_data={i:j for x in tempPaperData for i,j in x.items()}
write_dataFile(filter_duplicate_data(merged_data))





