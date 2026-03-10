from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from chart_generator import generate_chart
from write_pdf import render_latex_pdf
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

from arxiv_tool import *
from read_pdf import *
from write_pdf import * 
from langgraph.prebuilt import ToolNode

# Add generate_chart to the list
tools = [arxiv_search, read_pdf, render_latex_pdf, generate_chart] 
tool_node = ToolNode(tools)

import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Bind the tools to the model 
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    api_key=os.getenv("GOOGLE_API_KEY")
).bind_tools(tools)

from langgraph.prebuilt import ToolNode
from langgraph.graph import END, START, StateGraph

def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return{"messages": [response]}

def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()
config = {"configurable": {"thread_id": 222222}}

graph = workflow.compile(checkpointer=checkpointer)

# Step5: TESTING
INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper. For research information or getting papers, ALWAYS use arxiv.org.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper. Make sure that you
include mathematical equations in the paper. Once it's complete, you should
render it as a LaTeX PDF. When you give papers references, always attach the pdf links to the paper.

### CRITICAL RULES FOR PDF AND IMAGE GENERATION ###
1. NEVER apologize and NEVER say you cannot generate PDFs or images. You have the tools to do both.
2. If you need to include a graph, chart, or visual data in the paper, you MUST call the `generate_chart` tool FIRST to create the .png file.
3. Wait for `generate_chart` to return a success message with the filename.
4. When writing the LaTeX code, you MUST include `\\usepackage{graphicx}` in the preamble.
5. Insert the generated chart using `\\includegraphics{filename.png}`. DO NOT use folder paths (like output/filename.png), just the exact filename.
6. Once the LaTeX code is written, pass it directly to the `render_latex_pdf` tool. DO NOT output the raw LaTeX in the chat.
7. COMPILATION FIX: When writing LaTeX, NEVER use `\\\\` to create new lines after section headings or between paragraphs. Leave a blank line instead. Using `\\\\` improperly will crash the compiler with a "There's no line here to end" error.
"""
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        print(f"Message received: {message.content[:200]}...")
        message.pretty_print()

"""while True:
    user_input = input("User: ")
    if user_input:
        messages = [
                    {"role": "system", "content": INITIAL_PROMPT},
                    {"role": "user", "content": user_input}
                ]
        input_data = {
            "messages" : messages
        }
        print_stream(graph.stream(input_data, config, stream_mode="values"))"""