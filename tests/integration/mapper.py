import argparse
from pathlib import Path
from typing import Any, override
import numpy as np
import json
import libtokamap


def map(mapper: libtokamap.Mapper, mapping: str, signal: str, shot: int):
    res = mapper.map(mapping, signal, {'shot': shot})
    if res.dtype == 'S1':
        res = res.tobytes().decode()
    print(f"{signal}: {res}")
    return res


def map_all(mapper: libtokamap.Mapper, mapping: str, key: str, shot: int):
    map(mapper, mapping, key, shot)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--shot", 
                        type=int, 
                        default=1, 
                        help="Experimental shot number")

    parser.add_argument("--mds-host", 
                        type=str, 
                        default="localhost", 
                        help="MDSPLUS server IP or DNS")
    parser.add_argument("--mds-port", 
                        type=int, 
                        default=8000, 
                        help="MDSPLUS server port number")

    parser.add_argument("--mapping", 
                        type=str, 
                        default="test/ip", 
                        help="Mapping key string")
    parser.add_argument("--device", 
                        type=str, 
                        default="dummy_mds", 
                        help="Device name (mapping folder name)")
    parser.add_argument("--mapping-directory-path", 
                        type=str, 
                        default="mappings", 
                        help="Path to the json mappings directory")
    parser.add_argument("--config-path", 
                        type=str, 
                        default="config.toml", 
                        help="Path to the libtokamap config.toml")
    parser.add_argument("--data-source-lib-path", 
                        type=str, 
                        default="build/libmdsplus_data_source.dylib", 
                        help="Path to the data source shared library")
    parser.add_argument("--factory-name", 
                        type=str, 
                        default="mdsplus_factory", 
                        help="Data source factory name")

    args = parser.parse_args()

    print("Calling LibTokaMap version:", libtokamap.__version__)
    print("Mapping options:")
    print(args)

    mapper = libtokamap.Mapper(args.config_path)
    # mapper.register_data_source_factory(args.factory_name, args.data_source_lib_path)
    #
    # plugin_args = {
    #         "host": args.mds_host,
    #         "port": args.mds_port,
    #         }
    # mapper.register_data_source(args.mds_plugin_name, args.factory_name, plugin_args)
    mapping = args.device

    try:
        map_all(mapper, mapping, args.mapping, args.shot)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    import sys
    # import timeit
    # print(timeit.timeit("main()", number=10, setup="from __main__ import main"))
    main()
