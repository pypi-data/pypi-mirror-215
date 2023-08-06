import logging

import wx
from wbBase.control import PanelMixin
from wx import aui
from wx.html2 import (
    WEBVIEWIE_EMU_IE11,
    WebView,
    WebViewBackendDefault,
    WebViewBackendEdge,
    WebViewBackendIE,
)

log = logging.getLogger(__name__)

__version__ = "0.2.3"

name = "HTML"


class HtmlWin(wx.Panel, PanelMixin):
    def __init__(self, parent: wx.Window):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        WebView.MSWSetEmulationLevel(WEBVIEWIE_EMU_IE11)
        self.backend = WebViewBackendDefault
        if WebView.IsBackendAvailable(WebViewBackendEdge):
            self.backend = WebViewBackendEdge
        elif WebView.IsBackendAvailable(WebViewBackendIE):
            self.backend = WebViewBackendIE
        self.webView = WebView.New(self, backend=self.backend)
        sizer.Add(self.webView, 1, wx.EXPAND)
        self.SetSizer(sizer)


HTMLinfo = aui.AuiPaneInfo()
HTMLinfo.Name(name)
HTMLinfo.Caption(name)
HTMLinfo.Dock()
HTMLinfo.Bottom()
HTMLinfo.Resizable()
HTMLinfo.MaximizeButton(True)
HTMLinfo.MinimizeButton(True)
HTMLinfo.CloseButton(False)
HTMLinfo.FloatingSize(wx.Size(300, 200))
HTMLinfo.BestSize(wx.Size(800, 400))
HTMLinfo.MinSize(wx.Size(200, 100))
HTMLinfo.Icon(wx.ArtProvider.GetBitmap("HTML_FILE", wx.ART_FRAME_ICON))

panels = [(HtmlWin, HTMLinfo)]
