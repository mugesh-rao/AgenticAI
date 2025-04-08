import os
from dotenv import load_dotenv
from src.agents.agent_config import AgentConfig
from src.tools.tool_config import ToolConfig, Parameter
from src.core.chat_manager import ChatManager
from src.utils.llm_utils import setup_openai
from src.agents.meeting_assistant import MeetingAssistant

def create_tools():
    """Create and return a list of available tools."""
    tools = []
    
    # Calculator tool
    calculator_tool = ToolConfig(
        name="calculator",
        description="Performs basic mathematical calculations",
        parameters=[
            Parameter("expression", "Mathematical expression to evaluate", True, "string")
        ],
        expected_response_format="Numerical result",
        callable_function=lambda expression: eval(expression)
    )
    tools.append(calculator_tool)
    
    # Weather tool (example - you would need to implement the actual API call)
    weather_tool = ToolConfig(
        name="weather",
        description="Gets weather information for a location",
        parameters=[
            Parameter("location", "City name or coordinates", True, "string"),
            Parameter("days", "Number of days forecast (max 7)", False, "integer")
        ],
        expected_response_format="Weather information as text",
        callable_function=lambda location, days=1: f"Weather info for {location} for {days} days"
    )
    tools.append(weather_tool)
    
    return tools

def create_agents(tools):
    """Create and return a list of available agents."""
    agents = []
    
    # Math Agent
    math_agent = AgentConfig(
        name="Math Assistant",
        background="I am specialized in performing mathematical calculations and solving math problems.",
        tools=[tools[0]],  # Calculator tool
        expected_output="Mathematical results with explanations"
    )
    agents.append(math_agent)
    
    # Weather Agent
    weather_agent = AgentConfig(
        name="Weather Assistant",
        background="I am specialized in providing weather information and forecasts.",
        tools=[tools[1]],  # Weather tool
        expected_output="Weather information in a user-friendly format"
    )
    agents.append(weather_agent)
    
    # Meeting Assistant
    meeting_assistant = MeetingAssistant()
    agents.append(meeting_assistant)
    
    return agents

def main():
    # Load environment variables
    load_dotenv()
    
    # Setup OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    setup_openai(api_key)
    
    # Create tools and agents
    tools = create_tools()
    agents = create_agents(tools)
    
    # Initialize chat manager
    chat_manager = ChatManager(agents=agents, openai_api_key=api_key)
    
    # Main chat loop
    print("Welcome to AgenticAI! Type 'exit' to end the conversation.")
    print("Available agents:", ", ".join(agent.name for agent in agents))
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            response = chat_manager.handle_input(user_input)
            print(f"Assistant: {response}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main() 