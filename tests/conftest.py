"""Report each test as a sentence, the way the dotfiles' checks read."""

import pytest

MARKS = {"passed": ("green", "✓"), "failed": ("red", "✗"), "skipped": ("yellow", "-")}


def first_line(doc: str | None, fallback: str) -> str:
    """Return a docstring's first line, or the fallback when there is none."""
    return doc.strip().splitlines()[0] if doc and doc.strip() else fallback


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Give each report its test's sentence and its module's subject."""
    report = yield
    report.sentence = first_line(item.obj.__doc__, item.name)
    report.subject = first_line(item.module.__doc__, item.module.__name__)
    return report


def pytest_report_teststatus(report):
    """Stop pytest printing its own dot or letter for each test."""
    return report.outcome, "", ""


def pytest_assertrepr_compare(op, left, right):
    """Show a failed == as expected and got."""
    if op == "==":
        return ["", f"expected: {right!r}", f"got:      {left!r}"]


class Sentences:
    """Print a heading per subject, a line per test, and the totals."""

    def __init__(self, config):
        self.out = config.get_terminal_writer()
        self.counts = dict.fromkeys(MARKS, 0)
        self.subject = None

    def line(self, outcome, sentence, note="", detail=""):
        """Print one check's line, a note beside it, and any detail under it."""
        color, mark = MARKS[outcome]
        self.counts[outcome] += 1
        self.out.write(f"  {mark}", **{color: True})
        self.out.write(f" {sentence}")
        self.out.line(f" ({note})" if note else "", **{color: True})
        for text in detail.splitlines():
            self.out.line(f"      {text.strip()}")

    def pytest_collectreport(self, report):
        """Report a test file that couldn't be read."""
        if report.failed:
            self.line("failed", f"{report.nodeid} loads", detail=str(report.longrepr))

    def pytest_runtest_logreport(self, report):
        """Report a test once: when it ran, or when its setup stopped it."""
        if report.when == "call" or not report.passed:
            if report.subject != self.subject:
                self.subject = report.subject
                self.out.line()
                self.out.line(self.subject, bold=True)
            if report.skipped:
                reason = report.longrepr[2].removeprefix("Skipped: ")
                self.line("skipped", report.sentence, note=f"skipped: {reason}")
            elif report.failed:
                message = report.longrepr.reprcrash.message
                detail = message.removeprefix("AssertionError: assert ")
                self.line("failed", report.sentence, detail=detail.strip())
            else:
                self.line("passed", report.sentence)

    def pytest_unconfigure(self):
        """Print the totals."""
        totals = (f"{count} {outcome}" for outcome, count in self.counts.items())
        self.out.line(", ".join(totals), bold=True)


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    """Register the reporter once pytest's own terminal reporter exists."""
    config.pluginmanager.register(Sentences(config))
