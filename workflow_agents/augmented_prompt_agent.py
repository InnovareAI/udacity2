
"""
Augmented Prompt Agent - Enhanced prompt optimization and structure improvement
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse

class AugmentedPromptAgent(BaseAgent):
    """
    Specialized agent for prompt enhancement and optimization:
    - Prompt structure optimization
    - Context enhancement and clarity improvement
    - Template creation and standardization
    - Prompt engineering best practices
    - Domain-specific prompt adaptation
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "prompt_enhancement", "structure_optimization", "context_addition",
            "clarity_improvement", "template_creation", "prompt_engineering"
        ]
        self.specialties = [
            "project_management_prompts", "technical_prompts", "evaluation_prompts",
            "planning_prompts", "analysis_prompts", "creative_prompts"
        ]
        
        # Prompt enhancement patterns
        self.enhancement_patterns = {
            "structure": {
                "add_sections": ["Context", "Objective", "Requirements", "Output Format"],
                "formatting": ["Headers", "Bullet points", "Numbered lists", "Clear sections"],
                "organization": ["Logical flow", "Priority ordering", "Dependency mapping"]
            },
            "clarity": {
                "language": ["Clear terminology", "Specific instructions", "Unambiguous wording"],
                "examples": ["Sample inputs", "Expected outputs", "Use cases"],
                "constraints": ["Explicit limitations", "Boundary conditions", "Success criteria"]
            },
            "context": {
                "background": ["Domain knowledge", "Historical context", "Current situation"],
                "stakeholders": ["Target audience", "User personas", "Stakeholder needs"],
                "environment": ["Technical constraints", "Resource limitations", "Time constraints"]
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process prompt enhancement requests
        
        Args:
            input_data: Dictionary containing:
                - original_prompt: The prompt to enhance
                - task_domain: Domain/context for the prompt
                - target_audience: Intended audience
                - enhancement_type: Type of enhancement needed
                - specific_requirements: Specific enhancement requirements
        """
        original_prompt = input_data.get('original_prompt', '')
        task_domain = input_data.get('task_domain', 'general')
        target_audience = input_data.get('target_audience', 'general_users')
        enhancement_type = input_data.get('enhancement_type', 'comprehensive')
        specific_requirements = input_data.get('specific_requirements', [])
        
        # Analyze current prompt
        prompt_analysis = self._analyze_prompt(original_prompt)
        
        system_prompt = """You are an expert prompt engineer and communication specialist with deep expertise in:

- Advanced prompt engineering techniques and best practices
- Clear and effective communication across diverse domains
- Structured information presentation and organization
- Context optimization for AI interactions
- Domain-specific prompt adaptation and customization
- User experience optimization for prompt-based interactions

Your enhancement approach should be:
- Systematic with clear structure and organization
- Context-rich with relevant background information
- User-focused with audience-appropriate language
- Actionable with specific, measurable instructions
- Comprehensive covering all necessary aspects
- Optimized for AI understanding and response quality
- Scalable and reusable across similar use cases

Always maintain the original intent while significantly improving clarity, structure, and effectiveness."""
        
        user_prompt = f"""
        PROMPT ENHANCEMENT REQUEST
        
        Original Prompt:
        {original_prompt}
        
        Enhancement Context:
        - Task Domain: {task_domain}
        - Target Audience: {target_audience}
        - Enhancement Type: {enhancement_type}
        - Specific Requirements: {specific_requirements}
        
        Current Prompt Analysis:
        - Structure Quality: {prompt_analysis['structure_quality']}
        - Clarity Level: {prompt_analysis['clarity_level']}
        - Context Completeness: {prompt_analysis['context_completeness']}
        - Specificity Score: {prompt_analysis['specificity_score']}
        - Identified Gaps: {prompt_analysis['gaps']}
        
        Please provide a comprehensive prompt enhancement including:
        
        1. ENHANCED PROMPT
           - Restructured and optimized version
           - Clear sections and organization
           - Improved clarity and specificity
           - Enhanced context and background
           - Explicit instructions and requirements
        
        2. ENHANCEMENT ANALYSIS
           - Key improvements made
           - Structure optimizations applied
           - Context additions and clarifications
           - Clarity improvements implemented
           - Specificity enhancements added
        
        3. PROMPT STRUCTURE BREAKDOWN
           - Section-by-section explanation
           - Purpose of each component
           - How sections work together
           - Flow and logical progression
        
        4. USAGE GUIDELINES
           - How to use the enhanced prompt effectively
           - Customization options for different contexts
           - Common variations and adaptations
           - Best practices for implementation
        
        5. QUALITY METRICS
           - Improvement measurements
           - Expected response quality enhancement
           - Clarity and comprehension improvements
           - Effectiveness indicators
        
        6. DOMAIN-SPECIFIC OPTIMIZATIONS
           - Adaptations for the specific domain
           - Technical terminology and concepts
           - Industry best practices integration
           - Stakeholder-specific considerations
        
        7. ALTERNATIVE VERSIONS
           - Simplified version for basic use
           - Detailed version for complex scenarios
           - Domain-specific variations
           - Audience-adapted alternatives
        
        8. VALIDATION AND TESTING
           - How to test prompt effectiveness
           - Success criteria and metrics
           - Iterative improvement suggestions
           - Feedback collection methods
        
        Ensure the enhanced prompt is significantly more effective than the original while maintaining its core purpose.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        # Calculate improvement metrics
        improvement_metrics = self._calculate_improvement_metrics(original_prompt, response_content)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "AugmentedPromptAgent",
                "enhancement_type": enhancement_type,
                "task_domain": task_domain,
                "target_audience": target_audience,
                "original_analysis": prompt_analysis,
                "improvement_metrics": improvement_metrics,
                "enhancement_categories": self._identify_enhancement_categories(response_content),
                "reusability_score": self._assess_reusability(response_content)
            },
            confidence_score=confidence_score,
            reasoning=f"Enhanced {task_domain} prompt for {target_audience} with {enhancement_type} improvements focusing on structure, clarity, and context"
        )
    
    def enhance_for_project_management(self, original_prompt: str) -> AgentResponse:
        """Enhance prompt specifically for project management context"""
        return self.process({
            'original_prompt': original_prompt,
            'task_domain': 'project_management',
            'target_audience': 'project_managers',
            'enhancement_type': 'project_focused',
            'specific_requirements': [
                'Add project context', 'Include stakeholder considerations',
                'Specify deliverables', 'Add timeline considerations'
            ]
        })
    
    def enhance_for_technical_tasks(self, original_prompt: str, technology: str = "") -> AgentResponse:
        """Enhance prompt for technical tasks"""
        return self.process({
            'original_prompt': original_prompt,
            'task_domain': 'technical',
            'target_audience': 'technical_professionals',
            'enhancement_type': 'technical_focused',
            'specific_requirements': [
                'Add technical context', 'Specify technical requirements',
                'Include best practices', f'Optimize for {technology}' if technology else 'General technical optimization'
            ]
        })
    
    def create_evaluation_prompt(self, evaluation_criteria: List[str], scoring_method: str = "1-10") -> AgentResponse:
        """Create structured evaluation prompt"""
        original_prompt = f"Evaluate based on: {', '.join(evaluation_criteria)} using {scoring_method} scale"
        return self.process({
            'original_prompt': original_prompt,
            'task_domain': 'evaluation',
            'target_audience': 'evaluators',
            'enhancement_type': 'evaluation_focused',
            'specific_requirements': [
                'Structure evaluation criteria', 'Add scoring guidelines',
                'Include examples', 'Specify output format'
            ]
        })
    
    def optimize_for_clarity(self, original_prompt: str) -> AgentResponse:
        """Optimize prompt specifically for clarity"""
        return self.process({
            'original_prompt': original_prompt,
            'enhancement_type': 'clarity_focused',
            'specific_requirements': [
                'Improve word choice', 'Simplify complex sentences',
                'Add examples', 'Remove ambiguity'
            ]
        })
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze current prompt quality and characteristics"""
        analysis = {
            'length': len(prompt),
            'structure_quality': self._assess_structure_quality(prompt),
            'clarity_level': self._assess_clarity_level(prompt),
            'context_completeness': self._assess_context_completeness(prompt),
            'specificity_score': self._assess_specificity(prompt),
            'gaps': self._identify_gaps(prompt)
        }
        return analysis
    
    def _assess_structure_quality(self, prompt: str) -> str:
        """Assess structural quality of prompt"""
        structure_indicators = ['#', '##', '###', '-', '*', '1.', '2.', '3.', '\n\n']
        structure_count = sum(1 for indicator in structure_indicators if indicator in prompt)
        
        if structure_count > 10:
            return 'excellent'
        elif structure_count > 5:
            return 'good'
        elif structure_count > 2:
            return 'fair'
        else:
            return 'poor'
    
    def _assess_clarity_level(self, prompt: str) -> str:
        """Assess clarity level of prompt"""
        clarity_indicators = ['clear', 'specific', 'detailed', 'example', 'format']
        ambiguity_indicators = ['maybe', 'perhaps', 'might', 'could', 'unclear']
        
        clarity_score = sum(1 for indicator in clarity_indicators if indicator in prompt.lower())
        ambiguity_score = sum(1 for indicator in ambiguity_indicators if indicator in prompt.lower())
        
        net_score = clarity_score - ambiguity_score
        
        if net_score > 3:
            return 'high'
        elif net_score > 0:
            return 'medium'
        else:
            return 'low'
    
    def _assess_context_completeness(self, prompt: str) -> str:
        """Assess context completeness"""
        context_indicators = ['background', 'context', 'situation', 'environment', 'constraints']
        context_count = sum(1 for indicator in context_indicators if indicator in prompt.lower())
        
        if context_count > 2:
            return 'complete'
        elif context_count > 0:
            return 'partial'
        else:
            return 'minimal'
    
    def _assess_specificity(self, prompt: str) -> float:
        """Assess specificity of prompt"""
        specific_indicators = ['exactly', 'specifically', 'must', 'required', 'format', 'include']
        vague_indicators = ['some', 'any', 'general', 'basic', 'simple']
        
        specific_count = sum(1 for indicator in specific_indicators if indicator in prompt.lower())
        vague_count = sum(1 for indicator in vague_indicators if indicator in prompt.lower())
        
        # Normalize to 0-1 scale
        total_words = len(prompt.split())
        specificity_ratio = (specific_count - vague_count) / max(total_words / 100, 1)
        
        return max(0, min(1, specificity_ratio + 0.5))  # Baseline of 0.5
    
    def _identify_gaps(self, prompt: str) -> List[str]:
        """Identify gaps in prompt structure"""
        gaps = []
        
        if 'context' not in prompt.lower() and 'background' not in prompt.lower():
            gaps.append('Missing context/background')
        
        if 'format' not in prompt.lower() and 'output' not in prompt.lower():
            gaps.append('Missing output format specification')
        
        if 'example' not in prompt.lower():
            gaps.append('Missing examples')
        
        if len(prompt) < 100:
            gaps.append('Too brief - needs more detail')
        
        if '?' not in prompt and 'please' not in prompt.lower():
            gaps.append('Missing clear request/question')
        
        return gaps
    
    def _calculate_improvement_metrics(self, original: str, enhanced: str) -> Dict[str, Any]:
        """Calculate improvement metrics"""
        return {
            'length_increase': len(enhanced) - len(original),
            'structure_improvement': self._compare_structure(original, enhanced),
            'clarity_improvement': self._compare_clarity(original, enhanced),
            'specificity_improvement': self._assess_specificity(enhanced) - self._assess_specificity(original)
        }
    
    def _compare_structure(self, original: str, enhanced: str) -> str:
        """Compare structural improvements"""
        original_quality = self._assess_structure_quality(original)
        enhanced_quality = self._assess_structure_quality(enhanced)
        
        quality_levels = ['poor', 'fair', 'good', 'excellent']
        original_index = quality_levels.index(original_quality)
        enhanced_index = quality_levels.index(enhanced_quality)
        
        improvement = enhanced_index - original_index
        
        if improvement > 1:
            return 'significant'
        elif improvement > 0:
            return 'moderate'
        else:
            return 'minimal'
    
    def _compare_clarity(self, original: str, enhanced: str) -> str:
        """Compare clarity improvements"""
        original_clarity = self._assess_clarity_level(original)
        enhanced_clarity = self._assess_clarity_level(enhanced)
        
        clarity_levels = ['low', 'medium', 'high']
        original_index = clarity_levels.index(original_clarity)
        enhanced_index = clarity_levels.index(enhanced_clarity)
        
        improvement = enhanced_index - original_index
        
        if improvement > 0:
            return 'improved'
        else:
            return 'maintained'
    
    def _identify_enhancement_categories(self, enhanced_content: str) -> List[str]:
        """Identify categories of enhancements applied"""
        categories = []
        
        if 'structure' in enhanced_content.lower() or '#' in enhanced_content:
            categories.append('structural')
        
        if 'context' in enhanced_content.lower() or 'background' in enhanced_content.lower():
            categories.append('contextual')
        
        if 'example' in enhanced_content.lower():
            categories.append('illustrative')
        
        if 'format' in enhanced_content.lower() or 'output' in enhanced_content.lower():
            categories.append('formatting')
        
        return categories
    
    def _assess_reusability(self, enhanced_content: str) -> float:
        """Assess reusability of enhanced prompt"""
        reusability_indicators = ['template', 'customize', 'adapt', 'modify', 'reuse']
        indicator_count = sum(1 for indicator in reusability_indicators if indicator in enhanced_content.lower())
        
        # Normalize to 0-1 scale
        return min(1.0, indicator_count / 3)
