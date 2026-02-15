import asyncio
import json
import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("🤖 AI Copilot ready! Type 'exit' to quit.\n")

            while True:
                user = input("You: ")

                if user == "exit":
                    break

                messages = [
                    {
                        "role": "system",
                        "content": f"""
You are a smart AI copilot.

Use tools when helpful.
You may use multiple tools.

If a tool is needed:
Respond ONLY in JSON:
{{"tool":"tool_name","arguments":{{...}}}}

When you have the final answer:
Respond normally.

Available tools:
{tools}
"""
                    },
                    {"role": "user", "content": user},
                ]

                final_answer = None

                for _ in range(3):

                    response = ollama.chat(
                        model="llama3",
                        messages=messages
                    )

                    msg = response["message"]["content"]

                    try:
                        data = json.loads(msg)

                        result = await session.call_tool(
                            data["tool"],
                            arguments=data["arguments"]
                        )

                        tool_output = str(result.content)

                        messages.append({
                            "role": "assistant",
                            "content": msg
                        })

                        messages.append({
                            "role": "tool",
                            "content": tool_output
                        })

                    except:
                        final_answer = msg
                        break

                print("\n🤖 Copilot:\n")
                print(final_answer, "\n")


asyncio.run(main())