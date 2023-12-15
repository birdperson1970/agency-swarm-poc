from agency_swarm.agents import Agent


class TestAgent(Agent):
    def __init__(self):
        super().__init__()
        self.description = "Software Architect"
        self.instructions = "./instructions.md"
