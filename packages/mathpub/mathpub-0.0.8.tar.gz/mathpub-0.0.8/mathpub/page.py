from io import StringIO


class PlainText:
    def __init__(self, string: str):
        self._s = string

    def __str__(self):
        return self._s

    def latex(self):
        return f"\\text{{{self._s}}}"


class Latex:
    def __init__(self, string: str):
        self._s = string

    def __str__(self):
        return f"${self._s}$"

    def latex(self):
        return self._s


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
    class DisplayPrinter:
        def __init__(self, page):
            self._page = page

        def _repr_latex_(self):
            return ''.join(x.latex() for x in self._page.lines)

        __str__ = _repr_latex_

    @property
    def display(self):
        return self.DisplayPrinter(self)

    @property
    def markup(self):
        return ''.join(str(x) for x in self.lines)

    class DebugPrinter:
        def __init__(self, page):
            self._page = page

        def __repr__(self):
            return self._page.markup

    @property
    def debug(self):
        return self.DebugPrinter(self)

    def __init__(self):
        self.lines = []
        self._last_length = 0

    def _add_line(self, st: str):
        res = []

        ss = StringIO()
        is_latex = False

        for c in st:
            if c == "$":
                cur = ss.getvalue()
                ss.close()

                if is_latex:
                    res.append(Latex(cur))
                else:
                    res.append(PlainText(cur))

                is_latex = not is_latex
                ss = StringIO()
            else:
                ss.write(c)

        cur = ss.getvalue()
        if is_latex:
            cur = "$" + cur

        if cur:
            res.append(PlainText(cur))

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
