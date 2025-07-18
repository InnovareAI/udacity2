
"""
Fixed Action Planning Agent - Enhanced with explicit step extraction logic from user prompts
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
import json
import re

class ActionPlanningAgent(BaseAgent):
    """
    Enhanced action planning agent with explicit step extraction from user prompts
    """
    
    def __init__(self, api_key: str = None, knowledge_action_planning: Dict[str, Any] = None):
        super().__init__(api_key)
        self.knowledge_action_planning = knowledge_action_planning or {}
        
        self.capabilities = [
            "action_plan_creation", "step_extraction", "task_breakdown",
            "workflow_design", "implementation_strategy", "explicit_sequencing"
        ]
        self.specialties = [
            "step_by_step_planning", "user_prompt_analysis", "explicit_step_extraction",
            "sequential_task_organization", "implementation_roadmaps"
        ]
        
        # Step extraction patterns
        self.step_patterns = [
            r'step\s+(\d+)[:\.]?\s*(.+?)(?=step\s+\d+|$)',
            r'(\d+)[:\.\)]\s*(.+?)(?=\d+[:\.\)]|$)',
            r'first[ly]?\s*[:\-]?\s*(.+?)(?=second|then|next|$)',
            r'second[ly]?\s*[:\-]?\s*(.+?)(?=third|then|next|$)',
            r'third[ly]?\s*[:\-]?\s*(.+?)(?=fourth|then|next|$)',
            r'then\s*[:\-]?\s*(.+?)(?=then|next|finally|$)',
            r'next\s*[:\-]?\s*(.+?)(?=then|next|finally|$)',
            r'finally\s*[:\-]?\s*(.+?)$'
        ]
        
        # Action verbs for step identification
        self.action_verbs = [
            'create', 'develop', 'implement', 'design', 'build', 'test', 'deploy',
            'analyze', 'review', 'evaluate', 'plan', 'organize', 'coordinate',
            'establish', 'configure', 'setup', 'install', 'execute', 'perform'
        ]
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process action planning requests with explicit step extraction
        """
        goal = input_data.get('goal', '')
        user_prompt = input_data.get('user_prompt', goal)  # Use user_prompt if provided
        project_type = input_data.get('project_type', 'general')
        timeline = input_data.get('timeline', 'flexible')
        resources = input_data.get('resources', 'to_be_determined')
        complexity = input_data.get('complexity', 'medium')
        
        # Extract explicit steps from user prompt
        extracted_steps = self._extract_steps_from_prompt(user_prompt)
        
        # Analyze prompt for implicit requirements
        implicit_requirements = self._analyze_implicit_requirements(user_prompt)
        
        # Generate comprehensive action plan
        action_plan = self._generate_action_plan(
            goal, extracted_steps, implicit_requirements, project_type, timeline, resources, complexity
        )
        
        system_prompt = """You are a senior project planning specialist and implementation strategist with expertise in:

- Explicit step extraction from user requirements
- Comprehensive action plan development
- Task breakdown and sequencing optimization
- Implementation strategy design
- Resource allocation and timeline planning
- Risk-aware planning with contingency strategies

Your planning approach should be systematic, well-structured, and directly address user-specified steps while enhancing them with professional project management practices."""
        
        user_prompt_formatted = f"""
        ACTION PLANNING REQUEST
        
        Goal: {goal}
        Original User Prompt: {user_prompt}
        Project Type: {project_type}
        Timeline: {timeline}
        Resources: {resources}
        Complexity: {complexity}
        
        EXTRACTED STEPS FROM USER PROMPT:
        {json.dumps(extracted_steps, indent=2)}
        
        IMPLICIT REQUIREMENTS IDENTIFIED:
        {json.dumps(implicit_requirements, indent=2)}
        
        GENERATED ACTION PLAN FRAMEWORK:
        {json.dumps(action_plan, indent=2)}
        
        Please provide a comprehensive action plan that:
        
        1. RESPECTS USER-SPECIFIED STEPS
           - Incorporates all explicitly mentioned steps
           - Maintains user's intended sequence where logical
           - Enhances user steps with professional detail
        
        2. FILLS GAPS WITH PROFESSIONAL PLANNING
           - Adds missing critical steps
           - Includes proper project management phases
           - Incorporates risk mitigation steps
        
        3. PROVIDES DETAILED IMPLEMENTATION GUIDANCE
           - Specific actions for each step
           - Resource requirements per step
           - Timeline estimates and dependencies
           - Success criteria and deliverables
        
        4. INCLUDES QUALITY ASSURANCE
           - Review and validation steps
           - Testing and verification points
           - Feedback and iteration cycles
        
        5. ADDRESSES RISK MANAGEMENT
           - Identifies potential risks per step
           - Provides mitigation strategies
           - Includes contingency planning
        
        Format as a structured action plan with clear phases, steps, and implementation details.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_formatted}
        ]
        
        response_content = self._call_openai(messages)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "ActionPlanningAgent",
                "extracted_steps": extracted_steps,
                "implicit_requirements": implicit_requirements,
                "action_plan_framework": action_plan,
                "project_type": project_type,
                "complexity": complexity,
                "step_extraction_method": "explicit_pattern_matching"
            },
            confidence_score=0.85 + (0.1 if len(extracted_steps) > 0 else 0),
            reasoning=f"Extracted {len(extracted_steps)} explicit steps and generated comprehensive action plan"
        )
    
    def _extract_steps_from_prompt(self, prompt: str) -> List[Dict[str, Any]]:
        """Extract explicit steps from user prompt using pattern matching"""
        extracted_steps = []
        prompt_lower = prompt.lower()
        
        # Try different step extraction patterns
        for pattern in self.step_patterns:
            matches = re.finditer(pattern, prompt, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match.groups()) == 2:
                    step_num = match.group(1)
                    step_text = match.group(2).strip()
                elif len(match.groups()) == 1:
                    step_num = len(extracted_steps) + 1
                    step_text = match.group(1).strip()
                else:
                    continue
                
                if step_text and len(step_text) > 5:  # Filter out very short matches
                    extracted_steps.append({
                        "step_number": step_num,
                        "description": step_text,
                        "source": "explicit_user_prompt",
                        "pattern_used": pattern
                    })
        
        # Remove duplicates and sort
        unique_steps = []
        seen_descriptions = set()
        for step in extracted_steps:
            if step["description"] not in seen_descriptions:
                unique_steps.append(step)
                seen_descriptions.add(step["description"])
        
        return unique_steps
    
    def _analyze_implicit_requirements(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt for implicit requirements and missing steps"""
        implicit_reqs = {
            "planning_phase_needed": False,
            "testing_phase_needed": False,
            "deployment_phase_needed": False,
            "documentation_needed": False,
            "stakeholder_involvement": False,
            "risk_management_needed": False,
            "quality_assurance_needed": False
        }
        
        prompt_lower = prompt.lower()
        
        # Check for implicit requirements
        if any(word in prompt_lower for word in ['project', 'develop', 'build', 'create']):
            implicit_reqs["planning_phase_needed"] = True
        
        if any(word in prompt_lower for word in ['software', 'application', 'system', 'code']):
            implicit_reqs["testing_phase_needed"] = True
            implicit_reqs["deployment_phase_needed"] = True
        
        if any(word in prompt_lower for word in ['document', 'manual', 'guide', 'specification']):
            implicit_reqs["documentation_needed"] = True
        
        if any(word in prompt_lower for word in ['team', 'stakeholder', 'client', 'user']):
            implicit_reqs["stakeholder_involvement"] = True
        
        if any(word in prompt_lower for word in ['risk', 'critical', 'important', 'complex']):
            implicit_reqs["risk_management_needed"] = True
        
        if any(word in prompt_lower for word in ['quality', 'review', 'validate', 'verify']):
            implicit_reqs["quality_assurance_needed"] = True
        
        return implicit_reqs
    
    def _generate_action_plan(self, goal: str, extracted_steps: List, implicit_reqs: Dict, 
                            project_type: str, timeline: str, resources: str, complexity: str) -> Dict[str, Any]:
        """Generate comprehensive action plan framework"""
        
        plan = {
            "phases": [],
            "total_estimated_duration": timeline,
            "resource_requirements": resources,
            "complexity_level": complexity,
            "user_specified_steps": len(extracted_steps),
            "enhancement_areas": []
        }
        
        # Standard phases based on project type
        if project_type in ['software_development', 'technical']:
            plan["phases"] = ["Planning", "Design", "Development", "Testing", "Deployment"]
        elif project_type in ['project_management', 'business']:
            plan["phases"] = ["Initiation", "Planning", "Execution", "Monitoring", "Closure"]
        else:
            plan["phases"] = ["Planning", "Execution", "Review", "Completion"]
        
        # Add enhancement areas based on implicit requirements
        for req, needed in implicit_reqs.items():
            if needed:
                plan["enhancement_areas"].append(req.replace("_", " ").title())
        
        return plan
    
    def create_action_plan_from_prompt(self, user_prompt: str, goal: str = None) -> AgentResponse:
        """Convenience method for creating action plan from user prompt"""
        return self.process({
            'user_prompt': user_prompt,
            'goal': goal or user_prompt,
            'project_type': 'general'
        })
