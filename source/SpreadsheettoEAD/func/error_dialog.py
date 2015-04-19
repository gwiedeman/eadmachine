"""This module, when imported, overrides the default unhandled exception hook
with one that displays a fancy wxPython error dialog."""

import sys
import textwrap
import traceback
import winsound

import wx

def custom_excepthook(exception_type, value, tb):
    dialog = ExceptionDialog(exception_type, value, tb)
    dialog.ShowModal()


class ExceptionDialog(wx.Dialog):
    """This class displays an error dialog with details information about the
    input exception, including a traceback."""

    def __init__(self, exception_type, exception, tb):
        wx.Dialog.__init__(self, None, -1, title="Unhandled error",
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetSize((640, 480))
        self.SetMinSize((420, 200))

        self.exception = (exception_type, exception, tb)
        self.initialize_ui()

        winsound.MessageBeep(winsound.MB_ICONHAND)

    def initialize_ui(self):
        extype, exception, tb = self.exception

        panel = wx.Panel(self, -1)

        # Create the top row, containing the error icon and text message.
        top_row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        error_bitmap = wx.ArtProvider.GetBitmap(
            wx.ART_ERROR, wx.ART_MESSAGE_BOX
        )
        error_bitmap_ctrl = wx.StaticBitmap(panel, -1)
        error_bitmap_ctrl.SetBitmap(error_bitmap)

        message_text = textwrap.dedent("""\
            I'm afraid there has been an unhandled error. This may be a problem with EADMachine, 
			or you may be using uncommon EAD encoding that is not supported. If you would like to 
			help fix these issues, please send the contents of the text control below along with the XML 
			files you are using to the developer at GWiedeman@Albany.edu.\
        """)
        message_label = wx.StaticText(panel, -1, message_text)

        top_row_sizer.Add(error_bitmap_ctrl, flag=wx.ALL, border=10)
        top_row_sizer.Add(message_label, flag=wx.ALIGN_CENTER_VERTICAL)

        # Create the text control with the error information.
        exception_info_text = textwrap.dedent("""\
            Exception type: {}

            Exception: {}

            Traceback:
            {}\
        """)
        exception_info_text = exception_info_text.format(
            extype, exception, ''.join(traceback.format_tb(tb))
        )

        text_ctrl = wx.TextCtrl(panel, -1,
                                style=wx.TE_MULTILINE | wx.TE_DONTWRAP)
        text_ctrl.SetValue(exception_info_text)

        # Create the OK button in the bottom row.
        ok_button = wx.Button(panel, -1, 'OK')
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=ok_button)
        ok_button.SetFocus()
        ok_button.SetDefault()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(top_row_sizer)
        # sizer.Add(message_label, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND)
        sizer.Add(ok_button, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

        panel.SetSizer(sizer)

    def on_ok(self, event):
        self.Destroy()