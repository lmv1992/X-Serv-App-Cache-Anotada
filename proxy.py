#!/usr/bin/python

import webapp
import urllib2

class proxy(webapp.webApp):
	DiccUrl = {}
	def parse(self,request):
		print request
		recurso = request.split(' ',2)[1][1:]
		recurso = 'http://www.'+recurso
		return (recurso)

	def process(self,request):
		recurso = request
		request_url = urllib2.Request(recurso)
		try:
			resp = urllib2.urlopen(request_url)
		except urllib2.HTTPError as e:
			httpCode = '404 Not Found'
			if e.code == 404:
				htmlBody = '<html><body>'
				htmlBody += '<p>PAGINA NO ENCONTRADA, ENVIE OTRA URL</p>'
				htmlBody += '</html></body>'
			else:
				httpCode = '404 Not Found'
				htmlBody = '<html><body>'
				htmlBody += '<p>----PROBLRMA DESCONOCIDO AL CARGAR LA URL, ENVIE OTRA URL</p>'
				htmlBody += '</html></body>'
		except urllib2.URLError as e:
			httpCode = '404 Not Found'
			htmlBody = '<html><body>'
			htmlBody += '<p>HAY UN PROBLEMA CON LA URL,ESCRIBALA DE FORMA CORRECTA</p>'
			htmlBody += '</html></body>'
		else:
			httpCode = '200 OK'
			if recurso in self.DiccUrl:
				htmlBody = self.DiccUrl[recurso]
			else:
				body = resp.read()
				body1 = body.split('<body', 1)
				body2 = body1[1].split('>', 1)
				body = body1[0] + '<body '
				body += body2[0] + '>' + '<a href="' + recurso + '">ORIGINAL</a>'
				body += body2[1]
				self.DiccUrl[recurso] = body
				htmlBody = self.DiccUrl[recurso]
		return (httpCode, htmlBody)

if __name__ == "__main__":
	main = proxy("localhost", 1234)
