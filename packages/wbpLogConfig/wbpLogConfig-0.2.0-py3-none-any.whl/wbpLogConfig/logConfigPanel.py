"""
logConfigPanel
===============================================================================

Implementation of the main panel used by the wbpLogConfig plugin.
"""
import logging

import wx

from .logConfigPanelUI import LogConfigPanelUI

log = logging.getLogger(__name__)


class LogConfigPanel(LogConfigPanelUI):

    @property
    def handler(self):
        for h in logging.root.handlers:
            if h.name == wx.GetApp().AppName + " - Console":
                return h

    # --------------------------------------------------------------------------
    # Event Handler
    # --------------------------------------------------------------------------

    def on_logTreeCtrl_SelChanged(self, event):
        logger = self.logTreeCtrl.selectedLogger
        if isinstance(logger, logging.Logger):
            self.txt_currentLogger.Value = logger.name
            log.info(
                "current logger: %s, effective level: %s",
                logger.name,
                logging.getLevelName(logger.getEffectiveLevel()),
            )
        else:
            log.info("no current logger")
        # event.Skip()

    def on_btn_refresh(self, event):
        self.logTreeCtrl.RefreshItems()

    def on_Update_currentLogger(self, event):
        logger = self.logTreeCtrl.selectedLogger
        if isinstance(logger, logging.Logger):
            self.txt_currentLogger.Value = logger.name
        else:
            self.txt_currentLogger.Value = ""

    def on_choice_currentLevel(self, event):
        logger = self.logTreeCtrl.selectedLogger
        if isinstance(logger, logging.Logger):
            logger.setLevel(self.choice_currentLevel.StringSelection)
            log.info(
                "Log-Level for %s set to %s",
                logger.name,
                logging.getLevelName(logger.level),
            )

    def on_Update_currentLevel(self, event):
        logger = self.logTreeCtrl.selectedLogger
        if isinstance(logger, logging.Logger):
            event.Enable(True)
            level = logging.getLevelName(logger.level)
            if level != self.choice_currentLevel.StringSelection:
                self.choice_currentLevel.SetStringSelection(level)
        else:
            self.choice_currentLevel.SetSelection(wx.NOT_FOUND)
            event.Enable(False)

    def on_choice_rootLevel(self, event):
        logging.root.setLevel(self.choice_rootLevel.StringSelection)
        log.info(
            "Log-Level for root logger set to %s",
            logging.getLevelName(logging.root.level),
        )

    def on_Update_rootLevel(self, event):
        level = logging.getLevelName(logging.root.level)
        if level != self.choice_rootLevel.StringSelection:
            self.choice_rootLevel.SetStringSelection(level)

    def on_format(self, event):
        handler = self.handler
        if handler and self.txt_format.Value != handler.formatter._fmt:
            handler.formatter = logging.Formatter(self.txt_format.Value)

    def on_Update_format(self, event):
        handler = self.handler
        if handler and self.txt_format.Value != handler.formatter._fmt:
            self.txt_format.Value = handler.formatter._fmt
