#!/usr/bin/env python3


import os
import re
import sys
import fire
import enum
import jinja2
import datetime
import colorama
import subprocess
from typing import Union


__version__: str = "20230622"


def _ljust(s: str) -> str:
    return " " + s.ljust(9, " ")


class Miao:
    """
    Project manager for generating CMake file
    """

    sep: str = os.sep
    width: int = os.get_terminal_size()[0]

    # Basic CMakeLists.txt file
    basic_template: str = """
cmake_minimum_required(VERSION 3.0)
project({{ project_name }})
{{ language_options }}
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
add_executable({{ project_name }} ${SOURCES})
    """.strip()

    # CXX language options
    template_cpp: str = """
set(CMAKE_CXX_STANDARD {{ lang_standard }})
file(GLOB_RECURSE SOURCES "src/*.cpp")
    """.strip()

    # C language options
    template_c: str = """
set(CMAKE_C_STANDARD {{ lang_standard }})
file(GLOB_RECURSE SOURCES "src/*.c")
    """.strip()

    class _ConsoleOutputType(enum.Enum):
        """
        Apply different colors according to the different output types."
        """

        LOG = enum.auto()
        WARNING = enum.auto()
        ERROR = enum.auto()

    def __init__(self, use_color: bool = True):
        """
        If the standard output is TTY,
        then enable color; otherwise, do not enable it.
        """
        print(f"Miao Version {__version__}")
        self.use_color: bool = use_color

    @property
    def current_directory(self) -> str:
        return os.getcwd()

    def _print(
        self,
        text: str = "",
        prefix: str = "",
        output_type: _ConsoleOutputType = _ConsoleOutputType.LOG,
    ):
        if self.use_color:
            if output_type is Miao._ConsoleOutputType.ERROR:
                prefix = f"{colorama.Fore.RED}{prefix}{colorama.Fore.RESET}"
            elif output_type is Miao._ConsoleOutputType.WARNING:
                prefix = f"{colorama.Fore.YELLOW}{prefix}{colorama.Fore.RESET}"
            else:
                prefix = f"{colorama.Fore.GREEN}{prefix}{colorama.Fore.RESET}"
        print(f"{prefix} {text}")

    def _find_project_root(self, start, filename: str) -> Union[str, None]:
        current = start
        while True:
            if filename in os.listdir(current):
                return current
            else:
                parent = os.path.dirname(current)
                if parent == current:
                    return None
                else:
                    current = parent

    def find_project_root(self) -> Union[str, None]:
        return self._find_project_root(self.current_directory, "CMakeLists.txt")

    def run(self):
        """
        Run the current project.
        """

        executable: str = self.build()
        time_now: str = str(datetime.datetime.now())
        print(f"{time_now.center(self.width, '=')}")
        self._print(executable, "Running")
        print(self.width * "=")
        subprocess.run([executable])

    def _enter_build_dir(self, *, echo: bool = True) -> str:
        """
        If the path does not exist,
        create the directory.
        This function will establish some instance variables so that they can be used in other functions that call it.
        This function also returns the path to the build directory for further use,
        such as in the clean command.
        Since CMake does not come with a built-in clean command,
        the best practice suggested online is to delete the build directory.
        """
        root: Union[str, None] = self.find_project_root()
        if root is None:
            self._print(
                f"could not find `CMakeLists.txt` in `{self.current_directory}` or any parent directory",
                "error:",
                Miao._ConsoleOutputType.ERROR,
            )
            sys.exit(2)
        if echo:
            self._print(root, _ljust("root: "))
        self.project_name = root.split(self.sep)[-1]
        old_dir: str = self.current_directory
        if echo:
            self._print(old_dir, _ljust("pwd: "))
        if os.path.exists(build_dir := f"{root}/build"):
            if echo:
                self._print(build_dir, _ljust("Entering"))
            os.chdir(build_dir)
        else:
            self._print(build_dir, "mkdir")
            os.mkdir(build_dir)
            if echo:
                self._print(build_dir, "Entering")
            os.chdir(build_dir)
        self.project_root: str = root
        self.old_dir: str = old_dir
        self.build_dir: str = build_dir
        return build_dir

    def build(self) -> str:
        self._enter_build_dir()
        subprocess.run(["cmake", self.project_root])
        subprocess.run(["make"])
        os.chdir(self.old_dir)
        return f"{self.build_dir}/{self.project_name}"

    def clean(self):
        build_dir: str = self._enter_build_dir(echo=False)
        self._print(build_dir, "Removing")
        subprocess.run(["rm", "-rf", build_dir])

    def new(self, project_name: str = "", *, language: str = "cpp", standard: str = ""):
        """
        Create a new project.
        """
        project_name = project_name.replace(" ", "_")

        # Check if project name is valid.
        def is_valid_string(s: str) -> bool:
            return bool(re.fullmatch(r"^[\w-]+$", s))

        if (
            project_name == ""
            or project_name[0].isdigit()
            or not is_valid_string(project_name)
        ):
            self._print(
                "invalid project name", _ljust("error"), Miao._ConsoleOutputType.ERROR
            )
            sys.exit(1)

        language_options: str = ""
        language = language.lower()

        if language not in ("c", "cpp", "cxx", "c++"):
            self._print(
                "invalid language option",
                _ljust("error"),
                Miao._ConsoleOutputType.ERROR,
            )
            sys.exit(1)
        else:
            if language in ("cpp", "cxx", "c++"):
                language_options += self.template_cpp
                if standard == "":
                    standard = "17"
            elif language == "c":
                language_options += self.template_c
                if standard == "":
                    standard = "11"
            else:
                sys.exit(1)

            # Embed it into the template string later.
            self.language_options = jinja2.Template(language_options).render(
                lang_standard=standard
            )

        # Check if directory exists
        for file_name in os.listdir():
            if project_name == file_name:
                # Instead of
                # ```raise RuntimeError("Already exists")```,
                # handle it more elegantly
                self._print(
                    f"directory `{project_name}` already exists",
                    _ljust("error"),
                    Miao._ConsoleOutputType.ERROR,
                )
                sys.exit(1)

        # Creating project directory
        os.mkdir(project_name)
        self.project_name = project_name
        self._print(self.project_name, _ljust("Created"))
        project_directory: str = f"{self.current_directory}/{self.project_name}"

        # Creating `CMakeLists.txt`
        with open(f"{project_directory}/CMakeLists.txt", "w") as cmake_list:
            cmake_list.write(
                jinja2.Template(self.basic_template).render(
                    project_name=self.project_name,
                    language_options=self.language_options,
                )
            )
            self._print("CMakelists.txt", _ljust("Added"))

        # for debugging purpose,
        # so that users will know what was written to
        # the CMake file immediately & directly from
        # their terminal
        __tmp: str = self.language_options.replace("\n", _ljust("\n    "))
        self._print(f"```{__tmp}```", _ljust("(debug)"))

        # Creating `src` directory
        os.mkdir(f"{project_directory}/src")
        self._print("src/ directory", _ljust("Created"))

        # Creating minimum source file
        source_code_file_name: str = f"main.{'c' if language == 'c' else 'cpp'}"
        with open(
            f"{project_directory}/src/{source_code_file_name}", "w"
        ) as minimum_source_code:
            MINIMUM_SOURCE_CODE: str = """
#include <stdio.h>


int main(int argc, char** argv) {

    puts("Hello, world!");
    return 0;
}
            """.strip()
            minimum_source_code.write(MINIMUM_SOURCE_CODE)
            self._print(source_code_file_name, _ljust("Added"))

        # Creating `build` directory
        os.mkdir(f"{project_directory}/build")
        self._print("build/ directory", _ljust("Created"))

    def _todo(self):
        import inspect

        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        caller_name = caller_frame[1][3]
        self._print("comming soon", f"`{caller_name}`", Miao._ConsoleOutputType.WARNING)
        self._print(
            "not implemented", f"`{caller_name}`", Miao._ConsoleOutputType.WARNING
        )


def main():
    fire.Fire(Miao(True if sys.stdout.isatty() else False))


if __name__ == "__main__":
    main()
