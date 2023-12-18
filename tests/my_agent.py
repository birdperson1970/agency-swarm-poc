import os

from agency_swarm import set_openai_key
set_openai_key(os.getenv('OPENAI_API_KEY'))


from agency_swarm.tools import BaseTool
from pydantic import Field
from datetime import datetime
import pytz

class MyCustomTool(BaseTool):
    """
    get the current time
    """

    # Define the fields with descriptions using Pydantic Field
    timezone_str: str = Field(
        ..., description="The timezone you want the time in."
    )

    # Additional fields as required
    # ...

    def run(self):
        """
        The implementation of the run method, where the tool's main functionality is executed.
        This method should utilize the fields defined above to perform its task.
        Doc string description is not required for this method.
        """
        try:
            # Create a timezone object using the pytz library
            timezone = pytz.timezone(self.timezone_str)
            
            # Get the current time in UTC
            utc_dt = datetime.now(pytz.utc)
            
            # Convert the UTC time to the specified timezone
            dt = utc_dt.astimezone(timezone)
            
            # Print the current time in the specified timezone
            print(f"The current time in {self.timezone_str} is {dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Unknown timezone: {self.timezone_str}")
        
        return f"Unknown timezone: {self.timezone_str}"
    
from agency_swarm import Agent

ceo = Agent(name="CEO",
            description="Responsible for client communication, task planning and management.",
            instructions="You must converse with other agents to ensure complete task execution.", # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool])

sa = Agent(name="Software Architect",
            description="Responsible for client communication, task planning and management.",
            instructions="""You are a software architect. Do what you are told.
Always give complete and detailed responses and NEVER summersize your responses as your developers can't fill in the blanks.
The developers depend on you to supply all of the details so they can complete their tasks. """, # can be a file like ./instructions.md
            files_folder=None,
            tools=[MyCustomTool])

from agency_swarm import Agency

agency = Agency([
    ceo,  # CEO will be the entry point for communication with the user
    [ceo, sa],  # CEO can initiate communication with Developer
 ], shared_instructions='agency_manifesto.md') # shared instructions for all agents


gen= (agency.get_completion("""

say hello to the architect                


"""))

while True:
    try:
    # Yield each message from the generator
        for bot_message in gen:
            # if bot_message.sender_name.lower() == "user":
            #     continue

            message = bot_message.get_sender_emoji() + " " + bot_message.get_formatted_content()
            print(message)

    except StopIteration:
    # Handle the end of the conversation if necessary
        pass        


# agency.demo_gradio(height=900)