#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Linters for SublimeLiner plugin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from SublimeLinter.lint import Linter
from SublimeLinter.lint import NodeLinter
from SublimeLinter.lint import util


class OdyDennis(Linter):
    """Provides an interface to dennis.

    Installed with ``sudo pip3 install dennis``.

    Based on: https://github.com/NotSqrt/SublimeLinter-contrib-dennis
    """
    name = "Dennis"
    cmd = ("dennis-cmd", "lint", "--reporter", "line", "${args}", "${temp_file}")
    defaults = {
        "selector": "source.po",
        "args": [
            "--excluderules",
            # https://dennis.readthedocs.io/en/latest/linting.html#table-of-warnings-and-errors
            # Comma separated list of rules.
            "W302"  # Ignore "Translated string is identical to source string" rule.
        ]
    }
    regex = r"^.*:(?P<line>\d+):(\d+):(?P<code>(?:(?P<error>[E])|(?P<warning>[W]))\d+):(?P<message>.+)$"
    tempfile_suffix = "dennis-linter"
    word_re = None


class OdyGLSL(Linter):
    """Provides an interface to glslangValidator.

    Download glslang-master-linux-Release.zip package from https://github.com/KhronosGroup/glslang
    releases and place bin/glslangValidator in PATH.

    Based on: https://github.com/numb3r23/SublimeLinter-contrib-glsl
    """
    name = "GLSL"
    cmd = ("glslangValidator", "${file_on_disk}")
    defaults = {
        "selector": "source.glsl",
        "args": [
            # "--suppress-warnings"
        ]
    }
    regex = (r"^ERROR:\s.*:(?P<line>\d+):\s\'(?P<near>.*)\'\s:\s+(?P<message>.+)")
    tempfile_suffix = "-"
    word_re = None


class OdyYamlLint(Linter):
    """Provides an interface to yamllint.

    Installed with ``sudo pip3 install yamllint``.

    Based on: https://github.com/thomasmeeus/SublimeLinter-contrib-yamllint
    """
    name = "YamlLint"
    cmd = ("yamllint", "--format", "parsable", "${file_on_disk}")
    defaults = {
        "selector": "source.yaml",
        "args": [
            "-c", "~/.config/yamllint/config/.yamllint.yaml"
        ]
    }
    regex = (
        r"^.+?:(?P<line>\d+):(?P<col>\d+): \[((?P<warning>warning)|(?P<error>error))\] (?P<message>.+)"
    )
    error_stream = util.STREAM_STDOUT
    word_re = r'^(".*?"|[-\w]+)'
    tempfile_suffix = "-"


class OdyMarkdownLint(NodeLinter):
    """Provides an interface to markdownlint.

    Installed with `sudo npm install -g markdownlint-cli`.

    Based on: https://github.com/jonlabelle/SublimeLinter-contrib-markdownlint
    """
    name = "MDLint"
    cmd = ("markdownlint", "${args}", "${file}")
    defaults = {
        "selector": "text.html.markdown,"
                    "text.html.markdown.multimarkdown,"
                    "text.html.markdown.extended,"
                    "text.html.markdown.gfm",
        "args": [
            "--config", "~/.markdownlintrc"
        ]
    }
    regex = r".+?(?:[:](?P<line>\d+))(?:[:](?P<col>\d+))?\s+(?P<error>MD\d+)?[/]?(?P<message>.+)"
    multiline = False
    line_col_base = (1, 1)
    error_stream = util.STREAM_STDERR
    word_re = None
    tempfile_suffix = "-"


class OdyCppcheck(Linter):
    """Provides an interface to cppcheck.

    Installed cppcheck from repositories. Had to build from source a newer version of cppcheck
    so the ``column`` placeholder can be used in the ``--template`` parameter.

    Based on: https://github.com/SublimeLinter/SublimeLinter-cppcheck
    """
    name = "CppCheck"
    cmd = (
        "cppcheck",
        "--template={file}:{line}:{column}:{severity}:{id}:{message}",
        "--inline-suppr",
        "--quiet",
        "${args}",
        "${file}"
    )
    defaults = {
        "selector": "source.c, source.c++",
        "--std=,+": [],  # example ["c99", "c89"]
        "--enable=,": "style,warning",
    }
    regex = (
        r"^(?P<filename>(:\\|[^:])+):(?P<line>\d+):((?P<col>\d+):)"
        r"((?P<error>error)|(?P<warning>warning|style|performance|portability|information)):"
        r"(?P<code>\w+):(?P<message>.+)"
    )
    on_stderr = None  # handle stderr via split_match
    tempfile_suffix = "-"
