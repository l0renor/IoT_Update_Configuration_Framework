#!/usr/bin/env python3
import subprocess


class CallError(Exception):
    pass


def call(cmd: str) -> str:
    try:
        output: str = subprocess.run(
            cmd,
            shell=True,
            check=True,
            executable="/bin/bash",
            capture_output=True,
            text=True
        ).stdout
        return output
    except subprocess.CalledProcessError as e:
        raise CallError(e.stderr)
