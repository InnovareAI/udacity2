
"""
Project Manager Agent - Handles comprehensive project management tasks
Enhanced with specialized prompts and improved functionality
"""

from typing import Dict, Any
from .base_agent import BaseAgent, AgentResponse

class ProjectManagerAgent(BaseAgent):
    """
    Specialized agent for project management tasks:
    - Project planning and scheduling
    - Resource allocation and management
    - Risk assessment and mitigation
    - Stakeholder communication
    - Progress tracking and reporting
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "project_planning", "resource_management", "risk_assessment",
            "stakeholder_management", "timeline_planning", "budget_management"
        ]
        self.specialties = [
            "comprehensive_project_planning", "agile_methodology", "waterfall_methodology",
            "risk_management", "resource_optimization", "stakeholder_engagement"
        ]
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process project management requests
        
        Args:
            input_data: Dictionary containing:
                - task_type: Type of PM task (planning, assessment, etc.)
                - project_details: Detailed project information
                - requirements: Specific requirements
                - timeline: Project timeline constraints
                - resources: Available resources
        """
        task_type = input_data.get('task_type', 'general_planning')
        project_details = input_data.get('project_details', '')
        requirements = input_data.get('requirements', '')
        timeline = input_data.get('timeline', 'flexible')
        resources = input_data.get('resources', 'to_be_determined')
        
        system_prompt = """You are a senior project manager with 15+ years of experience managing complex technology projects. You excel at:

- Creating comprehensive project plans with realistic timelines
- Identifying and mitigating project risks proactively
- Optimizing resource allocation for maximum efficiency
- Managing stakeholder expectations and communications
- Implementing both Agile and Waterfall methodologies
- Ensuring project delivery within scope, time, and budget constraints

Your responses should be:
- Structured and professional
- Actionable with specific recommendations
- Risk-aware with mitigation strategies
- Resource-conscious and realistic
- Stakeholder-focused with clear communication plans

Always provide concrete deliverables, timelines, and success metrics."""
        
        user_prompt = f"""
        Project Management Task: {task_type}
        
        Project Details:
        {project_details}
        
        Requirements:
        {requirements}
        
        Timeline Constraints: {timeline}
        Available Resources: {resources}
        
        Please provide a comprehensive project management response including:
        
        1. PROJECT OVERVIEW
           - Executive summary
           - Key objectives and success criteria
           - Project scope and boundaries
        
        2. PROJECT PLAN
           - Phase breakdown with timelines
           - Key milestones and deliverables
           - Dependencies and critical path
        
        3. RESOURCE MANAGEMENT
           - Team structure and roles
           - Resource allocation plan
           - Skills and capacity requirements
        
        4. RISK ASSESSMENT
           - Identified risks and impact analysis
           - Mitigation strategies
           - Contingency planning
        
        5. STAKEHOLDER MANAGEMENT
           - Stakeholder identification and analysis
           - Communication plan
           - Engagement strategies
        
        6. MONITORING & CONTROL
           - Progress tracking methods
           - Quality assurance processes
           - Change management procedures
        
        7. SUCCESS METRICS
           - Key performance indicators
           - Quality gates and checkpoints
           - Definition of done criteria
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "ProjectManagerAgent",
                "task_type": task_type,
                "methodology_recommended": self._recommend_methodology(project_details),
                "estimated_duration": self._estimate_duration(project_details, timeline),
                "risk_level": self._assess_risk_level(project_details),
                "resource_complexity": self._assess_resource_complexity(resources)
            },
            confidence_score=confidence_score,
            reasoning=f"Applied project management expertise to {task_type} with focus on comprehensive planning and risk management"
        )
    
    def create_project_plan(self, project_description: str, constraints: Dict[str, Any] = None) -> AgentResponse:
        """Create a comprehensive project plan"""
        return self.process({
            'task_type': 'comprehensive_planning',
            'project_details': project_description,
            'requirements': str(constraints or {}),
            'timeline': constraints.get('timeline', 'flexible') if constraints else 'flexible',
            'resources': constraints.get('resources', 'to_be_determined') if constraints else 'to_be_determined'
        })
    
    def assess_project_risks(self, project_details: str) -> AgentResponse:
        """Assess project risks and provide mitigation strategies"""
        return self.process({
            'task_type': 'risk_assessment',
            'project_details': project_details,
            'requirements': 'Comprehensive risk analysis with mitigation strategies'
        })
    
    def plan_resource_allocation(self, project_details: str, available_resources: str) -> AgentResponse:
        """Plan optimal resource allocation"""
        return self.process({
            'task_type': 'resource_planning',
            'project_details': project_details,
            'resources': available_resources,
            'requirements': 'Optimal resource allocation with efficiency maximization'
        })
    
    def _recommend_methodology(self, project_details: str) -> str:
        """Recommend project methodology based on project characteristics"""
        agile_indicators = ['iterative', 'flexible', 'changing', 'uncertain', 'innovative']
        waterfall_indicators = ['sequential', 'fixed', 'defined', 'regulatory', 'compliance']
        
        project_lower = project_details.lower()
        agile_score = sum(1 for indicator in agile_indicators if indicator in project_lower)
        waterfall_score = sum(1 for indicator in waterfall_indicators if indicator in project_lower)
        
        if agile_score > waterfall_score:
            return "Agile/Scrum"
        elif waterfall_score > agile_score:
            return "Waterfall"
        else:
            return "Hybrid"
    
    def _estimate_duration(self, project_details: str, timeline: str) -> str:
        """Estimate project duration based on complexity"""
        if timeline != 'flexible':
            return timeline
        
        complexity_indicators = {
            'simple': ['basic', 'simple', 'straightforward', 'minimal'],
            'medium': ['moderate', 'standard', 'typical', 'regular'],
            'complex': ['complex', 'comprehensive', 'advanced', 'enterprise']
        }
        
        project_lower = project_details.lower()
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in project_lower for indicator in indicators):
                duration_map = {
                    'simple': '4-8 weeks',
                    'medium': '8-16 weeks',
                    'complex': '16-32 weeks'
                }
                return duration_map[complexity]
        
        return '8-16 weeks'
    
    def _assess_risk_level(self, project_details: str) -> str:
        """Assess overall project risk level"""
        high_risk_indicators = ['new technology', 'tight deadline', 'large team', 'complex integration']
        medium_risk_indicators = ['established technology', 'moderate timeline', 'experienced team']
        
        project_lower = project_details.lower()
        high_risk_count = sum(1 for indicator in high_risk_indicators if indicator in project_lower)
        medium_risk_count = sum(1 for indicator in medium_risk_indicators if indicator in project_lower)
        
        if high_risk_count > 1:
            return 'High'
        elif medium_risk_count > 0 or high_risk_count == 1:
            return 'Medium'
        else:
            return 'Low'
    
    def _assess_resource_complexity(self, resources: str) -> str:
        """Assess resource management complexity"""
        if 'to_be_determined' in resources.lower():
            return 'High'
        elif 'limited' in resources.lower() or 'constraint' in resources.lower():
            return 'Medium'
        else:
            return 'Low'
