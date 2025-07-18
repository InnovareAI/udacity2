
"""
Evaluation Agent - Comprehensive evaluation and assessment capabilities
Enhanced with specialized evaluation prompts and scoring systems
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
import json

class EvaluationAgent(BaseAgent):
    """
    Specialized agent for evaluation and assessment tasks:
    - Quality assessment and scoring
    - Performance evaluation
    - Deliverable review and feedback
    - Compliance checking
    - Improvement recommendations
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "quality_assessment", "performance_evaluation", "deliverable_review",
            "compliance_checking", "feedback_generation", "scoring_systems"
        ]
        self.specialties = [
            "project_deliverable_evaluation", "code_quality_assessment", 
            "documentation_review", "process_evaluation", "stakeholder_feedback"
        ]
        
        # Evaluation criteria templates
        self.evaluation_criteria = {
            "project_deliverable": {
                "completeness": "How complete is the deliverable?",
                "quality": "What is the overall quality level?",
                "usability": "How usable is the deliverable?",
                "documentation": "How well documented is it?",
                "maintainability": "How maintainable is the solution?",
                "performance": "How well does it perform?",
                "security": "How secure is the implementation?",
                "scalability": "How scalable is the solution?"
            },
            "code_quality": {
                "readability": "How readable is the code?",
                "structure": "How well structured is the code?",
                "documentation": "How well documented is the code?",
                "testing": "How comprehensive is the testing?",
                "performance": "How efficient is the code?",
                "security": "How secure is the code?",
                "maintainability": "How maintainable is the code?",
                "standards": "How well does it follow standards?"
            },
            "documentation": {
                "clarity": "How clear is the documentation?",
                "completeness": "How complete is the documentation?",
                "accuracy": "How accurate is the documentation?",
                "organization": "How well organized is it?",
                "usability": "How usable is the documentation?",
                "maintenance": "How maintainable is the documentation?"
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process evaluation requests
        
        Args:
            input_data: Dictionary containing:
                - item_to_evaluate: The item/content to evaluate
                - evaluation_type: Type of evaluation (project_deliverable, code_quality, etc.)
                - criteria: Specific evaluation criteria
                - scoring_scale: Scoring scale to use (1-10, 1-5, etc.)
                - context: Additional context for evaluation
        """
        item_to_evaluate = input_data.get('item_to_evaluate', '')
        evaluation_type = input_data.get('evaluation_type', 'project_deliverable')
        criteria = input_data.get('criteria', self.evaluation_criteria.get(evaluation_type, {}))
        scoring_scale = input_data.get('scoring_scale', '1-10')
        context = input_data.get('context', '')
        
        system_prompt = """You are a senior quality assurance specialist and evaluation expert with extensive experience in:

- Comprehensive quality assessment across multiple domains
- Objective scoring and measurement systems
- Constructive feedback and improvement recommendations
- Industry standards and best practices evaluation
- Risk assessment and compliance checking
- Performance and usability evaluation

Your evaluation approach should be:
- Objective and evidence-based
- Constructive with actionable feedback
- Comprehensive covering all relevant aspects
- Balanced highlighting both strengths and weaknesses
- Professional with clear scoring rationale
- Forward-looking with improvement recommendations

Always provide specific examples, quantitative scores, and concrete improvement suggestions."""
        
        criteria_text = "\n".join([f"- {criterion}: {description}" for criterion, description in criteria.items()])
        
        user_prompt = f"""
        EVALUATION REQUEST
        
        Item to Evaluate:
        {item_to_evaluate}
        
        Evaluation Type: {evaluation_type}
        Scoring Scale: {scoring_scale}
        Context: {context}
        
        Evaluation Criteria:
        {criteria_text}
        
        Please provide a comprehensive evaluation including:
        
        1. EXECUTIVE SUMMARY
           - Overall assessment and key findings
           - Primary strengths and weaknesses
           - Overall score with justification
        
        2. DETAILED EVALUATION
           For each criterion, provide:
           - Score ({scoring_scale})
           - Detailed assessment
           - Supporting evidence/examples
           - Specific observations
        
        3. STRENGTHS ANALYSIS
           - Key strengths identified
           - What works well and why
           - Best practices observed
           - Positive differentiators
        
        4. AREAS FOR IMPROVEMENT
           - Specific weaknesses identified
           - Impact assessment of each issue
           - Priority ranking of improvements
           - Root cause analysis where applicable
        
        5. RECOMMENDATIONS
           - Specific actionable recommendations
           - Implementation priority and effort
           - Expected impact of improvements
           - Success metrics for tracking progress
        
        6. RISK ASSESSMENT
           - Identified risks and concerns
           - Potential impact if not addressed
           - Mitigation strategies
        
        7. COMPLIANCE & STANDARDS
           - Adherence to relevant standards
           - Regulatory compliance status
           - Industry best practices alignment
        
        8. NEXT STEPS
           - Immediate actions required
           - Short-term improvements (1-4 weeks)
           - Long-term enhancements (1-6 months)
           - Follow-up evaluation schedule
        
        Provide quantitative scores for each criterion and an overall weighted score.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        # Extract scores from response for metadata
        scores = self._extract_scores(response_content, criteria.keys(), scoring_scale)
        overall_score = self._calculate_overall_score(scores)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "EvaluationAgent",
                "evaluation_type": evaluation_type,
                "scoring_scale": scoring_scale,
                "criteria_evaluated": list(criteria.keys()),
                "individual_scores": scores,
                "overall_score": overall_score,
                "recommendation_priority": self._assess_priority(response_content),
                "compliance_status": self._assess_compliance(response_content)
            },
            confidence_score=confidence_score,
            reasoning=f"Conducted comprehensive {evaluation_type} evaluation using {len(criteria)} criteria with {scoring_scale} scoring scale"
        )
    
    def evaluate_project_deliverable(self, deliverable_content: str, context: str = "") -> AgentResponse:
        """Evaluate a project deliverable"""
        return self.process({
            'item_to_evaluate': deliverable_content,
            'evaluation_type': 'project_deliverable',
            'context': context,
            'scoring_scale': '1-10'
        })
    
    def evaluate_code_quality(self, code_content: str, language: str = "") -> AgentResponse:
        """Evaluate code quality"""
        return self.process({
            'item_to_evaluate': code_content,
            'evaluation_type': 'code_quality',
            'context': f"Programming language: {language}",
            'scoring_scale': '1-10'
        })
    
    def evaluate_documentation(self, documentation_content: str, doc_type: str = "") -> AgentResponse:
        """Evaluate documentation quality"""
        return self.process({
            'item_to_evaluate': documentation_content,
            'evaluation_type': 'documentation',
            'context': f"Documentation type: {doc_type}",
            'scoring_scale': '1-10'
        })
    
    def custom_evaluation(self, content: str, criteria: Dict[str, str], scoring_scale: str = "1-10") -> AgentResponse:
        """Perform custom evaluation with specific criteria"""
        return self.process({
            'item_to_evaluate': content,
            'evaluation_type': 'custom',
            'criteria': criteria,
            'scoring_scale': scoring_scale
        })
    
    def _extract_scores(self, response_content: str, criteria: List[str], scoring_scale: str) -> Dict[str, float]:
        """Extract individual scores from evaluation response"""
        scores = {}
        max_score = int(scoring_scale.split('-')[1]) if '-' in scoring_scale else 10
        
        # Simple heuristic to extract scores - in production, this would be more sophisticated
        for criterion in criteria:
            # Look for patterns like "criterion: 8/10" or "criterion: 8"
            import re
            pattern = rf"{criterion}.*?(\d+)(?:/\d+)?"
            match = re.search(pattern, response_content, re.IGNORECASE)
            if match:
                scores[criterion] = min(float(match.group(1)), max_score)
            else:
                # Default score if not found
                scores[criterion] = max_score * 0.7  # 70% as default
        
        return scores
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        if not scores:
            return 0.0
        
        # Equal weighting for all criteria
        return sum(scores.values()) / len(scores)
    
    def _assess_priority(self, response_content: str) -> str:
        """Assess improvement priority based on response content"""
        high_priority_indicators = ['critical', 'urgent', 'immediate', 'severe', 'major']
        medium_priority_indicators = ['important', 'moderate', 'significant']
        
        content_lower = response_content.lower()
        high_count = sum(1 for indicator in high_priority_indicators if indicator in content_lower)
        medium_count = sum(1 for indicator in medium_priority_indicators if indicator in content_lower)
        
        if high_count > 2:
            return 'High'
        elif medium_count > 1 or high_count > 0:
            return 'Medium'
        else:
            return 'Low'
    
    def _assess_compliance(self, response_content: str) -> str:
        """Assess compliance status from response"""
        compliance_indicators = ['compliant', 'meets standards', 'follows guidelines']
        non_compliance_indicators = ['non-compliant', 'violates', 'fails to meet']
        
        content_lower = response_content.lower()
        compliant_count = sum(1 for indicator in compliance_indicators if indicator in content_lower)
        non_compliant_count = sum(1 for indicator in non_compliance_indicators if indicator in content_lower)
        
        if non_compliant_count > 0:
            return 'Non-Compliant'
        elif compliant_count > 0:
            return 'Compliant'
        else:
            return 'Partial'
    
    def get_evaluation_criteria(self, evaluation_type: str) -> Dict[str, str]:
        """Get evaluation criteria for a specific type"""
        return self.evaluation_criteria.get(evaluation_type, {})
    
    def add_custom_criteria(self, evaluation_type: str, criteria: Dict[str, str]):
        """Add custom evaluation criteria"""
        if evaluation_type not in self.evaluation_criteria:
            self.evaluation_criteria[evaluation_type] = {}
        self.evaluation_criteria[evaluation_type].update(criteria)
