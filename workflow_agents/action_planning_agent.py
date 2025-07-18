
"""
Action Planning Agent - Enhanced comprehensive action planning and task breakdown
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
import json

class ActionPlanningAgent(BaseAgent):
    """
    Specialized agent for action planning and task breakdown:
    - Detailed action plan creation
    - Task breakdown and sequencing
    - Implementation strategy development
    - Workflow design and optimization
    - Resource and timeline planning
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "action_plan_creation", "task_breakdown", "workflow_design",
            "implementation_strategy", "resource_planning", "timeline_optimization"
        ]
        self.specialties = [
            "step_by_step_planning", "project_implementation", "process_optimization",
            "milestone_planning", "dependency_management", "execution_strategy"
        ]
        
        # Planning templates for different project types
        self.planning_templates = {
            "software_development": {
                "phases": ["Planning", "Design", "Development", "Testing", "Deployment"],
                "typical_duration": "12-16 weeks",
                "key_activities": [
                    "Requirements analysis", "Architecture design", "Implementation",
                    "Quality assurance", "User acceptance testing", "Production deployment"
                ]
            },
            "project_management": {
                "phases": ["Initiation", "Planning", "Execution", "Monitoring", "Closure"],
                "typical_duration": "8-24 weeks",
                "key_activities": [
                    "Project charter", "Work breakdown structure", "Resource allocation",
                    "Progress tracking", "Risk management", "Project closure"
                ]
            },
            "research": {
                "phases": ["Literature Review", "Methodology", "Data Collection", "Analysis", "Reporting"],
                "typical_duration": "8-20 weeks",
                "key_activities": [
                    "Background research", "Research design", "Data gathering",
                    "Statistical analysis", "Report writing", "Peer review"
                ]
            },
            "marketing": {
                "phases": ["Strategy", "Planning", "Creation", "Launch", "Optimization"],
                "typical_duration": "6-12 weeks",
                "key_activities": [
                    "Market research", "Campaign strategy", "Content creation",
                    "Campaign launch", "Performance monitoring", "Optimization"
                ]
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process action planning requests
        
        Args:
            input_data: Dictionary containing:
                - goal: Main goal or objective
                - project_type: Type of project (software_development, project_management, etc.)
                - timeline: Available timeline
                - resources: Available resources
                - constraints: Any constraints or limitations
                - complexity: Project complexity level
        """
        goal = input_data.get('goal', '')
        project_type = input_data.get('project_type', 'general')
        timeline = input_data.get('timeline', 'flexible')
        resources = input_data.get('resources', 'to_be_determined')
        constraints = input_data.get('constraints', {})
        complexity = input_data.get('complexity', 'medium')
        
        # Get planning template if available
        template = self.planning_templates.get(project_type, self._get_default_template())
        
        system_prompt = """You are a senior project planning specialist and implementation strategist with expertise in:

- Comprehensive action plan development across multiple domains
- Task breakdown and work structure optimization
- Implementation strategy and execution planning
- Resource allocation and timeline optimization
- Risk-aware planning with contingency strategies
- Agile and traditional project management methodologies

Your planning approach should be:
- Systematic and well-structured with clear phases
- Actionable with specific, measurable tasks
- Realistic with achievable timelines and milestones
- Resource-conscious with efficient allocation
- Risk-aware with mitigation strategies
- Flexible with adaptation mechanisms
- Quality-focused with validation checkpoints

Always provide concrete deliverables, success criteria, and progress tracking mechanisms."""
        
        user_prompt = f"""
        ACTION PLANNING REQUEST
        
        Goal/Objective: {goal}
        Project Type: {project_type}
        Timeline: {timeline}
        Available Resources: {resources}
        Constraints: {constraints}
        Complexity Level: {complexity}
        
        Template Information:
        Suggested Phases: {template['phases']}
        Typical Duration: {template['typical_duration']}
        Key Activities: {template['key_activities']}
        
        Please create a comprehensive action plan including:
        
        1. EXECUTIVE SUMMARY
           - Project overview and objectives
           - Key success factors
           - Critical assumptions and dependencies
           - Overall timeline and resource summary
        
        2. DETAILED ACTION PLAN
           For each phase, provide:
           - Phase objectives and deliverables
           - Specific tasks and activities
           - Timeline and duration estimates
           - Resource requirements
           - Dependencies and prerequisites
           - Success criteria and validation methods
        
        3. TASK BREAKDOWN STRUCTURE
           - Hierarchical task organization
           - Task priorities and sequencing
           - Effort estimates and resource assignments
           - Milestone definitions and checkpoints
        
        4. IMPLEMENTATION STRATEGY
           - Execution approach and methodology
           - Team structure and role assignments
           - Communication and coordination plans
           - Quality assurance processes
        
        5. TIMELINE AND MILESTONES
           - Detailed project schedule
           - Critical path identification
           - Key milestones and deliverables
           - Buffer time and contingency planning
        
        6. RESOURCE PLANNING
           - Human resource requirements
           - Technical resource needs
           - Budget considerations
           - Resource optimization strategies
        
        7. RISK MANAGEMENT
           - Identified risks and impact assessment
           - Risk mitigation strategies
           - Contingency plans
           - Risk monitoring and response procedures
        
        8. MONITORING AND CONTROL
           - Progress tracking mechanisms
           - Key performance indicators (KPIs)
           - Reporting and communication protocols
           - Change management procedures
        
        9. SUCCESS METRICS
           - Quantitative success measures
           - Quality gates and acceptance criteria
           - Performance benchmarks
           - Stakeholder satisfaction metrics
        
        10. NEXT STEPS
            - Immediate actions required
            - Preparation activities
            - Stakeholder approvals needed
            - Implementation kickoff plan
        
        Provide specific, actionable tasks with clear timelines and responsibilities.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        # Extract planning metadata
        planning_metadata = self._extract_planning_metadata(response_content, template)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "ActionPlanningAgent",
                "project_type": project_type,
                "complexity": complexity,
                "template_used": template,
                "estimated_phases": len(template['phases']),
                "planning_approach": self._determine_planning_approach(complexity, project_type),
                "resource_intensity": self._assess_resource_intensity(resources, complexity),
                "timeline_feasibility": self._assess_timeline_feasibility(timeline, complexity),
                "planning_metadata": planning_metadata
            },
            confidence_score=confidence_score,
            reasoning=f"Created comprehensive action plan for {project_type} project with {complexity} complexity using structured planning methodology"
        )
    
    def create_project_plan(self, goal: str, project_type: str = "general", constraints: Dict[str, Any] = None) -> AgentResponse:
        """Create a comprehensive project plan"""
        constraints = constraints or {}
        return self.process({
            'goal': goal,
            'project_type': project_type,
            'timeline': constraints.get('timeline', 'flexible'),
            'resources': constraints.get('resources', 'to_be_determined'),
            'constraints': constraints,
            'complexity': constraints.get('complexity', 'medium')
        })
    
    def break_down_task(self, task_description: str, context: str = "", complexity: str = "medium") -> AgentResponse:
        """Break down a complex task into actionable steps"""
        return self.process({
            'goal': task_description,
            'project_type': 'task_breakdown',
            'complexity': complexity,
            'constraints': {'context': context}
        })
    
    def create_implementation_strategy(self, objective: str, resources: str, timeline: str) -> AgentResponse:
        """Create detailed implementation strategy"""
        return self.process({
            'goal': objective,
            'project_type': 'implementation',
            'resources': resources,
            'timeline': timeline,
            'complexity': 'medium'
        })
    
    def optimize_workflow(self, current_workflow: str, optimization_goals: List[str]) -> AgentResponse:
        """Optimize existing workflow for better efficiency"""
        return self.process({
            'goal': f"Optimize workflow: {current_workflow}",
            'project_type': 'workflow_optimization',
            'constraints': {'optimization_goals': optimization_goals},
            'complexity': 'medium'
        })
    
    def _get_default_template(self) -> Dict[str, Any]:
        """Get default planning template for general projects"""
        return {
            "phases": ["Analysis", "Planning", "Implementation", "Review", "Completion"],
            "typical_duration": "8-12 weeks",
            "key_activities": [
                "Requirement analysis", "Solution design", "Implementation",
                "Testing and validation", "Documentation", "Deployment"
            ]
        }
    
    def _extract_planning_metadata(self, response_content: str, template: Dict[str, Any]) -> Dict[str, Any]:
        """Extract planning metadata from response"""
        metadata = {
            "phases_identified": len(template['phases']),
            "has_timeline": "timeline" in response_content.lower(),
            "has_milestones": "milestone" in response_content.lower(),
            "has_resources": "resource" in response_content.lower(),
            "has_risks": "risk" in response_content.lower(),
            "structure_quality": self._assess_structure_quality(response_content)
        }
        return metadata
    
    def _assess_structure_quality(self, content: str) -> str:
        """Assess the structural quality of the plan"""
        structure_indicators = ['#', '##', '###', '-', '*', '1.', '2.', '3.']
        structure_count = sum(1 for indicator in structure_indicators if indicator in content)
        
        if structure_count > 20:
            return 'excellent'
        elif structure_count > 10:
            return 'good'
        elif structure_count > 5:
            return 'fair'
        else:
            return 'poor'
    
    def _determine_planning_approach(self, complexity: str, project_type: str) -> str:
        """Determine optimal planning approach"""
        if complexity == 'high' or project_type in ['software_development', 'research']:
            return 'detailed_structured'
        elif complexity == 'low':
            return 'simplified_agile'
        else:
            return 'balanced_hybrid'
    
    def _assess_resource_intensity(self, resources: str, complexity: str) -> str:
        """Assess resource intensity requirements"""
        if 'limited' in resources.lower() or complexity == 'high':
            return 'high'
        elif 'adequate' in resources.lower() or complexity == 'medium':
            return 'medium'
        else:
            return 'low'
    
    def _assess_timeline_feasibility(self, timeline: str, complexity: str) -> str:
        """Assess timeline feasibility"""
        if timeline == 'flexible':
            return 'feasible'
        elif 'tight' in timeline.lower() or 'urgent' in timeline.lower():
            return 'challenging' if complexity != 'low' else 'feasible'
        else:
            return 'feasible'
    
    def get_planning_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available planning templates"""
        return self.planning_templates
    
    def add_custom_template(self, project_type: str, template: Dict[str, Any]):
        """Add custom planning template"""
        self.planning_templates[project_type] = template
    
    # Additional methods for test compatibility
    def break_down_task(self, task_description: str, context: str = "") -> AgentResponse:
        """Break down a task into actionable steps - alias for compatibility"""
        return self.process({
            'goal': task_description,
            'project_type': 'general',
            'context': context,
            'complexity': 'medium'
        })
    
    def create_project_plan(self, project_description: str, project_type: str = "general", context: Dict[str, Any] = None) -> AgentResponse:
        """Create a comprehensive project plan - alias for compatibility"""
        context = context or {}
        return self.process({
            'goal': project_description,
            'project_type': project_type,
            'timeline': context.get('timeline', 'flexible'),
            'resources': context.get('resources', 'to_be_determined'),
            'complexity': context.get('complexity', 'medium')
        })
