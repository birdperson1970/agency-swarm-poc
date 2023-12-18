import asyncio
import os
from agency_server.tools.file_patch_tool import FilePatchTool
from agency_server.tools.openai_agency_tools import CurrentTimeTool, GoogleSearchTool
from agency_server.tools.shell_tool import ShellTool, GitHubTool

from agency_swarm import set_openai_key
set_openai_key(os.getenv('OPENAI_API_KEY'))


from agency_swarm.tools import BaseTool
from pydantic import Field
from datetime import datetime
import pytz
import os
from typing import Any, List

from agency_swarm import set_openai_key

from agency_swarm import Agency

from langchain.tools import YouTubeSearchTool
from agency_swarm.tools import ToolFactory
from agency_swarm.util.logging import getLogger
logger = getLogger('SwarmServer')
from agency_swarm import Agent

from langchain.agents import load_tools


logger.info(f"GOOGLE_CSE_ID={os.getenv('GOOGLE_CSE_ID')}  GOOGLE_API_KEY={os.getenv('GOOGLE_API_KEY')}")


from langchain.tools import YouTubeSearchTool
from agency_swarm.tools import ToolFactory
tools =[]
tools.append(ToolFactory.from_langchain_tool(YouTubeSearchTool))
#tools = ToolFactory.from_langchain_tool(ShellTool)


tools.append(CurrentTimeTool)
tools.append(GoogleSearchTool)
tools.append(ShellTool)
#tools.append(GitHubTool)
tools.append(FilePatchTool)

agent_po = Agent(name="agent-po",
            description="Responsible for client communication, task planning and management.",
            instructions="instructions/agent-po.md", # can be a file like ./instructions.md
            files_folder=None,
          #  model="gpt-3.5-turbo-1106",
            tools=tools[:])

agent_arch = Agent(name="agent-architect",
            description="Responsible for creating design and documentation for the project.",
            instructions="instructions/agent-architect.md" ,# can be a file like ./instructions.md
            files_folder=None,
           # model="gpt-3.5-turbo-1106",
            tools=tools[:])

agent_dev = Agent(name="agent-developer",
            description="Reposonsible for implementing all coding tasks.",
            instructions="instructions/agent-developer.md", # can be a file like ./instructions.md
            files_folder=None,
            #model="gpt-3.5-turbo-1106",
            tools=tools[:])

agent_va = Agent(name="agent-va",
            description="Responsible for completing all other tasks.",
            instructions="instructions/agent-va.md", # can be a file like ./instructions.md
            files_folder=None,
            #model="gpt-3.5-turbo-1106",
            tools=tools[:])



class ClusterServer():
    api_key: str
    user_input: str
    name: str
    content: str

    complete: bool = False
    _agency: Agency = None


    def __init__(self): 
        
        self._agency = Agency([
                agent_po,  
                [agent_po, agent_dev],  
                [agent_po, agent_va],   # CEO can initiate communication with Virtual Assistant
                [agent_po, agent_arch],
                [agent_arch, agent_dev],
                [agent_dev, agent_arch]            
            ], shared_instructions='agents/manifesto.md') # shared instructions for all agents

    async def run(self):
       

        self._agency.demo_gradio(height=900)
        # try:
        #     # Yield each message from the generator
        #     for bot_message in gen:
        #         msg =  bot_message.get_formatted_content()
        #         print(f"msg: {msg}")
              
                    
                
        # except StopIteration:
        #     # Handle the end of the conversation if necessary
        #     self.complete = True



server = ClusterServer()

asyncio.run(server.run())

import gradio as gr

def fetch_threads():
    # TODO: Replace placeholder logic with actual thread-fetching logic
    # Example placeholder data
    return [{'thread_id': 1, 'thread_title': 'Thread A', 'thread_content': 'Content A'},
            {'thread_id': 2, 'thread_title': 'Thread B', 'thread_content': 'Content B'},]

def display_threads(thread_data):
    # Transform thread data for display, if necessary.
    return ''.join([f"ID: {thread['thread_id']} Title: {thread['thread_title']} Content: {thread['thread_content']}" for thread in thread_data])

# Gradio interface to display threads
threads_interface = gr.Interface(fn=display_threads, inputs='textbox', outputs='text', title="Thread Display")
# TODO: Integrate threads_interface into the demo_gradio layout within the ClusterServer class.


    # Placeholder for integrating threads_interface into the demo_gradio layout
def demo_gradio(self):
    # Existing Gradio setup...
    
    # Integration of threads_interface
    threads_panel = gr.TabbedInterface([threads_interface], title="Threads")

    # Combine the existing interface(s) and threads_panel into the Gradio layout
    # This is conceptual and needs to be adjusted to the actual implementation of demo_gradio
    existing_demo = gr.Group([]) # This should actually be the existing setup
    final_layout = gr.Split([existing_demo, threads_panel], orientation="vertical")
    final_layout.launch()

