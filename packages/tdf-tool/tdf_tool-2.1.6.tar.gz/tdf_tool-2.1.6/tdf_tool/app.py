import fire

from tdf_tool.pipeline import Pipeline
from ruamel import yaml

from tdf_tool.tools.print import Print


def main():
    fire.Fire(Pipeline())
