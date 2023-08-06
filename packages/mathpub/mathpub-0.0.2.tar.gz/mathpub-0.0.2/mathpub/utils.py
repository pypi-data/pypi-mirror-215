def b(ins):
    """When writing inside f-string, it is much more convenient to write {b(ins)} than {{{ins}}} """
    return f"{{{ins}}}"


def frac(num, den):
    return f"\\frac{b(num)}{b(den)}"


def dfrac(num, den):
    return f"\\dfrac{b(num)}{b(den)}"


def underline(ins):
    return f"\\underline{b(ins)}"


def overline(ins):
    return f"\\overline{b(ins)}"


def lower_index(ind):
    return f"_{b(ind)}"


def upper_ind(ind):
    return f"^{b(ind)}"


def lr(ins, left, right):
    """Wraps \\left and \\right (with delimiters left and right respectively) around ins """
    return f"\\left {left} {ins} \\right {right}"


def sqrt(ins):
    return f"\\sqrt{b(ins)}"


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
