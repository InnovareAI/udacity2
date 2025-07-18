
"""
Direct Prompt Agent - Passes user prompts directly to LLM without system prompts
"""

from typing import Dict, Any
from .base_agent import BaseAgent, AgentResponse

class DirectPromptAgent(BaseAgent):
    """
    Direct prompt agent that passes user prompts directly to LLM without system prompts.
    This agent provides unfiltered, direct access to the language model.
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "direct_llm_access", "unfiltered_prompting", "raw_text_generation",
            "flexible_response_format", "minimal_processing"
        ]
        self.specialties = [
            "direct_user_interaction", "raw_prompt_processing", "unstructured_output",
            "creative_generation", "flexible_formatting"
        ]
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process direct prompt requests without system prompts
        
        Args:
            input_data: Dictionary containing:
                - prompt: The direct user prompt to send to LLM
                - context: Optional context (will be appended to prompt)
                - temperature: Optional temperature setting
                - max_tokens: Optional max tokens setting
        """
        prompt = input_data.get('prompt', '')
        context = input_data.get('context', '')
        temperature = input_data.get('temperature', 0.7)
        max_tokens = input_data.get('max_tokens', 2000)
        
        if not prompt:
            return AgentResponse(
                success=False,
                content="Error: No prompt provided",
                metadata={"agent_type": "DirectPromptAgent", "error": "missing_prompt"},
                confidence_score=0.0,
                reasoning="No prompt was provided for direct processing"
            )
        
        # Combine prompt and context if provided
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"
        
        # Create messages with only user content (no system prompt)
        messages = [
            {"role": "user", "content": full_prompt}
        ]
        
        try:
            # Call OpenAI directly with user prompt only
            response_content = self._call_openai(messages, temperature=temperature, max_tokens=max_tokens)
            
            return AgentResponse(
                success=True,
                content=response_content,
                metadata={
                    "agent_type": "DirectPromptAgent",
                    "prompt_length": len(full_prompt),
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "direct_processing": True
                },
                confidence_score=0.9,  # High confidence for direct processing
                reasoning="Direct prompt processed without system intervention"
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                content=f"Error processing direct prompt: {str(e)}",
                metadata={
                    "agent_type": "DirectPromptAgent",
                    "error": str(e),
                    "prompt_length": len(full_prompt)
                },
                confidence_score=0.0,
                reasoning=f"Failed to process direct prompt: {str(e)}"
            )
    
    def direct_prompt(self, prompt: str, context: str = "", temperature: float = 0.7) -> AgentResponse:
        """
        Convenience method for direct prompting
        
        Args:
            prompt: The direct user prompt
            context: Optional context
            temperature: Temperature setting for generation
        """
        return self.process({
            'prompt': prompt,
            'context': context,
            'temperature': temperature
        })
