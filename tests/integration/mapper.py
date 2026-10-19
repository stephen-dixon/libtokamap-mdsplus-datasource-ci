import argparse
import json
import sys

import numpy as np
import libtokamap


def map_signal(mapper: libtokamap.Mapper, experiment: str, mapping: str, shot: int):
    res = mapper.map(experiment, mapping, {'shot': shot})
    # libtokamap >= 0.3.0 returns str for string values; older versions returned an S1 array
    if isinstance(res, np.ndarray) and res.dtype == 'S1':
        res = res.tobytes().decode()
    print(f"{mapping}: {res}")
    return res


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shot",
                        type=int,
                        default=1,
                        help="Experimental shot number")
    parser.add_argument("--mapping",
                        type=str,
                        default="test/ip",
                        help="Mapping key string")
    parser.add_argument("--device",
                        type=str,
                        default="dummy_mds",
                        help="Device name (mapping folder name)")
    parser.add_argument("--config-path",
                        type=str,
                        default="config.toml",
                        help="Path to the libtokamap config.toml")
    parser.add_argument("--expected",
                        type=json.loads,
                        default=None,
                        help="Expected result as a JSON value; the test fails if the mapped data differs")

    args = parser.parse_args()

    print("Calling LibTokaMap version:", libtokamap.__version__)
    print("Mapping options:", args)

    mapper = libtokamap.Mapper(args.config_path)

    try:
        res = map_signal(mapper, args.device, args.mapping, args.shot)
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    if args.expected is not None and not np.array_equal(np.asarray(res), np.asarray(args.expected)):
        print(f"FAILED: expected {args.expected}, got {res}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
