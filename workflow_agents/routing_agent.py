
"""
Routing Agent - Enhanced intelligent task routing with comprehensive analysis
"""

from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentResponse
import json
import re

class RoutingAgent(BaseAgent):
    """
    Enhanced routing agent that intelligently routes tasks to appropriate specialized agents:
    - Advanced task analysis and classification
    - Multi-agent workflow coordination
    - Confidence-based routing decisions
    - Alternative routing suggestions
    - Workflow optimization recommendations
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "intelligent_task_routing", "workflow_coordination", "agent_selection",
            "multi_agent_orchestration", "routing_optimization"
        ]
        self.specialties = [
            "task_classification", "agent_capability_matching", "workflow_design",
            "routing_confidence_assessment", "alternative_path_analysis"
        ]
        
        # Enhanced agent capabilities with detailed routing logic
        self.agent_capabilities = {
            'ProjectManagerAgent': {
                'specialties': [
                    'project_planning', 'resource_allocation', 'timeline_management', 
                    'risk_assessment', 'stakeholder_management', 'budget_planning',
                    'milestone_tracking', 'team_coordination'
                ],
                'keywords': [
                    'project', 'plan', 'timeline', 'milestone', 'resource', 'risk', 
                    'stakeholder', 'budget', 'scope', 'deliverable', 'schedule',
                    'coordination', 'management', 'planning'
                ],
                'task_types': ['planning', 'management', 'coordination', 'oversight'],
                'confidence_threshold': 0.7,
                'complexity_handling': ['low', 'medium', 'high'],
                'typical_outputs': ['project_plans', 'timelines', 'risk_assessments']
            },
            'AugmentedPromptAgent': {
                'specialties': [
                    'prompt_enhancement', 'context_addition', 'structure_optimization', 
                    'clarity_improvement', 'prompt_engineering'
                ],
                'keywords': [
                    'prompt', 'enhance', 'improve', 'structure', 'clarity', 'context', 
                    'optimize', 'refine', 'format', 'template'
                ],
                'task_types': ['enhancement', 'optimization', 'formatting'],
                'confidence_threshold': 0.8,
                'complexity_handling': ['low', 'medium'],
                'typical_outputs': ['enhanced_prompts', 'structured_requests']
            },
            'KnowledgeAugmentedPromptAgent': {
                'specialties': [
                    'domain_knowledge_integration', 'best_practices', 'framework_application', 
                    'expertise_addition', 'methodology_integration'
                ],
                'keywords': [
                    'knowledge', 'expertise', 'best_practice', 'framework', 'methodology', 
                    'domain', 'standard', 'guideline', 'principle', 'approach'
                ],
                'task_types': ['knowledge_integration', 'expertise_application'],
                'confidence_threshold': 0.75,
                'complexity_handling': ['medium', 'high'],
                'typical_outputs': ['knowledge_enhanced_content', 'expert_recommendations']
            },
            'RAGKnowledgePromptAgent': {
                'specialties': [
                    'information_retrieval', 'knowledge_search', 'source_integration', 
                    'fact_checking', 'research_augmentation'
                ],
                'keywords': [
                    'retrieve', 'search', 'source', 'reference', 'lookup', 'find', 
                    'information', 'research', 'data', 'facts'
                ],
                'task_types': ['research', 'information_gathering', 'fact_checking'],
                'confidence_threshold': 0.8,
                'complexity_handling': ['medium', 'high'],
                'typical_outputs': ['research_results', 'sourced_information']
            },
            'EvaluationAgent': {
                'specialties': [
                    'quality_assessment', 'scoring', 'feedback_generation', 
                    'performance_evaluation', 'compliance_checking', 'review_processes'
                ],
                'keywords': [
                    'evaluate', 'assess', 'score', 'quality', 'feedback', 'review', 
                    'grade', 'measure', 'analyze', 'critique', 'audit'
                ],
                'task_types': ['evaluation', 'assessment', 'review', 'analysis'],
                'confidence_threshold': 0.85,
                'complexity_handling': ['low', 'medium', 'high'],
                'typical_outputs': ['evaluation_reports', 'scores', 'recommendations']
            },
            'ActionPlanningAgent': {
                'specialties': [
                    'task_breakdown', 'action_planning', 'step_sequencing', 
                    'implementation_strategy', 'workflow_design', 'process_planning'
                ],
                'keywords': [
                    'action', 'plan', 'step', 'task', 'implement', 'execute', 
                    'strategy', 'breakdown', 'sequence', 'workflow', 'process'
                ],
                'task_types': ['planning', 'implementation', 'process_design'],
                'confidence_threshold': 0.75,
                'complexity_handling': ['low', 'medium', 'high'],
                'typical_outputs': ['action_plans', 'step_by_step_guides', 'workflows']
            }
        }
        
        # Task classification patterns
        self.task_patterns = {
            'project_management': [
                r'project.*plan', r'manage.*project', r'timeline.*project',
                r'resource.*allocation', r'risk.*assessment', r'stakeholder.*management'
            ],
            'evaluation': [
                r'evaluate.*', r'assess.*quality', r'review.*deliverable',
                r'score.*', r'feedback.*', r'quality.*check'
            ],
            'planning': [
                r'create.*plan', r'action.*plan', r'step.*by.*step',
                r'implementation.*strategy', r'breakdown.*task'
            ],
            'enhancement': [
                r'improve.*prompt', r'enhance.*', r'optimize.*',
                r'refine.*', r'better.*structure'
            ],
            'research': [
                r'find.*information', r'research.*', r'lookup.*',
                r'retrieve.*knowledge', r'search.*for'
            ]
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process routing requests with comprehensive analysis
        
        Args:
            input_data: Dictionary containing:
                - task_description: Description of the task to route
                - context: Additional context about the task
                - priority: Task priority level
                - constraints: Any routing constraints
                - preferred_agents: Preferred agents if any
        """
        task_description = input_data.get('task_description', '')
        context = input_data.get('context', '')
        priority = input_data.get('priority', 'medium')
        constraints = input_data.get('constraints', {})
        preferred_agents = input_data.get('preferred_agents', [])
        
        # Comprehensive task analysis
        task_analysis = self._analyze_task_comprehensively(task_description, context)
        
        # Determine optimal routing
        routing_decision = self._make_routing_decision(task_analysis, constraints, preferred_agents)
        
        # Generate routing recommendations
        routing_recommendations = self._generate_routing_recommendations(task_analysis, routing_decision)
        
        system_prompt = """You are an expert AI workflow orchestrator and task routing specialist with deep expertise in:

- Intelligent task analysis and classification
- Agent capability assessment and matching
- Multi-agent workflow design and optimization
- Routing confidence evaluation and risk assessment
- Alternative pathway analysis and contingency planning

Your routing decisions should be:
- Data-driven based on comprehensive task analysis
- Confidence-scored with clear reasoning
- Alternative-aware with backup options
- Workflow-optimized for efficiency and quality
- Risk-conscious with mitigation strategies
- Scalable and maintainable

Always provide detailed reasoning, confidence scores, and actionable recommendations."""
        
        user_prompt = f"""
        TASK ROUTING REQUEST
        
        Task Description: {task_description}
        Context: {context}
        Priority: {priority}
        Constraints: {constraints}
        Preferred Agents: {preferred_agents}
        
        ANALYSIS RESULTS:
        Task Classification: {task_analysis['classification']}
        Complexity Level: {task_analysis['complexity']}
        Domain: {task_analysis['domain']}
        Key Patterns: {task_analysis['patterns']}
        Multi-Agent Need: {task_analysis['multi_agent_required']}
        
        ROUTING DECISION:
        Primary Agent: {routing_decision['primary_agent']}
        Confidence: {routing_decision['confidence']:.2f}
        Alternative Agents: {routing_decision['alternatives']}
        
        Please provide a comprehensive routing analysis including:
        
        1. ROUTING RECOMMENDATION
           - Primary agent selection with detailed reasoning
           - Confidence score justification
           - Expected outcomes and deliverables
           - Success probability assessment
        
        2. ALTERNATIVE ROUTING OPTIONS
           - Secondary agent recommendations
           - Fallback strategies if primary fails
           - Comparative analysis of options
           - Risk-benefit assessment for each
        
        3. MULTI-AGENT WORKFLOW DESIGN
           - Sequential workflow recommendations
           - Parallel processing opportunities
           - Agent coordination strategies
           - Handoff points and dependencies
        
        4. OPTIMIZATION RECOMMENDATIONS
           - Efficiency improvements
           - Quality enhancement strategies
           - Resource utilization optimization
           - Timeline optimization
        
        5. RISK ASSESSMENT
           - Potential routing risks
           - Agent capability limitations
           - Mitigation strategies
           - Contingency planning
        
        6. MONITORING & FEEDBACK
           - Success metrics for routing decision
           - Quality checkpoints
           - Feedback collection strategies
           - Continuous improvement recommendations
        
        Provide specific, actionable recommendations with confidence scores and reasoning.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = routing_decision['confidence']
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "RoutingAgent",
                "primary_agent": routing_decision['primary_agent'],
                "routing_confidence": confidence_score,
                "alternative_agents": routing_decision['alternatives'],
                "task_analysis": task_analysis,
                "routing_decision": routing_decision,
                "workflow_recommendations": routing_recommendations,
                "priority": priority,
                "multi_agent_workflow": task_analysis['multi_agent_required']
            },
            confidence_score=confidence_score,
            reasoning=f"Analyzed task using {len(task_analysis['patterns'])} patterns and recommended {routing_decision['primary_agent']} with {confidence_score:.2f} confidence"
        )
    
    def _analyze_task_comprehensively(self, task_description: str, context: str) -> Dict[str, Any]:
        """Perform comprehensive task analysis for routing"""
        combined_text = f"{task_description} {context}".lower()
        
        analysis = {
            'classification': self._classify_task_advanced(combined_text),
            'complexity': self._assess_complexity_detailed(combined_text),
            'domain': self._identify_domain_advanced(combined_text),
            'patterns': self._extract_task_patterns(combined_text),
            'keywords': self._extract_routing_keywords(combined_text),
            'multi_agent_required': self._assess_multi_agent_requirement(combined_text),
            'urgency': self._assess_urgency(combined_text),
            'scope': self._assess_scope(combined_text)
        }
        
        return analysis
    
    def _classify_task_advanced(self, text: str) -> str:
        """Advanced task classification using pattern matching"""
        classification_scores = {}
        
        for task_type, patterns in self.task_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            classification_scores[task_type] = score
        
        if max(classification_scores.values()) > 0:
            return max(classification_scores, key=classification_scores.get)
        else:
            return 'general'
    
    def _assess_complexity_detailed(self, text: str) -> str:
        """Detailed complexity assessment"""
        complexity_indicators = {
            'high': [
                'complex', 'comprehensive', 'detailed', 'multi-step', 'integration',
                'enterprise', 'advanced', 'sophisticated', 'intricate'
            ],
            'medium': [
                'moderate', 'standard', 'typical', 'regular', 'normal',
                'intermediate', 'balanced'
            ],
            'low': [
                'simple', 'basic', 'quick', 'straightforward', 'minimal',
                'elementary', 'fundamental'
            ]
        }
        
        scores = {}
        for level, indicators in complexity_indicators.items():
            scores[level] = sum(1 for indicator in indicators if indicator in text)
        
        # Factor in text length and structure
        text_length_factor = len(text) / 1000  # Normalize by 1000 chars
        if text_length_factor > 2:
            scores['high'] += 2
        elif text_length_factor > 1:
            scores['medium'] += 1
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'medium'
    
    def _identify_domain_advanced(self, text: str) -> str:
        """Advanced domain identification"""
        domain_patterns = {
            'project_management': [
                r'project.*management', r'timeline.*planning', r'resource.*allocation',
                r'stakeholder.*engagement', r'risk.*management'
            ],
            'software_development': [
                r'software.*development', r'code.*review', r'application.*development',
                r'programming.*', r'technical.*implementation'
            ],
            'quality_assurance': [
                r'quality.*assurance', r'testing.*', r'evaluation.*quality',
                r'assessment.*', r'review.*process'
            ],
            'documentation': [
                r'documentation.*', r'technical.*writing', r'user.*guide',
                r'specification.*', r'manual.*creation'
            ],
            'research': [
                r'research.*', r'investigation.*', r'analysis.*',
                r'study.*', r'exploration.*'
            ]
        }
        
        domain_scores = {}
        for domain, patterns in domain_patterns.items():
            score = 0
            for pattern in patterns:
                score += len(re.findall(pattern, text, re.IGNORECASE))
            domain_scores[domain] = score
        
        return max(domain_scores, key=domain_scores.get) if max(domain_scores.values()) > 0 else 'general'
    
    def _extract_task_patterns(self, text: str) -> List[str]:
        """Extract relevant task patterns"""
        found_patterns = []
        for task_type, patterns in self.task_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    found_patterns.append(f"{task_type}:{pattern}")
        return found_patterns
    
    def _extract_routing_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract keywords relevant for each agent"""
        agent_keywords = {}
        for agent_name, capabilities in self.agent_capabilities.items():
            found_keywords = [keyword for keyword in capabilities['keywords'] if keyword in text]
            if found_keywords:
                agent_keywords[agent_name] = found_keywords
        return agent_keywords
    
    def _assess_multi_agent_requirement(self, text: str) -> bool:
        """Assess if task requires multiple agents"""
        multi_agent_indicators = [
            'comprehensive', 'end-to-end', 'complete', 'full', 'integrated',
            'multiple phases', 'various aspects', 'different perspectives',
            'holistic approach', 'multi-faceted'
        ]
        
        return any(indicator in text for indicator in multi_agent_indicators)
    
    def _assess_urgency(self, text: str) -> str:
        """Assess task urgency"""
        urgent_indicators = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        normal_indicators = ['soon', 'timely', 'reasonable', 'standard']
        
        if any(indicator in text for indicator in urgent_indicators):
            return 'high'
        elif any(indicator in text for indicator in normal_indicators):
            return 'medium'
        else:
            return 'low'
    
    def _assess_scope(self, text: str) -> str:
        """Assess task scope"""
        large_scope_indicators = ['enterprise', 'organization-wide', 'comprehensive', 'complete']
        medium_scope_indicators = ['department', 'team', 'project-specific']
        small_scope_indicators = ['individual', 'specific', 'focused', 'targeted']
        
        if any(indicator in text for indicator in large_scope_indicators):
            return 'large'
        elif any(indicator in text for indicator in medium_scope_indicators):
            return 'medium'
        else:
            return 'small'
    
    def _make_routing_decision(self, task_analysis: Dict[str, Any], constraints: Dict[str, Any], preferred_agents: List[str]) -> Dict[str, Any]:
        """Make intelligent routing decision based on analysis"""
        agent_scores = {}
        
        # Score each agent based on multiple factors
        for agent_name, capabilities in self.agent_capabilities.items():
            score = 0
            
            # Keyword matching (40% weight)
            agent_keywords = task_analysis['keywords'].get(agent_name, [])
            keyword_score = len(agent_keywords) / len(capabilities['keywords'])
            score += keyword_score * 0.4
            
            # Task type alignment (30% weight)
            task_classification = task_analysis['classification']
            if task_classification in capabilities['task_types']:
                score += 0.3
            
            # Complexity handling (20% weight)
            if task_analysis['complexity'] in capabilities['complexity_handling']:
                score += 0.2
            
            # Domain alignment (10% weight)
            if task_analysis['domain'] in ' '.join(capabilities['specialties']):
                score += 0.1
            
            # Preferred agent bonus
            if agent_name in preferred_agents:
                score += 0.1
            
            agent_scores[agent_name] = min(score, 1.0)  # Cap at 1.0
        
        # Select primary agent
        primary_agent = max(agent_scores, key=agent_scores.get)
        confidence = agent_scores[primary_agent]
        
        # Get alternatives (excluding primary)
        alternatives = []
        for agent, score in sorted(agent_scores.items(), key=lambda x: x[1], reverse=True):
            if agent != primary_agent and score > 0.3:  # Minimum threshold
                alternatives.append({"agent": agent, "confidence": score})
        
        return {
            'primary_agent': primary_agent,
            'confidence': confidence,
            'alternatives': alternatives[:3],  # Top 3 alternatives
            'all_scores': agent_scores
        }
    
    def _generate_routing_recommendations(self, task_analysis: Dict[str, Any], routing_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow and optimization recommendations"""
        recommendations = {
            'workflow_type': 'sequential' if not task_analysis['multi_agent_required'] else 'multi_agent',
            'optimization_suggestions': [],
            'risk_mitigation': [],
            'success_metrics': []
        }
        
        # Add specific recommendations based on analysis
        if task_analysis['complexity'] == 'high':
            recommendations['optimization_suggestions'].append('Consider breaking down into smaller tasks')
            recommendations['risk_mitigation'].append('Implement checkpoints for quality validation')
        
        if task_analysis['multi_agent_required']:
            recommendations['workflow_type'] = 'orchestrated'
            recommendations['optimization_suggestions'].append('Design clear handoff protocols between agents')
        
        if routing_decision['confidence'] < 0.7:
            recommendations['risk_mitigation'].append('Consider human oversight for quality assurance')
        
        return recommendations
    
    def route_task(self, task_description: str, context: str = "", priority: str = "medium") -> AgentResponse:
        """Route a specific task with enhanced analysis"""
        return self.process({
            'task_description': task_description,
            'context': context,
            'priority': priority
        })
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Get detailed information about available agents and their capabilities"""
        return self.agent_capabilities
    
    def analyze_routing_patterns(self, routing_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze routing patterns for optimization (future enhancement)"""
        # Placeholder for routing pattern analysis
        return {
            'most_used_agents': [],
            'success_rates': {},
            'optimization_opportunities': []
        }
