import argparse


def get_argparser():
    parser = argparse.ArgumentParser(description='NVCCPlugin params')
    parser.add_argument(
        '-t', 
        '--timeit',
        action='store_true',
        help='If set, returns the output of the "timeit" built-in ipython magic instead of stdout.',
    )
    parser.add_argument(
        '-p', 
        '--profile', 
        action='store_true',
        help='If set, runs the nvidia nsight compute profiler. Has no effect if used with --timeit.',
    )
    parser.add_argument(
        '-a',
        '--profiler-args',
        type=str,
        default='',
        help='Extra options that can be passed to the nvidia nsight compute profiler.',
    )
    return parser


def print_out(out: str):
    for l in out.split('\n'):
        print(l)
