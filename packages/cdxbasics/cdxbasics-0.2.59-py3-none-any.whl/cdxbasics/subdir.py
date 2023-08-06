"""
subdir
Simple class to keep track of directory sturctures and for automated caching on disk
Hans Buehler 2020

WARNING
This is under development. I have not figured out how to test file i/o on GitHub
"""

from .logger import Logger
from .util import CacheMode, uniqueHash48
_log = Logger(__file__)

import os
import os.path
import uuid
import threading
from functools import wraps
import pickle
import tempfile
import shutil
import datetime
from collections.abc import Collection, Mapping

uniqueFileName48 = uniqueHash48

def _remove_trailing( path ):
    if len(path) > 0:
        if path[-1] in ['/' or '\\']:
            return _remove_trailing(path[:-1])
    return path

class SubDir(object):
    """
    SubDir implements a transparent interface for storing data in files, with a common extension.
    The generic pattern is:

        1) create a root 'parentDir':
            Absolute:                      parentDir = SubDir("C:/temp/root")
            In system temp directory:      parentDir = SubDir("!/root")
            In user directory:             parentDir = SubDir("~/root")
            Relative to current directory: parentDir = SubDir("./root")

        2) Use SubDirs to transparently create hierachies of stored data:
           assume f() will want to store some data:

               def f(parentDir, ...):

                   subDir = parentDir('subdir')    <-- note that the call () operator is overloaded: if a second argument is provided, the directory will try to read the respective file.
                   or
                   subDir = SubDir('subdir', parentDir)
                    :
                    :
            Write data:

                   subDir['item1'] = item1       <-- dictionary style
                   subDir.item2 = item2          <-- member style
                   subDir.write('item3',item3)   <-- explicit

            Note that write() can write to multiple files at the same time.

        3) Reading is similar

                def readF(parentDir,...):

                    subDir = parentDir('subdir')

                    item = subDir('item', 'i1')     <-- returns 'i1' if not found.
                    item = subdir.read('item')      <-- returns None if not found
                    item = subdir.read('item','i2') <-- returns 'i2' if not found
                    item = subDir['item']           <-- throws a KeyError if not found
                    item = subDir.item              <-- throws an AttributeError if not found

        4) Treating data like dictionaries

                def scanF(parentDir,...)

                    subDir = parentDir('f')

                    for item in subDir:
                        data = subDir[item]

            Delete items:

                    del subDir['item']             <-- silently fails if 'item' does not exist
                    del subDir.item                <-- silently fails if 'item' does not exist
                    subDir.delete('item')          <-- silently fails if 'item' does not exist
                    subDir.delete('item', True)    <-- throw a KeyError if 'item' does not exit

        5) Cleaning up

                parentDir.deleteAllContent()       <-- silently deletes all files and sub directories.

        Several other operations are supported; see help()

        Hans Buehler May 2020
    """

    class __RETURN_SUB_DIRECTORY(object):
        pass

    DEFAULT_EXT = "pck"
    DEFAULT_RAISE_ON_ERROR = False
    RETURN_SUB_DIRECTORY = __RETURN_SUB_DIRECTORY     # comparison between classes is unique accross Python name space

    def __init__(self, name : str, parent = None, *, ext : str = None, eraseEverything : bool = False ):
        """
        Creates a sub directory which contains pickle files with a common extension.

        Absolute directories
            sd  = SubDir("!/subdir")           - relative to system temp directory
            sd  = SubDir("~/subdir")           - relative to user home directory
            sd  = SubDir("./subdir")           - relative to current working directory (explicit)
            sd  = SubDir("subdir")             - relative to current working directory (implicit)
            sd  = SubDir("/tmp/subdir")        - absolute path (linux)
            sd  = SubDir("C:/temp/subdir")     - absolute path (windows)
        Short-cut
            sd  = SubDir("")                   - current working directory

        It is often desired that the user specifies a sub-directory name under some common parent directory.
        You can create sub directories if you provide a 'parent' directory:
            sd2 = SubDir("subdir2", parent=sd) - relative to other sub directory
            sd2 = sd("subdir2")                - using call operator
        Works with strings, too:
            sd2 = SubDir("subdir2", parent="~/my_config") - relative to ~/my_config

        All files managed by SubDir will have the same extension.
        The extension can be specified with 'ext', or as part of the directory string:
            sd  = SubDir("~/subdir;*.bin")      - set extension to 'bin'

        COPY CONSTRUCTION
        The function also allows copy construction, and constrution from a repr() string.

        HANDLING KEYS
        SubDirs allows reading data using the item and attribute notation, i.e. we may use
            sd = SubDir("~/subdir")
            x  = sd.x
            y  = sd['y']
        If the respective keys are not found, exceptions are thrown.

        NONE OBJECTS
        It is possible to set the directory name to 'None'. In this case the directory will behave as if:
            No files exist
            Writing fails with a EOFError.


        Parameters
        ----------
            name          - Name of the directory.
                               '.' for current directory
                               '~' for home directory
                               '!' for system default temp directory
                            May contain a formatting string for defining 'ext' on the fly:
                                Use "!/test;*.bin" to specify 'test' in the system temp directory as root directory with extension 'bin'
                            Can be set to None, see above.
            parent         - Parent directory. If provided, will also set defaults for 'ext' and 'raiseOnError'
            ext            - standard file extenson for data files. All files will share the same extension.
                             If None, use the parent extension, or if that is not specified DEFAULT_EXT (pck)
                             Set to "" to turn off managing extensions.
            eraseEverything - delete all contents in the newly defined subdir
        """
        # copy constructor support
        if isinstance(name, SubDir):
            assert parent is None, "Internal error: copy construction does not accept additional keywords"
            self._path = name._path
            self._ext = name._ext if ext is None else ext
            return

        # reconstruction from a dictionary
        if isinstance(name, Mapping):
            assert parent is None, "Internal error: dictionary construction does not accept additional keywords"
            self._path = name['_path']
            self._ext = name['_ext'] if ext is None else ext
            return

        # parent
        if isinstance(parent, str):
            parent = SubDir(parent, ext=ext )
        _log.verify( parent is None or isinstance(parent, SubDir), "'parent' must be SubDir or None. Found object of type %s", type(parent))

        # operational flags
        _name  = name if not name is None else "(none)"

        # extension
        if not name is None:
            _log.verify( isinstance(name, str), "'name' must be string. Found object of type %s", type(name))
            name   = name.replace('\\','/')

            # extract extension information
            ext_i = name.find(";*.")
            if ext_i >= 0:
                _ext = name[ext_i+3:]
                _log.verify( ext is None or ext == _ext, "Canot specify an extension both in the name string ('%s') and as 'ext' ('%s')", _name, ext)
                ext  = _ext
                name = name[:ext_i]
        if ext is None:
            self._ext = ("." + SubDir.DEFAULT_EXT) if parent is None else parent._ext
        else:
            _log.verify( isinstance(ext,str), "Extension 'ext' must be a string. Found type %s", type(ext))
            if len(ext) == 0:
                self._ext = ""
            else:
                _log.verify( not ext in ['.','/','\\'], "Extension 'ext' cannot be '%s'", ext )
                sub, _ = os.path.split(ext)
                _log.verify( len(sub) == 0, "Extension 'ext' '%s' contains directory information", ext)
                self._ext = ("." + ext) if ext[:1] != '.' else ext

        # name
        if name is None:
            if not parent is None and not parent._path is None:
                name = parent._path[:-1]
        else:
            # expand name
            name = _remove_trailing(name)
            if name == "" and parent is None:
                name = "."
            if name[:1] in ['.', '!', '~']:
                _log.verify( len(name) == 1 or name[1] == '/', "If 'name' starts with '%s', then the second character must be '/' (or '\\' on windows). Found 'name' set to '%s'", name[:1], _name)
                if name[0] == '!':
                    name = SubDir.tempDir()[:-1] + name[1:]
                elif name[0] == ".":
                    name = SubDir.workingDir()[:-1] + name[1:]
                else:
                    assert name[0] == "~"
                    name = SubDir.userDir()[:-1] + name[1:]
            elif not parent is None:
                # path relative to 'parent'
                name = (parent._path + name) if not parent.is_none else name

        if name is None:
            self._path = None
        else:
            # expand path
            self._path = os.path.abspath(name) + '/'
            self._path = self._path.replace('\\','/')

            # create directory
            if not os.path.exists( self._path[:-1] ):
                os.makedirs( self._path[:-1] )
            else:
                _log.verify( os.path.isdir(self._path[:-1]), "Cannot use sub directory %s: object exists but is not a directory", self._path[:-1] )
                # erase all content if requested
                if eraseEverything:
                    self.eraseEverything(keepDirectory = True)

    # -- self description --

    def __str__(self) -> str: # NOQA
        if self._path is None: return "(none)"
        return self._path if len(self._ext) == 0 else self._path + ";*" + self._ext

    def __repr__(self) -> str: # NOQA
        if self._path is None: return "SubDir(None)"
        return "SubDir(%s)" % self.__str__()

    def __eq__(self, other) -> bool: # NOQA
        """ Tests equality between to SubDirs, or between a SubDir and a directory """
        if isinstance(other,str):
            return self._path == other
        _log.verify( isinstance(other,SubDir), "Cannot compare SubDir to object of type '%s'", type(other))
        return self._path == other._path and self._ext == other._ext

    def __bool__(self) -> bool:
        """ Returns True if 'self' is set, or False if 'self' is a None directory """
        return not self.is_none

    def __hash__(self) -> str: #NOQA
        return hash( (self._path, self._ext) )

    @property
    def is_none(self) -> bool:
        """ Whether this object is 'None' or not """
        return self._path is None

    @property
    def path(self) -> str:
        """ Return current path, including trailing '/' """
        return self._path

    @property
    def ext(self) -> str:
        """ Returns the common extension of the files in this directory """
        return self._ext

    def fullKeyName(self, key : str) -> str:
        """
        Returns fully qualified key name
        Note this function is not robustified against 'key' containing directory features
        """
        if self._path is None:
            return None
        _log.verify( len(key) > 0, "'key' cannot be empty")
        _log.verify( key.find("/") == -1, "'key' must be a filename without directory information. It cannot contain forward slashes '/'. Found %s", key)
        _log.verify( key.find("\\") == -1, "'key' must be a filename without directory information. It cannot contain backward slashes '\\'. Found %s", key)
        _log.verify( key.find(":") == -1, "'key' must be a filename without directory information. It cannot contain ':'. Found %s", key)
        _log.verify( key.find("~") == -1, "'key' must be a filename without directory information. It cannot contain '~'. Found %s", key)
        _log.verify( key[0] != '!', "'key' must be a filename without directory information. It cannot start with '!'. Found %s", key)

        if len(self._ext) > 0 and key[-len(self._ext):] != self._ext:
            return self._path + key + self._ext
        return self._path + key

    @staticmethod
    def tempDir() -> str:
        """
        Return system temp directory. Short cut to tempfile.gettempdir()
        Result contains trailing '/'
        """
        d = tempfile.gettempdir()
        _log.verify( len(d) == 0 or not (d[-1] == '/' or d[-1] == '\\'), "*** Internal error 13123212-1: %s", d)
        return d + "/"

    @staticmethod
    def workingDir() -> str:
        """
        Return current working directory. Short cut for os.getcwd()
        Result contains trailing '/'
        """
        d = os.getcwd()
        _log.verify( len(d) == 0 or not (d[-1] == '/' or d[-1] == '\\'), "*** Internal error 13123212-2: %s", d)
        return d + "/"

    @staticmethod
    def userDir() -> str:
        """
        Return current working directory. Short cut for os.path.expanduser('~')
        Result contains trailing '/'
        """
        d = os.path.expanduser('~')
        _log.verify( len(d) == 0 or not (d[-1] == '/' or d[-1] == '\\'), "*** Internal error 13123212-3: %s", d)
        return d + "/"

    # -- read --

    def _read( self, reader, key : str, default, raiseOnError : bool ):
        """
        Utility function for read() and readLine()

        Parameters
        ----------
            reader( key, fullFileName, default )
                A function which is called to read the file once the correct directory is identified
                key : key (for error messages, might include '/')
                fullFileName : full file name
                default value
            key : str or list
                str: fully qualified key
                list: list of fully qualified names
            default :
                default value. None is a valid default value
                list : list of defaults for a list of keys
            raiseOnError : bool
                If True, and the file does not exist, throw exception
        """
        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string, or an interable object. Found type %s", type(key))
            l = len(key)
            if default is None or isinstance(default,str) or getattr(default,"__iter__",None) is None:
                default = [ default ] * l
            else:
                _log.verify( len(default) == l, "'default' must have same lengths as 'key', found %ld and %ld", len(default), l )
            return [ self._read(reader=reader,key=k,default=d,raiseOnError=raiseOnError) for k, d in zip(key,default) ]

        # deleted directory?
        if self._path is None:
            _log.verify( not raiseOnError, "Trying to read '%s' from an empty directory object", key)
            return default

        # single key
        _log.verify(len(key) > 0, "'key' missing (the filename)" )
        sub, key = os.path.split(key)
        if len(sub) > 0:
            return SubDir(self,sub)._read(reader,key,default)
        _log.verify(len(key) > 0, "'key' %s indicates a directory, not a file", key)

        # does file exit?
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            if raiseOnError:
                raise KeyError(key)
            return default
        _log.verify( os.path.isfile(fullFileName), "Cannot read %s: object exists, but is not a file (full path %s)", key, fullFileName )

        # read content
        # delete existing files upon read error
        try:
            return reader( key, fullFileName, default )
        except EOFError:
            try:
                os.remove(fullFileName)
                _log.warning("Cannot read %s; file deleted (full path %s)",key,fullFileName)
            except Exception as e:
                _log.warning("Cannot read %s; attempt to delete file failed (full path %s): %s",key,fullFileName,str(e))
        if raiseOnError:
            raise KeyError(key)
        return default

    def read( self, key, default = None, raiseOnError : bool = False ):
        """
        Read pickled data from 'key' if the file exists, or return 'default'
        -- Supports 'key' containing directories
        -- Supports 'key' being iterable.
           In this case any any iterable 'default' except strings are considered accordingly.
           In order to have a unit default which is an iterable, you will have to wrap it in another iterable, e.g.
           E.g.:
              keys = ['file1', 'file2']

              sd.read( keys )
              --> works, both are using default None

              sd.read( keys, 1 )
              --> works, both are using default '1'

              sd.read( keys, [1,2] )
              --> works, defaults 1 and 2, respectively

              sd.read( keys, [1] )
              --> produces error as len(keys) != len(default)

            Strings are iterable but are treated as single value.
            Therefore
                sd.read( keys, '12' )
            means the default value '12' is used for both files.
            Use
                sd.read( keys, ['1','2'] )
            in case the intention was using '1' and '2', respectively.

        Returns the read object, or a list of objects if 'key' was iterable.
        If the current directory is 'None', then behaviour is as if the file did not exist.
        """
        def reader( key, fullFileName, default ):
            with open(fullFileName,"rb") as f:
                return pickle.load(f)
        return self._read( reader=reader, key=key, default=default, raiseOnError=raiseOnError )

    get = read

    def readString( self, key, default = None, raiseOnError = False ):
        """
        Reads text from 'key' or returns 'default'. Removes trailing EOLs
        -- Supports 'key' containing directories#
        -- Supports 'key' being iterable. In this case any 'default' can be a list, too.

        Returns the read string, or a list of strings if 'key' was iterable.
        If the current directory is 'None', then behaviour is as if the file did not exist.

        See additional comments for read()
        """
        def reader( key, fullFileName, default ):
            with open(fullFileName,"r") as f:
                line = f.readline()
                if len(line) > 0 and line[-1] == '\n':
                    line = line[:-1]
                return line
        return self._read( reader=reader, key=key, default=default, raiseOnError=raiseOnError )

    # -- write --

    def _write( self, writer, key, obj, raiseOnError ) -> bool:
        """ Utility function for write() and writeLine() """
        if self._path is None:
            raise EOFError("Cannot write to '%s': current directory is not specified" % key)

        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            l = len(key)
            if obj is None or isinstance(obj,str) or not isinstance(obj, Collection):
                obj = [ obj ] * l
            else:
                _log.verify( len(obj) == l, "'obj' must have same lengths as 'key', found %ld and %ld", len(obj), l )
            ok = True
            for (k,o) in zip(key,obj):
                ok |= self._write( writer, k, o, raiseOnError=raiseOnError )
            return ok

        # single key
        _log.verify(len(key) > 0, "'key is empty (the filename)" )
        sub, key = os.path.split(key)
        _log.verify(len(key) > 0, "'key '%s' refers to a directory, not a file", key)
        if len(sub) > 0:
            return SubDir(self,sub)._write(writer,key,obj, raiseOnError=raiseOnError)

        # write to temp file
        # then rename into target file
        # this reduces collision when i/o operations
        # are slow
        fullFileName = self.fullKeyName(key)
        tmp_file     = uniqueHash48( [ key, uuid.getnode(), os.getpid(), threading.get_ident(), datetime.datetime.now() ] )
        tmp_i        = 0
        fullTmpFile  = self.fullKeyName(tmp_file) + ".tmp"
        while os.path.exists(fullTmpFile):
            fullTmpFile = self.fullKeyName(tmp_file) + "." + str(tmp_i) + ".tmp"
            tmp_i       += 1
            if tmp_i >= 10:
                raise RuntimeError("Failed to generate temporary file for writing '%s': too many temporary files found. For example, this file already exists: '%s'" % ( fullFileName, fullTmpFile ) )

        if not writer( key, fullTmpFile, obj ):
            return False
        if os.path.exists(fullTmpFile):
            try:
                if os.path.exists(fullFileName):
                    os.remove(fullFileName)
                os.rename(fullTmpFile, fullFileName)
            except Exception as e:
                os.remove(fullTmpFile)
                if raiseOnError:
                    raise e
                return False
        return True

    def write( self, key, obj, raiseOnError = True ) -> bool:
        """
        Pickles 'obj' into key.
        -- Supports 'key' containing directories
        -- Supports 'key' being a list.
           In this case, if obj is an iterable it is considered the list of values for the elements of 'keys'
           If 'obj' is not iterable, it will be written into all 'key's

              keys = ['file1', 'file2']

              sd.write( keys, 1 )
              --> works, writes '1' in both files.

              sd.read( keys, [1,2] )
              --> works, writes 1 and 2, respectively

              sd.read( keys, "12" )
              --> works, writes '12' in both files

              sd.write( keys, [1] )
              --> produces error as len(keys) != len(obj)

        If the current directory is 'None', then the function throws an EOFError exception
        """
        def writer( key, fullFileName, obj ):
            try:
                with open(fullFileName,"wb") as f:
                    pickle.dump(obj,f,-1)
            except Exception as e:
                if raiseOnError:
                    raise e
                return False
            return True
        return self._write( writer=writer, key=key, obj=obj, raiseOnError=raiseOnError )

    set = write

    def writeString( self, key, line, raiseOnError = True ) -> bool:
        """
        Writes 'line' into key. A trailing EOL will not be read back
        -- Supports 'key' containing directories
        -- Supports 'key' being a list.
           In this case, line can either be the same value for all key's or a list, too.

        If the current directory is 'None', then the function throws an EOFError exception
        See additional comments for write()
        """
        if len(line) == 0 or line[-1] != '\n':
            line += '\n'
        def writer( key, fullFileName, obj ):
            try:
                with open(fullFileName,"w") as f:
                    f.write(obj)
            except Exception as e:
                if raiseOnError:
                    raise e
                return False
            return True
        return self._write( writer=writer, key=key, obj=line, raiseOnError=raiseOnError )

    # -- iterate --

    def keys(self) -> list:
        """
        Returns a list of keys in this subdirectory with the correct extension.
        Note that the keys do not include the extension themselves.

        In other words, if the extension is ".pck", and the files are "file1.pck", "file2.pck", "file3.bin"
        then this function will return [ "file1", "file2" ]

        This function ignores directories.

        If self is None, then this function returns an empty list.
        """
        if self._path is None:
            return []
        ext_l = len(self._ext)
        keys = []
        with os.scandir(self._path) as it:
            for entry in it:
                if not entry.is_file():
                    continue
                if ext_l > 0:
                    if len(entry.name) <= ext_l or entry.name[-ext_l:] != self._ext:
                        continue
                    keys.append( entry.name[:-ext_l] )
                else:
                    keys.append( entry.name )
        return keys

    def subDirs(self) -> list:
        """
        Returns a list of all sub directories
        If self is None, then this function returns an empty list.
        """
        # do not do anything if the object was deleted
        if self._path is None:
            return []
        subdirs = []
        with os.scandir(self._path[:-1]) as it:
            for entry in it:
                if not entry.is_dir():
                    continue
                subdirs.append( entry.name )
        return subdirs

    # -- delete --

    def delete( self, key, raiseOnError = False ):
        """
        Deletes 'key'; 'key' might be a list.

        Parameters
        ----------
            key : filename, or list of filenames
            raiseOnError : if False, do not throw KeyError if file does not exist. If None, use subdir's default.
        """
        # do not do anything if the object was deleted
        if self._path is None:
            if raiseOnError: raise EOFError("Cannot delete '%s': current directory not specified" % key)
            return
        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            for k in key:
                self.delete(k, raiseOnError=raiseOnError)
            return
        # single key
        _log.verify(len(key) > 0, "'key' is empty" )
        sub, key2 = os.path.split(key)
        _log.verify(len(key2) > 0, "'key' %s indicates a directory, not a file", key)
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            if raiseOnError:
                raise KeyError(key)
        else:
            os.remove(fullFileName)

    def deleteAllKeys( self, raiseOnError = False ):
        """ Deletes all valid keys in this sub directory """
        # do not do anything if the object was deleted
        if self._path is None:
            if raiseOnError: raise EOFError("Cannot delete all files: current directory not specified")
            return
        self.delete( self.keys(), raiseOnError=raiseOnError )

    def deleteAllContent( self, deleteSelf = False, raiseOnError = False ):
        """
        Deletes all valid keys and subdirectories in this sub directory.
        Does not delete files with other extensions.
        Use eraseEverything() if the aim is to delete everything.

        Parameters
        ----------
            deleteSelf: whether to delete the directory or only its contents
            raiseOnError: False for silent failure
        """
        # do not do anything if the object was deleted
        if self._path is None:
            if raiseOnError: raise EOFError("Cannot delete all contents: current directory not specified")
            return
        # delete sub directories
        subdirs = self.subDirs();
        for subdir in subdirs:
            SubDir(subdir, parent=self).deleteAllContent( deleteSelf=True, raiseOnError=raiseOnError )
        # delete keys
        self.deleteAllKeys( raiseOnError=raiseOnError )
        # delete myself
        if not deleteSelf:
            return
        rest = list( os.scandir(self._path[:-1]) )
        txt = str(rest)
        txt = txt if len(txt) < 50 else (txt[:47] + '...')
        if len(rest) > 0:
            _log.verify( not raiseOnError, "Cannot delete my own directory %s: directory not empty: found %ld object(s): %s", self._path,len(rest), txt)
            return
        os.rmdir(self._path[:-1])   ## does not work ????
        self._path = None

    def eraseEverything( self, keepDirectory = True ):
        """
        Deletes the entire sub directory will all contents
        WARNING: deletes ALL files, not just those with the present extension.
        Will keep the subdir itself by default.
        If not, it will invalidate 'self._path'

        If self is None, do nothing. That means you can call this function several times.
        """
        if self._path is None:
            return
        shutil.rmtree(self._path[:-1], ignore_errors=True)
        if not keepDirectory and os.path.exists(self._path[:-1]):
            os.rmdir(self._path[:-1])
            self._path = None
        elif keepDirectory and not os.path.exists(self._path[:-1]):
            os.makedirs(self._path[:-1])

    # -- file ops --

    def exists(self, key ):
        """ Checks whether 'key' exists. Works with iterables """
        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            return [ self.exists(k) for k in key ]
        # empty directory
        if self._path is None:
            return False
        # single key
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            return False
        if not os.path.isfile(fullFileName):
            raise _log.Exceptn("Structural error: key %s: exists, but is not a file (full path %s)",rel=key,abs=fullFileName)
        return True

    def getCreationTime( self, key ):
        """
        Returns the creation time of 'key', or None if file was not found.
        Works with key as list.
        See comments on os.path.getctime() for compatibility
        """
        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            return [ self.getCreationTime(k) for k in key ]
        # empty directory
        if self._path is None:
            return None
        # single key
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            return None
        return datetime.datetime.fromtimestamp(os.path.getctime(fullFileName))

    def getLastModificationTime( self, key ):
        """
        Returns the last modification time of 'key', or None if file was not found.
        Works with key as list.
        See comments on os.path.getmtime() for compatibility
        """
        # vector version11
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            return [ self.getLastModificationTime(k) for k in key ]
        # empty directory
        if self._path is None:
            return None
        # single key
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            return None
        return datetime.datetime.fromtimestamp(os.path.getmtime(fullFileName))

    def getLastAccessTime( self, key ):
        """
        Returns the last access time of 'key', or None if file was not found.
        Works with key as list.
        See comments on os.path.getatime() for compatibility
        """
        # vector version
        if not isinstance(key,str):
            _log.verify( isinstance(key, Collection), "'key' must be a string or an interable object. Found type %s", type(key))
            return [ self.getLastAccessTime(k) for k in key ]
        # empty directory
        if self._path is None:
            return None
        # single key
        fullFileName = self.fullKeyName(key)
        if not os.path.exists(fullFileName):
            return None
        return datetime.datetime.fromtimestamp(os.path.getatime(fullFileName))

    # -- dict-like interface --

    def __call__(self, keyOrSub, default = RETURN_SUB_DIRECTORY ):
        """
        Return either the value of a sub-key (file), or return a new sub directory.
        If only one argument is used, then this function returns a new sub directory.
        If two arguments are used, then this function returns read( keyOrSub, default ).

        Member access:
            sd  = SubDir("!/test")
            x   = sd('x', None)                      reads 'x' with default value None
            x   = sd('sd/x', default=1)              reads 'x' from sub directory 'sd' with default value 1
        Create sub directory:
            sd2 = sd("subdir")                       creates and returns handle to subdirectory 'subdir'
            sd2 = sd("subdir1/subdir2")              creates and returns handle to subdirectory 'subdir1/subdir2'

        Parameters
        ----------
            keyOrSub:
                identify the object requested. Should be a string, or a list.
            default:
                If specified, this function reads 'keyOrSub' with read( keyOrSub, default )
                If not specified, then this function calls subDir( keyOrSub ).

        Returns
        -------
            Either the value in the file, a new sub directory, or lists thereof.
            Returns None if an element was not found.
        """
        if default == SubDir.RETURN_SUB_DIRECTORY:
            if not isinstance(keyOrSub, str):
                _log.verify( isinstance(keyOrSub, Collection), "'keyOrSub' must be a string or an iterable object. Found type '%s;", type(keyOrSub))
                return [ SubDir(k,parent=self) for k in keyOrSub ]
            return SubDir(keyOrSub,parent=self)
        return self.read( key=keyOrSub, default=default )

    def __getitem__( self, key ):
        """
        Reads self[key]
        If 'key' does not exist, throw a KeyError
        """
        return self.read( key=key, default=None, raiseOnError=True )

    def __setitem__( self, key, value):
        """ Writes 'value' to 'key' """
        self.write(key,value)

    def __delitem__(self,key):
        """ Silently delete self[key] """
        self.delete(key, False )

    def __len__(self) -> int:
        """ Return the number of files (keys) in this directory """
        return len(self.keys())

    def __iter__(self):
        """ Returns an iterator which allows traversing through all keys (files) below this directory """
        return self.keys().__iter__()

    def __contains__(self, key):
        """ Implements 'in' operator """
        return self.exists(key)

    # -- object like interface --

    def __getattr__(self, key):
        """
        Allow using member notation to get data
        This function throws an AttributeError if 'key' is not found.
        """
        if not self.exists(key):
            raise AttributeError(key)
        return self.read( key=key, raiseOnError=True )

    def __setattr__(self, key, value):
        """
        Allow using member notation to write data
        Note: keys starting with '_' are /not/ written to disk
        """
        if key[0] == '_':
            self.__dict__[key] = value
        else:
            self.write(key,value)

    def __delattr__(self, key):
        """ Silently delete a key with member notation. """
        _log.verify( key[:1] != "_", "Deleting protected or private members disabled. Fix __delattr__ to support this")
        return self.delete( key=key, raiseOnError=False )

    # -- short cuts for manual caching --

    def cache_read( self, cache_mode : CacheMode, key, default = None ):
        """
        Standard caching pattern ahead of a complex function:
            1) Check whether the cache is to be cleared. If so, delete any existing files and return 'default'
            2) If caching is enabled attempt to read the file 'key'. Return 'default' if not possible or enabled.
        """
        if cache_mode.delete:
            self.delete(key,raiseOnError=False)
            return default
        if cache_mode.read:
            return self.read(key,default=default,raiseOnError=False)
        return default

    def cache_write( self, cache_mode : CacheMode, key, value ):
        """
        Standard caching pattern at the end of a complex function:
            3) If caching is enabled, write 'value' to file 'key'
        """
        if cache_mode.write:
            self.write( key, value )

    # -- automatic caching --

    def cache(self, f, cacheName = None, cacheSubDir = None):
        """
        Decorater to create an automatically cached version of 'f'.

        The wrapped function will
            1) Compute a hash key for all parameters to be passed to 'f'
            2) Depending on an additional cacheMode optional parameter, attempt to read the cache from disk
            3) If not possible, call 'f', and store the result on disk

        This decorate is used when the caching "subdir" is set at the scope surrounding the function, e.g. at module level.
        It also works if the caching "subdir" is a static class member.
        Use member_cache to decorate a member function of a class.

        Example:

            autoRoot = SubDir("!/caching")   # create directory

            @autoRoot.cache
            def my_function( x, y ):
                return x*y

            x1 = my_function(2,3)                 # compute & generate cache
            x2 = my_function(2,3)                 # return cached result
            x3 = my_function(2,3,cacheMode="off") # ignore cache & compute

            print("Used cache" if my_function.cached else "Cached not used")
            print("Cache file: " + f.cacheFullKey)

        Example with a class:

            class Test(object):

                autoRoot = SubDir("!/caching")   # create directory

                def __init__(self, x):
                    self.x = x

                @autoRoot.cache
                def my_function( self, y ):
                    return self.x*y

        This works as expected. Important notice: the caching hash is computed using cdxbasics.util.uniqueHash() which

        Advanced arguments to the decorator:
           cacheName        : specify name for the cache for this function.
                              By default it is the name of the function, potentiall hashed if it is too long
           cacheSubDir      : specify a subdirectory for the function directory
                              By default it is the module name, potentially hashed if it is too long

        When calling the resulting decorated functions, you can pass the following argumets:
            cacheVersion    : sets the version of the function. Default is 1.00.00.
                              Change this value if you make changes to the function which are not backward compatible.
            cacheMode       : A cdxbasics.util.CacheMode identifier:
                               cacheMode='on'      : default, caching is on; delete existing caches with the wrong version
                               cacheMode='gen'     : caching on; do not delete existing caches with the wrong version
                               cacheMode='off'     : no caching
                               cacheMode='clear'   : delete existing cache. Do not update
                               cacheMode='update'  : update cache.
                               cacheMode='readonly': only read; do not write.

        The wrapped function has the following properties set after a function call
           cached           : True or False to indicate whether cached data was used
           cacheArgKey      : The hash key for this particular set of arguments
           cacheFullKey     : Full key path
        """
        f_subDir = SubDir( uniqueFileName48(f.__module__ if cacheSubDir is None else cacheSubDir), parent=self)
        f_subDir = SubDir( uniqueFileName48(f.__name__ if cacheName is None else cacheName), parent=f_subDir)

        @wraps(f)
        def wrapper(*vargs,**kwargs):
            caching = CacheMode('on')
            version = "1.00.00"
            if 'cacheMode' in kwargs:
                caching = CacheMode( kwargs['cacheMode'] )
                del kwargs['cacheMode']        # do not pass 'cacheMode' as parameter to 'f'
            if 'cacheVersion' in kwargs:
                version = str( kwargs['cacheVersion'] )
                del kwargs['cacheVersion']     # do not pass 'cacheVersion' as parameter to 'f'
            # simply no caching
            if caching.is_off:
                wrapper.cached       = False
                wrapper.cacheArgKey  = None
                wrapper.cacheFullKey = None
                return f(*vargs,**kwargs)
            # compute key
            key = uniqueFileName48(f.__module__, f.__name__,vargs,kwargs)
            wrapper.cacheArgKey  = key
            wrapper.cacheFullKey = f_subDir.fullKeyName(key)
            wrapper.cached       = False
            # clear?
            if caching.delete:
                f_subDir.delete(key)
            # read?
            if caching.read and key in f_subDir:
                cv             = f_subDir[key]
                version_       = cv[0]
                cached         = cv[1]
                if version == version_:
                    wrapper.cached = True
                    return cached
                if caching.del_incomp:
                    f_subDir.delete(key)
            # call function 'f'
            value = f(*vargs,**kwargs)
            # cache
            if caching.write:
                f_subDir.write(key,[version,value])
            return value

        return wrapper

