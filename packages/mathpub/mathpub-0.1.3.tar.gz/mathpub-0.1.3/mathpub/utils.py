def br(ins):
    """When writing inside f-string, it is much more convenient to write {br(ins)} than {{{ins}}} """
    return f"{{{ins}}}"


def frac(num, den):
    return f"\\frac{br(num)}{br(den)}"


def dfrac(num, den):
    return f"\\dfrac{br(num)}{br(den)}"


def underline(ins):
    return f"\\underline{br(ins)}"


def overline(ins):
    return f"\\overline{br(ins)}"


def lower_index(ind):
    return f"_{br(ind)}"


def upper_index(ind):
    return f"^{br(ind)}"


def lr(ins, left, right):
    """Wraps \\left and \\right (with delimiters left and right respectively) around ins """
    return f"\\left {left} {ins} \\right {right}"


def sqrt(ins):
    return f"\\sqrt{br(ins)}"


class _Abc:
    def __init__(self):
        alph = [
            "alpha",
            "beta",
            "gamma",
            "delta",
            "epsilon",
            "zeta",
            "eta",
            "theta",
            "iota",
            "kappa",
            "lambda",
            "mu",
            "nu",
            "xi",
            "omicron",
            "pi",
            "rho",
            "sigma",
            "tau",
            "upsilon",
            "phi",
            "chi",
            "psi",
            "omega"
        ]

        def name(x):
            return x if x != "lambda" else f"{x}_"

        for a in alph:
            setattr(self, name(a), f"\\{a}")
            setattr(self, name(a).capitalize(), f"\\{a.capitalize()}")


abc = _Abc()

lbrace = r"\{"
rbrace = r"\}"
bslash = "\\"
