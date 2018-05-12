from pytube import YouTube
import wx
import subprocess
import threading
import os
import mutagen

if os.access("Videos", os.R_OK):
	pass
else:
	os.makedirs("Videos")

if os.access("AudioFiles", os.R_OK):
	pass
else:
	os.makedirs("AudioFiles")
	
class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size = (-1,-1), style = wx.DEFAULT_FRAME_STYLE)
		
		self.panel = wx.Panel(self)
		
		self.desc = wx.StaticText(self.panel, label = "Enter the Song's URL:")
		self.url_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.album_desc = wx.StaticText(self.panel, label = "Enter the Song's Album:")
		self.album_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.artist_desc = wx.StaticText(self.panel, label = "Enter the Song's Artist:")
		self.artist_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.genre_desc = wx.StaticText(self.panel, label = "Enter the Song's Genre:")
		self.genre_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.download = wx.Button(self.panel, wx.ID_ANY, "Download", size = (-1,-1))
		self.Bind(wx.EVT_BUTTON, self.OnDownload, self.download)
		
		self.download_list = wx.ListCtrl(self.panel, wx.ID_ANY, style = wx.LC_REPORT)
		self.download_list.InsertColumn(0, "Status", width = 100)
		self.download_list.InsertColumn(1, "File", width = wx.LIST_AUTOSIZE_USEHEADER)
		self.pos = 0
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add((0,10), 0)
		self.sizer.Add(self.desc, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.url_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.album_desc, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.album_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.artist_desc, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.artist_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.genre_desc, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.genre_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add((0,5), 0)
		self.sizer.Add(self.download, 0, wx.CENTER, 5)
		self.sizer.Add((0,10), 0)
		self.sizer.Add(self.download_list, 1, wx.CENTER|wx.EXPAND, 5)
		
		self.sizer.SetSizeHints(self.panel)
		self.panel.SetSizerAndFit(self.sizer)
		
		self.Show(True)
		self.SetMinSize(self.GetSize())
		
	def OnDownload(self, event):
		test = self.url_ctrl.GetValue()
		def TestMe(test):
			position = self.pos

			album = self.album_ctrl.GetValue()
			artist = self.artist_ctrl.GetValue()
			genre = self.genre_ctrl.GetValue()
			
			yt = YouTube(test)
			raw_title = yt.title
			raw_title = raw_title.translate({ord(x): None for x in ".',/:"})
			
			title = '\"%s\"' % (raw_title)
			self.download_list.InsertItem(position, "Downloading...")
			self.download_list.SetItem(position, 1, title)
			
			yt.streams.filter(progressive=True, file_extension = 'mp4').first().download("Videos")
			
			self.download_list.SetItem(position, 0, "Converting...")
			
			try:
				check = subprocess.run("ffmpeg -i Videos/%s.mp4 -vn -acodec libvorbis AudioFiles/%s.mp4" % (title, title), check = True)
				self.download_list.SetItem(position, 0, "Complete")
			except subprocess.CalledProcessError:
				self.download_list.SetItem(position, 0, "Conversion Failed")

			mp4Obj = mutagen.File("AudioFiles/" + raw_title + ".mp4")
			mp4Obj['\xa9alb'] = album
			mp4Obj['\xa9ART'] = artist
			mp4Obj['\xa9gen'] = genre
			mp4Obj.save()
			
		t = threading.Thread(target = TestMe, args = (test,))
		t.start()
		self.url_ctrl.SetValue("")
		self.pos += 1
		
app = wx.App(False)
frame = MainWindow(None, "YouTube Video Downloader")
app.MainLoop()