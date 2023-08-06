#!/usr/bin/env python3

import argparse
from . import dump
from . import send
from . import decode

def add_arguments(parser: 'argparse.ArgumentParser') -> None:
	subparsers = parser.add_subparsers()
	dump.add_parser(subparsers)
	send.add_parser(subparsers)
	decode.add_parser(subparsers)
