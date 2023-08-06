"""
This example shows how to create an agent with an API server behavior.

The API server behavior is a behavior that exposes a REST API to interact with
the agent. It is based on the FastAPI library.

This example requires the 'webapi' extra to be installed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from piaf.agent import Agent
from piaf.api.behavior import APIServerBehavior

if TYPE_CHECKING:
    from piaf.comm import AID
    from piaf.ptf import AgentPlatformFacade


class APIAgent(Agent):
    """
    An agent running a REST API server to control the simulation.

    It should be launched as a service.
    """

    def __init__(self, aid: AID, platform: AgentPlatformFacade):
        super().__init__(aid, platform)
        self.add_behavior(APIServerBehavior(self))


if __name__ == "__main__":
    import logging

    from piaf.launcher import PlatformLauncher, ServiceDescription

    # Configure logging level and handler to see things
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Create the platform launcher
    launcher = PlatformLauncher("localhost")

    # Add agent
    launcher.add_service(ServiceDescription("API", APIAgent))

    # The program will run until you hit Ctrl+C
    launcher.run()
