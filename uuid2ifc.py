#! /usr/bin/env python3

"""
  uuid2ifc.py

  [About]
  Convert between UUIDs and IFC IDs

  [Usage]
  
  To convert from an IFC ID to a UUIDs
  python3 uuid2ifc -i [IFC]

  To convert from a UUID to an IFC ID
  python3 uuid2ifc -g [UUID]

  To generate a new UUID
  python3 uuid2ifc -n
"""

__author__ = "Francesco Anselmo"
__copyright__ = "Copyright 2022"
__credits__ = ["Francesco Anselmo"]
__license__ = "Apache v2"
__version__ = "0.1"
__maintainer__ = "Francesco Anselmo"
__email__ = "francesco.anselmo@gmail.com"
__status__ = "dev"

import uuid
import string
import argparse
from functools import reduce

chars = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_$'

def compress(g):
    bs = [int(g[i:i + 2], 16) for i in range(0, len(g), 2)]

    def b64(v, l=4):
        return ''.join([chars[(v // (64 ** i)) % 64] for i in range(l)][::-1])

    return ''.join([b64(bs[0], 2)] + [b64((bs[i] << 16) + (bs[i + 1] << 8) + bs[i + 2]) for i in range(1, 16, 3)])

def expand(g):
    def b64(v):
        return reduce(lambda a, b: a * 64 + b, map(lambda c: chars.index(c), v))

    bs = [b64(g[0:2])]
    for i in range(5):
        d = b64(g[2 + 4 * i:6 + 4 * i])
        bs += [(d >> (8 * (2 - j))) % 256 for j in range(3)]
    return ''.join(['%02x' % b for b in bs])

def split(g):
    return '%s-%s-%s-%s-%s' % (g[:8], g[8:12], g[12:16], g[16:20], g[20:])

def new_ifc():
    return compress(uuid.uuid4().hex)

def new_uuid():
    return uuid.uuid4().hex

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i","--ifc", default="", help="convert an IFC ID to a UUID")
    group.add_argument("-u","--uuid", default="", help="convert a UUID to an IFC ID")
    parser.add_argument("-n","--new", action='store_true', help="generate a new UUID")

    args = parser.parse_args()

    if args.ifc != "":
        print(split(expand(args.ifc)))
    elif args.uuid != "":
        uuid_stripped = str(args.uuid).replace("-","")
        print(compress(uuid_stripped))
    elif args.new:
        print(split(new_uuid()))

if __name__ == '__main__':
    main()