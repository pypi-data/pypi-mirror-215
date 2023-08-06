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

    class MarkupPrinter:
        def __init__(self, page):
            self._page = page

        def __str__(self):
            return ''.join(str(x) for x in self._page.lines)

        def __repr__(self):
            return repr(str(self))

    @property
    def display(self):
        return self.DisplayPrinter(self)

    @property
    def markup(self):
        return self.MarkupPrinter(self)

    def __init__(self):
        self.lines = []

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
