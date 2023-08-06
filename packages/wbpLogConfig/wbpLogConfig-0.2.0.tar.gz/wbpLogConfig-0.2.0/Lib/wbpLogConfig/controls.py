"""
controls
===============================================================================

Implementation of the custom controls used by the wbpLogConfig plugin.
"""
from logging import Logger, root, PlaceHolder

import wx
from wx.lib.mixins.treemixin import VirtualTree


class LogTreeCtrl(VirtualTree, wx.TreeCtrl):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TR_DEFAULT_STYLE,
        validator=wx.DefaultValidator,
        name="LogTreeCtrl",
    ):
        style |= wx.TR_HIDE_ROOT
        super().__init__(
            parent=parent,
            id=id,
            pos=pos,
            size=size,
            style=style,
            validator=validator,
            name=name,
        )
        self.imageList = wx.ImageList(16, 16)
        self.img_empty = None
        self.img_logger = None
        self.CreateImageList()
        self.RefreshItems()

    def CreateImageList(self):
        size = 16
        self.img_empty = self.imageList.Add(
            wx.Bitmap.FromRGBA(
                size, size, red=0xCC, green=0xCC, blue=0xCC, alpha=wx.ALPHA_OPAQUE
            )
        )
        self.img_logger = self.imageList.Add(
            wx.Bitmap.FromRGBA(
                size, size, red=0x03, green=0x72, blue=0x30, alpha=wx.ALPHA_OPAQUE
            )
        )
        self.AssignImageList(self.imageList)


    def makeItem(self, name):
        if "." in name:
            label, tail = name.split(".", 1)
            return [label, [self.makeItem(tail)]]
        return [name, []]

    def insertInTree(self, item, tree):
        if tree:
            for _label, _tree in tree:
                if _label == item[0]:
                    for _item in item[1]:
                        self.insertInTree(_item, _tree)
                    _tree.sort()
                    return
        tree.append(item)

    @property
    def logTree(self):
        tree = []
        for name in sorted(root.manager.loggerDict):
            item = self.makeItem(name)
            self.insertInTree(item, tree)
        return tree

    @property
    def selectedLogger(self):
        if self.Selection:
            return self.getLogger(self.GetIndexOfItem(self.Selection))

    def getItem(self, indices):
        text, children = "Hidden root", self.logTree
        for index in indices:
            text, children = children[index]
        return text, children

    def getLogger(self, indices):
        parts = []
        tree = self.logTree
        for i in indices:
            try:
                name, tree = tree[i]
            except IndexError:
                continue
            parts.append(name)
        name = ".".join(parts)
        return root.manager.loggerDict.get(name)

    def OnGetItemText(self, index, column=0):
        return self.getItem(index)[0]

    def OnGetItemImage(self, index, which=wx.TreeItemIcon_Normal, column=0):
        logger = self.getLogger(index)
        if isinstance(logger, Logger):
            return self.img_logger
        if isinstance(logger, PlaceHolder):
            return self.img_empty
        return -1

    def OnGetChildrenCount(self, index):
        return len(self.getItem(index)[1])
