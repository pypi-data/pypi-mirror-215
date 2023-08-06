# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Oct 29 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

from .controls import LogTreeCtrl
import wx
import wx.xrc

###########################################################################
## Class LogConfigPanelUI
###########################################################################

class LogConfigPanelUI ( wx.Panel ):

    def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
        wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

        sizer_main = wx.BoxSizer( wx.VERTICAL )

        self.logTreeCtrl = LogTreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_NO_LINES|wx.TR_TWIST_BUTTONS|wx.BORDER_NONE )
        sizer_main.Add( self.logTreeCtrl, 1, wx.EXPAND, 0 )

        self.btn_refresh = wx.Button( self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
        sizer_main.Add( self.btn_refresh, 0, wx.ALL, 5 )

        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.lbl_currentLogger = wx.StaticText( self, wx.ID_ANY, u"Current Logger", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lbl_currentLogger.Wrap( -1 )

        fgSizer1.Add( self.lbl_currentLogger, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.txt_currentLogger = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
        fgSizer1.Add( self.txt_currentLogger, 0, wx.ALL|wx.EXPAND, 5 )

        self.lbl_currentLevel = wx.StaticText( self, wx.ID_ANY, u"Current Level", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lbl_currentLevel.Wrap( -1 )

        fgSizer1.Add( self.lbl_currentLevel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        choice_currentLevelChoices = [ u"CRITICAL", u"ERROR", u"WARNING", u"INFO", u"DEBUG", u"NOTSET" ]
        self.choice_currentLevel = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_currentLevelChoices, 0 )
        self.choice_currentLevel.SetSelection( 0 )
        self.choice_currentLevel.Enable( False )

        fgSizer1.Add( self.choice_currentLevel, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.lbl_rootLevel = wx.StaticText( self, wx.ID_ANY, u"Root Level", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lbl_rootLevel.Wrap( -1 )

        fgSizer1.Add( self.lbl_rootLevel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        choice_rootLevelChoices = [ u"CRITICAL", u"ERROR", u"WARNING", u"INFO", u"DEBUG", u"NOTSET" ]
        self.choice_rootLevel = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_rootLevelChoices, 0 )
        self.choice_rootLevel.SetSelection( 0 )
        fgSizer1.Add( self.choice_rootLevel, 0, wx.ALL|wx.EXPAND, 5 )

        self.lbl_format = wx.StaticText( self, wx.ID_ANY, u"Format", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lbl_format.Wrap( -1 )

        fgSizer1.Add( self.lbl_format, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.txt_format = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txt_format.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer1.Add( self.txt_format, 0, wx.ALL|wx.EXPAND, 5 )


        sizer_main.Add( fgSizer1, 0, wx.EXPAND, 5 )


        self.SetSizer( sizer_main )
        self.Layout()

        # Connect Events
        self.logTreeCtrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_logTreeCtrl_SelChanged )
        self.btn_refresh.Bind( wx.EVT_BUTTON, self.on_btn_refresh )
        self.txt_currentLogger.Bind( wx.EVT_UPDATE_UI, self.on_Update_currentLogger )
        self.choice_currentLevel.Bind( wx.EVT_CHOICE, self.on_choice_currentLevel )
        self.choice_currentLevel.Bind( wx.EVT_UPDATE_UI, self.on_Update_currentLevel )
        self.choice_rootLevel.Bind( wx.EVT_CHOICE, self.on_choice_rootLevel )
        self.choice_rootLevel.Bind( wx.EVT_UPDATE_UI, self.on_Update_rootLevel )
        self.txt_format.Bind( wx.EVT_TEXT, self.on_format )
        self.txt_format.Bind( wx.EVT_UPDATE_UI, self.on_Update_format )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def on_logTreeCtrl_SelChanged( self, event ):
        event.Skip()

    def on_btn_refresh( self, event ):
        event.Skip()

    def on_Update_currentLogger( self, event ):
        event.Skip()

    def on_choice_currentLevel( self, event ):
        event.Skip()

    def on_Update_currentLevel( self, event ):
        event.Skip()

    def on_choice_rootLevel( self, event ):
        event.Skip()

    def on_Update_rootLevel( self, event ):
        event.Skip()

    def on_format( self, event ):
        event.Skip()

    def on_Update_format( self, event ):
        event.Skip()


