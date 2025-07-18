
"""
Fixed Routing Agent - Enhanced with text embedding and cosine similarity using text-embedding-3-large
"""

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentResponse
import json
import re
import numpy as np
from openai import OpenAI

class RoutingAgent(BaseAgent):
    """
    Enhanced routing agent with text embedding and cosine similarity for intelligent task routing
    """
    
    def __init__(self, api_key: str = None, agents: Dict[str, Any] = None):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key or "dummy-key")
        self.agents = agents or {}
        self.embedding_model = "text-embedding-3-large"
        
        self.capabilities = [
            "intelligent_task_routing", "embedding_based_matching", "cosine_similarity_analysis",
            "multi_agent_orchestration", "routing_optimization"
        ]
        
        # Agent route dictionaries with embeddings
        self.route_configs = {
            'ProjectManagerAgent': {
                'description': 'Handles project planning, resource allocation, timeline management, risk assessment, and stakeholder coordination',
                'keywords': ['project', 'plan', 'timeline', 'resource', 'risk', 'stakeholder', 'management'],
                'embedding': None  # Will be computed
            },
            'ActionPlanningAgent': {
                'description': 'Creates detailed action plans, task breakdowns, implementation strategies, and workflow designs',
                'keywords': ['action', 'plan', 'step', 'task', 'implement', 'strategy', 'workflow'],
                'embedding': None
            },
            'EvaluationAgent': {
                'description': 'Evaluates quality, provides scoring, generates feedback, and assesses performance',
                'keywords': ['evaluate', 'assess', 'score', 'quality', 'feedback', 'review'],
                'embedding': None
            },
            'DirectPromptAgent': {
                'description': 'Provides direct access to LLM without system prompts for flexible text generation',
                'keywords': ['direct', 'prompt', 'generate', 'creative', 'flexible', 'raw'],
                'embedding': None
            }
        }
        
        # Initialize embeddings
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embeddings for all route configurations"""
        try:
            for agent_name, config in self.route_configs.items():
                text_to_embed = f"{config['description']} {' '.join(config['keywords'])}"
                embedding = self._get_embedding(text_to_embed)
                config['embedding'] = embedding
        except Exception as e:
            # Fallback to dummy embeddings if API fails
            for agent_name, config in self.route_configs.items():
                config['embedding'] = np.random.rand(3072)  # text-embedding-3-large dimension
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text using OpenAI's text-embedding-3-large"""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            # Return random embedding as fallback
            return np.random.rand(3072)
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except:
            return 0.0
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process routing requests using embedding-based similarity matching
        """
        task_description = input_data.get('task_description', '')
        context = input_data.get('context', '')
        priority = input_data.get('priority', 'medium')
        
        # Get embedding for the task
        task_text = f"{task_description} {context}"
        task_embedding = self._get_embedding(task_text)
        
        # Calculate similarities with all agents
        similarities = {}
        for agent_name, config in self.route_configs.items():
            if config['embedding'] is not None:
                similarity = self._cosine_similarity(task_embedding, config['embedding'])
                similarities[agent_name] = similarity
        
        # Sort by similarity
        sorted_agents = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Select best agent
        best_agent = sorted_agents[0][0] if sorted_agents else 'DirectPromptAgent'
        best_similarity = sorted_agents[0][1] if sorted_agents else 0.5
        
        # Get alternatives
        alternatives = [
            {"agent": agent, "similarity": sim} 
            for agent, sim in sorted_agents[1:4]  # Top 3 alternatives
        ]
        
        system_prompt = """You are an expert AI workflow orchestrator specializing in intelligent task routing using advanced embedding-based similarity matching."""
        
        user_prompt = f"""
        EMBEDDING-BASED ROUTING ANALYSIS
        
        Task: {task_description}
        Context: {context}
        Priority: {priority}
        
        SIMILARITY ANALYSIS:
        Best Match: {best_agent} (similarity: {best_similarity:.3f})
        
        Alternative Options:
        {json.dumps(alternatives, indent=2)}
        
        Please provide routing recommendation with:
        1. Primary agent selection reasoning
        2. Confidence assessment based on similarity scores
        3. Alternative routing strategies
        4. Expected outcomes
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "RoutingAgent",
                "primary_agent": best_agent,
                "routing_confidence": best_similarity,
                "similarity_scores": similarities,
                "alternatives": alternatives,
                "embedding_model": self.embedding_model,
                "routing_method": "cosine_similarity"
            },
            confidence_score=min(0.95, best_similarity + 0.1),
            reasoning=f"Selected {best_agent} based on embedding similarity of {best_similarity:.3f}"
        )
    
    def route_task_with_embedding(self, task_description: str, context: str = "") -> AgentResponse:
        """Route task using embedding-based similarity"""
        return self.process({
            'task_description': task_description,
            'context': context
        })
