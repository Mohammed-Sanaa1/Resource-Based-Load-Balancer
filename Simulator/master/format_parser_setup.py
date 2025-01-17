from master.format_util import tf_presets
import argparse

def parse_and_setup_format():
    parser = argparse.ArgumentParser(description="enable or disable pretty output")
    parser.add_argument("-p","--pretty", action="store_true", help="enable pretty formatting")
    args = parser.parse_args()
    return tf_presets(pretty=args.pretty)