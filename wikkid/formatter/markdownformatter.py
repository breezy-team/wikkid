# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Wikkid Developers.
#
# This software is licensed under the GNU Affero General Public License
# version 3 (see the file LICENSE).

"""A text to html formatter using markdown."""

import cgi
import markdown
from zope.interface import implements

from wikkid.interface.formatter import ITextFormatter


class MarkdownFormatter(object):
    """Format source files as HTML using markdown."""

    implements(ITextFormatter)

    def format(self, filename, text):
        """Format the text.
        """
        md = markdown.Markdown(safe_mode='replace')
        return md.convert(text)

