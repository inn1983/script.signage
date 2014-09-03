# -*- coding: utf-8 -*-
# helloworld.py
# hello world demo

import os
import os.path
import xbmc, xbmcgui
import tweepy
import urllib
import time
from pytube import YouTube

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_PREVIOUS_MENU = 10

CONSUMER_KEY = 'DiQUYaXwuYKXO3fwrhlVig'
CONSUMER_SECRET = 'WdjMktKi6MVt5fwcgKxzPQJhqbSNA3I37PrPgCsdMo'
ACCESS_KEY = '364842064-FJ5D5SqvmQpmwNytdYOtyIhtC8JZtc2uDdbgROAv'
ACCESS_SECRET = 'zITrDfjdeSUOfsor8YTJiOeQKq9ITWNAdgTqgcpWvPA'
 #（上4行は、すでに発行してもらっているものをコピペ）
file_run = ""
class MyClass(xbmcgui.WindowXML):
	#def onInit(self):
	def onInit(self):
		self.strActionInfo = xbmcgui.ControlLabel(100, 120, 200, 200, '', 'font13', '0xFFFF00FF')
		self.addControl(self.strActionInfo)
		self.strActionInfo.setLabel('Push BACK to quit')
		self.button0 = xbmcgui.ControlButton(250, 100, 80, 30, "HELLO")
		self.addControl(self.button0)
		self.button1 = xbmcgui.ControlButton(250, 200, 80, 30, "HELLO2")
		self.addControl(self.button1)
		self.button2 = xbmcgui.ControlButton(450, 200, 80, 30, "HELLO3")
		self.addControl(self.button2)
		self.setFocus(self.button0)
		self.button0.controlDown(self.button1)
		self.button1.controlUp(self.button0)
		self.button1.controlRight(self.button2)
		self.button2.controlLeft(self.button1)
		self.telop = self.getControl(101)
		print "telop",self.telop
		print "twitter of telop is ", twittertext
		self.telop.setLabel(twittertext)
		self.file_run ='/root/douga/IronMan2.mp4'
	
	def onAction(self, action):
		if action == ACTION_PREVIOUS_MENU:
			self.close()
 
	def onClick(self, controlID):
		"""
            Notice: onClick not onControl
            Notice: it gives the ID of the control not the control object
        """
		print "controlID", self.button0.getId()
		if controlID == self.button0.getId():
			print 'you pushed the 1st button'
			self.message('you pushed the 1st button')
			xbmc.executebuiltin(self.file_run)
			#self.show()
			#print "self.show()"
		if controlID == self.button1.getId():
			self.message('you pushed the 2nd button')
			xbmc.Player().play(self.file_run) 
			#self.show()
			#print "self.show()"
			winid = xbmcgui.getCurrentWindowDialogId()
			print "winid",winid
			
		if controlID == self.button2.getId():
			self.message('you pushed the 3rd button')
	 
	def message(self, message):
		dialog = xbmcgui.Dialog()
		dialog.ok(" My message title", message)
		

while 1:
	try:
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
		api = tweepy.API(auth, api_root='/1.1')
		break
	except:
		print 'tweepy error!!!!'
		time.sleep(60)
	
imgurl = ''
slid_run_flag = 0
slid_run = 'Slideshow(' + '/root/mysn/slid' + '/)'
slid_stop = 'Action(PreviousMenu)'
twittertext_old = ''
imgfile = ''
yt = YouTube()
url = ''
hasvideo_flg = 0
while 1:
	time.sleep(15)
	while 1:
		try:	
			twstatus = api.user_timeline(screen_name="cubiesignage")[0]
			twittertext =twstatus.text.encode('utf_8')
			ent = twstatus.entities
			break
		except:
			print 'tweepy error!!!!'
			time.sleep(30)
	
	# get the image	
	imgurl = ''
	try:
		media = ent[u'urls']
		media_url = media[0][u'url'].encode('utf_8')
		print 'media url', media_url
		twittertext = twittertext.replace(media_url,'')
		print 'twittertext', twittertext
		imgurl = media[0][u'media_url_https']
		imgfile = imgurl.replace('https://pbs.twimg.com/media/', '')
		print 'imgfile', imgfile
		imgurl = imgurl + ':large'
		print 'imgurl', imgurl
	except:
		print 'There is no image in the tweet.'
	
	#get the video
	hasvideo_flg = 0
	try:
		url = ent[u'urls'][0]
		exp_url = url[u'expanded_url'].encode('utf_8')
		if exp_url.find(u'youtu.be') != -1:
			videoid = exp_url.replace('http://youtu.be/','')
			video_watch_url = 'http://www.youtube.com/watch?v=' + videoid
			yt.url = video_watch_url
			print 'yt.url', yt.url
			YoutubeVideo = yt.get('mp4', '720p')
			print 'YoutubeVideo.url', YoutubeVideo.url
			hasvideo_flg = 1
	except Exception,e:
		print 'Error:', str(e)
		print 'There is no video in the tweet.'
	
	if twittertext == '' or twittertext == twittertext_old:
		print 'There is no new tweet.'
	else:
		#Update twittertext
		builtin = 'UpdateTwitter(' + twittertext + ')'
		print 'builtin', builtin
		xbmc.executebuiltin(builtin)
		for (root, dirs, files) in os.walk('/root/mysn/slid/', topdown=False):
			for f in files:
				os.remove(os.path.join(root, f))
						
	print "twitter is ", twittertext
	twittertext_old = twittertext

	imgfilepath = '/root/mysn/slid/' + imgfile
	print 'imgfilepath', imgfilepath
	imgsexists = os.path.exists(imgfilepath)
	print 'imgsexists', imgsexists
	if (imgurl != '') and (imgsexists == False) and (hasvideo_flg == 0):
		print 'slid show update!!'
		try:
			urllib.urlretrieve(imgurl, '/root/mysn/slid/' + imgfile)

		except IOError:
			try:
				imgurl = imgurl.replace(':large', '')
				urllib.urlretrieve(imgurl, '/root/mysn/slid/' + imgfile)
			except IOError:
				print 'IOError!!'
		#stop and run the slidshow		
		xbmc.executebuiltin(slid_stop)					
		xbmc.executebuiltin(slid_run)
	
	print 'hasvideo_flg', hasvideo_flg
	if  hasvideo_flg != 0 and xbmc.Player().isPlaying() != True:
		print 'video start!'
		#xbmc.Player().play('/root/mysn/video/Perfume.mp4')	
		xbmc.Player().play(YoutubeVideo.url)
	
#mydisplay = MyClass("Custom_Overlay1.xml", "/root/mysn/", "DefaultSkin")
#mydisplay .doModal()
#print "setLabel "
#mydisplay.telop.setLabel(twittertext)
#del mydisplay
