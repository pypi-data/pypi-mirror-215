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


class SpecialCharacter:
    chars = {}

    def __init_subclass__(cls, sym, **kwargs):  # noqa
        super().__init_subclass__(**kwargs)
        cls.chars[sym] = cls
        cls.sym = sym

    def __new__(cls, sym=None):
        if sym is not None:
            return cls.chars[sym]()
        return super().__new__(cls)

    def __str__(self):
        return self.sym


class Backslash(SpecialCharacter, sym="\\"):
    def latex(self):
        return r"\backslash"


class Circum(SpecialCharacter, sym="^"):
    def latex(self):
        return r"\textasciicircum"


class Tilde(SpecialCharacter, sym="~"):
    def latex(self):
        return r"\textasciitilde"


escapable_characters = {
    "#": "Num",
    "%": "Percent",
    "&": "Ampersand",
    "_": "Underscore",
    "{": "LBrace",
    "}": "RBrace"
}


def latex_gen(sym):
    def latex(self):
        return f"\\{sym}"

    return latex


for sym, name in escapable_characters.items():
    type(name, (SpecialCharacter,), {"latex": latex_gen(sym)}, sym=sym)


def process_text(chr_iter):
    res = []
    esc = False

    ss = StringIO()

    def get():
        nonlocal ss
        st = ss.getvalue()
        ss.close()
        ss = StringIO()
        return st

    entered = False

    for c in chr_iter:
        entered = True
        if c == "\\":
            if esc:
                cur = get()
                if cur:
                    res.append(PlainText(cur))
                res.append(Backslash())
            esc = True
        elif esc and c != "$":
            cur = get()
            if cur:
                res.append(PlainText(cur))
            res.append(Backslash())
            ss.write(c)
            esc = False
        elif esc and c == "$":
            ss.write("\\")
            ss.write(c)
            esc = False
        elif c == "$":
            cur = get()
            if cur:
                res.append(PlainText(cur))
            break
        elif c in SpecialCharacter.chars:
            cur = get()
            if cur:
                res.append(PlainText(cur))

            res.append(SpecialCharacter(c))
        else:
            ss.write(c)

    if not entered:
        raise StopIteration

    cur = get()
    if cur:
        res.append(PlainText(cur))
    ss.close()
    return res


def process_latex(char_iter):
    esc = False

    ss = StringIO()

    entered = False

    for c in char_iter:
        entered = True
        if not esc and c == "$":
            res = ss.getvalue()
            ss.close()
            return [Latex(res)]

        if c == "\\":
            esc = True
        else:
            esc = False
        ss.write(c)

    if not entered:
        raise StopIteration

    res = ss.getvalue()
    ss.close()

    return process_text(res)
