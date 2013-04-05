# Ctags reader library

from pytags import TagFile, Tag
import re

reTag = re.compile(r'^(?P<name>[^!][^\t]*)\t(?P<file>[^\t]*)\t(?P<cmd>.*?)(?:;"(?P<info>.*))?$')
class CtagFile(TagFile):
    def parse(self, f):
        for l in f:
            m = reTag.match(l)
            if m:
                t = Tag()
                t.file = m.group('file')
                t.name = m.group('name')
                t.line = m.group('cmd') #XXX: Less than ideal :(
                if t.name in self.tags:
                    self.tags[t.name].append(t)
                else:
                    self.tags[t.name] = [t]
                if t.file in self.files:
                    self.files[t.file].append(t)
                else:
                    self.files[t.file] = [t]
            elif l[0] == "!": #comment
                continue
            else:
                raise RuntimeError, "Can't parse: {0!r}".format(l)

