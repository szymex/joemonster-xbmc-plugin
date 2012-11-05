# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui, xbmc
import joemonster, xbmcUtil

scriptID = 'plugin.video.plugin.video.joemonster'
scriptname = "JoeMonster"
# ptv = xbmcaddon.Addon(scriptID)



class JoeMonsterAddon (xbmcUtil.ViewAddonAbstract):

	def init(self):
		self.addHandler('newest', self.handleNewest)
		self.addHandler('popular', self.handlePopular)
		self.addHandler('topfav', self.handleTopFav)
		self.addHandler('top-popular', self.handleTopPopular)

	def handleNewest(self, pg=1, args={}):
		jm = joemonster.JoeMonster(False)
		result = jm.scrapVideoList(int(pg), 'najnowsze');
		if (pg==1):
			self.addViewLink('[ NAJPOTWORNIEJSZE ]','popular')
	  
		for img, link, title in result:
			self.addVideoLink(title,link, img,)
		self.addViewLink('[ NASTEPNA -'+str(pg+1)+'- ]','newest',pg+1)
	  
		if (pg==1):
			self.addViewLink('[ 2011 Najpopularniejsze ]','top-popular')
			self.addViewLink('[ 2011 Ulubione ]','topfav')
	  
		#xbmcUtil.endOfDir()

	def handlePopular(self, pg=1, args=[]):
		jm = joemonster.JoeMonster(False)
		result = jm.scrapPopularFilms();
	  
		for link, img, title in result:
			self.addVideoLink(title,link, img)

		#xbmcUtil.endOfDir()

	def handleVideo(self, link):
		jm = joemonster.JoeMonster(False)
		vid = jm.scrapVideo(link)
		
		if (vid != None):
			vidType, vidLink = vid
			if (vidType == 'youtube'):
				youtubeLink = "plugin://plugin.video.youtube/?action=play_video&path=/root/video&videoid=" + vidLink
				return youtubeLink

			if (vidType == 'link'):
				return vidLink
		return None
		
	   
	def handleTopPopular(self, pg=1, args=[]):
	  jm = joemonster.JoeMonster(False)
	  result = jm.scrapVideoList(int(pg), 'najpopularniejsze');

	  for img, link, title in result:
	    self.addVideoLink(title,link, img)

	  pg = int(pg) + 1
	  self.addViewLink('[ NASTEPNA -'+str(pg)+'- ]','top-popular', pg)
	  #xbmcUtil.endOfDir()
	   
	def handleTopFav(self, pg=1, args=[]):
	  jm = joemonster.JoeMonster(False)
	  result = jm.scrapVideoList(int(pg), 'ulubione');

	  for img, link, title in result:
	    self.addVideoLink(title,link, img)

	  pg = int(pg) + 1
	  self.addViewLink('[ NASTEPNA -'+str(pg)+'- ]','topfav', pg)
	  #xbmcUtil.endOfDir()


# -----------

addon = JoeMonsterAddon()
addon.init()
addon.handle()
