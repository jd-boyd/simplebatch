import os, sys
import argparse

def main(args):
    parser = argparse.ArgumentParser(description='Run jobs int the queue')

    #parser.add_argument('--single', action="store_true", default=False)
    
    options = parser.parse_args(args)

def start():
    """Entry point.  It just calls main with the CLI args to make it 
    easier to test."""
    main(sys.argv[1:])

