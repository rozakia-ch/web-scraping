# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
#plugin scraping
import requests
from bs4 import BeautifulSoup
#database
from interface.models import *
import re
# selenium
from selenium import webdriver
import time
# Create your views here.
def jawapos(keyword):
	driver = webdriver.Firefox()
	driver.get('https://www.jawapos.com/news/search?keyword='+keyword)
	# hitung pagination
	time.sleep(30)
	count = driver.find_elements_by_class_name('gsc-cursor-page')

	jumlah = []
	for item in count:
		jumlah.append(item.text)

	total = len(jumlah)+1
	# print total
	# get href
	posts = driver.find_elements_by_class_name("gs-title")
	link = []
	for post in posts:
		link.append(post.get_attribute("href"))

	for x in range(2,total):
		try:
			x = str(x)
			driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div[11]/div/div['+x+']').click()
			time.sleep(5)				
			posts2 = driver.find_elements_by_class_name("gs-title")
		except:
			time.sleep(5)
			continue

		for post in posts2:
			link.append(post.get_attribute("href"))

	link2 = filter(None, link)
	url_link = []
	for x in link2:
		str1 = str(x)
		url_link.append(str1)

	driver.close()

	s = []
	for i in url_link:
	       if i not in s:
	          s.append(i)
	
	for add_link in s:
		url = requests.get(add_link)
		soup = BeautifulSoup(url.content,"lxml")
		ambil = soup.find_all("div", {"class": "mainnews-terkini"})
		for item in ambil:
			try:
				s.append(item.contents[1].find_all('a')[0].get('href'))
			except:
				pass
	a = []
	for i in s:
	       if i not in a:
	          a.append(i)
	print a

	for url_link in a:
		cek = tbl_berita.objects.filter(url_berita = url_link).count()
		# print cek
		if cek == 0:
			url = requests.get(url_link)
			soup = BeautifulSoup(url.content,"lxml")
			title = soup.find_all("div", {"class": "primary-title-article"})
			news  = soup.find_all("div", {"class": "paragraph-article-detail"})
			author = soup.find_all("div", {"class": "time-publiser-by"})
					
			judul = []
			for item in title:
				for x in range(1,5):
					try:
						judul.append(item.contents[x].text)
					except:
						pass

			isi_berita = []

			for item in news:
				for x in range(23):		
					try:
						isi_berita.append(item.find_all('p')[x].text)
					except:
						pass

			publiser = []
			for item3 in author:
				try:
					publiser.append(item3.contents[1].text)
				except:
					pass

			con = None
			str1 = " ".join(judul)
			str2 = "\n ".join(isi_berita)
			str3 = " ".join(publiser)
							
			if str1 != '':
				query = tbl_berita(judul = str1, isi_berita = str2, time_publiserby = str3, sumber_berita = "jawapos", status_berita = "", url_berita = url_link )
				query.save()
			else:
				pass
		else:
			pass
	return

def kompas(keyword):
	driver = webdriver.Firefox()
	driver.get('https://search.kompas.com/search/?q='+keyword+'&submit=Submit')
	# hitung pagination
	time.sleep(30)
	count = driver.find_elements_by_class_name('gsc-cursor-page')
	jumlah = []
	for item in count:
		jumlah.append(item.text)
	total = len(jumlah)+1
	
	# get href
	posts = driver.find_elements_by_class_name("gs-title")
	link = []
	for post in posts:
		link.append(post.get_attribute("href"))

	for x in range(2,total):		
		try:
			x = str(x)
			driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/div/div[5]/div[2]/div[1]/div/div[3]/div[11]/div/div['+x+']').click()
			time.sleep(5)				
			posts2 = driver.find_elements_by_class_name("gs-title")
		except:
			time.sleep(5)
			continue

		for post in posts2:
			link.append(post.get_attribute("href"))

	url_link = filter(None, link)
	
	driver.close()

	s = []
	for i in url_link:
	       if i not in s:
	          s.append(i)
	print s
	for url_link in s:
		cek = tbl_berita.objects.filter(url_berita = url_link).count()
		# print cek
		if cek == 0:
			url = requests.get(url_link)
			soup = BeautifulSoup(url.content,"lxml")
			title = soup.find_all("h1", {"class": "read__title"})
			news = soup.find_all("div", {"class": "col-bs9-7"})
			author1 = soup.find_all("div", {"class": "read__author"})
			author2 = soup.find_all("div", {"class": "read__time"})
			daftar = soup.find_all("ol")

			judul = []
			for item in title:
				try:
					judul.append(item.text)
				except:
					pass
			
			publiser = []

			for item in author1:
				try:
					publiser.append(item.text)
				except:
					pass

			for item in author2:
				try:
					publiser.append(item.text)
				except:
					pass

			isi_berita = []
			for item in news:
				for x in range(50):
					try:
						isi_berita.append(item.contents[3].find_all("p")[x].text)
					except:
						pass
				
			daf = ''
			for item in daftar:
				daf = item.text

			str1 = " ".join(judul)
			str2 = "\n ".join(isi_berita)
			str3 = " ".join(publiser)

			if daf != '':
				str2 = str2 + daf

			con = None
			if str1 != '':
				query = tbl_berita(judul = str1, isi_berita = str2, time_publiserby = str3, sumber_berita = "kompas", status_berita = "", url_berita = url_link )
				query.save()
			else:
				pass
		else:
			pass
	return

def detik(keyword):	
	url = requests.get("https://www.detik.com/search/searchall?query="+keyword)
	sp = BeautifulSoup(url.content,"lxml")
	link = sp.find_all("article")
	page = sp.find_all("div", {"class":"paging text_center"})
	link_url = []

	for item in link:
	    link_url.append(item.find_all("a")[0].get('href'))
	try:
		for item in page:
			jumlah = item.text
		jumlah = jumlah.replace("\n", "")
		jumlah = " ".join(jumlah)
		jumlah = jumlah.split(' ')
		jumlah = len(jumlah)

		pagination = []
		for x in xrange(1,jumlah):
			for item in page:
				pagination.append(item.find_all("a")[x].get('href'))

		for link in pagination:
			url = requests.get(link)
			sp = BeautifulSoup(url.content,"lxml")
			link = sp.find_all("article")

			for item in link:
				link_url.append(item.find_all("a")[0].get('href'))
	except:
		pass
		
	s = []
	for i in link_url:
	       if i not in s:
	          s.append(i)
	print s

	for url_link in s:
		cek = tbl_berita.objects.filter(url_berita = url_link).count()
		# print cek
		if cek == 0:
			try:
				driver = webdriver.Firefox()
				driver.get(url_link)
				# time.sleep(30)
				date = driver.find_element_by_class_name('date')
				author = driver.find_element_by_class_name('author')
				title = driver.find_element_by_tag_name('h1')
				news = driver.find_element_by_class_name('detail_text')

				tanggal = date.text
				editor =  author.text
				judul = title.text
				berita = news.text
				isi_berita = re.sub('"', '', berita)
				isi = isi_berita.replace("'", "")
				publiser = tanggal + " | " + editor
				driver.close()

				query = tbl_berita(judul = judul, isi_berita = isi, time_publiserby = publiser, sumber_berita = "detik", status_berita = "", url_berita = url_link )
				query.save()
			
			except:
				pass
				driver.close()
		else:
			pass
	return 