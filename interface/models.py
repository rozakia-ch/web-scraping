# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class tbl_berita(models.Model):
	url_berita = models.TextField()
	judul = models.CharField(max_length=200)
	isi_berita = models.TextField()
	time_publiserby = models.CharField(max_length=200)
	sumber_berita = models.CharField(max_length=20)
	status_berita = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.judul