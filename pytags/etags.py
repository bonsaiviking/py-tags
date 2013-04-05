# Etags reader library

from pytags import TagFile, Tag
import re

reTag = re.compile(r'^(?P<text>[^\x7f]*)\x7f(?P<name>[^\x01]*)\x01(?P<line>\d*),(?P<byte>\d*)$')
reHead = re.compile(r'^(?P<file>[^,]*),(?P<size>\d*)$')
class EtagFile(TagFile):
    def parse(self, f):
        current_file = None
        for l in f:
            if l == "\x0c\n":
                nextline = f.next()
                m = reHead.match(nextline)
                if m:
                    current_file = m.group('file')
                    if current_file not in self.files:
                        self.files[current_file] = []
                else:
                    current_file = nextline #oops
                continue
            else:
                m = reTag.match(l)
                if m:
                    t = Tag()
                    t.file = current_file
                    t.text = m.group('text')
                    t.name = m.group('name')
                    t.line = m.group('line')
                    t.byte = m.group('byte')
                    if t.name in self.tags:
                        self.tags[t.name].append(t)
                    else:
                        self.tags[t.name] = [t]
                    self.files[current_file].append(t)
                else:
                    raise RuntimeError, "Can't parse: {0!r}".format(l)

