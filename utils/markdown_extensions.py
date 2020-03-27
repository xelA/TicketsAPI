from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class TicketsExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(TicketsTreeprocessor(md), 'tickets', 8)

    def reset(self):
        self.md.TicketsExtension = {}


class TicketsTreeprocessor(Treeprocessor):
    def run(self, doc):
        for elem in doc.iter():
            if elem.tag == "p":
                elem.set("class", "msg")


def makeExtension(**kwargs):
    return TicketsExtension(**kwargs)
