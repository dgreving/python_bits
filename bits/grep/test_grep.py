from contextlib import contextmanager, redirect_stdout, redirect_stderr
from io import StringIO
from importlib.machinery import SourceFileLoader
import os
import sys
from tempfile import NamedTemporaryFile
from textwrap import dedent
import unittest
import warnings


class GrepTests(unittest.TestCase):

    """Tests for grep.py"""

    file1 = dedent("""
        Hello
        My name is Trey
        Welcome to my file
        This file is lovely
        Goodbye
    """).lstrip('\n')

    file2 = dedent("""
        This is
        A second file
        It has words in it
        It's a pretty good file
        For demonstrating grepping
    """).lstrip('\n')

    file3 = "".join(str(n) + "\n" for n in range(39))

    file4 = "b\n" + "\n" * 1000 + "b\n"

    def test_one_exact_match(self):
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['Trey', my_file])
            self.assertEqual(output, "My name is Trey\n")

    def test_different_capitalization(self):
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['trey', my_file])
            self.assertEqual(output, "")

    def test_two_matches(self):
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['me', my_file])
            self.assertEqual(output, "My name is Trey\nWelcome to my file\n")

    def test_multiple_files(self):
        with make_file(self.file1) as file1, make_file(self.file2) as file2:
            output = run_program('grep.py', ['el', file1, file2])
            self.assertEqual(output, dedent(f"""
                {file1}:Hello
                {file1}:Welcome to my file
                {file1}:This file is lovely
            """).lstrip('\n'))
        with make_file(self.file1) as file1, make_file(self.file2) as file2:
            output = run_program('grep.py', ['file', file1, file2])
            self.assertEqual(output, dedent(f"""
                {file1}:Welcome to my file
                {file1}:This file is lovely
                {file2}:A second file
                {file2}:It's a pretty good file
            """).lstrip('\n'))

    def test_ignoring_capitalization(self):
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['--ignore-case', 'trey', my_file])
            self.assertEqual(output, "My name is Trey\n")
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['trey', my_file, '-i'])
            self.assertEqual(output, "My name is Trey\n")

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_regular_expression_and_line_numbers(self):
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['file$', my_file])
            self.assertEqual(output, "Welcome to my file\n")
        with make_file(self.file2) as my_file:
            output = run_program('grep.py', [r'\ba\b', my_file, '-i'])
            self.assertEqual(
                output,
                "A second file\nIt's a pretty good file\n",
            )
        with make_file(self.file1) as my_file:
            output = run_program('grep.py', ['Trey', my_file, '--line-number'])
            self.assertEqual(output, "2:My name is Trey\n")
        with make_file(self.file1) as file1, make_file(self.file2) as file2:
            output = run_program('grep.py', ['-n', 'el', file1, file2])
            self.assertEqual(output, dedent(f"""
                {file1}:1:Hello
                {file1}:3:Welcome to my file
                {file1}:4:This file is lovely
            """).lstrip())

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_invert_match(self):
        # Lines without the word "file"
        with make_file(self.file1) as file1:
            output = run_program('grep.py', ['--invert-match', 'file', file1])
            self.assertEqual(output, dedent(f"""
                Hello
                My name is Trey
                Goodbye
            """).lstrip('\n'))
        # Lines without spaces
        with make_file(self.file1) as file1, make_file(self.file2) as file2:
            output = run_program('grep.py', ['-v', ' ', file1, file2])
            self.assertEqual(output, dedent(f"""
                {file1}:Hello
                {file1}:Goodbye
            """).lstrip('\n'))

    # To test the Bonus part of this exercise, comment out the following line
    # @unittest.expectedFailure
    def test_initial_tab(self):
        with make_file(self.file4) as file4:
            output = run_program('grep.py', ['-T', '-n', 'b', file4])
            self.assertEqual(
                output.expandtabs(),
                "   1:   b\n1002:   b\n",
            )
        with make_file(self.file3) as file3:
            output = run_program('grep.py', ['-Tn', '0$', file3])
            self.assertEqual(
                output.expandtabs(),
                "  1:    0\n 11:    10\n 21:    20\n 31:    30\n",
            )


class DummyException(Exception):
    """No code will ever raise this exception."""


def run_program(path, args=[], raises=DummyException):
    """
    Run program at given path with given arguments.

    If raises is specified, ensure the given exception is raised.
    """
    old_args = sys.argv
    assert all(isinstance(a, str) for a in args)
    warnings.simplefilter("ignore", ResourceWarning)
    try:
        sys.argv = [path] + args
        with redirect_stdout(StringIO()) as output:
            with redirect_stderr(output):
                try:
                    if '__main__' in sys.modules:
                        del sys.modules['__main__']
                    SourceFileLoader('__main__', path).load_module()
                except raises:
                    return output.getvalue()
                except SystemExit as e:
                    if e.args != (0,):
                        raise SystemExit(output.getvalue()) from e
                if raises is not DummyException:
                    raise AssertionError("{} not raised".format(raises))
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
        os.remove(f.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)