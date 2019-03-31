#!usr/bin/env python
import os

from nupic.swarming import permutations_runner
from swarm_description import SWARM_DESCRIPTION


def swarm(inputFile):

    swarmWorkDir = os.path.abspath("swarm")
    if not os.path.exists(swarmWorkDir):
        os.mkdir(swarmWorkDir)

    permutations_runner.runWithConfig(
        SWARM_DESCRIPTION,
        {"maxWorkers":4, "overwrite":True},
        outputLabel = "network_output",
        outDir=swarmWorkDir,
        permWorkDir=swarmWorkDir
    )

    pass





if __name__ = "__main__":
    swarm("test.csv")
