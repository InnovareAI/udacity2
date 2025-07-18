"""
Corrected Support Functions for Enhanced Agentic Workflow
Implements the exact support functions required by Udacity feedback:
- product_manager_support_function
- program_manager_support_function  
- development_engineer_support_function

Each function follows the required pattern:
1. Accept an input query (a step from the action plan)
2. Call the respond() method of the corresponding KnowledgeAugmentedPromptAgent
3. Pass the response to the evaluate() method of the corresponding EvaluationAgent
4. Return the final, validated response (from the 'final_response' key)
"""

from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def product_manager_support_function(query: str, knowledge_agent, evaluation_agent) -> Dict[str, Any]:
    """
    Product Manager support function that chains knowledge agent's respond() to evaluation agent's evaluate()
    
    Args:
        query: Input query (a step from the action plan)
        knowledge_agent: KnowledgeAugmentedPromptAgent instance for Product Manager
        evaluation_agent: EvaluationAgent instance for Product Manager
        
    Returns:
        Final validated response from evaluation agent's 'final_response' key
    """
    try:
        # Step 1: Call the respond() method of the corresponding KnowledgeAugmentedPromptAgent
        knowledge_response = knowledge_agent.respond(query)
        
        # Step 2: Pass the response from the Knowledge Agent to the evaluate() method of the corresponding EvaluationAgent
        evaluation_result = evaluation_agent.evaluate(knowledge_response.content)
        
        # Step 3: Return the final, validated response (from the 'final_response' key of the evaluation result)
        return {
            "final_response": evaluation_result.get('final_response', evaluation_result),
            "knowledge_response": knowledge_response.content,
            "evaluation_metadata": evaluation_result,
            "timestamp": datetime.now().isoformat(),
            "function_type": "product_manager_support_function"
        }
        
    except Exception as e:
        logger.error(f"Error in product_manager_support_function: {e}")
        return {
            "final_response": f"Error processing query: {e}",
            "error": str(e),
            "function_type": "product_manager_support_function"
        }

def program_manager_support_function(query: str, knowledge_agent, evaluation_agent) -> Dict[str, Any]:
    """
    Program Manager support function that chains knowledge agent's respond() to evaluation agent's evaluate()
    
    Args:
        query: Input query (a step from the action plan)
        knowledge_agent: KnowledgeAugmentedPromptAgent instance for Program Manager
        evaluation_agent: EvaluationAgent instance for Program Manager
        
    Returns:
        Final validated response from evaluation agent's 'final_response' key
    """
    try:
        # Step 1: Call the respond() method of the corresponding KnowledgeAugmentedPromptAgent
        knowledge_response = knowledge_agent.respond(query)
        
        # Step 2: Pass the response from the Knowledge Agent to the evaluate() method of the corresponding EvaluationAgent
        evaluation_result = evaluation_agent.evaluate(knowledge_response.content)
        
        # Step 3: Return the final, validated response (from the 'final_response' key of the evaluation result)
        return {
            "final_response": evaluation_result.get('final_response', evaluation_result),
            "knowledge_response": knowledge_response.content,
            "evaluation_metadata": evaluation_result,
            "timestamp": datetime.now().isoformat(),
            "function_type": "program_manager_support_function"
        }
        
    except Exception as e:
        logger.error(f"Error in program_manager_support_function: {e}")
        return {
            "final_response": f"Error processing query: {e}",
            "error": str(e),
            "function_type": "program_manager_support_function"
        }

def development_engineer_support_function(query: str, knowledge_agent, evaluation_agent) -> Dict[str, Any]:
    """
    Development Engineer support function that chains knowledge agent's respond() to evaluation agent's evaluate()
    
    Args:
        query: Input query (a step from the action plan)
        knowledge_agent: KnowledgeAugmentedPromptAgent instance for Development Engineer
        evaluation_agent: EvaluationAgent instance for Development Engineer
        
    Returns:
        Final validated response from evaluation agent's 'final_response' key
    """
    try:
        # Step 1: Call the respond() method of the corresponding KnowledgeAugmentedPromptAgent
        knowledge_response = knowledge_agent.respond(query)
        
        # Step 2: Pass the response from the Knowledge Agent to the evaluate() method of the corresponding EvaluationAgent
        evaluation_result = evaluation_agent.evaluate(knowledge_response.content)
        
        # Step 3: Return the final, validated response (from the 'final_response' key of the evaluation result)
        return {
            "final_response": evaluation_result.get('final_response', evaluation_result),
            "knowledge_response": knowledge_response.content,
            "evaluation_metadata": evaluation_result,
            "timestamp": datetime.now().isoformat(),
            "function_type": "development_engineer_support_function"
        }
        
    except Exception as e:
        logger.error(f"Error in development_engineer_support_function: {e}")
        return {
            "final_response": f"Error processing query: {e}",
            "error": str(e),
            "function_type": "development_engineer_support_function"
        }

# Additional helper functions for the workflow
def validate_support_function_response(response: Dict[str, Any]) -> bool:
    """Validate that a support function response has the required structure"""
    required_keys = ['final_response', 'function_type']
    return all(key in response for key in required_keys)

def format_support_function_output(response: Dict[str, Any]) -> str:
    """Format support function output for display"""
    if not validate_support_function_response(response):
        return "Invalid support function response format"
    
    output = f"""
Support Function: {response.get('function_type', 'Unknown')}
Timestamp: {response.get('timestamp', 'Unknown')}

Final Response:
{response.get('final_response', 'No response')}

Knowledge Agent Response:
{response.get('knowledge_response', 'No knowledge response')}
"""
    
    if 'error' in response:
        output += f"\nError: {response['error']}"
    
    return output
