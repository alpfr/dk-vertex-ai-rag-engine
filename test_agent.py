import sys
import asyncio

# Load agent environment variables
from google.adk.cli.utils.envs import load_dotenv_for_agent
load_dotenv_for_agent("rag", ".")

from rag.agent import agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

async def main():
    prompt = "Create a RAG corpus named 'adk-test-corpus-alpfr' with description 'adk-test-corpus' and import the file gs://adk-test-bucket-alpfr-2026/sample.txt into the RAG corpus."
    print("User: " + prompt)
    
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="rag",
        agent=agent,
        session_service=session_service,
        auto_create_session=True
    )
    
    from google.genai.types import Content, Part
    msg = Content(role="user", parts=[Part.from_text(text=prompt)])
    
    agen = runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=msg
    )
    
    async for event in agen:
        if hasattr(event, "content") and event.content:
            try:
                print(f"Agent Response: {event.content.text}")
            except:
                print(f"Agent Response: {event.content}")
                
    # Now that we've populated the corpus, test querying it
    query_prompt = "Search across all corpora for information about what the ADK agent handles routing."
    print("\nUser: " + query_prompt)
    
    query_msg = Content(role="user", parts=[Part.from_text(text=query_prompt)])
    query_agen = runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=query_msg
    )
    
    async for event in query_agen:
        if hasattr(event, "content") and event.content:
            try:
                print(f"Agent Response: {event.content.text}")
            except:
                print(f"Agent Response: {event.content}")

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
