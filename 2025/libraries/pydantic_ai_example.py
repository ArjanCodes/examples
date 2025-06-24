from pydantic_ai import Agent

agent = Agent(
    "google-gla:gemini-1.5-flash",
    system_prompt="Be concise, reply with one sentence.",
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
"""
The first known use of "hello, world" was in a 1974 textbook about the C programming language.
"""
