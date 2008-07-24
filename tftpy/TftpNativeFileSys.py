import os
from TftpShared import TftpException, logger

class TftpNativeFileSys(object):
    """This class implements the access functions to the filesystem. It
    ensures that all access remains within the root directory tree."""

    def __init__(self, root):
        """Class constructor. It takes a single argument, which is
        the path to the root directory to serve files from and/or write
        them to."""
        self.root = os.path.abspath(root)
        if os.path.exists(self.root):
            logger.debug("tftproot %s does exist" % self.root)
            if not os.path.isdir(self.root):
                raise TftpException, "The tftproot must be a directory."
            else:
                logger.debug("tftproot %s is a directory" % self.root)
                if os.access(self.root, os.R_OK):
                    logger.debug("tftproot %s is readable" % self.root)
                else:
                    raise TftpException, "The tftproot must be readable"
                if os.access(self.root, os.W_OK):
                    logger.debug("tftproot %s is writable" % self.root)
                else:
                    logger.warning("The tftproot %s is not writable" % self.root)
        else:
            raise TftpException, "The tftproot does not exist."

    def get_path(self, path):
        """Return an abstract file system path object from the relative string
        path."""
        return TftpNativeFilePath(self, path)

class TftpNativeFilePath(object):
    """This class implements the access functions to a certain native file
    path."""

    def __init__(self, file_sys, path):
        """Class constructor. It takes a single argument, which is
        the path to the root directory to serve files from and/or write
        them to."""
        self.file_sys = file_sys
        self.path = path
        self.full_path = os.path.abspath(self.file_sys.root + os.path.sep \
                + path)
        logger.debug("The absolute path is %s" % self.full_path)

    def safe(self):
        """This method checks whether the specified path lies within the
        root tree."""
        # Security check. Make sure it's prefixed by the tftproot.
        if self.full_path.find(self.file_sys.root) == 0:
            logger.debug("The path appears to be safe: %s" % self.full_path)
            return True
        else:
            return False

    def exists(self):
        """This method checks whether path actually exists."""
        return os.path.exists(self.full_path)

    def open_read(self):
        """This method returns a file-like object with read-access to the
        path."""
        return open(self.full_path, "rb")

    def get_path(self):
        return self.path

    def get_full_path(self):
        return self.full_path

    def get_size(self):
        return os.stat(self.full_path).st_size

    def __str__(self):
        return self.full_path

# vim:set sw=4 et sts=4:
