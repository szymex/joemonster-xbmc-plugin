# JoeMonster class

import urllib2,urllib,re,sys
import CommonFunctions
import xbmc

reload(sys) 
sys.setdefaultencoding('utf8')

common = CommonFunctions
common.plugin = "plugin.video.katsomo"

class JoeMonster:

 	def readContentList(self, pg=1, category="najnowsze"):
		url='http://www.joemonster.org/filmy/' + category + '/'+str(pg)
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		content=response.read()
		response.close()
		return content

	def scrapVideoList2(self, pg=1, category='najnowsze'):
		content = self.readContentList(pg, category) 	
		matchTitle=re.compile("<tr valign=\"top\".*?img src=\"(.*?)\".*?<a href=\"(.*?)\".*?<b>(.*?)</b>.*?</tr>", re.DOTALL).findall(content)
		xbmc.log(str(matchTitle))
		retList = []		
		for m in matchTitle:
			img = m[0]
			link = m[1]
			title = m[2]
			retList.append({'title': title, 'link':link, 'img': img })
		return retList
	
	def scrapVideoList(self, pg=1, category='najnowsze'):
		url='http://www.joemonster.org/filmy/%s/%d' % (category, pg)
		xbmc.log(url)
		
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		content=response.read()
		content = content.decode('iso-8859-2')#.encode('utf8')
		#xbmc.log(content)
		ret = common.parseDOM(content, "div", {'style': 'float:left;width:630px; position: relative'})

		ret = common.parseDOM(ret, "div", {'class':'mtv-row'})

		retList = []		
		for r in ret:
			#xbmc.log(r)
			#title = common.parseDOM(r, "a", {'class': 'title'})[0]
			#title = title.decode('iso-8859-2')#.encode('utf8')
			#xbmc.log(title)
			#title = common.parseDOM(title, "b")[0]
			link = common.parseDOM(r, "a", {'class': 'title'}, 'href')[0]
			img = common.parseDOM(r, "img", {}, 'src')[0]
			title = common.parseDOM(r, "img", {}, 'title')[0]
			plot = common.parseDOM(r, 'DIV')[0].replace('<br>', '')
			#xbmc.log(str(plot))
			#plot = plot[0].replace('<br>', '') if len(plot)>0 else ''
			
			duration=re.compile('Czas trwania:</b>(.*?)<br>', re.DOTALL).findall(r)
			duration=duration[0] if len(duration)>0 else ''
			isHit = 'lata' in r
			if isHit: xbmc.log('hit: ' + title)
			retList.append({'title': title, 'link':link, 'img': img, 'plot': plot, 'duration': duration, 'isHit':isHit })
		
		return retList


	def readPopularFilms(self):
		url='http://www.joemonster.org/filmy'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link


	def scrapPopularFilms(self):
		content = self.readPopularFilms() 	
		matchTitle=re.compile("<div class='mtvTopLista'><a href=\"(.*?)\".*?<img src=(.*?) .*?>(.*?)<.*?</div>").findall(content)
					
		#link, img, title
		return matchTitle

	def readVideoContent(self, link):
		url='http://www.joemonster.org/' + link
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link

	def scrapVideo(self, link):
		content = self.readVideoContent(link) 	
		    
		#---- youtube ----
		matchTitle=re.compile("<object.*?data=\"http://www.youtube.com/v/(.*?)\"").findall(content)
	
		if (len(matchTitle) > 0):
			vid = matchTitle[0]
			return 'youtube', vid

		#---- joemonster video with redirection ----
		matchTitle=re.compile("<embed src=\"http://www.joemonster.org/emb/(.*?)\".*?>").findall(content)
		if (len(matchTitle) > 0):
			vidUrl = 'http://www.joemonster.org/emb/' + matchTitle[0]
	  		req = urllib2.Request(vidUrl)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			matchTitle=re.compile("file=(.*?)&").findall(response.geturl())
			response.close()

			jmVidLink = matchTitle[0]
			return 'link', jmVidLink

		#---- joemonster video ----
		matchTitle=re.compile("file=(.*?)&").findall(content)
		if (len(matchTitle) > 0):
			jmVidLink = urllib.unquote(matchTitle[0])
			return 'link', jmVidLink

		#---- vimeo ----
		matchTitle=re.compile('<embed src=\"http://vimeo.com/moogaloop.swf\?clip_id=(.*?)"').findall(content)
		if (len(matchTitle) > 0):
			vid = matchTitle[0]
			return 'vimeo', vid

		#could not scrap video	
		return None
  

