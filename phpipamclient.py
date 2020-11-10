#!/usr/bin/env python

import sys
import httplib2
from urllib.parse import quote,urlencode
from base64 import b64encode
import json


class IPAMClient(object):
	def __init__(self, host, app, user, pswd):
		self.host = host
		self.app  = app
		self.user = user
		self.pswd = pswd
		self.h=httplib2.Http()
		self.token = None
		self.login()

	TYPE_USED=2

	def login(self):
		cookie = b64encode("{0}:{1}".format(self.user, self.pswd).encode()).decode()
		auth={"Authorization": "Basic "+cookie}
		url = "http://" + self.host + quote("/api/" + self.app + "/user/")
		r, content = self.h.request(url, "POST", headers=auth)
		try:
			d = json.loads(content)
		except Exception:
			print("JSON fail: ",content)
			raise
		if (d['success'] == True):
			self.token = d['data']['token']
		else:
			raise Exception("Login failed")

	def request(self, path, method="GET", data=None):
		if not self.token:
			self.login()
		headers={ "PHPIPAM_TOKEN": self.token, "Content-type": "application/x-www-form-urlencoded" }
		url = "http://" + self.host + quote("/api/" + self.app + "/" + path)
		if (url[-1:] != '/'):
			url = url+'/'
		if data:
			data=urlencode(data)
		r,content = self.h.request(url, method, data, headers=headers)
		try:
			d = json.loads(content)
		except:
			print("JSON fail: ",content)
			raise
		if (d["success"] == True):
			return d["data"]
		if (d["code"] == 404):
			return {}
		#print(json.dumps(d, indent=4))
		raise Exception(d["message"])

	def getaddressbyhostname(self, hostname):
		return self.request("addresses/search_hostname/"+hostname)

	def getsubnetbycidr(self, cidr):
		return self.request("subnets/cidr/"+cidr)

	def getsubnet(self, subnetid):
		return self.request("subnets/"+subnetid)

	def getslavenets(self, subnetid):
		return self.request("subnets/"+subnetid+"/slaves/")

	def getsubnetaddresses(self, subnetid):
		return self.request("subnets/"+subnetid+"/addresses/")

	def getaddressesbytype(self, type):
		# type==2 -> used
		return self.request("addresses/tags/"+type.__str__()+"/addresses/")

	def getaddressbyip(self, ip):
		return self.request("addresses/search/"+ip)

	def getaddress(self, addressid):
		return self.request("addresses/"+addressid)

	def setaddress(self, ip, hostname):
		# TBD currently hardcoded, it won't change unless IPAM is reinstalled
		# but it should hunt down the top of the tree
		d = {
			"subnetId": 225,
			"ip": ip,
			"hostname": hostname
		}
		return self.request("addresses/", "POST", d)

	def deladdress(self, ip):
		a = self.request("addresses/search/"+ip)
		#print(json.dumps(a, indent=4))
		if a:
			if type(a)==list:
				a = a[0]
			self.request("addresses/"+a["id"], "DELETE")

