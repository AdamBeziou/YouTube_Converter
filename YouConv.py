from pytube import YouTube
import wx
import subprocess
import threading
import os

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
		wx.Frame.__init__(self, parent, title=title, size = (300,100), style = wx.DEFAULT_FRAME_STYLE)
		
		self.panel = wx.Panel(self)
		self.desc = wx.StaticText(self.panel, label = "Enter the Video's URL:")
		self.url_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.download = wx.Button(self.panel, wx.ID_ANY, "Download", size = (-1,-1))
		self.Bind(wx.EVT_BUTTON, self.OnDownload, self.download)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.desc, 0, wx.CENTER, 5)
		self.sizer.Add(self.url_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add(self.download, 0 ,wx.CENTER, 5)
		
		self.sizer.SetSizeHints(self.panel)
		self.panel.SetSizerAndFit(self.sizer)
		
		self.Show(True)
		self.SetMinSize(self.GetSize())
		
	def OnDownload(self, event):
		test = self.url_ctrl.GetValue()
		def TestMe(test):
			yt = YouTube(test)
			raw_title = yt.title
			raw_title = raw_title.translate({ord(x): None for x in ".'"})
			
			title = '"%s"' % (raw_title)
			
			yt.streams.filter(progressive=True, file_extension = 'mp4').first().download("Videos")
			
			subprocess.call("ffmpeg -i Videos/%s.mp4 -vn -acodec libvorbis AudioFiles/%s.mp4" % (title, title))
			return
			
		t = threading.Thread(target = TestMe, args = (test,))
		t.start()
		self.url_ctrl.SetValue("")
		
app = wx.App(False)
frame = MainWindow(None, "YouTube Video Downloader")
app.MainLoop()
