# JoeMonster class

import urllib2,urllib,re

class JoeMonster:
  def __init__(self):
    self.test=False;
    return

  def __init__(self, test):
    self.test=test;
    return


  def readContentList(self, pg=1, category="najnowsze"):
	if (self.test==False):	
		url='http://www.joemonster.org/filmy/' + category + '/'+str(pg)
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	else:
		print 'readContentList-testing'
		f = open("/home/szymon/.xbmc/addons/plugin.video.joemonster/joemonster-filmy.xml", "r")
		link = f.read()
        return link

  def scrapVideoList(self, pg=1, category='najnowsze'):
	content = self.readContentList(pg, category) 	
	matchTitle=re.compile("<tr valign=\"top\".*?img src=\"(.*?)\".*?<a href=\"(.*?)\".*?<b>(.*?)</b>.*?</tr>", re.DOTALL).findall(content)
	print len(matchTitle)
        #img, link, title
        return matchTitle


  def readPopularFilms(self):
	if (self.test==False):	
		url='http://www.joemonster.org/filmy'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	else:
		print 'testing'
		f = open("/home/szymon/.xbmc/addons/plugin.video.joemonster/joemonster-filmy.xml", "r")
		link = f.read()
        return link



  def scrapPopularFilms(self):
	content = self.readPopularFilms() 	
	matchTitle=re.compile("<div class='mtvTopLista'><a href=\"(.*?)\".*?<img src=(.*?) .*?>(.*?)<.*?</div>").findall(content)
	
        #link, img, title
        return matchTitle

  def readVideoContent(self, link):
	if (self.test==False):	
		url='http://www.joemonster.org/' + link
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	else:
		print 'testing'
		f = open("/home/szymon/.xbmc/addons/plugin.video.joemonster/joemonster-filmy-utalentowana.xml", "r")
		link = f.read()
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
	#could not scrap video	
	return None
  

