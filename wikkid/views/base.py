#
# Copyright (C) 2010 Wikkid Developers
#
# This file is part of Wikkid.
#
# Wikkid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wikkid.  If not, see <http://www.gnu.org/licenses/>

"""The base view class."""

import logging

class BaseView(object):
    """The base view class.

    This is an abstract base class.
    """

    def __init__(self, skin, resource_info, path, user):
        self.skin = skin
        self.resource = resource_info.resource
        self.file_type = resource_info.file_type
        self.file_path = resource_info.path
        self.request_path = path
        self.user = user
        self.logger = logging.getLogger('wikkid')

    def template_args(self):
        """Needs to be implemented in the derived classes.

        :returns: A dict of values.
        """
        raise {
            'view': self,
            'user': self.user,
            }

    def render(self):
        """Render the page.

        Return a tuple of content type and content.
        """
        template = self.skin.get_template(self.template)
        rendered = template.render(**self.template_args())
        return ('text/html', rendered)
