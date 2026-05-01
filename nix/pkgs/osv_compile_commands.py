import json
import argparse
import sys
import re
import shlex
from subprocess import Popen, PIPE
from pathlib import Path
from textwrap import dedent
from enum import Enum
from enum import auto as enumAuto

gnuParser = argparse.ArgumentParser(
    description='parse gnu toolkits commands')
gnuParser.add_argument('sources', nargs='*')


class LOG_LEVEL(Enum):
    INFO = enumAuto()
    WARNING = enumAuto()
    ERROR = enumAuto()


def log(msg, level=LOG_LEVEL.INFO):
    dist = {
        LOG_LEVEL.ERROR: sys.stderr,
    }.get(level, sys.stdout)

    print(msg, file=dist)


def echo(obj):
    """ for debugging """
    print(obj)
    return obj


invalidFilenameChars = re.compile(r'[<>:"/?*\\|]')


def is_valid_filename(filename):
    return invalidFilenameChars.search(filename) is None


if __name__ == "__main__":
    argsParser = argparse.ArgumentParser(
        description='generate compile_commands.json.')
    argsParser.add_argument('-f', '--makefile', default=None,
                            help="specify makefile, leave it empty to parse the makefile under current folder")
    argsParser.add_argument('-t', '--targets', nargs='+', required=True,
                            help="specify the targets to build (e.g., 'all')")
    argsParser.add_argument('-c', '--compilers', nargs='*',
                            default=['gcc', 'g++', 'clang', 'clang++', 'cc'],
                            help="specify the compiler executable names")

    args = argsParser.parse_args()

    compilers = args.compilers

    currentDir = Path().resolve()
    makefile = Path(args.makefile) if args.makefile else Path('Makefile')

    compileCmds = {}

    for target in args.targets:
        # Build the make command
        makeCmd = ['make', target, '--just-print']
        if args.makefile:
            makeCmd.extend(['-f', str(makefile)])

        # Run make and capture the output
        process = Popen(makeCmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')

        # Parse each line of the make output
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue

            # Split the line into command segments
            commandSeg = shlex.split(line)
            if len(commandSeg) == 0 or commandSeg[0] not in compilers:
                continue

            # Parse the compile command to extract source files
            info, _ = gnuParser.parse_known_args(commandSeg[1:])
            for source in info.sources:
                if not is_valid_filename(source):
                    log(dedent(f"""\
                        filename "{source}" in command
                            {line}
                        is not a valid filename.
                        Skipping this command.
                        """), LOG_LEVEL.ERROR)
                    continue
                if source not in compileCmds:
                    try:
                        compileCmds[source] = {
                            "directory": str(currentDir.resolve()),
                            "command": line,
                            "file": str((currentDir / source).resolve())
                        }
                    except OSError as err:
                        log(dedent(f"""\
                            during parsing of command
                                {line}
                            an error occurred:
                                {err}
                            Skipping this command.
                            """), LOG_LEVEL.ERROR)

    # Write the compile_commands.json file
    with Path('./compile_commands.json').open('w+') as resultFile:
        json.dump([*compileCmds.values()], resultFile, indent=4)

