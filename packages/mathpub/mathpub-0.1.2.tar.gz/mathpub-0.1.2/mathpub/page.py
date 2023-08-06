from mathpub.text_processing import process_text, process_latex
from IPython.display import display, Latex, clear_output
from ipywidgets import Button


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

    def _display_unchanged(self):
        display(Latex(self.str_latex()))

    def _display_changed(self):
        before_checkpoint = ''.join(x.latex() for x in self.lines[:self._last_length])
        if before_checkpoint:
            display(Latex("$" + before_checkpoint + "$"))
        display("-------Checkpoint-------")
        after_checkpoint = "$" + ''.join(x.latex() for x in self.lines[self._last_length:]) + "$"
        display(Latex(after_checkpoint))

        if self.interactive_buttons:
            checkpoint_button = Button(description="Checkpoint")
            checkpoint_button.style.button_color = "lightgreen"
            checkpoint_button.on_click(lambda b: (self.checkpoint(), clear_output(), self._display_unchanged()))
            display(checkpoint_button)

            rollback_button = Button(description="Rollback")
            checkpoint_button.style.button_color = "red"
            checkpoint_button.on_click(lambda b: (self.rollback(), clear_output(), self._display_unchanged()))
            display(rollback_button)

    def display(self):
        if self._changes_made:
            self._display_changed()
        else:
            self._display_unchanged()

    def __init__(self, *, interactive_buttons=False):
        self.lines = []
        self._last_length = 0
        self._changes_made = False
        self.interactive_buttons = interactive_buttons

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

        self._changes_made = True
        return self

    def checkpoint(self):
        self._last_length = len(self.lines)
        self._changes_made = False

    def rollback(self):
        self.lines = self.lines[:self._last_length]
        self._changes_made = False

    @property
    def latest(self):
        new_page = Page()
        new_page.lines = self.lines[self._last_length:]
        new_page.checkpoint()
        return new_page
