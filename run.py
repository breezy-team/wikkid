#! /usr/bin/python
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

"""The server class for the wiki."""

import atexit
import logging
import optparse
import os
import shutil
import sys
import tempfile

from bzrlib.workingtree import WorkingTree

from wikkid.bzr.filestore import FileStore
from wikkid.bzr.user import UserFactory
from wikkid.server import Server
from wikkid.twistedserver import TwistedServer


def setup_logging():
    """Set up a logger sending to stderr."""
    handler = logging.StreamHandler(strm=sys.stderr)
    fmt = '%(asctime)s %(levelname)-7s %(message)s'
    formatter = logging.Formatter(
        fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)


def main(args):
    parser = optparse.OptionParser(
        description="Run a Wikkid Wiki server.")
    parser.add_option('--branch', help='The branch to use as a wiki.')
    parser.add_option('--port', type='int', default=8080,
                      help='The port to listen on.  Defaults to 8080.')
    options, args = parser.parse_args(sys.argv[1:])
    if len(args):
        print "Unexpected positional args:", args
        sys.exit(1)
    setup_logging()
    logger = logging.getLogger('wikkid')
    logger.setLevel(logging.DEBUG)

    # Overwrite the bzr home env.
    temp_dir = tempfile.mkdtemp(prefix='wikkid')
    logger.debug('Using %s for bzr home.', temp_dir)
    os.environ['BZR_HOME'] = temp_dir
    atexit.register(shutil.rmtree, temp_dir, True)

    working_tree = WorkingTree.open(options.branch)
    logger.info('Using: %s', working_tree)
    filestore = FileStore(working_tree)
    server = TwistedServer(
        Server(filestore),
        UserFactory(working_tree.branch),
        port=options.port)
    server.run()


if __name__ == "__main__":
    main(sys.argv)
