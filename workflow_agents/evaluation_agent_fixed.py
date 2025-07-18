
"""
Fixed Evaluation Agent - Enhanced with iterative loop and max_interactions for correction instructions
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
import json

class EvaluationAgent(BaseAgent):
    """
    Enhanced evaluation agent with iterative correction capabilities:
    - Quality assessment and scoring with iterative refinement
    - Performance evaluation with correction loops
    - Deliverable review with improvement iterations
    - Compliance checking with correction instructions
    - Improvement recommendations with iterative feedback
    """
    
    def __init__(self, api_key: str = None, max_interactions: int = 3):
        super().__init__(api_key)
        self.max_interactions = max_interactions
        self.capabilities = [
            "quality_assessment", "performance_evaluation", "deliverable_review",
            "compliance_checking", "feedback_generation", "scoring_systems",
            "iterative_correction", "improvement_loops"
        ]
        self.specialties = [
            "project_deliverable_evaluation", "code_quality_assessment", 
            "documentation_review", "process_evaluation", "stakeholder_feedback",
            "iterative_improvement", "correction_instructions"
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
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process evaluation requests with iterative correction capability
        
        Args:
            input_data: Dictionary containing:
                - item_to_evaluate: The item/content to evaluate
                - evaluation_type: Type of evaluation
                - criteria: Specific evaluation criteria
                - scoring_scale: Scoring scale to use
                - context: Additional context for evaluation
                - enable_corrections: Whether to enable iterative corrections
                - correction_threshold: Minimum score to trigger corrections
        """
        item_to_evaluate = input_data.get('item_to_evaluate', '')
        evaluation_type = input_data.get('evaluation_type', 'project_deliverable')
        criteria = input_data.get('criteria', self.evaluation_criteria.get(evaluation_type, {}))
        scoring_scale = input_data.get('scoring_scale', '1-10')
        context = input_data.get('context', '')
        enable_corrections = input_data.get('enable_corrections', True)
        correction_threshold = input_data.get('correction_threshold', 7.0)
        
        # Initial evaluation
        evaluation_result = self._perform_evaluation(
            item_to_evaluate, evaluation_type, criteria, scoring_scale, context
        )
        
        # Iterative correction loop if enabled and score is below threshold
        correction_history = []
        current_item = item_to_evaluate
        interaction_count = 0
        
        if enable_corrections and evaluation_result.get('overall_score', 0) < correction_threshold:
            while interaction_count < self.max_interactions:
                interaction_count += 1
                
                # Generate correction instructions
                correction_instructions = self._generate_correction_instructions(
                    evaluation_result, current_item, criteria
                )
                
                # Apply corrections (simulated - in real implementation would integrate with other agents)
                corrected_item = self._apply_corrections(current_item, correction_instructions)
                
                # Re-evaluate
                new_evaluation = self._perform_evaluation(
                    corrected_item, evaluation_type, criteria, scoring_scale, context
                )
                
                correction_history.append({
                    "iteration": interaction_count,
                    "previous_score": evaluation_result.get('overall_score', 0),
                    "new_score": new_evaluation.get('overall_score', 0),
                    "corrections_applied": correction_instructions,
                    "improvement": new_evaluation.get('overall_score', 0) - evaluation_result.get('overall_score', 0)
                })
                
                # Update for next iteration
                evaluation_result = new_evaluation
                current_item = corrected_item
                
                # Break if score meets threshold
                if evaluation_result.get('overall_score', 0) >= correction_threshold:
                    break
        
        return AgentResponse(
            success=True,
            content=self._format_evaluation_response(evaluation_result, correction_history),
            metadata={
                "agent_type": "EvaluationAgent",
                "evaluation_type": evaluation_type,
                "overall_score": evaluation_result.get('overall_score', 0),
                "iterations_performed": interaction_count,
                "corrections_enabled": enable_corrections,
                "correction_history": correction_history,
                "final_item": current_item if interaction_count > 0 else item_to_evaluate
            },
            confidence_score=min(0.9, evaluation_result.get('overall_score', 0) / 10),
            reasoning=f"Evaluation completed with {interaction_count} correction iterations"
        )
    
    def _perform_evaluation(self, item: str, eval_type: str, criteria: Dict, scale: str, context: str) -> Dict[str, Any]:
        """Perform the actual evaluation"""
        system_prompt = """You are a senior quality assurance specialist and evaluation expert with extensive experience in comprehensive quality assessment. Your evaluation approach should be objective, evidence-based, and constructive with actionable feedback."""
        
        user_prompt = f"""
        EVALUATION REQUEST
        
        Item to Evaluate: {item}
        Evaluation Type: {eval_type}
        Context: {context}
        Scoring Scale: {scale}
        
        Evaluation Criteria:
        {json.dumps(criteria, indent=2)}
        
        Please provide a comprehensive evaluation including:
        1. Individual scores for each criterion
        2. Overall score calculation
        3. Strengths and weaknesses
        4. Specific improvement recommendations
        5. Risk assessment
        
        Format your response as JSON with the following structure:
        {{
            "individual_scores": {{"criterion": score}},
            "overall_score": numeric_score,
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "recommendations": ["rec1", "rec2"],
            "risk_assessment": "risk_level"
        }}
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        
        try:
            return json.loads(response_content)
        except:
            # Fallback if JSON parsing fails
            return {
                "individual_scores": {},
                "overall_score": 5.0,
                "strengths": ["Evaluation completed"],
                "weaknesses": ["JSON parsing failed"],
                "recommendations": ["Review evaluation format"],
                "risk_assessment": "medium"
            }
    
    def _generate_correction_instructions(self, evaluation: Dict, item: str, criteria: Dict) -> List[str]:
        """Generate specific correction instructions based on evaluation"""
        instructions = []
        
        # Generate instructions based on weaknesses
        for weakness in evaluation.get('weaknesses', []):
            instructions.append(f"Address weakness: {weakness}")
        
        # Generate instructions based on low-scoring criteria
        for criterion, score in evaluation.get('individual_scores', {}).items():
            if score < 6:  # Below acceptable threshold
                instructions.append(f"Improve {criterion}: {criteria.get(criterion, 'Focus on this area')}")
        
        # Add general recommendations
        for rec in evaluation.get('recommendations', []):
            instructions.append(f"Implement: {rec}")
        
        return instructions
    
    def _apply_corrections(self, item: str, instructions: List[str]) -> str:
        """Apply corrections to the item (simulated improvement)"""
        # In a real implementation, this would integrate with other agents
        # For now, we simulate improvement by appending correction notes
        corrections_text = "\n\nCORRECTIONS APPLIED:\n" + "\n".join(f"- {inst}" for inst in instructions)
        return item + corrections_text
    
    def _format_evaluation_response(self, evaluation: Dict, correction_history: List) -> str:
        """Format the evaluation response"""
        response = f"""
EVALUATION RESULTS

Overall Score: {evaluation.get('overall_score', 0)}/10

INDIVIDUAL SCORES:
{json.dumps(evaluation.get('individual_scores', {}), indent=2)}

STRENGTHS:
{chr(10).join(f"• {strength}" for strength in evaluation.get('strengths', []))}

WEAKNESSES:
{chr(10).join(f"• {weakness}" for weakness in evaluation.get('weaknesses', []))}

RECOMMENDATIONS:
{chr(10).join(f"• {rec}" for rec in evaluation.get('recommendations', []))}

RISK ASSESSMENT: {evaluation.get('risk_assessment', 'Not assessed')}
"""
        
        if correction_history:
            response += f"\n\nCORRECTION ITERATIONS: {len(correction_history)}\n"
            for correction in correction_history:
                response += f"Iteration {correction['iteration']}: {correction['previous_score']:.1f} → {correction['new_score']:.1f} (Δ{correction['improvement']:+.1f})\n"
        
        return response
    
    def evaluate_with_corrections(self, item: str, evaluation_type: str = "project_deliverable", 
                                max_iterations: int = None) -> AgentResponse:
        """Convenience method for evaluation with corrections"""
        if max_iterations:
            self.max_interactions = max_iterations
            
        return self.process({
            'item_to_evaluate': item,
            'evaluation_type': evaluation_type,
            'enable_corrections': True,
            'correction_threshold': 7.0
        })
