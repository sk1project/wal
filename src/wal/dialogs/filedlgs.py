# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013-2020 by Ihor E. Novikov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import typing as tp

import wx

from .. import const


def get_open_file_name(parent: wx.Window, title: str = '', default_dir: str = '~',
                       wildcard: str = 'All files (*.*)|*;*.*') -> tp.Optional[str]:
    """Shows Open File dialog

    :param parent: (wx.Window) parent window
    :param title: (str) dialog title
    :param default_dir: (str) startup directory path
    :param wildcard: (str) wildcard filtering string
    :return: (str) path to file
    """
    ret = None
    title = '' if const.IS_MAC else (title or 'Open')

    style = wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
    dlg = wx.FileDialog(
        parent, message=title,
        defaultDir=os.path.abspath(os.path.expanduser(default_dir)),
        defaultFile='',
        wildcard=wildcard,
        style=wx.FD_OPEN | style
    )
    dlg.CenterOnParent()
    if dlg.ShowModal() == wx.ID_OK:
        ret = dlg.GetPath()
    dlg.Destroy()
    return ret


def get_save_file_name(parent: wx.Window, path: str, title: str = '',
                       wildcard: str = 'Text files (*.txt)|*.txt') -> tp.Optional[str]:
    """Shows Save File dialog

    :param parent: (wx.Window) parent window
    :param path: (str) default file path
    :param title: (str) dialog title
    :param wildcard: (str) wildcard filtering string
    :return: (str) path to file
    """
    ret = None
    title = '' if const.IS_MAC else (title or 'Save As...')

    path = os.path.abspath(os.path.expanduser(path))
    doc_folder = os.path.dirname(path)
    doc_name = os.path.basename(path)

    style = wx.FD_CHANGE_DIR | wx.FD_OVERWRITE_PROMPT | wx.FD_PREVIEW
    dlg = wx.FileDialog(
        parent, message=title,
        defaultDir=doc_folder,
        defaultFile=doc_name,
        wildcard=wildcard,
        style=wx.FD_SAVE | style
    )
    dlg.CenterOnParent()
    if dlg.ShowModal() == wx.ID_OK:
        ret = (dlg.GetPath(), dlg.GetFilterIndex())
    dlg.Destroy()
    return ret


def get_dir_path(parent: wx.Window, path: str = '~', title: str = '') -> tp.Optional[str]:
    """Shows Select Directory dialog

    :param parent: (wx.Window) parent window
    :param path: (str) startup directory path
    :param title: (str) dialog title
    :return: (str) path to directory
    """
    ret = None

    title = '' if const.IS_MAC else (title or 'Select directory')

    dlg = wx.DirDialog(
        parent, message=title,
        defaultPath=os.path.abspath(os.path.expanduser(path)),
        style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
    )
    dlg.CenterOnParent()
    if dlg.ShowModal() == wx.ID_OK:
        ret = dlg.GetPath()
    dlg.Destroy()
    return ret
