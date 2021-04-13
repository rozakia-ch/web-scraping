# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from interface.models import *
from interface.forms import *
from scraping import *
# Create your views here.

def login(request):
	return render(request, 'contents/form-login.html')

def statistik(request):
	jawapos = tbl_berita.objects.filter(sumber_berita='jawapos').exclude(status_berita__isnull=False, status_berita__exact='').exclude(status_berita__exact='Buang').count()
	kompas	= tbl_berita.objects.filter(sumber_berita='kompas').exclude(status_berita__isnull=False, status_berita__exact='').exclude(status_berita__exact='Buang').count()
	detik	= tbl_berita.objects.filter(sumber_berita='detik').exclude(status_berita__isnull=False, status_berita__exact='').exclude(status_berita__exact='Buang').count()
	labels	= ["Jawapos","Kompas","Detik"]
	query	= [jawapos, kompas, detik]
	data	= {
				"labels": labels,
				"default": query,
	}

	return JsonResponse(data, safe=False)

def condition(request):
	positif = tbl_berita.objects.filter(status_berita='Positif').count()
	negatif	= tbl_berita.objects.filter(status_berita='Negatif').count()
	query = [positif, negatif]
	labels = ["Positif","Negatif"]
	data	= {
				"labels": labels,
				"default": query,
	}
	return JsonResponse(data, safe=False)

def dashboard(request):
	return render(request, 'contents/index.html')

def getNews(request, pk):
	query = tbl_berita.objects.extra(where=['id='+pk])
	for item in query:
		id_berita = item.id
		judul = item.judul
		berita = item.isi_berita

	data = {"id": id_berita,
	 		"judul": judul,
	 		"berita": berita,
	 		}
	data = [data]
	return JsonResponse(data, safe=False)

def berita(request):
	news = tbl_berita.objects.all().filter(status_berita = '')
	news2 = tbl_berita.objects.all().exclude(status_berita__isnull=False, status_berita__exact='').exclude(status_berita__exact='Buang')
	news3 = tbl_berita.objects.all().filter(status_berita = 'Buang').exclude(status_berita__isnull=False, status_berita__exact='')
	return render(request, 'contents/berita.html', {'news': news, 'news2': news2, 'news3':news3})

def update(request, pk):
	query = get_object_or_404(tbl_berita, pk=pk)
	if request.method == "POST":
		form = FormUpdate(request.POST, instance=query)
		if form.is_valid():
			query = form.save(commit=False)
			query.save()
			return redirect('berita')
	else:
		query = get_object_or_404(tbl_berita, pk=pk)
    	return render(request, 'contents/detail.html', {'item': query})

def delete(request, pk):
    query = get_object_or_404(tbl_berita, pk = pk)
    query.delete()
    return redirect('berita')

def create(request):
	keyword = request.GET['key']
	keyword = keyword.replace(" ", "+")
	situs	= request.GET['situs']
	if keyword == "":
		return redirect('berita')
	else:
		if situs == "Jawapos":
			jawapos(keyword)
		elif situs == "Kompas":
			kompas(keyword)
		elif situs == "Detik":
			detik(keyword)
		else:
			jawapos(keyword)
			kompas(keyword)
			detik(keyword)

		return redirect('berita')

def test(request):
	return render(request, 'contents/json.html')