
import asyncio
from agency_swarm.tools import BaseTool

from pydantic import Field
from datetime import datetime
import pytz

class CurrentTimeTool(BaseTool):
    timezone_str: str = Field(
        ..., description="The timezone you want the time in."
    )
    def run(self):
        try:
            timezone = pytz.timezone(self.timezone_str)
            utc_dt = datetime.now(pytz.utc)
            dt = utc_dt.astimezone(timezone)
            print(f"The current time in {self.timezone_str} is {dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            return dt.strftime('%Y-%m-%d %H:%M:%S %Z%z')
            
        except pytz.exceptions.UnknownTimeZoneError:
            print(f"Unknown timezone: {self.timezone_str}")
        
        return f"Unknown timezone: {self.timezone_str}"
    
from langchain.utilities.google_search import GoogleSearchAPIWrapper    
class GoogleSearchTool(BaseTool):
    _api_wrapper= GoogleSearchAPIWrapper()
    # Define the fields with descriptions using Pydantic Field
    query_str: str = Field(
        ..., description="A wrapper around Google Search. Useful for when you need to answer questions about current events. Input should be a search query. Output is a JSON array of the query results"
    )

    def run(self):
        print(f"query: {self.query_str}")
        return self._api_wrapper.run(self.query_str)
    
