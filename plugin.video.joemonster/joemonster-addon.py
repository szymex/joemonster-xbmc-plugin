# -*- coding: utf-8 -*-

from datetime import date

import joemonster
import xbmcutil as xbmcUtil


scriptID = 'plugin.video.plugin.video.joemonster'
scriptname = "JoeMonster"


class JoeMonsterAddon(xbmcUtil.ViewAddonAbstract):
	ADDON_ID = 'plugin.video.joemonster'
	NEXT = '[COLOR blue]   ➔  NASTĘPNA (%d)  ➔[/COLOR]'

	def __init__(self):
		xbmcUtil.ViewAddonAbstract.__init__(self)
		self.addHandler('newest', self.handleNewest)
		self.addHandler('popular', self.handlePopular)
		self.addHandler('topfav', self.handleTopFav)
		self.addHandler('top-popular', self.handleTopPopular)
		self.addHandler('waiting', self.handleWaiting)

	def handleNewest(self, pg=1, args={}):
		jm = joemonster.JoeMonster()
		result = jm.scrapVideoList(int(pg), 'najnowsze')
		if pg == 1:
			self.addViewLink('[COLOR blue][B]NAJPOTWORNIEJSZE [/B][/COLOR]', 'popular')

		for r in result:
			title = r['title']
			plot = r['plot']

			if r['isHit']:
				title = '[COLOR red]HIT[/COLOR] ' + title
				plot = '[COLOR red][I]Hicior sprzed lat[/I][/COLOR] \n' + plot

			duration = r['duration-sec'] / 60 if r['duration-sec'] > 0 else ''
			self.addVideoLink(title, r['link'], r['img'], infoLabels={'plot': plot, 'duration': str(duration)}, videoStreamInfo={'duration': r['duration-sec']})

		self.addViewLink(self.NEXT % (pg + 1), 'newest', pg + 1)

		if pg == 1:
			prevYear = date.today().year - 1
			self.addViewLink('[COLOR blue] POCZEKALNIA [/COLOR]', 'waiting')
			self.addViewLink("[COLOR brown] %d Najpopularniejsze [/COLOR]" % prevYear, 'top-popular')
			self.addViewLink("[COLOR brown] %d Ulubione [/COLOR]" % prevYear, 'topfav')

	def handlePopular(self, pg=1, args=[]):
		jm = joemonster.JoeMonster()
		result = jm.scrapPopularFilms()

		i = 0
		for link, img, title in result:
			i += 1
			if i == 1:
				self.addViewLink('[COLOR blue][B] ULUBIONE [/B][/COLOR]', '')
			if i == 11:
				self.addViewLink('[COLOR blue][B] OGLĄDANE [/B][/COLOR]', '')
			if i == 21:
				self.addViewLink('[COLOR blue][B] KOMENTSY [/B][/COLOR]', '')

			num = title[:title.find('.') + 1]
			title = "[COLOR green]%s[/COLOR] %s" % (num, title[(title.find('.') + 2):].strip())

			self.addVideoLink(title, link, img)

	def handleVideo(self, link):
		jm = joemonster.JoeMonster()
		vid = jm.scrapVideo(link)

		if vid is not None:
			vidType, vidLink = vid
			if vidType == 'youtube':
				youtubeLink = "plugin://plugin.video.youtube/?action=play_video&path=/root/video&videoid=" + vidLink
				return youtubeLink

			if vidType == 'vimeo':
				# 'plugin://plugin.video.vimeo/', '0', '?path=/root/explore/staffpicks&action=play_video&videoid=47140924
				vimeoLink = "plugin://plugin.video.vimeo/play/?video_id=" + vidLink
				return vimeoLink

			if vidType == 'daily':
				# plugin://plugin.video.dailymotion_com/?url=%VIDEOID%&mode=playVideo
				dailyLink = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url=" + vidLink
				return dailyLink

			if vidType == 'link':
				return vidLink
		return None

	def handleTopPopular(self, pg=1, args=[]):
		jm = joemonster.JoeMonster()
		result = jm.scrapVideoList(int(pg), 'najpopularniejsze')

		for r in result:
			self.addVideoLink(r['title'], r['link'], r['img'])

		pg = int(pg) + 1
		self.addViewLink('[ NASTEPNA -' + str(pg) + '- ]', 'top-popular', pg)

	# xbmcUtil.endOfDir()

	def handleTopFav(self, pg=1, args=[]):
		jm = joemonster.JoeMonster()
		result = jm.scrapVideoList(int(pg), 'ulubione')

		for r in result:
			self.addVideoLink(r['title'], r['link'], r['img'])

		pg = int(pg) + 1
		self.addViewLink('[ NASTEPNA -' + str(pg) + '- ]', 'topfav', pg)

	def handleWaiting(self, pg=1, args=[]):
		jm = joemonster.JoeMonster()
		result = jm.scrapWaitingVideos(pg)
		i = 0

		for r in result:
			self.addVideoLink('[COLOR brown](' + r['likes'] + ')[/COLOR] ' + r['title'], r['link'], r['img'])


# -----------

addon = JoeMonsterAddon()
addon.handle()
