from mathpub.text_processing import process_text, process_latex
from IPython.display import display, Latex


class Line:
    def __init__(self, atoms: list):
        self._atoms = atoms

    def __str__(self):
        endl = "\n\n"
        return f"{''.join(str(x) for x in self._atoms)}{endl}"

    def latex(self):
        endl = r"\\"

        return f"{''.join(x.latex() for x in self._atoms)}{endl}"


class Page:
    def str_markdown(self):
        return ''.join(str(x) for x in self.lines)

    def repr_markdown(self):
        return repr(self.str_markdown())

    def str_latex(self):
        return "$" + ''.join(x.latex() for x in self.lines) + "$"

    def repr_latex(self):
        return repr(self.str_latex())

    def display(self):
        display(Latex(self.str_latex()))

    def __init__(self):
        self.lines = []
        self._last_length = 0

    def _add_line(self, st: str):
        res = []
        line = iter(st)
        try:
            while True:
                res.extend(process_text(line))
                res.extend(process_latex(line))
        except StopIteration:
            self.lines.append(Line(res))

    def __iadd__(self, other):
        for line in other.split("\n"):
            self._add_line(line)

        return self

    def checkpoint(self):
        self._last_length = len(self.lines)

    def rollback(self):
        self.lines = self.lines[:self._last_length]

    @property
    def latest(self):
        new_page = Page()
        new_page.lines = self.lines[self._last_length:]
        return new_page
