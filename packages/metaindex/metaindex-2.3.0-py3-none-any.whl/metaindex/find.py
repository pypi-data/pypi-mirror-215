import pathlib
import os
import sys

from metaindex import logger
from metaindex.cache import Cache


def find(cache, args):
    query = args.query or []
    symlink_folder = None

    if args.link is not None:
        symlink_folder = pathlib.Path(args.link).expanduser().resolve()

        if symlink_folder.exists() and not symlink_folder.is_dir():
            logger.fatal("%s is not a directory.", symlink_folder)
            return 1
        symlink_folder.mkdir(parents=True, exist_ok=True)

        files = len(list(symlink_folder.iterdir()))
        symlinks = 0

        if args.force:
            symlinks = len([f for f in symlink_folder.iterdir() if f.is_symlink()])

        if args.force and files-symlinks > 0:
            logger.fatal("Can not create symbolic links in %s: some files are not symlinks.",
                         symlink_folder)
            return 2

        if not args.force and files > 0:
            logger.fatal(f"Can not create symbolic links in {symlink_folder}: not empty")
            return 2

        if args.force and symlinks > 0 and not args.keep:
            for symlink in symlink_folder.iterdir():
                symlink.unlink()

    if query == ['-']:
        query = sys.stdin.read().strip()
    else:
        query = ' '.join(query)

    results = cache.find(query)

    for result in sorted(results):
        print(result.path)

        if symlink_folder is not None:
            target = pathlib.Path(result[0])
            counter = ""
            while True:
                fn = symlink_folder / (target.stem + counter + target.suffix)
                if fn.exists() and fn.readlink().resolve() != target:
                    if counter == "":
                        counter = "_1"
                    else:
                        counter = "_" + str(int(counter[1:])+1)
                    continue
                break

            # curiosity: using .exists() would send the wrong signal, because
            # fn.exists() checks for the existence of the fn's target if fn
            # is a symlink; but we only care whether the actual fn exists, not
            # the target (e.g. the previous fn target has been moved and the
            # new fn replaces that symlink)
            if not fn.is_symlink():
                os.symlink(target, fn)

        show_keys = set(result.keys())
        if args.tags is None:
            continue

        if len(args.tags) > 0:
            show_keys = cache.config.expand_synonyms(args.tags)

        for key in sorted(show_keys):
            values = result[key]
            if len(values) == 0:
                continue

            if len(values) == 1:
                print(f"  {key}: {values[0]}")
            else:
                print(f"  {key}:")
                for value in values:
                    print(f"    - {value}")
    return 0
