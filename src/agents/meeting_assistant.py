from typing import Dict, Any, Tuple
from .agent_config import AgentConfig
from ..tools.meeting_notes_tool import GetMeetingNotesTool
from ..utils.llm_utils import create_chat_completion
import json

class MeetingAssistant(AgentConfig):
    """Specialized agent for handling meeting-related queries."""

    def __init__(self):
        super().__init__(
            name="Meeting Assistant",
            background="I specialize in retrieving and analyzing meeting transcripts to answer questions about past meetings.",
            tools=[GetMeetingNotesTool()],
            expected_output="Meeting information and transcript analysis"
        )

    def can_handle(self, instruction: str) -> bool:
        """Determine if this agent can handle the meeting-related query."""
        meeting_keywords = [
            "meeting", "discussion", "call", "sync", "standup", 
            "review", "transcript", "notes", "minutes"
        ]
        return any(keyword in instruction.lower() for keyword in meeting_keywords)

    def run_agent(self, instruction: str) -> Tuple[str, Dict[str, Any]]:
        """Process a meeting-related query and return relevant information."""
        
        # 1. Create meeting context description
        context_prompt = f"""
        Based on this question, create a brief description of the meeting context needed:
        Question: {instruction}
        Respond with just the description, no other text.
        """
        
        meeting_description = create_chat_completion([
            {"role": "system", "content": context_prompt},
            {"role": "user", "content": instruction}
        ])

        # 2. Get meeting transcripts
        meeting_tool = next(t for t in self.tools if t.name == "get_meeting_notes")
        result = meeting_tool.run_tool({"description": meeting_description})

        if not result["found"]:
            return (
                "I couldn't find any meeting transcripts matching your query. "
                "Could you provide more specific details about the meeting you're interested in?",
                {"found": False}
            )

        # 3. Analyze transcripts and generate response
        analysis_prompt = f"""
        Based on these meeting transcripts, answer the following question:
        Question: {instruction}

        Transcripts:
        {json.dumps(result["transcripts"], indent=2)}

        If the information is incomplete, mention that in your response.
        Be concise but informative.
        """

        response = create_chat_completion([
            {"role": "system", "content": analysis_prompt},
            {"role": "user", "content": instruction}
        ])

        return response, {
            "found": True,
            "confidence": result["confidence"],
            "meeting_description": meeting_description
        } 