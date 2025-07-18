
"""
AI-Powered Agentic Workflow for Project Management
Workflow Agents Package

This package contains eight specialized agents for project management:
1. ProjectManagerAgent - Orchestrates overall project management tasks
2. AugmentedPromptAgent - Enhances prompts with context and structure
3. KnowledgeAugmentedPromptAgent - Integrates domain knowledge into prompts
4. RAGKnowledgePromptAgent - Uses retrieval-augmented generation
5. EvaluationAgent - Evaluates and scores project deliverables with iterative corrections
6. RoutingAgent - Routes tasks using embedding-based similarity matching
7. ActionPlanningAgent - Creates detailed action plans with explicit step extraction
8. DirectPromptAgent - Provides direct LLM access without system prompts
"""

from .project_manager_agent import ProjectManagerAgent
from .augmented_prompt_agent import AugmentedPromptAgent
from .knowledge_augmented_prompt_agent import KnowledgeAugmentedPromptAgent
from .rag_knowledge_prompt_agent import RAGKnowledgePromptAgent
from .evaluation_agent_fixed import EvaluationAgent
from .routing_agent_fixed import RoutingAgent
from .action_planning_agent_fixed import ActionPlanningAgent
from .direct_prompt_agent import DirectPromptAgent

__all__ = [
    "ProjectManagerAgent",
    "AugmentedPromptAgent", 
    "KnowledgeAugmentedPromptAgent",
    "RAGKnowledgePromptAgent",
    "EvaluationAgent",
    "RoutingAgent",
    "ActionPlanningAgent",
    "DirectPromptAgent"
]

__version__ = "2.0.0"
