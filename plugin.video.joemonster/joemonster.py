# JoeMonster class

import urllib2
import urllib
import re
import sys
from datetime import datetime
import time

import CommonFunctions
import xbmc

reload(sys)
sys.setdefaultencoding('utf8')

common = CommonFunctions
common.plugin = "plugin.video.katsomo"


class JoeMonster:
	def __init__(self):
		pass

	@staticmethod
	def readContentList(pg=1, category="najnowsze"):
		url = 'http://www.joemonster.org/filmy/' + category + '/' + str(pg)
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		content = response.read()
		response.close()
		return content

	def scrapVideoList2(self, pg=1, category='najnowsze'):
		content = self.readContentList(pg, category)
		matchTitle = re.compile("<tr valign=\"top\".*?img src=\"(.*?)\".*?<a href=\"(.*?)\".*?<b>(.*?)</b>.*?</tr>", re.DOTALL).findall(content)
		# xbmc.log(str(matchTitle))
		retList = []
		for m in matchTitle:
			img = m[0]
			link = m[1]
			title = m[2]
			retList.append({'title': title, 'link': link, 'img': img})
		return retList

	@staticmethod
	def scrapVideoList(pg=1, category='najnowsze'):
		url = 'http://www.joemonster.org/filmy/%s/%d' % (category, pg)
		xbmc.log(url)

		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		content = response.read()
		# content = content.decode('iso-8859-2')#.encode('utf8')
		ret = common.parseDOM(content, "div", {'class': 'mtv-row'})

		retList = []
		for r in ret:
			if len(common.parseDOM(r, "a", {'class': 'title'}, 'href')) == 0:
				continue

			link = common.parseDOM(r, "a", {'class': 'title'}, 'href')[0]
			img = common.parseDOM(r, "img", {}, 'src')[0]
			title = common.parseDOM(r, "img", {}, 'title')[0]

			# TODO: fix plot
			plot = ""
			# plot = common.parseDOM(r, 'div')[0].replace('<br>', '')

			duration = re.compile('Czas trwania:</b>(.*?)<br>', re.DOTALL).findall(r)
			duration = duration[0].strip() if len(duration) > 0 else ''
			durationSec = 0
			if len(duration) > 0:
				try:
					durationTs = datetime.strptime(duration, '%M:%S')
				except TypeError:
					durationTs = datetime(*(time.strptime(duration, '%M:%S')[0:6]))
				durationSec = durationTs.second + durationTs.minute * 60 + durationTs.hour * 3600

			isHit = 'lata' in r

			retList.append({'title': title, 'link': link, 'img': img, 'plot': plot, 'duration': duration, 'duration-sec': durationSec, 'isHit': isHit})

		return retList

	@staticmethod
	def scrapWaitingVideos(pg=1):
		url = 'http://www.joemonster.org/filmy/poczekalnia/%d' % pg
		xbmc.log(url)

		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		content = response.read()
		# content = content.decode('iso-8859-2')

		ret = common.parseDOM(content, "div", {'class': 'mtvPoczekalniaFilm'})

		retList = []
		for r in ret:

			matchImg = re.compile('IMG SRC=\"(.*?)\"', re.DOTALL).findall(r)
			img = matchImg[0] if len(matchImg) > 0 else ''
			title = common.parseDOM(r, "h2")[0]
			link = common.parseDOM(r, "a", {'class': 'titulo'}, 'href')[0]
			likes = common.parseDOM(r, "div", {'class': 'mtvPoczekalniaOk'})[0]

			if link.startswith('/filmy'):
				retList.append({'title': title, 'link': link, 'img': img, 'likes': likes})

		return retList

	@staticmethod
	def readPopularFilms():
		url = 'http://www.joemonster.org/filmy'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link

	def scrapPopularFilms(self):
		content = self.readPopularFilms()
		# content = content.decode('iso-8859-2')#.encode('utf8')
		matchTitle = re.compile("<div class='mtvTopLista'>.*?<a href=\"(.*?)\".*?<img src=(.*?) .*?>(.*?)<.*?</div>", re.DOTALL).findall(content)

		# link, img, title
		return matchTitle

	@staticmethod
	def readVideoContent(link):
		if link.startswith("http"):
			url = link
		else:
			url = 'http://www.joemonster.org/' + link
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link = response.read()
		response.close()
		return link

	def scrapVideo(self, link):
		content = self.readVideoContent(link)

		# ---- youtube ----
		matchTitle = re.compile('src="http://www.youtube.com/embed/(.*?)\?').findall(content)

		if len(matchTitle) > 0:
			vid = matchTitle[0]
			return 'youtube', vid

		# ---- joemonster video with redirection ----
		matchTitle = re.compile("<embed src=\"http://(www.|)joemonster.org/emb/(.*?)\".*?>").findall(content)
		if len(matchTitle) > 0:
			vidUrl = 'http://www.joemonster.org/emb/' + matchTitle[0][1]
			req = urllib2.Request(vidUrl)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			matchTitle = re.compile("file=(.*?)&").findall(response.geturl())
			response.close()

			jmVidLink = matchTitle[0]
			return 'link', jmVidLink

		# ---- joemonster video ----
		matchTitle = re.compile("file=(.*?)&").findall(content)
		if len(matchTitle) > 0:
			jmVidLink = urllib.unquote(matchTitle[0])
			return 'link', jmVidLink

		# ---- vimeo ----
		matchTitle = re.compile('<IFRAME src=\"http://player.vimeo.com/video/(.*?)"').findall(content)
		if len(matchTitle) > 0:
			vid = matchTitle[0]
			return 'vimeo', vid

		# ---- joemonster iframe ----
		matchTitle = re.compile('<iframe .*? src=\"http://joemonster.org/.embtv.php(.*?)"').findall(content)
		if len(matchTitle) > 0:
			iframeLink = 'embtv.php' + matchTitle[0]
			iframeContent = self.readVideoContent(iframeLink)
			matchLink = re.compile('src=\"(http://vader.*?\.mp4)"').findall(iframeContent)
			if len(matchLink) > 0:
				return 'link', matchLink[0]

		# ---- funnyordie ----
		matchTitle = re.compile('<IFRAME src=\"(http://www.funnyordie.com/embed/.*?)"').findall(content)
		if len(matchTitle) > 0:
			iframeContent = self.readVideoContent(matchTitle[0])
			matchLink = re.compile('src=\"(http://.*?\.mp4)"').findall(iframeContent)
			if len(matchLink) > 0:
				return 'link', matchLink[0]

		# could not scrap video
		return None
