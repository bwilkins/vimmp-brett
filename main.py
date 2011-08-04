#coding: utf-8

# vimmp - vim client for xmms2 and mpd
# Copyright (C) 2008 Xin Wang <wxyzin@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import vim
import vimmp

def vimmp_toggle():
    global g_vimmp

    winnum = vim.eval('bufwinnr("__VIMMP__")')
    # If bufwinnr returns -1, then there's no window named __VIMMP__,
    # so we create one, otherwise we close it.
    if winnum == '-1':
        try:
            g_vimmp.create_window()
        except NameError:
            g_vimmp = vimmp.VimMP()
            vimmp_keymap()
            vim.command('au WinEnter __VIMMP__ py g_vimmp.refresh_window()')
            vim.command('au CursorHold * py g_vimmp.refresh_window_if_open()')
    else:
        # If current window is __VIMMP__, we close it directly.
        # But when the cursor is in other window, we first remember
        # the window number, and jump to __VIMMP__, close it,
        # then jump back to previous window.
        bufname = vim.current.buffer.name
        if bufname != None and bufname.endswith('__VIMMP__'):
            # We close __VIMMP__ only when there are other windows exists.
            if len(vim.windows) > 1:
                vim.command('close')
        else:
            prevbuf = vim.eval('bufnr("%")')
            vim.command(winnum + 'wincmd w')
            vim.command('close')
            prevwin = vim.eval('bufwinnr(%s)' % prevbuf)
            if vim.eval('winnr()') != prevwin:
                vim.command(prevwin + 'wincmd w')

def vimmp_keymap():
    """Key mappings."""
    mapcmd = 'nnoremap <buffer> <silent> %s :py g_vimmp.%s()<cr>'
    maplist = [
        ('r',       'refresh_window'),
        ('<space>', 'play'),
        ('<cr>',    'play'),
        ('=',       'increase_volume'),
        ('-',       'decrease_volume'),
        ('la',      'add_path'),
        ('lc',      'clear_playlist'),
        ('ld',      'delete'),
        ('lf',      'shuffle_playlist'),
        ('ll',      'load_playlist'),
        ('ln',      'save_playlist'),
        ('ls',      'sort_playlist'),
        ('cp',      'pause_play'),
        ('cr',      'set_repeat_mode'),
        ('cs',      'stop_play'),
        ('<2-leftmouse>', 'play'),
    ]

    for item in maplist:
        vim.command(mapcmd % item)
