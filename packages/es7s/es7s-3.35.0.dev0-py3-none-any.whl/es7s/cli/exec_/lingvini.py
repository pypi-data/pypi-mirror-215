# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import re
import typing as t
from math import floor
from os import getcwd
from pathlib import Path

import click
import pytermor as pt
from pytermor import NOOP_STYLE

from es7s.shared import FrozenStyle, Styles, get_logger, get_stdout
from es7s.shared.exception import SubprocessExitCodeError
from es7s.shared.git import GitRepo
from es7s.shared.plang import PLang
from .._decorators import _catch_and_log_and_exit, cli_argument, cli_command, cli_option
from ...shared.linguist import Linguist


@cli_command(__file__, short_help="programming language statistics")
@cli_argument("path", type=click.Path(exists=True), nargs=-1, required=False)
@cli_option(
    "-D",
    "--docker",
    is_flag=True,
    default=False,
    help="Run github-linguist in a docker container.",
)
@cli_option(
    "-N",
    "--no-cache",
    is_flag=True,
    default=False,
    help="Calculate the value regardless of the cache state and do not update it.",
)
@_catch_and_log_and_exit
class LangBreakdownCommand:
    """
    ...
    """

    COL_PAD = pt.pad(2)
    SHARED_SCALE_LEN = 40
    SHARED_SCALE_CHAR = "▔"  # "━▁"

    def __init__(
        self,
        docker: bool,
        no_cache: bool,
        path: tuple[Path, ...] | None = None,
        **kwargs,
    ):
        self._use_cache = not no_cache

        stdout = get_stdout()
        if not path:
            path = [
                getcwd(),
            ]

        psetd = dict()
        psetf = set()
        for p in path:
            absp = Path(p).resolve()
            if os.path.isdir(absp):  # linguist cannot collect stats on repo part (i.e. a path),
                try:  # only on the whole thing. that's why we resolve folder paths to
                    repo = GitRepo(absp)  # corresponding top-level git dir, and "unique" them
                except ValueError as e:
                    get_logger().warning(f"Skipping: {e}")
                    continue
                psetd.setdefault(repo.path, repo)
            else:
                psetf.add(absp)

        ps = [(k, v) for k, v in psetd.items()]
        ps += [(k, None) for k in sorted(psetf)]
        for idx, (absp, repo) in enumerate(ps):
            self._run(absp, docker, repo)
            if idx < len(ps) - 1:
                stdout.echo()

    def _run(self, target: Path, docker: bool, repo: GitRepo = None):
        stdout = get_stdout()
        target_is_dir = repo is not None

        title = str(target)
        cpout = None

        if repo:
            if self._use_cache:
                cpout = repo.get_cached_stats()
            if repo_name := repo.get_repo_name():
                title = repo_name

        if not cpout:
            try:
                cpout = Linguist.get_lang_statistics(target, docker, breakdown=target_is_dir)
            except SubprocessExitCodeError as e:
                stdout.echo(title + ': ', nl=False)
                stdout.echo_rendered("<error>", Styles.ERROR)
                get_logger().non_fatal_exception(e)
                return
            if cpout and repo and self._use_cache:
                repo.update_cached_stats(cpout)

        if not cpout:
            stdout.echo(title + ': ', nl=False)
            stdout.echo_rendered("<empty>", Styles.TEXT_DEFAULT)
            get_logger().debug("Empty stdout -- no data")
            return

        lines = cpout.splitlines()
        assert len(lines)

        if target_is_dir:
            get_logger().debug("Rendering as directory stats")
            self._render_dir_info(lines, title)
            stdout.echo()
        else:
            get_logger().debug("Rendering as file stats")
            self._render_file_info(lines, title)

    def _render_dir_info(self, lines: list[str], title: str):
        data: t.List[t.Sequence[pt.RT, ...]] = []
        shared_scale: pt.Text = pt.Text()
        failed_lines = []
        for line in lines:
            if not line.strip() and not failed_lines:  # if empty string and all previous were fine,
                break                                  # its a separator between brief and details
            try:
                perc, linenum, lang = re.split(r"\s+", line)
                ratio = float(perc.removesuffix("%")) / 100
            except:
                failed_lines.append(line)
                continue

            lang_st = self._get_lang_st(lang)
            scale = Scale(ratio, NOOP_STYLE, lang_st)

            shared_scale += Scale(
                ratio, NOOP_STYLE, lang_st, self.SHARED_SCALE_LEN, False, self.SHARED_SCALE_CHAR
            ).blocks

            data.append(
                (
                    scale,
                    pt.highlight(linenum.strip()),
                    pt.Fragment(lang, lang_st),
                )
            )

        if failed_lines:
            get_logger().warning(f"Failed to parse:" + "\n> ".join(("", *failed_lines)))

        def col_lens():
            if not len(data):
                return
            for col in range(len(data[0])):
                yield max(len(r[col]) for r in data)

        stdout = get_stdout()
        stdout.echo(title.center(self.SHARED_SCALE_LEN))

        if len(shared_scale) and len(frags := shared_scale.as_fragments()):
            if (chars_short := self.SHARED_SCALE_LEN - len(shared_scale)) > 0:
                if first_frag := frags.pop(0):
                    shared_scale.prepend(
                        pt.Fragment(first_frag.raw()[0] * chars_short, first_frag.style)
                    )
            stdout.echo_rendered(shared_scale)

        col_len = [*col_lens()]
        for line in data:
            for idx, cell in enumerate(line):
                val = cell
                vpad = pt.pad(col_len[idx] - len(cell))
                if idx in (0, 1):
                    val = vpad + val
                else:
                    val += vpad
                val += self.COL_PAD
                stdout.echo_rendered(val, nl=False)
            get_stdout().echo()

    def _render_file_info(self, lines: list[str], title: str):
        stdout = get_stdout()
        col_lens = [9, 9, PLang.get_longest_key_len(), None]
        data_row = []
        first_line = lines.pop(0)
        zero_len = False
        if ":" in first_line and "lines" in first_line:
            _, code_lines_str = first_line.rsplit(":", 1)
            code_lines, logic_lines = re.findall(r"\d+", code_lines_str.strip())
            if code_lines == "0" or logic_lines == "0":
                zero_len = True
                zfrag = pt.Fragment("-", pt.Highlighter.STYLE_NUL)
                data_row.extend([zfrag] * 2)
            else:
                data_row.extend((pt.highlight(code_lines), pt.highlight(logic_lines)))

        def next_value():
            return lines.pop(0).partition(":")[2].strip()

        ftype = next_value()
        mime = next_value()

        lang = next_value()
        if not lang:
            lang_st = NOOP_STYLE if not zero_len else pt.Highlighter.STYLE_NUL
            lang_frag = pt.Fragment(ftype, lang_st)
        else:
            lang_st = self._get_lang_st(lang)
            lang_frag = pt.Fragment(lang, lang_st)
        data_row.append(lang_frag)

        for idx, cell in enumerate(data_row):
            vpad = pt.pad((col_lens[idx] or 0) - len(cell))
            if idx < 2:
                val = vpad + cell
            else:
                val = cell + vpad
            stdout.echo_rendered(self.COL_PAD + val, nl=False)

        stdout.echo(title, nl=False)

    def _get_lang_st(self, lang_str: str) -> FrozenStyle:
        if lang_color := PLang.get(lang_str.strip()):
            return FrozenStyle(fg=pt.ColorRGB(pt.rgb_to_hex(lang_color)))
        return NOOP_STYLE


class Scale(pt.Text):
    SCALE_LEN = 10

    def __init__(
        self,
        ratio: float,
        label_st: pt.FT,
        scale_st: pt.FT,
        length: int = SCALE_LEN,
        allow_partials: bool = True,
        full_block_char: str = "█",
    ):
        self._ratio = ratio
        self._label_st = label_st
        self._scale_st = scale_st
        self._length = length
        self._allow_partials = allow_partials
        self._full_block_char = full_block_char

        self.label: str
        self.blocks: str
        super().__init__(*self._make())

    def _make(self) -> t.Iterable[pt.Fragment]:
        label_str = pt.format_auto_float(100 * self._ratio, 3) + "% "
        self.label = pt.Fragment(" " + label_str, self._label_st)

        char_num: float = self._length * self._ratio
        full_block_num = floor(char_num)
        blocks_str = self._full_block_char * full_block_num
        if self._allow_partials:
            blocks_str += self._get_partial_block(char_num - full_block_num)
        self.blocks = pt.Fragment(blocks_str, self._scale_st)

        yield self.label
        yield self.blocks
        yield pt.Fragment(" " * (self._length - len(self.blocks)), self._scale_st)

    def _get_partial_block(self, val: float) -> str:
        if val >= 7 / 8:
            return "▉"
        elif val >= 6 / 8:
            return "▊"
        elif val >= 5 / 8:
            return "▋"
        elif val >= 4 / 8:
            return "▌"
        elif val >= 3 / 8:
            return "▍"
        elif val >= 2 / 8:
            return "▎"
        elif val >= 1 / 8:
            return "▏"
        return ""
