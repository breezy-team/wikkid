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

"""Tests for the wikkid.server."""

from testtools import TestCase

from wikkid.interfaces import FileType
from wikkid.page import (
    BinaryFile,
    DirectoryListingPage,
    MissingPage,
    OtherTextPage,
    WikiPage,
    )
from wikkid.server import Server
from wikkid.tests.fakes import TestUserFactory
from wikkid.volatile.filestore import FileStore

# TODO: make a testing filestore that can produce either a volatile filestore
# or a bzr filestore.


class TestServer(TestCase):
    """Tests for the Wikkid Server.

    I'm going to write a few notes here.  I want to make sure that the server
    has meaningful names, but also is functional enough.  I have been thinking
    over the last few days that the IFile inteface needs to expose the file-id
    of the underlying file for those cases where the file is moved by one
    person, and edited by another.  I makes sense to use the functionality of
    bzr here to have good editing while moving the file.

    Also since I want this designed in a way that it will integrate well into
    Launchpad, we need to expose partial rendering of the underlying files
    through the interface.  There may well be images or binaries stored as
    part of the branch that need to be served directly (or as directly as
    possible), but also we need to be able to access the rendered page before
    any rendering into a skin.

    I want to provide meaningful directory type listings, but that also means
    doing the on-the-fly conversion of files to 'wiki pages'.  We then want to
    be able to traverse a directory, and product a list of tuples (or objects)
    which define the display name, filename, and mimetype.

    Wiki pages are going to be quite tightly defined.  Must have a wiki name
    (Sentence case joined word), ending in '.txt'.

    What should we do about HTML files that are stored in the branch?
    """

    def make_server(self, content=None):
        """Make a server with a volatile filestore."""
        filestore = FileStore(content)
        return Server(filestore, TestUserFactory())

    def test_missing_resource(self):
        # If the path doesn't exist in the filestore, then the resoruce info
        # shows a missing status.
        server = self.make_server()
        info = server.get_info('/a-file')
        self.assertEqual(FileType.MISSING, info.file_type)
        self.assertEqual('a-file', info.path)
        self.assertIs(None, info.resource)

    def test_text_file(self):
        # A normal text file is text/plain.
        server = self.make_server([
                ('readme.txt', 'A readme file.')])
        info = server.get_info('/readme.txt')
        self.assertEqual(FileType.TEXT_FILE, info.file_type)
        self.assertEqual('readme.txt', info.path)
        self.assertIsNot(None, info.resource)

    def test_get_page_directory(self):
        # A directory
        server = self.make_server([
                ('some-dir/', None),
                ])
        page = server.get_page('/some-dir')
        self.assertIsInstance(page, DirectoryListingPage)

    def test_get_page_source_file(self):
        # A text file that isn't .txt
        server = self.make_server([
                ('test.cpp', '// Some source'),
                ])
        page = server.get_page('/test.cpp')
        self.assertIsInstance(page, OtherTextPage)

    def test_get_page_wiki_page(self):
        # wiki pages end with a .txt
        server = self.make_server([
                ('a-wiki-page.txt', "Doesn't need caps."),
                ])
        page = server.get_page('/a-wiki-page.txt')
        self.assertIsInstance(page, WikiPage)

    def test_get_page_missing_page(self):
        # A missing file renders a missing page view.
        server = self.make_server()
        page = server.get_page('/Missing')
        self.assertIsInstance(page, MissingPage)

    def test_get_page_wiki_no_suffix(self):
        # A wiki page can be accessed without the .txt
        server = self.make_server([
                ('WikiPage.txt', "Works with caps too."),
                ])
        page = server.get_page('/WikiPage')
        self.assertIsInstance(page, WikiPage)

    def test_get_page_wiki_with_matching_dir(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('WikiPage.txt', "Works with caps too."),
                ('WikiPage/SubPage.txt', "A sub page."),
                ])
        page = server.get_page('/WikiPage')
        self.assertIsInstance(page, WikiPage)
        self.assertEqual('/WikiPage', page.path)
        self.assertEqual('WikiPage.txt', page.resource.path)

    def test_get_page_wiki_in_subdir(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('WikiPage/SubPage.txt', "A sub page."),
                ])
        page = server.get_page('/WikiPage/SubPage')
        self.assertIsInstance(page, WikiPage)

    def test_get_page_root_path_no_front_page(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server()
        page = server.get_page('/')
        self.assertIsInstance(page, MissingPage)
        self.assertEqual('/FrontPage', page.path)

    def test_get_page_root_file_exists(self):
        # If the path matches a directory, but the .txt file exists with the
        # same name, then return return the wiki page.
        server = self.make_server([
                ('FrontPage.txt', "The first page."),
                ])
        page = server.get_page('/')
        self.assertIsInstance(page, WikiPage)
        self.assertEqual('/FrontPage', page.path)
        self.assertEqual('FrontPage.txt', page.resource.path)

    def test_get_page_binary_file(self):
        # Images are served as binary files.
        server = self.make_server([
                ('image.png', "An image."),
                ])
        page = server.get_page('/image.png')
        self.assertIsInstance(page, BinaryFile)
