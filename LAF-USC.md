---
date created: Tuesday, April 14th 2026, 2:19:56 pm
date modified: Tuesday, April 14th 2026, 2:21:39 pm
---

```
from typing import Any

  

from google.adk.agents import llm_agent

from google.adk.sessions import vertex_ai_session_service

from vertexai.preview.reasoning_engines import AdkApp

from google.adk.tools import agent_tool

from google.adk.tools.google_search_tool import GoogleSearchTool

from google.adk.tools import url_context

  
  
  

VertexAiSessionService = vertex_ai_session_service.VertexAiSessionService

  
  

class AgentClass:

  

  def __init__(self):

    self.app = None

  

  def session_service_builder(self):

    return VertexAiSessionService()

  

  def set_up(self):

    """Sets up the ADK application."""

    the_butler_google_search_agent = llm_agent.LlmAgent(

      name='The_Butler_google_search_agent',

      model='gemini-2.5-pro',

      description=(

          'Agent specialized in performing Google searches.'

      ),

      sub_agents=[],

      instruction='Use the GoogleSearchTool to find information on the web.',

      tools=[

        GoogleSearchTool()

      ],

    )

    the_butler_url_context_agent = llm_agent.LlmAgent(

      name='The_Butler_url_context_agent',

      model='gemini-2.5-pro',

      description=(

          'Agent specialized in fetching content from URLs.'

      ),

      sub_agents=[],

      instruction='Use the UrlContextTool to retrieve content from provided URLs.',

      tools=[

        url_context

      ],

    )

    root_agent = llm_agent.LlmAgent(

      name='The_Butler',

      model='gemini-2.5-pro',

      description=(

          'The Butler is the CHIEF of STAFF here, the GCP -- the Google Cloud Palace, the \'Affable Bastion\' in the sky... He directs affairs for the US-CLOUD.'

      ),

      sub_agents=[],

      instruction='',

      tools=[

        agent_tool.AgentTool(agent=the_butler_google_search_agent),

        agent_tool.AgentTool(agent=the_butler_url_context_agent)

      ],

    )

  

    self.app = AdkApp(

        agent=root_agent,

        session_service_builder=self.session_service_builder

    )

  

  async def stream_query(self, query: str, user_id: str = 'test') -> Any:

    """Streaming query."""

    async for chunk in self.app.async_stream_query(

        message=query,

        user_id=user_id,

    ):

      yield chunk

  
  

app = AgentClass()
```
---
The world is quiet here. [^⸮]