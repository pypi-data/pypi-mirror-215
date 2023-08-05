import configparser
import pathlib
import os
import sys
import re
import fnmatch
import importlib
import mimetypes

from metaindex import logger
from metaindex import stores
from metaindex import shared
from metaindex import ocr


HERE = pathlib.Path(__file__).parent

HOME = pathlib.Path().home()
PROGRAMNAME = 'metaindex'
CONFFILENAME = PROGRAMNAME + os.path.extsep + 'conf'
CONFIGFILE = HOME / ".config" / CONFFILENAME
CACHEPATH = HOME / ".local" / 'state' / PROGRAMNAME
DATAPATH = HOME / ".local" / "share" / PROGRAMNAME
SOCKETPATH = HOME / ".local" / "state" / PROGRAMNAME

IGNORE_DIRS = [".git", ".svn", ".hg", ".bzr",
               "System Volume Information",
               ".stfolder",
               "__pycache__",
               "__MACOSX"]
IGNORE_FILES = ['*.aux', '*.toc', '*.out', '*.log', '*.nav',
                '*.exe', '*.sys',
                '*.bat', '*.ps',
                '*.sh', '*.fish',
                '*~', '*.swp', '*.bak', '*.sav', '*.backup', '*.old',
                '*.old', '*.orig', '*.rej',
                'tags', '*.log',
                '*.a', '*.out', '*.o', '*.obj', '*.so']
IMPLICIT_TAGS = ['author', 'type', 'title', 'tag', 'series', 'filename']
SYNONYMS = {'author': {
                "extra.author",
                "extra.artist",
                "extra.creator",
                "id3.artist",
                "pdf.author",
                "rules.author",
                "exif.image.artist",
                "comicbook.writer",
                "xmp.dc.name",
                "gpx.author",
                "opf.creator",
                "opendocument.creator",
                "officeopenxml.creator",
                },
            'type': {
                "extra.type",
                "rules.type",
                "xmp.dc.type",
                },
            'date': {
                "extra.date",
                "rules.date",
                "comicbook.date",
                "gpx.time",
                "opendocument.date",
                "officeopenxml.date",
                "filetags.date",
                "html.date",
                "exif.date",
                "pdf.date",
                "pdf.creation_date",
                "pdf.modification_date",
                },
            'time': {
                "extra.time",
                "rules.time",
                "filetags.time",
                "html.time",
                "exif.time",
                "opendocument.time",
                "officeopenxml.time",
                "pdf.time",
            },
            'title': {
                "extra.title",
                "opf.title",
                "id3.title",
                "rules.title",
                "pdf.title",
                "filetags.title",
                "abc.title",
                "comicbook.title",
                "xmp.dc.title",
                "gpx.name",
                "opendocument.title",
                "officeopenxml.title",
                },
            'tag': {
                "extra.tag",
                "extra.tags",
                "extra.subject",
                "pdf.keywords",
                "pdf.categories",
                "xmp.dc.subject",
                "rules.tags",
                "rules.tag",
                "rules.subject",
                "pdf.Subject",
                "comicbook.tags",
                "opf.subject",
                "gpx.keyword",
                "opendocument.keyword",
                "opendocument.subject",
                "officeopenxml.keyword",
                "officeopenxml.subject",
                "filetags.tag",
                },
            'rating': {
                "extra.rating",
                "xmp.rating",
                },
            'resolution': {
                "image.resolution",
            },
            'language': {
                "opf.language",
                "pdf.Language",
                "xmp.dc.language",
                "extra.language",
                "rules.language",
                "comicbook.languageiso"
                "ocr.language",
                "opendocument.language",
                },
            'series': {
                'extra.series',
                'comicbook.series',
                },
            'series_index': {
                'extra.series_index',
                'comicbook.number',
                },
            }


try:
    from xdg import BaseDirectory
    CONFIGFILE = pathlib.Path(BaseDirectory.load_first_config(CONFFILENAME) or CONFIGFILE)
    DATAPATH = pathlib.Path(BaseDirectory.save_data_path(PROGRAMNAME) or DATAPATH)
    SOCKETPATH = pathlib.Path(BaseDirectory.get_runtime_dir() or SOCKETPATH)
except ImportError:
    BaseDirectory = None

SOCKETPATH /= SOCKETPATH / (PROGRAMNAME + '.sock')

ADDONSPATH = DATAPATH / "addons"
LOGFILEPATH = CACHEPATH / "metaindex.log"
LOGLEVEL = 'WARNING'

EXTRA_MIMETYPES = [
    ('application/gpx+xml', '.gpx'),
]

SECTION_GENERAL = 'General'
SECTION_SYNONYMS = 'Synonyms'
SECTION_INCLUDE = 'Include'
SECTION_SERVER = 'Server'
CONFIG_CACHE = 'cache'
CONFIG_SOCKET = 'socket'
CONFIG_RECURSIVE_EXTRA_METADATA = 'recursive-extra-metadata'
CONFIG_COLLECTION_METADATA = 'collection-metadata'
CONFIG_IGNORE_DIRS = 'ignore-dirs'
CONFIG_IGNORE_FILES = 'ignore-files'
CONFIG_ACCEPT_FILES = 'accept-files'
CONFIG_INDEX_UNKNOWN = 'index-unknown'
CONFIG_IGNORE_INDEXERS = 'ignore-indexers'
CONFIG_PREFERRED_SIDECAR_FORMAT = 'preferred-sidecar-format'
CONFIG_OCR = 'ocr'
CONFIG_FULLTEXT = 'fulltext'
CONFIG_MIMETYPES = 'mimetypes'
CONFIG_IMPLICIT_TAGS = 'implicit-tags'
CONFIG_LOGFILE = 'logfile'
CONFIG_LOGLEVEL = 'loglevel'
CONFIG_AUTOSTART = 'autostart'
CONFIG_DYNAMIC_TAGS = 'index-new-tags'

CONF_DEFAULTS = {SECTION_GENERAL: {
                    CONFIG_CACHE: str(CACHEPATH),
                    CONFIG_SOCKET: str(SOCKETPATH),
                    CONFIG_RECURSIVE_EXTRA_METADATA: "yes",
                    CONFIG_COLLECTION_METADATA: ".metadata, metadata",
                    CONFIG_IGNORE_DIRS: "\n".join(IGNORE_DIRS),
                    CONFIG_IGNORE_FILES: "\n".join(IGNORE_FILES),
                    CONFIG_ACCEPT_FILES: '',
                    CONFIG_INDEX_UNKNOWN: 'yes',
                    CONFIG_IGNORE_INDEXERS: '',
                    CONFIG_PREFERRED_SIDECAR_FORMAT: '.json, .opf',
                    CONFIG_OCR: 'no',
                    CONFIG_FULLTEXT: 'no',
                    CONFIG_IMPLICIT_TAGS: ', '.join(IMPLICIT_TAGS),
                 },
                 SECTION_SERVER: {
                    CONFIG_LOGFILE: str(LOGFILEPATH),
                    CONFIG_LOGLEVEL: str(LOGLEVEL),
                    CONFIG_AUTOSTART: 'yes',
                    CONFIG_DYNAMIC_TAGS: 'no',
                 },
                 SECTION_SYNONYMS: {k: ', '.join(v)
                                    for k, v in SYNONYMS.items()},
                 SECTION_INCLUDE: {
                 },
                }


class BaseConfiguration:
    """Convenience wrapper for configparser"""
    TRUE = ['y', 'yes', '1', 'true', 'on']
    FALSE = ['n', 'no', '0', 'false', 'off']

    def __init__(self, conf=None):
        self.conf = conf or configparser.ConfigParser(interpolation=None)
        self._userfile = None

    def __getitem__(self, group):
        return self.conf[group]

    def __contains__(self, item):
        return item in self.conf

    def set(self, group, key, value):
        if group not in self.conf:
            self.conf[group] = {}
        self.conf[group][key] = value

    def get(self, group, item, default=None):
        if group in self.conf:
            return self.conf[group].get(item, default)
        return default

    def bool(self, group, item, default='n'):
        return self.get(group, item, default).lower() in self.TRUE

    def number(self, group, item, default='0'):
        value = self.get(group, item, default)
        if value.isnumeric():
            return int(value)
        return None

    def path(self, group, item, default=None):
        value = self.get(group, item, default)
        if value is not None:
            value = pathlib.Path(value).expanduser().resolve()
        return value

    def list(self, group, item, default='', separator=',', strip=True, skipempty=True):
        result = []
        for v in self.get(group, item, default).split(separator):
            if strip:
                v = v.strip()
            if skipempty and len(v) == 0:
                continue
            result.append(v)
        return result


class Configuration(BaseConfiguration):
    """Wrapper for BaseConfiguration (aka configparser) with additional convenience accessors

    If no ``baseconfig`` is provided, the defaults will be loaded.

    :type baseconfig: ``configparser.ConfigParser`` instance"""
    def __init__(self, baseconfig=None):
        if baseconfig is None:
            baseconfig = configparser.ConfigParser(interpolation=None)
            baseconfig.read_dict(CONF_DEFAULTS)
        super().__init__(baseconfig)
        self._collection_metadata = None

        self.extract_fulltext = False
        """Whether or not or for what files to run fulltext extraction"""
        self._update_property(SECTION_GENERAL, CONFIG_FULLTEXT)

        self.ignore_dirs = []
        """List of directories to ignore during indexing"""
        self._update_property(SECTION_GENERAL, CONFIG_IGNORE_DIRS)

        self.index_unknown = False
        """Whether or not to index files when no indexers return successful"""
        self._update_property(SECTION_GENERAL, CONFIG_INDEX_UNKNOWN)

        self.recursive_extra_metadata = True
        """Whether or not extra metadata is considered recursive"""
        self._update_property(SECTION_GENERAL, CONFIG_RECURSIVE_EXTRA_METADATA)

        self.ignore_file_patterns = []
        """Patterns of files to ignore"""
        self.accept_file_patterns = None
        """Patterns of files to index.
        If this option is set, **only** these files must be indexed and
        ``ignore_file_patterns`` can safely be ignored.
        """
        self._update_property(SECTION_GENERAL, CONFIG_ACCEPT_FILES)

        self.ocr = ocr.Dummy()
        """The OCR facility, as configured by the user"""
        self._update_property(SECTION_GENERAL, CONFIG_OCR)

        self.ignore_indexers = []
        """List of all indexers by name that should be ignored"""
        self._update_property(SECTION_GENERAL, CONFIG_IGNORE_INDEXERS)

        self.synonyms = {}
        """Mapping of synonym -> synonymized tags (e.g. author -> pdf.creator)"""
        self.synonymized = {}
        """Mapping of synonymized -> synonym (e.g. pdf.creator -> author)"""
        self._update_property(SECTION_SYNONYMS, None)

        self.accepted_tags = set(sum(list(list(t) for t in self.synonyms.values()),
                                     start=[]))
        """The tags that are accepted, ie. not discarded during indexing"""

        self.implicit_tags = set()
        """Tags whose values should be indexed without a prefix, too"""
        self._update_property(SECTION_GENERAL, CONFIG_IMPLICIT_TAGS)

    def set(self, group, key, value):
        super().set(group, key, value)
        self._update_property(group, key)

    def _update_property(self, section, key):
        if section == SECTION_SYNONYMS:
            self.synonyms = {}
            for name in self[SECTION_SYNONYMS]:
                synonyms = {s for s in self.list(SECTION_SYNONYMS, name) if len(s) > 0}
                if '*' in synonyms:
                    synonyms.remove('*')
                    synonyms |= SYNONYMS.get(name, set())
                self.synonyms[name] = synonyms

            self.synonymized = {}
            for synonym, tags in self.synonyms.items():
                self.synonymized.update({t: synonym for t in tags})

            return

        if section != SECTION_GENERAL:
            return

        if key == CONFIG_IGNORE_DIRS:
            self.ignore_dirs = self.list(section, key, "", separator="\n")

        if key == CONFIG_FULLTEXT:
            fulltext_opts = self.list(section, key, "no")
            if len(fulltext_opts) == 0 or fulltext_opts[0].lower() in self.FALSE:
                fulltext_opts = False
            elif fulltext_opts[0].lower() in self.TRUE:
                fulltext_opts = True

            self.extract_fulltext = fulltext_opts

        if key == CONFIG_INDEX_UNKNOWN:
            self.index_unknown = self.bool(section, key, "no")

        if key == CONFIG_RECURSIVE_EXTRA_METADATA:
            self.recursive_extra_metadata = self.bool(section, key, "y")

        if key in [CONFIG_ACCEPT_FILES, CONFIG_IGNORE_FILES]:
            self.ignore_file_patterns = []
            self.accept_file_patterns = None

            accept = self.list(SECTION_GENERAL,
                               CONFIG_ACCEPT_FILES,
                               '', separator="\n")
            ignore = self.list(SECTION_GENERAL,
                               CONFIG_IGNORE_FILES,
                               '', separator="\n")

            if len(accept) > 0:
                self.accept_file_patterns = [re.compile(fnmatch.translate(pattern.strip()), re.I)
                                             for pattern in accept]
            elif len(ignore) > 0:
                self.ignore_file_patterns = [re.compile(fnmatch.translate(pattern.strip()), re.I)
                                             for pattern in ignore]

        if key == CONFIG_OCR:
            self.ocr = ocr.Dummy()

            ocr_opts = self.list(section, key, "no")

            if len(ocr_opts) == 0 or ocr_opts[0].lower() in self.FALSE:
                ocr_opts = False
            elif ocr_opts[0].lower() in self.TRUE:
                ocr_opts = True
            if ocr_opts:
                self.ocr = ocr.TesseractOCR(ocr_opts)

        if key == CONFIG_IGNORE_INDEXERS:
            self.ignore_indexers = [indexer
                                    for indexer in self.list(section, key, '')
                                    if len(indexer) > 0]

        if key == CONFIG_IMPLICIT_TAGS:
            self.implicit_tags = {t.lower() for t in self.list(section, key)}

    @property
    def collection_metadata(self):
        """Return a list of all valid filenames for collection metadata.

        The list is ordered by user's preference for sidecar file format and
        name of collection metadata file.
        """
        if self._collection_metadata is None:
            lst = self.list(SECTION_GENERAL, CONFIG_COLLECTION_METADATA, "")
            if len(lst) > 0:
                lst = sum([[fn + store.SUFFIX for store in self.get_preferred_sidecar_stores()]
                           for fn in lst
                           if len(fn) > 0], start=[])
            self._collection_metadata = lst
        return self._collection_metadata

    def expand_synonyms(self, tags):
        """Expand all synonyms of this iterable of tags (or a single tag)

        This function will return a set of tags (at least the one(s) you passed
        in), expanding all those tags that are synonyms.

        You might call this with a single tag, to expand it to its actual tags,
        if it is a synonym. If it isn't one, this function will just return the
        tag again (in a set).

        You can also call this with an iterable of tags. In that case all synonyms
        in that iterable are expanded accordingly.
        """
        if not isinstance(tags, (set, list, tuple)):
            tags = {tags}
        return set(sum([list(self.synonyms.get(k, {k}))
                        for k in tags], start=[]))

    def is_sidecar_file(self, path):
        """Return True if the file at path is a sidecar file (either collection metadata or not)"""
        if not path.is_file():
            # not file? can't be a metadata file
            return False
        if path.name in self.collection_metadata:
            # the filename *is* the name of a valid collection metadata file
            return True
        # check whether there are any sidecar files for any of the valid stores
        return any(path.suffix == store.SUFFIX and
                    any(fn.is_file() and fn != path and fn.stem == path.stem
                        for fn in path.parent.iterdir())
                   for store in stores.STORES)

    def get_preferred_sidecar_stores(self):
        """Returns a list of all available metadata stores, sorted by preference of the user"""
        preferred = self.list(SECTION_GENERAL, CONFIG_PREFERRED_SIDECAR_FORMAT, '.json')
        preferred = [stores.BY_SUFFIX[suffix] for suffix in preferred if suffix in stores.BY_SUFFIX]
        return preferred \
             + [store for store in stores.STORES if store not in preferred]

    def find_all_sidecar_files(self, path):
        """Find all sidecar files for this file

        Generates a sequence of (pathlib.Path, bool) with the location of the
        existing sidecar file and whether or not it is a collection metadata file.

        The files are returned in order of preference and direct sidecar files
        before collection sidecar files.

        May return an empty list, if no sidecar files exist.
        """
        all_stores = list(self.get_preferred_sidecar_stores())

        for store in all_stores:
            sidecar = path.parent / (path.stem + store.SUFFIX)
            if sidecar.is_file() and sidecar != path:
                yield sidecar, False

        for store in all_stores:
            for collection_fname in self.collection_metadata:
                if not collection_fname.endswith(store.SUFFIX):
                    continue
                sidecar = path.parent / collection_fname
                if sidecar.is_file() and sidecar != path:
                    yield sidecar, True

    def resolve_sidecar_for(self, path, allow_collections=True):
        """Get a sidecar file path for this file

        Returns a tuple (path, is_collection, store) with the pathlib.Path to the sidecar file
        (which may or may not exist), a boolean whether or not the sidecar file is a collection
        file, and the store module that can be used to read/write the metadata to this sidecar.

        ``allow_collections`` controls whether this function will return any
        existing collection sidecar files.

        May return (None, False, None) in case there is no usable storage.
        """
        # find what type of metadata file should be used
        sidecar = None
        is_collection = None
        all_stores = [(store, hasattr(store, 'store'))
                      for store in self.get_preferred_sidecar_stores()]
        usable_stores = [store for store, usable in all_stores if usable]
        if len(usable_stores) == 0:
            return None, False, None

        logger.debug("Resolving sidecar files for %s", path)
        logger.debug(" ... available stores: %s", usable_stores)

        prefer_collection = False

        # find existing sidecar file
        for store, usable in all_stores:
            location = path.parent / (path.stem + store.SUFFIX)
            if location.is_file() and usable:
                sidecar = location
                break

        logger.debug(" ... any direct sidecar? %s", sidecar)

        # if there was none, find existing collection sidecar file
        if sidecar is None and allow_collections:
            for store, is_usable in all_stores:
                for collection_name in self.collection_metadata:
                    if not collection_name.endswith(store.SUFFIX):
                        continue
                    location = path.parent / collection_name
                    logger.debug(" ... trying at %s", location.name)
                    if location.is_file():
                        logger.debug(" ... found a collection sidecar file at %s", location)
                        if is_usable:
                            sidecar = location
                            is_collection = True
                            break
                        logger.debug(" ... but it cannot be used")
                        prefer_collection = True
                if sidecar is not None:
                    break
        # still none? just take the first preferred sidecar store and create a sidecar file
        if sidecar is None:
            if prefer_collection:
                sidecar_name = self.collection_metadata[0]
                is_collection = True
            else:
                sidecar_name = path.stem
            sidecar = path.parent / (sidecar_name + usable_stores[0].SUFFIX)

        return sidecar, is_collection, stores.BY_SUFFIX[sidecar.suffix]

    def find_indexable_files(self, paths, recursive=True):
        """Find all files that can be indexed in the given paths

        :param paths: A list of paths to search through
        :param recursive: Whether or not any given directories should be indexed
                          recursively"""
        paths = [pathlib.Path(path).resolve() for path in paths]

        # filter out ignored directories
        paths = [path for path in paths
                 if not any(ignoredir in path.parts
                            for ignoredir in self.ignore_dirs)]

        dirs = [path for path in paths if path.is_dir()]
        files = {path for path in paths if path.is_file() and self._accept_file(path)}
        files |= {fn for fn in shared.find_files(dirs, recursive, self.ignore_dirs)
                     if self._accept_file(fn)}

        return files

    def _accept_file(self, path):
        if any(ignoredir in path.parts[:-1] for ignoredir in self.ignore_dirs):
            return False
        if self.is_sidecar_file(path):
            return False
        pathstr = str(path)
        if self.accept_file_patterns is not None:
            return any(pattern.match(pathstr) for pattern in self.accept_file_patterns)
        return not any(pattern.match(pathstr) for pattern in self.ignore_file_patterns)

    def load_mimetypes(self):
        """Load the user-configured extra mimetypes"""
        extra_mimetypes = [str(pathlib.Path(fn.strip()).expanduser().resolve())
                           for fn in self.list(SECTION_GENERAL, CONFIG_MIMETYPES, "", "\n")]
        if len(extra_mimetypes) > 0:
            mimetypes.init(files=extra_mimetypes)

        for type_, suffix in EXTRA_MIMETYPES:
            mimetypes.add_type(type_, suffix)

    @staticmethod
    def load_addons():
        """Load the indexer addons"""
        # load indexer addons
        if ADDONSPATH.exists():
            prev_sys_path = sys.path.copy()
            sys.path = [str(ADDONSPATH)] + prev_sys_path
            for item in ADDONSPATH.iterdir():
                if item.is_file() and item.suffix == '.py':
                    logger.info(f"Loading addon {item.name}")
                    importlib.import_module(item.stem)
            sys.path = prev_sys_path


def load(conffile=None):
    """Load the metaindex configuration file ``conffile``

    If ``conffile`` is ``None``, the default location of the configuration file
    will be tried. As a last resort the built-in defaults will be used.

    This function will also ensure that all additional mimetypes and indexers
    are loaded and ignored indexers are removed from the list of registered
    indexers.
    """
    conf = configparser.ConfigParser(interpolation=None)
    conf.read_dict(CONF_DEFAULTS)

    if conffile is not None and not isinstance(conffile, pathlib.Path):
        conffile = pathlib.Path(conffile)
    elif conffile is None:
        conffile = CONFIGFILE
    conffile = conffile.expanduser().resolve()

    if conffile is not None and not conffile.is_file():
        logger.info(f"Configuration file {conffile} not found. "
                     "Using defaults.")
        conffile = None
    if conffile is None and CONFIGFILE.is_file():
        conffile = CONFIGFILE

    if conffile is not None:
        logger.info(f"Loading configuration from {conffile}.")
        conf.read([conffile])

    conf.read([str(pathlib.Path(conf['Include'][key]).expanduser().resolve())
               for key in sorted(conf['Include'])])

    config = Configuration(conf)
    config.load_mimetypes()
    config.load_addons()

    return config
