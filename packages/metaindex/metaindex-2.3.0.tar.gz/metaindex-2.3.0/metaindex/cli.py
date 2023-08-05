"""An interactive commandline to with the metaindex"""
import subprocess
import shlex
import shutil
import os
try:
    import readline
except ImportError:
    readline = None


class CLI:
    def __init__(self, cache):
        self.cache = cache
        self.quit = False
        self.listed_docs = []

        self.opener = shutil.which('xdg-open')
        if self.opener is not None:
            self.opener = shlex.split(self.opener)

        editor = None
        if editor is None:
            for name in ['VISUAL', 'EDITOR']:
                value = os.getenv(name)
                if value is None:
                    continue
                editor = shutil.which(value)
                if editor is not None:
                    break
        self.editor = editor
        if self.editor is not None:
            self.editor = shlex.split(self.editor)

        self.commands = {'quit': self.do_quit,
                         'help': self.help,
                         'find': self.do_find,
                         'list': self.do_find,
                         'stop': self.do_stop,
                         'info': self.do_info,
                         'open': self.do_open,
                         'cd': self.do_open_location,
                         'location': self.do_open_location,
                         }

    def do_quit(self, _):
        """Exit this commandline interface"""
        self.quit = True

    def do_stop(self, _):
        """Exit the commandline interface and also stop the server"""
        self.quit = True
        self.cache.shutdown()

    def help(self, _):
        """Show this help"""
        for cmd in sorted(self.commands.keys()):
            fnc = self.commands[cmd]
            print(f"{cmd}\t{fnc.__doc__}")

    def do_find(self, args):
        """Find files or list the most recently found files"""
        if len(args) > 0:
            query = " ".join(args)
            self.listed_docs = list(self.cache.find(query))
        self.print_list()

    def do_info(self, args):
        """Show the metadata of the selected file"""
        entry = self.doc_from_list(args)
        if entry is None:
            print("Usage: info entry-number")
            return

        skip = {'extra.fulltext',}
        skip |= {tag for tag, _ in entry if tag.endswith('.fulltext')}

        tagwidth = max(len(tag) for tag, _ in entry if tag not in skip)

        for tag, value in entry:
            if tag in skip:
                continue
            print(f"{tag: <{tagwidth}}    {value}")

    def do_open_location(self, args):
        """Open the folder/directory where the selected file is"""
        if self.opener is None:
            print("No opener defined")
            return

        entry = self.doc_from_list(args)
        if entry is None:
            print("Usage: cd entry-number")
            return

        subprocess.Popen(self.opener + [str(entry.path.parent)],
                         shell=False,
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)

    def do_open(self, args):
        """Open the document in an external program"""
        if self.opener is None:
            print("No opener defined")
            return

        entry = self.doc_from_list(args)
        if entry is None:
            print("Usage: open entry-number")
            return

        subprocess.Popen(self.opener + [str(entry.path)],
                         shell=False,
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)


    def doc_from_list(self, args):
        if len(args) < 1:
            return None
        if not args[0].isnumeric():
            return None
        nr = int(args[0])-1
        if nr >= len(self.listed_docs) or nr < 0:
            return None
        return self.listed_docs[nr]

    def print_list(self):
        idxwidth = len(str(len(self.listed_docs)))
        for idx, entry in enumerate(self.listed_docs):
            number = f"({idx+1: >{idxwidth}})"
            title = entry.path.stem
            for tag, value in entry:
                if tag.endswith('.title'):
                    title = str(value)
                    break
            print(f"{number} {title}")

    def run(self):
        if self.opener is None:
            print("[Warning] There is no document opener defined or the "
                  "defined document opener could not be found.\nThe 'open' "
                  "command will not work.\nPlease "
                  "check your configuration file to fix this.")
        if self.editor is None:
            print("[Warning] There is no metadata editor defined or the "
                  "defined editor could not be found.\nThe 'edit' "
                  "command will not work.\nPlease "
                  "check your configuration file to fix this.")
        while not self.quit:
            try:
                rawcmd = input('> ')
            except (KeyboardInterrupt, EOFError):
                self.quit = True
                continue

            cmds = tokenize(rawcmd)
            matches = []
            if len(cmds) > 0:
                for name in sorted(self.commands.keys()):
                    if name.startswith(cmds[0]):
                        matches.append(name)
            if len(matches) == 1:
                self.commands[matches[0]](cmds[1:])
            elif len(matches) > 1:
                print("Not quite sure what of these commands you meant:\n {}".format("\n ".join(matches)))
            elif len(rawcmd.strip()) > 0:
                print("I don't know what you mean. Try 'help' to see all available commands.")

        return 0


def tokenize(text):
    words = []

    word = ''
    quote = None
    escaped = False

    for letter in text:
        if escaped:
            word += letter
            escaped = False
        else:
            if letter == '\\':
                escaped = True
            elif quote is not None and letter == quote:
                quote = None
                words.append(word)
                word = ''
            elif quote is None and letter in " \t":
                words.append(word.strip())
                word = ''
            elif quote is None and letter in '"\'' and len(word.strip()) == 0:
                word = ''
                quote = letter
            else:
                word += letter

    if len(word.strip()) > 0:
        words.append(word.strip())

    return [word for word in words if len(word) > 0]
