# flake8: noqa  # pylint: disable=wrong-import-position,no-member
import os
from unittest.mock import patch
patch('os.urandom', wraps=os.urandom).start()
patch('random._urandom', new=os.urandom).start()

from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys
from tempfile import NamedTemporaryFile
from textwrap import dedent
import unittest
import warnings


WORDS1 = dedent("""
    acorn
    aged
    armor
    axis
    baker
    brink
    cape
    crawl
    crib
    deal
    decay
    dice
    dice
    doing
    drown
    eats
    ebony
    flock
    food
    fool
    frisk
    grit
    gummy
    hash
    heat
    jazz
    jog
    jot
    juror
    keg
    old
    petal
    proof
    puma
    repay
    rust
    said
    shore
    smog
    spend
    stood
    sweep
    taps
    taunt
    trade
    tusk
    widow
    wispy
    wok
    wool
""").lstrip('\n')

WORDS2 = dedent("""
    ebook
    creme
    blimp
    voice
    duo
""").lstrip('\n')

WORDS3 = dedent("""
    ivy
    perch
""").lstrip('\n')


class PassphraseTests(unittest.TestCase):

    """Tests for passphrase.py"""

    def setUp(self):
        os.urandom.reset_mock()

    def test_words_seem_random(self):
        with make_file(WORDS1) as my_file:
            output1 = run_program('passphrase.py', [my_file])
            output2 = run_program('passphrase.py', [my_file])
            self.assertNotEqual(
                output1,
                output2,
                "Running twice results in different words",
            )
            self.assertGreater(
                len(set(output1.split())),
                2,
                "4 words from 50 choices makes >2 unique words",
            )
            self.assertGreater(
                len(set(output2.split())),
                2,
                "4 words from 50 choices makes >2 unique words",
            )

    def test_four_words_printed(self):
        with make_file(WORDS2) as my_file:
            self.assertRegex(
                run_program('passphrase.py', [my_file]),
                r"\w+ \w+ \w+ \w+\n",
                "Should print 4 words with spaces between them",
            )

    def test_just_two_words_in_file(self):
        with make_file(WORDS3) as my_file:
            self.assertRegex(
                run_program('passphrase.py', [my_file]),
                r"(ivy|perch)( (ivy|perch)){3}\n",
            )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_specifying_number_of_words_to_generate(self):
        with make_file(WORDS2) as my_file:
            self.assertRegex(
                run_program('passphrase.py', ['-w 6', my_file]),
                r"\w+ \w+ \w+ \w+ \w+ \w+\n",
                "Should print 6 words with spaces between them",
            )
            self.assertRegex(
                run_program('passphrase.py', ['--words=8', my_file]),
                r"\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+\n",
                "Should print 8 words with spaces between them",
            )
            self.assertRegex(
                run_program('passphrase.py', [my_file, '-w 3']),
                r"\w+ \w+ \w+\n",
                "Should print 3 words with spaces between them",
            )
        with make_file(WORDS3) as my_file:
            self.assertIn(
                run_program('passphrase.py', [my_file, '--words=2']),
                {'ivy ivy\n', 'ivy perch\n', 'perch ivy\n', 'perch perch\n'},
                "2 words generated must be one of the 2 in the file",
            )
            self.assertIn(
                run_program('passphrase.py', [my_file, '-w 2']),
                {'ivy ivy\n', 'ivy perch\n', 'perch ivy\n', 'perch perch\n'},
                "2 words generated must be one of the 2 in the file",
            )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_actually_random(self):
        with make_file(WORDS2) as my_file:
            self.assertEqual(os.urandom.call_count, 0)
            self.assertRegex(
                run_program('passphrase.py', ['-w 6', my_file]),
                r"\w+ \w+ \w+ \w+ \w+ \w+\n",
                "Should print 6 words with spaces between them",
            )
            self.assertGreaterEqual(
                os.urandom.call_count,
                6,
                "At least 6 cryptographically-random numbers were generated",
            )

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_verbose_mode(self):
        with make_file(WORDS2) as my_file:
            self.assertEqual(
                run_program('passphrase.py', [my_file, '-w 6', '--verbose']).splitlines()[1:],
                [
                    "This 6-word passphrase picked from 5 words is similar to a"
                    " 2 character password (entropy 14)"
                ],
            )
        with make_file(WORDS1) as my_file:
            output, error = run_program(
                'passphrase.py',
                ['-w 21', '--verbose', my_file],
                stderr=True,
            )
            self.assertEqual(
                error,
                "This 21-word passphrase picked from 50 words is similar to a "
                "20 character password (entropy 119)\n",
            )


class DummyException(Exception):
    """No code will ever raise this exception."""


try:
    DIRECTORY = Path(__file__).resolve().parent
except NameError:
    DIRECTORY = Path.cwd()


def run_program(path, args=[], raises=DummyException, stderr=False):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    path = str(DIRECTORY / path)
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            error = StringIO() if stderr else output
            with redirect_stderr(error):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    SourceFileLoader('__main__', path).load_module()
                except raises:
                    pass
                except SystemExit as e:
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                else:
                    if raises is not DummyException:
                        raise AssertionError("{} not raised".format(raises))
                if stderr:
                    return output.getvalue(), error.getvalue()
                else:
                    return output.getvalue()
    finally:
        sys.argv = old_args


@contextmanager
def make_file(contents=None):
    """Context manager providing name of a file containing given contents."""
    with NamedTemporaryFile(mode='wt', encoding='utf-8', delete=False) as f:
        if contents:
            f.write(contents)
    try:
        yield f.name
    finally:
        Path(f.name).unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
