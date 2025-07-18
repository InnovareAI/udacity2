

"""
Knowledge Augmented Prompt Agent - Domain expertise and best practices integration
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse

class KnowledgeAugmentedPromptAgent(BaseAgent):
    """
    Specialized agent for integrating domain knowledge and expertise:
    - Domain-specific knowledge integration
    - Best practices and methodologies application
    - Framework and standard implementation
    - Expert-level guidance and recommendations
    - Industry-specific optimizations
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "domain_knowledge_integration", "best_practices_application", 
            "framework_implementation", "methodology_guidance", "expert_recommendations"
        ]
        self.specialties = [
            "project_management_expertise", "software_development_practices",
            "quality_assurance_standards", "business_analysis_methods",
            "technical_architecture_patterns", "industry_compliance"
        ]
        
        # Knowledge bases for different domains
        self.knowledge_bases = {
            "project_management": {
                "frameworks": ["PMI/PMBOK", "Agile/Scrum", "PRINCE2", "Lean", "Kanban"],
                "best_practices": [
                    "Stakeholder engagement throughout project lifecycle",
                    "Regular risk assessment and mitigation planning",
                    "Clear communication and documentation standards",
                    "Iterative planning with feedback incorporation",
                    "Quality gates and milestone reviews"
                ],
                "key_principles": [
                    "Scope-Time-Cost triangle management",
                    "Stakeholder value maximization",
                    "Continuous improvement and lessons learned",
                    "Risk-based decision making",
                    "Team empowerment and collaboration"
                ],
                "common_tools": ["Gantt charts", "Risk registers", "Stakeholder matrices", "WBS", "Burndown charts"]
            },
            "software_development": {
                "frameworks": ["SDLC", "DevOps", "CI/CD", "Test-Driven Development", "Clean Architecture"],
                "best_practices": [
                    "Code review and pair programming",
                    "Automated testing and continuous integration",
                    "Version control and branching strategies",
                    "Documentation and code commenting",
                    "Security-first development approach"
                ],
                "key_principles": [
                    "DRY (Don't Repeat Yourself)",
                    "SOLID principles",
                    "Separation of concerns",
                    "Fail fast and fail safe",
                    "Scalability and maintainability focus"
                ],
                "common_tools": ["Git", "Jenkins", "Docker", "Testing frameworks", "Code analyzers"]
            },
            "quality_assurance": {
                "frameworks": ["ISO 9001", "Six Sigma", "TQM", "CMMI", "Testing frameworks"],
                "best_practices": [
                    "Risk-based testing approach",
                    "Continuous quality monitoring",
                    "Defect prevention over detection",
                    "Stakeholder feedback integration",
                    "Process improvement and optimization"
                ],
                "key_principles": [
                    "Customer focus and satisfaction",
                    "Process approach to quality",
                    "Evidence-based decision making",
                    "Continuous improvement culture",
                    "Leadership and team engagement"
                ],
                "common_tools": ["Test management tools", "Defect tracking", "Quality metrics", "Audit checklists"]
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process knowledge augmentation requests
        
        Args:
            input_data: Dictionary containing:
                - content: Content to augment with knowledge
                - domain: Domain for knowledge integration
                - expertise_level: Required expertise level
                - frameworks: Specific frameworks to apply
                - context: Additional context for knowledge selection
        """
        content = input_data.get('content', '')
        domain = input_data.get('domain', 'project_management')
        expertise_level = input_data.get('expertise_level', 'intermediate')
        frameworks = input_data.get('frameworks', [])
        context = input_data.get('context', '')
        
        # Get relevant knowledge base
        knowledge_base = self.knowledge_bases.get(domain, self.knowledge_bases['project_management'])
        
        # Select relevant frameworks if not specified
        if not frameworks:
            frameworks = knowledge_base['frameworks'][:2]  # Use top 2 frameworks
        
        system_prompt = """You are a senior domain expert and knowledge integration specialist with deep expertise across multiple professional domains including:

- Project management methodologies and best practices
- Software development frameworks and engineering principles
- Quality assurance standards and testing methodologies
- Business analysis techniques and process optimization
- Technical architecture patterns and design principles
- Industry compliance and regulatory requirements

Your knowledge integration approach should be:
- Expert-level with deep domain understanding
- Practical with actionable recommendations and guidance
- Framework-based using established methodologies and standards
- Best-practice oriented with proven approaches
- Context-aware adapting to specific situations and requirements
- Comprehensive covering all relevant aspects and considerations
- Professional with industry-standard terminology and concepts

Always integrate authoritative knowledge sources, established frameworks, and proven best practices while maintaining practical applicability."""
        
        user_prompt = f"""
        KNOWLEDGE AUGMENTATION REQUEST
        
        Original Content:
        {content}
        
        Domain: {domain}
        Expertise Level: {expertise_level}
        Frameworks to Apply: {frameworks}
        Additional Context: {context}
        
        Available Knowledge Base:
        - Frameworks: {knowledge_base['frameworks']}
        - Best Practices: {knowledge_base['best_practices']}
        - Key Principles: {knowledge_base['key_principles']}
        - Common Tools: {knowledge_base['common_tools']}
        
        Please provide comprehensive knowledge augmentation including:
        
        1. KNOWLEDGE-ENHANCED CONTENT
           - Original content enhanced with domain expertise
           - Framework-based recommendations and guidance
           - Best practices integration and application
           - Expert-level insights and considerations
           - Industry-standard approaches and methodologies
        
        2. FRAMEWORK APPLICATION
           - Specific framework implementations
           - Methodology adaptations for the context
           - Standard processes and procedures
           - Framework-specific tools and techniques
           - Integration strategies for multiple frameworks
        
        3. BEST PRACTICES INTEGRATION
           - Industry best practices application
           - Proven approaches and methodologies
           - Success factors and critical considerations
           - Common pitfalls and avoidance strategies
           - Optimization opportunities and improvements
        
        4. EXPERT RECOMMENDATIONS
           - Professional-grade guidance and advice
           - Strategic considerations and implications
           - Risk mitigation and management strategies
           - Quality assurance and validation approaches
           - Performance optimization and enhancement
        
        5. DOMAIN-SPECIFIC INSIGHTS
           - Specialized knowledge and expertise
           - Industry trends and emerging practices
           - Regulatory and compliance considerations
           - Technology and tool recommendations
           - Stakeholder and organizational factors
        
        6. IMPLEMENTATION GUIDANCE
           - Step-by-step implementation approaches
           - Resource requirements and considerations
           - Timeline and milestone recommendations
           - Success metrics and measurement criteria
           - Change management and adoption strategies
        
        7. QUALITY AND STANDARDS
           - Quality assurance requirements
           - Industry standards and compliance
           - Validation and verification approaches
           - Documentation and reporting standards
           - Continuous improvement mechanisms
        
        8. PRACTICAL APPLICATIONS
           - Real-world implementation examples
           - Case studies and lessons learned
           - Adaptation strategies for different contexts
           - Scalability and sustainability considerations
           - ROI and value proposition analysis
        
        Ensure the augmented content demonstrates expert-level domain knowledge while remaining practical and actionable.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        # Analyze knowledge integration quality
        integration_analysis = self._analyze_knowledge_integration(response_content, knowledge_base, frameworks)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "KnowledgeAugmentedPromptAgent",
                "domain": domain,
                "expertise_level": expertise_level,
                "frameworks_applied": frameworks,
                "knowledge_base_used": domain,
                "integration_analysis": integration_analysis,
                "best_practices_count": len(knowledge_base['best_practices']),
                "frameworks_available": len(knowledge_base['frameworks']),
                "knowledge_depth": self._assess_knowledge_depth(response_content)
            },
            confidence_score=confidence_score,
            reasoning=f"Integrated {domain} expertise using {len(frameworks)} frameworks with {expertise_level} level knowledge augmentation"
        )
    
    def respond(self, content: str, domain: str = "project_management", expertise_level: str = "advanced") -> AgentResponse:
        """
        Main respond method for Udacity specification compliance
        
        Args:
            content: Content to augment with knowledge
            domain: Domain for knowledge integration
            expertise_level: Required expertise level
        """
        return self.process({
            'content': content,
            'domain': domain,
            'expertise_level': expertise_level,
            'context': 'Knowledge augmentation request'
        })
    
    def add_project_management_knowledge(self, content: str, methodology: str = "PMI") -> AgentResponse:
        """Add project management knowledge and best practices"""
        return self.process({
            'content': content,
            'domain': 'project_management',
            'expertise_level': 'advanced',
            'frameworks': [methodology, 'Agile'],
            'context': 'Project management enhancement'
        })
    
    def add_software_development_knowledge(self, content: str, approach: str = "Agile") -> AgentResponse:
        """Add software development knowledge and practices"""
        return self.process({
            'content': content,
            'domain': 'software_development',
            'expertise_level': 'advanced',
            'frameworks': [approach, 'DevOps'],
            'context': 'Software development enhancement'
        })
    
    def add_quality_assurance_knowledge(self, content: str, standard: str = "ISO 9001") -> AgentResponse:
        """Add quality assurance knowledge and standards"""
        return self.process({
            'content': content,
            'domain': 'quality_assurance',
            'expertise_level': 'expert',
            'frameworks': [standard, 'Six Sigma'],
            'context': 'Quality assurance enhancement'
        })
    
    def integrate_best_practices(self, content: str, domain: str, specific_practices: List[str] = None) -> AgentResponse:
        """Integrate specific best practices into content"""
        knowledge_base = self.knowledge_bases.get(domain, self.knowledge_bases['project_management'])
        practices_to_use = specific_practices or knowledge_base['best_practices'][:3]
        
        return self.process({
            'content': content,
            'domain': domain,
            'expertise_level': 'advanced',
            'context': f'Focus on best practices: {", ".join(practices_to_use)}'
        })
    
    def apply_framework(self, content: str, framework: str, domain: str = "project_management") -> AgentResponse:
        """Apply specific framework to content"""
        return self.process({
            'content': content,
            'domain': domain,
            'expertise_level': 'expert',
            'frameworks': [framework],
            'context': f'Framework-specific application: {framework}'
        })
    
    def _analyze_knowledge_integration(self, content: str, knowledge_base: Dict[str, Any], frameworks: List[str]) -> Dict[str, Any]:
        """Analyze quality of knowledge integration"""
        analysis = {
            'framework_mentions': self._count_framework_mentions(content, frameworks),
            'best_practices_integrated': self._count_best_practices(content, knowledge_base['best_practices']),
            'principles_applied': self._count_principles(content, knowledge_base['key_principles']),
            'tools_referenced': self._count_tools(content, knowledge_base['common_tools']),
            'expertise_level_demonstrated': self._assess_expertise_level(content),
            'practical_applicability': self._assess_practical_applicability(content)
        }
        return analysis
    
    def _count_framework_mentions(self, content: str, frameworks: List[str]) -> int:
        """Count framework mentions in content"""
        content_lower = content.lower()
        return sum(1 for framework in frameworks if framework.lower() in content_lower)
    
    def _count_best_practices(self, content: str, best_practices: List[str]) -> int:
        """Count best practices integrated"""
        content_lower = content.lower()
        count = 0
        for practice in best_practices:
            # Check for key terms from each practice
            practice_terms = practice.lower().split()[:3]  # First 3 words
            if any(term in content_lower for term in practice_terms):
                count += 1
        return count
    
    def _count_principles(self, content: str, principles: List[str]) -> int:
        """Count principles applied"""
        content_lower = content.lower()
        count = 0
        for principle in principles:
            principle_terms = principle.lower().split()[:2]  # First 2 words
            if any(term in content_lower for term in principle_terms):
                count += 1
        return count
    
    def _count_tools(self, content: str, tools: List[str]) -> int:
        """Count tools referenced"""
        content_lower = content.lower()
        return sum(1 for tool in tools if tool.lower() in content_lower)
    
    def _assess_expertise_level(self, content: str) -> str:
        """Assess demonstrated expertise level"""
        expert_indicators = [
            'methodology', 'framework', 'best practice', 'industry standard',
            'proven approach', 'established process', 'professional', 'strategic'
        ]
        
        indicator_count = sum(1 for indicator in expert_indicators if indicator in content.lower())
        
        if indicator_count > 6:
            return 'expert'
        elif indicator_count > 3:
            return 'advanced'
        elif indicator_count > 1:
            return 'intermediate'
        else:
            return 'basic'
    
    def _assess_practical_applicability(self, content: str) -> str:
        """Assess practical applicability of knowledge integration"""
        practical_indicators = [
            'implement', 'apply', 'execute', 'action', 'step',
            'process', 'procedure', 'method', 'approach', 'strategy'
        ]
        
        indicator_count = sum(1 for indicator in practical_indicators if indicator in content.lower())
        
        if indicator_count > 8:
            return 'highly_practical'
        elif indicator_count > 4:
            return 'practical'
        elif indicator_count > 2:
            return 'moderately_practical'
        else:
            return 'theoretical'
    
    def _assess_knowledge_depth(self, content: str) -> str:
        """Assess depth of knowledge demonstrated"""
        depth_indicators = [
            'comprehensive', 'detailed', 'thorough', 'in-depth',
            'extensive', 'complete', 'full', 'holistic'
        ]
        
        indicator_count = sum(1 for indicator in depth_indicators if indicator in content.lower())
        content_length = len(content)
        
        # Combine indicator count with content length
        depth_score = indicator_count + (content_length / 1000)
        
        if depth_score > 5:
            return 'deep'
        elif depth_score > 3:
            return 'moderate'
        else:
            return 'surface'
    
    def get_knowledge_base(self, domain: str) -> Dict[str, Any]:
        """Get knowledge base for specific domain"""
        return self.knowledge_bases.get(domain, {})
    
    def add_custom_knowledge(self, domain: str, knowledge_data: Dict[str, Any]):
        """Add custom knowledge to domain"""
        if domain not in self.knowledge_bases:
            self.knowledge_bases[domain] = {
                "frameworks": [],
                "best_practices": [],
                "key_principles": [],
                "common_tools": []
            }
        
        for key, value in knowledge_data.items():
            if key in self.knowledge_bases[domain]:
                self.knowledge_bases[domain][key].extend(value)

