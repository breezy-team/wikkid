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

"""Interfaces for the different resource types."""

from zope.interface import Attribute, Interface


class IResource(Interface):
    """The base resource interface."""

    path = Attribute('The full path for the resource.')

    title = Attribute(
        'The title of the resource. '
        'The title is shown in the web title bar.')

    write_filename = Attribute(
        'The full path of the file to write to in the filestore. '
        'This is either the filename as it directly corresponds to the '
        'path, or a related wiki page location.')


class IFileResource(IResource):
    """A resource that relates to a file in the filestore."""

    # TODO: think of a better variable name.
    file_resource = Attribute(
        'An IFile representing the file in the filestore.')


class IDirectoryResource(IResource):
    """A resource that relates to a file in the filestore."""

    # TODO: think of a better variable name.
    dir_resource = Attribute(
        'An IFile representing the directory in the filestore.')


class IRootResource(IDirectoryResource):
    """A special resource relating to the root object in the wiki."""


class IBinaryFile(IFileResource):
    """A marker interface for binary files."""


class ITextFile(IFileResource):
    """A marker interface for text files."""


class IWikiTextFile(ITextFile):
    """A marker interface for a wiki text file."""


class IMissingResource(IResource):
    """A resource that doesn't exist in the filestore."""
