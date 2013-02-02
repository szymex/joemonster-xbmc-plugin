# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui, xbmc
import joemonster
import xbmcutil as xbmcUtil

scriptID = 'plugin.video.plugin.video.joemonster'
scriptname = "JoeMonster"


class JoeMonsterAddon (xbmcUtil.ViewAddonAbstract):
	ADDON_ID = 'plugin.video.joemonster'
	NEXT = '[COLOR blue]   ➔  NASTĘPNA (%d)  ➔[/COLOR]'

	def __init__(self):
		xbmcUtil.ViewAddonAbstract.__init__(self)
		self.addHandler('newest', self.handleNewest)
		self.addHandler('popular', self.handlePopular)
		self.addHandler('topfav', self.handleTopFav)
		self.addHandler('top-popular', self.handleTopPopular)

	def handleNewest(self, pg=1, args={}):
		jm = joemonster.JoeMonster()
		result = jm.scrapVideoList(int(pg), 'najnowsze');
		if (pg==1):
			self.addViewLink('[COLOR blue][B]NAJPOTWORNIEJSZE [/B][/COLOR]','popular')
	  
		for r in result:
			title = r['title']
			plot = r['plot']
			
			if r['isHit']: 
				title = '[COLOR red]HIT[/COLOR] ' + title
				plot = '[COLOR red][I]Hicior sprzed lat[/I][/COLOR] \n' + plot
			#xbmc.log(title + '    ' + r['duration'])
			self.addVideoLink(title,r['link'], r['img'], infoLabels={'plot':plot},videoStreamInfo={'duration':r['duration']}  )

		self.addViewLink(self.NEXT % (pg+1),'newest',pg+1)
	  
		if (pg==1):
			self.addViewLink('[COLOR brown] 2012 Najpopularniejsze [/COLOR]','top-popular')
			self.addViewLink('[COLOR brown] 2012 Ulubione [/COLOR]','topfav')
	  

	def handlePopular(self, pg=1, args=[]):
		jm = joemonster.JoeMonster()
		result = jm.scrapPopularFilms();
	  
		i=0		
		for link, img, title in result:
			i+=1
			if i==1:self.addViewLink('[COLOR blue][B] ULUBIONE [/B][/COLOR]','')
			if i==11:self.addViewLink('[COLOR blue][B] OGLĄDANE [/B][/COLOR]','')
			if i==21:self.addViewLink('[COLOR blue][B] KOMENTSY [/B][/COLOR]','')

			num = title[:title.find('.')+1]			
			title = "[COLOR green]%s[/COLOR] %s" % (num,  title[(title.find('.')+2):] )

			self.addVideoLink(title,link, img)

		#xbmcUtil.endOfDir()

	def handleVideo(self, link):
		jm = joemonster.JoeMonster()
		vid = jm.scrapVideo(link)
		
		if (vid != None):
			vidType, vidLink = vid
			if (vidType == 'youtube'):
				youtubeLink = "plugin://plugin.video.youtube/?action=play_video&path=/root/video&videoid=" + vidLink
				return youtubeLink
			
			if (vidType == 'vimeo'):
				#'plugin://plugin.video.vimeo/', '0', '?path=/root/explore/staffpicks&action=play_video&videoid=47140924				
				vimeoLink = "plugin://plugin.video.vimeo/?action=play_video&videoid=" + vidLink
				return vimeoLink

			if (vidType == 'link'):
				return vidLink
		return None
		
	   
	def handleTopPopular(self, pg=1, args=[]):
	  jm = joemonster.JoeMonster()
	  result = jm.scrapVideoList(int(pg), 'najpopularniejsze');

	  for r in result:
	    self.addVideoLink(r['title'],r['link'], r['img'])

	  pg = int(pg) + 1
	  self.addViewLink('[ NASTEPNA -'+str(pg)+'- ]','top-popular', pg)
	  #xbmcUtil.endOfDir()
	   
	def handleTopFav(self, pg=1, args=[]):
	  jm = joemonster.JoeMonster()
	  result = jm.scrapVideoList(int(pg), 'ulubione');

	  for r in result:
	    self.addVideoLink(r['title'],r['link'], r['img'])

	  pg = int(pg) + 1
	  self.addViewLink('[ NASTEPNA -'+str(pg)+'- ]','topfav', pg)


# -----------

addon = JoeMonsterAddon()
addon.handle()
