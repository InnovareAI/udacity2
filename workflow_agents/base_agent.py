
"""
Base Agent Class for AI-Powered Project Management Workflow
Enhanced with proper error handling and mock responses for testing
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    success: bool
    content: str
    metadata: Dict[str, Any] = {}
    confidence_score: float = 0.0
    reasoning: str = ""

class BaseAgent(ABC):
    """Base class for all workflow agents"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.agent_name = self.__class__.__name__
        
        # Initialize OpenAI client only if valid API key is provided
        if self.api_key and self.api_key.startswith("sk-"):
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception:
                self.client = None
        else:
            self.client = None
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """Process input and return structured response"""
        pass
    
    def _call_openai(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
        """Helper method to call OpenAI API with fallback to mock responses"""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            except Exception as e:
                return self._get_mock_response(messages)
        else:
            return self._get_mock_response(messages)
    
    def _get_mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate mock response for testing when API is not available"""
        user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), "")
        agent_type = self.agent_name
        
        mock_responses = {
            "ProjectManagerAgent": f"""
# Project Management Analysis

Based on the request: {user_message[:100]}...

## Project Overview
This project requires comprehensive planning and coordination across multiple phases.

## Key Deliverables
1. Project charter and scope definition
2. Resource allocation and timeline planning
3. Risk assessment and mitigation strategies
4. Stakeholder communication plan

## Timeline Estimate
- Phase 1: Planning and Setup (2-4 weeks)
- Phase 2: Development/Implementation (8-12 weeks)
- Phase 3: Testing and Deployment (2-4 weeks)

## Resource Requirements
- Project Manager: 1 FTE
- Development Team: 3-5 members
- Quality Assurance: 1-2 members
- Stakeholder involvement: As needed

## Risk Assessment
- Technical complexity: Medium
- Resource availability: To be confirmed
- Timeline constraints: Manageable with proper planning

## Success Metrics
- On-time delivery
- Budget adherence
- Quality standards met
- Stakeholder satisfaction
            """,
            
            "RoutingAgent": f"""
# Task Routing Analysis

## Task Analysis
Input: {user_message[:100]}...

## Routing Recommendation
**Primary Agent**: EvaluationAgent
**Confidence**: 0.85

## Reasoning
Based on the task content analysis, this request is best handled by the EvaluationAgent due to:
- Evaluation keywords detected
- Assessment requirements identified
- Quality measurement needs

## Alternative Agents
1. ProjectManagerAgent (confidence: 0.65)
2. ActionPlanningAgent (confidence: 0.55)

## Workflow Suggestion
1. Route to EvaluationAgent for primary assessment
2. Consider ProjectManagerAgent for follow-up planning
3. ActionPlanningAgent for implementation steps
            """,
            
            "EvaluationAgent": f"""
# Quality Evaluation Report

## Item Evaluated
{user_message[:200]}...

## Evaluation Criteria
- Completeness: 8/10
- Clarity: 7/10
- Technical Accuracy: 8/10
- Usability: 7/10
- Documentation Quality: 6/10

## Overall Score: 7.2/10

## Strengths
- Well-structured approach
- Clear objectives
- Comprehensive coverage

## Areas for Improvement
1. Enhanced documentation needed
2. More detailed technical specifications
3. Better user experience considerations

## Recommendations
- Improve documentation quality
- Add more technical details
- Consider user feedback integration
- Implement quality assurance processes

## Next Steps
1. Address identified gaps
2. Implement improvements
3. Re-evaluate after changes
            """,
            
            "ActionPlanningAgent": f"""
# Action Plan

## Project Goal
{user_message[:100]}...

## Phase 1: Planning (Weeks 1-2)
### Week 1
- [ ] Requirements gathering
- [ ] Stakeholder interviews
- [ ] Technical assessment
- [ ] Resource planning

### Week 2
- [ ] Architecture design
- [ ] Technology selection
- [ ] Team formation
- [ ] Project charter approval

## Phase 2: Development (Weeks 3-10)
### Weeks 3-4: Foundation
- [ ] Environment setup
- [ ] Core infrastructure
- [ ] Basic functionality
- [ ] Initial testing framework

### Weeks 5-8: Core Development
- [ ] Feature implementation
- [ ] Integration development
- [ ] Unit testing
- [ ] Code reviews

### Weeks 9-10: Integration
- [ ] System integration
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Security review

## Phase 3: Deployment (Weeks 11-12)
### Week 11
- [ ] User acceptance testing
- [ ] Documentation completion
- [ ] Deployment preparation
- [ ] Training materials

### Week 12
- [ ] Production deployment
- [ ] Monitoring setup
- [ ] User training
- [ ] Project closure

## Success Criteria
- All features implemented
- Quality standards met
- Timeline adherence
- Budget compliance
            """
        }
        
        return mock_responses.get(agent_type, f"""
# {agent_type} Response

Thank you for your request: {user_message[:100]}...

This is a mock response generated for testing purposes. In a production environment with a valid OpenAI API key, this would be replaced with an AI-generated response tailored to the specific agent's capabilities and the input provided.

## Key Points
- Agent: {agent_type}
- Processing completed successfully
- Mock response for testing/demonstration
- Ready for integration with actual AI services

## Next Steps
- Configure valid OpenAI API key for production use
- Test with real AI responses
- Validate output quality and format
        """)
    
    def _calculate_confidence(self, response_content: str) -> float:
        """Calculate confidence score based on response characteristics"""
        if not response_content or "Error" in response_content:
            return 0.1
        
        # Enhanced confidence calculation
        length_score = min(len(response_content) / 500, 1.0)
        structure_indicators = ['#', '##', '###', '-', '*', '1.', '2.', '3.']
        structure_score = min(sum(1 for indicator in structure_indicators if indicator in response_content) / 10, 1.0)
        
        keyword_indicators = ['plan', 'step', 'action', 'recommendation', 'analysis', 'assessment']
        keyword_score = min(sum(1 for keyword in keyword_indicators if keyword.lower() in response_content.lower()) / 6, 1.0)
        
        return (length_score + structure_score + keyword_score) / 3

    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "name": self.agent_name,
            "has_api_key": bool(self.client),
            "capabilities": getattr(self, 'capabilities', []),
            "specialties": getattr(self, 'specialties', [])
        }
