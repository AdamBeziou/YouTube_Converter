from pytube import YouTube
import wx
import subprocess
import threading

def Download(url):
	yt = YouTube(url)
	raw_title = yt.title.split()
	title = '"%s"' % (yt.title)
	yt.streams.filter(progressive=True, file_extension = 'mp4').first().download("Videos")
	subprocess.call("ffmpeg -i Videos/%s.mp4 AudioFiles/%s.mp3" % (title, title))
	return

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size = (-1,-1), style = wx.DEFAULT_FRAME_STYLE)
		
		self.panel = wx.Panel(self)
		self.desc = wx.StaticText(self.panel, label = "Enter the Video's URL:")
		self.url_ctrl = wx.TextCtrl(self.panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.download = wx.Button(self.panel, wx.ID_ANY, "Download", size = (-1,-1))
		self.title = wx.StaticText(self.panel, label = "Ready")
		self.Bind(wx.EVT_BUTTON, self.OnDownload, self.download)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.desc, 0, wx.CENTER, 5)
		self.sizer.Add(self.url_ctrl, 0, wx.CENTER, 5)
		self.sizer.Add(self.download, 0 ,wx.CENTER, 5)
		self.sizer.Add(self.title, 0, wx.CENTER, 5)
		
		self.sizer.SetSizeHints(self.panel)
		self.panel.SetSizerAndFit(self.sizer)
		
		self.Show(True)
		self.SetMinSize(self.GetSize())
		
	def OnDownload(self, event):
		self.title.SetLabel('Downloading...')
		test = self.url_ctrl.GetValue()
		print(test)
		t = threading.Thread(target = Download, args = (test))
		t.start()
		
		self.title.SetLabel('Download Complete')
		
app = wx.App(False)
frame = MainWindow(None, "YouTube Video Downloader")
app.MainLoop()