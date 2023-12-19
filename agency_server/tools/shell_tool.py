import asyncio
import platform
import warnings
from typing import Any, List, Optional, Type, Union


from agency_swarm.tools import BaseTool


# """Wrapper around subprocess to run commands."""
# from __future__ import annotations
from pydantic import BaseModel, Field, root_validator
import platform
import re
import subprocess
from typing import TYPE_CHECKING, List, Union
from uuid import uuid4

import pexpect
from agency_swarm.util.logging import getLogger

logger = getLogger("BashProcess")


class BashProcess:
    """
    Wrapper class for starting subprocesses.
    Uses the python built-in subprocesses.run()
    Persistent processes are **not** available
    on Windows systems, as pexpect makes use of
    Unix pseudoterminals (ptys). MacOS and Linux
    are okay.

    Example:
        .. code-block:: python

            from langchain.utilities.bash import BashProcess

            bash = BashProcess(
                strip_newlines = False,
                return_err_output = False,
                persistent = False
            )
            bash.run('echo \'hello world\'')

    """

    strip_newlines: bool = False
    """Whether or not to run .strip() on the output"""
    return_err_output: bool = False
    """Whether or not to return the output of a failed
    command, or just the error message and stacktrace"""
    persistent: bool = False
    """Whether or not to spawn a persistent session
    NOTE: Unavailable for Windows environments"""

    def __init__(
        self,
        strip_newlines: bool = False,
        return_err_output: bool = False,
        persistent: bool = False,
    ):
        """
        Initializes with default settings
        """
        self.strip_newlines = strip_newlines
        self.return_err_output = return_err_output
        self.prompt = ""
        self.process = None
        if persistent:
            self.prompt = str(uuid4())
            self.process = self._initialize_persistent_process(self, self.prompt)

    @staticmethod
    def _lazy_import_pexpect() -> pexpect:
        """Import pexpect only when needed."""
        if platform.system() == "Windows":
            raise ValueError(
                "Persistent bash processes are not yet supported on Windows."
            )
        try:
            import pexpect

        except ImportError:
            raise ImportError(
                "pexpect required for persistent bash processes."
                " To install, run `pip install pexpect`."
            )
        return pexpect

    def _initialize_persistent_process(self, prompt: str) -> pexpect.spawn:
        # Start bash in a clean environment
        # Doesn't work on windows
        """
        Initializes a persistent bash setting in a
        clean environment.
        NOTE: Unavailable on Windows

        Args:
            Prompt(str): the bash command to execute
        """  # noqa: E501
        pexpect = self._lazy_import_pexpect()
        process = pexpect.spawn(
            "env", ["-i", "bash", "--norc", "--noprofile"], encoding="utf-8"
        )
        # Set the custom prompt
        process.sendline("PS1=" + prompt)

        process.expect_exact(prompt, timeout=10)
        return process

    def run(self, commands: Union[str, List[str]]) -> str:
        """
        Run commands in either an existing persistent
        subprocess or on in a new subprocess environment.

        Args:
            commands(List[str]): a list of commands to
                execute in the session
        """  # noqa: E501
        if isinstance(commands, str):
            commands = [commands]
        commands = ";".join(commands)
        if self.process is not None:
            return self._run_persistent(
                commands,
            )
        else:
            return self._run(commands)

    def _run(self, command: str) -> str:
        """
        Runs a command in a subprocess and returns
        the output.

        Args:
            command: The command to run
        """  # noqa: E501
        try:
            output = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            ).stdout.decode()
        except subprocess.CalledProcessError as error:
            if self.return_err_output:
                return error.stdout.decode()
            return str(error)
        if self.strip_newlines:
            output = output.strip()
        return output

    def process_output(self, output: str, command: str) -> str:
        """
        Uses regex to remove the command from the output

        Args:
            output: a process' output string
            command: the executed command
        """  # noqa: E501
        pattern = re.escape(command) + r"\s*\n"
        output = re.sub(pattern, "", output, count=1)
        return output.strip()

    def _run_persistent(self, command: str) -> str:
        """
        Runs commands in a persistent environment
        and returns the output.

        Args:
            command: the command to execute
        """  # noqa: E501
        pexpect = self._lazy_import_pexpect()
        if self.process is None:
            raise ValueError("Process not initialized")
        self.process.sendline(command)

        # Clear the output with an empty string
        self.process.expect(self.prompt, timeout=10)
        self.process.sendline("")

        try:
            self.process.expect([self.prompt, pexpect.EOF], timeout=10)
        except pexpect.TIMEOUT:
            return f"Timeout error while executing command {command}"
        if self.process.after == pexpect.EOF:
            return f"Exited with error status: {self.process.exitstatus}"
        output = self.process.before
        output = self.process_output(output, command)
        if self.strip_newlines:
            return output.strip()
        return output


class ShellInput(BaseTool):
    """Commands for the Bash Shell tool."""

    commands: Union[str, List[str]] = Field(
        ...,
        description="List of shell commands to run. Deserialized using json.loads",
    )
    """List of shell commands to run."""

    def _validate_commands(cls, values: dict) -> dict:
        """Validate commands."""
        # TODO: Add real validators
        commands = values.get("commands")
        if not isinstance(commands, list):
            values["commands"] = [commands]
        # Warn that the bash tool is not safe
        warnings.warn(
            "The shell tool has no safeguards by default. Use at your own risk."
        )
        return values


def _get_default_bash_process() -> Any:
    """Get default bash process."""

    return BashProcess(return_err_output=True)


def _get_platform() -> str:
    """Get platform."""
    system = platform.system()
    if system == "Darwin":
        return "MacOS"
    return system


class ShellTool(BaseTool):
    """Tool to run shell commands excluding git and gh use theGitHubTool instead."""

    commands: List[str] = Field(
        ...,
        description="Run shell list of commands on this {_get_platform()} machine. The bash shell command and argument you wish to ececute.",
    )

    def run(self):
        process = _get_default_bash_process()
        commands = [*self.commands]
        return process.run(commands)


class GitHubTool(BaseTool):
    """Tool to run GitHub commands."""

    agent_id: str = Field(..., description="Your agent_id to authorize you on GitHub.")
    commands: List[str] = Field(
        ..., description="Run GitHub 'git' and 'gh' commands you wish to ececute."
    )

    def run(self):
        process = _get_default_bash_process()

        commands = [f"~/bin/git_switch.sh {self.agent_id}", *self.commands]
        return process.run(commands)
