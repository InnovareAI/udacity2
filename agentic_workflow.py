
"""
Enhanced AI-Powered Agentic Workflow for Project Management
Phase 2: Complete Workflow Implementation with Support Functions

This script orchestrates multiple AI agents to handle comprehensive project management tasks
with proper routing, evaluation, and structured output generation.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import logging
from workflow_agents import (
    ProjectManagerAgent,
    AugmentedPromptAgent,
    KnowledgeAugmentedPromptAgent,
    RAGKnowledgePromptAgent,
    EvaluationAgent,
    RoutingAgent,
    ActionPlanningAgent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkflowSupportFunctions:
    """Support functions for routed tasks and workflow management"""
    
    @staticmethod
    def validate_input(input_data: Dict[str, Any], required_fields: List[str]) -> Tuple[bool, List[str]]:
        """Validate input data for required fields"""
        missing_fields = [field for field in required_fields if field not in input_data or not input_data[field]]
        return len(missing_fields) == 0, missing_fields
    
    @staticmethod
    def calculate_workflow_confidence(step_confidences: List[float]) -> float:
        """Calculate overall workflow confidence from individual step confidences"""
        if not step_confidences:
            return 0.0
        
        # Weighted average with higher weight for later steps
        weights = [i + 1 for i in range(len(step_confidences))]
        weighted_sum = sum(conf * weight for conf, weight in zip(step_confidences, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    @staticmethod
    def merge_agent_metadata(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge metadata from multiple agents"""
        merged = {
            "agents_used": [],
            "total_processing_steps": len(metadata_list),
            "confidence_scores": [],
            "processing_summary": {}
        }
        
        for metadata in metadata_list:
            if "agent_type" in metadata:
                merged["agents_used"].append(metadata["agent_type"])
            if "confidence_score" in metadata:
                merged["confidence_scores"].append(metadata["confidence_score"])
            
            # Merge specific metadata
            for key, value in metadata.items():
                if key not in ["agent_type", "confidence_score"]:
                    merged["processing_summary"][f"{metadata.get('agent_type', 'unknown')}_{key}"] = value
        
        return merged
    
    @staticmethod
    def format_structured_output(workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format workflow results into structured output"""
        return {
            "workflow_execution": {
                "id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "type": workflow_results.get("workflow_type", "unknown"),
                "status": "completed" if workflow_results.get("success", False) else "failed",
                "duration_info": "Real-time execution",
                "overall_confidence": workflow_results.get("overall_confidence", 0.0)
            },
            "request_analysis": {
                "original_request": workflow_results.get("request", ""),
                "processed_context": workflow_results.get("context", {}),
                "routing_decision": workflow_results.get("routing_analysis", {}),
                "complexity_assessment": workflow_results.get("complexity", "medium")
            },
            "agent_coordination": {
                "agents_involved": workflow_results.get("agents_used", []),
                "processing_steps": len(workflow_results.get("steps", [])),
                "coordination_pattern": workflow_results.get("coordination_pattern", "sequential"),
                "handoff_points": workflow_results.get("handoff_points", [])
            },
            "deliverables": {
                "primary_output": workflow_results.get("primary_output", ""),
                "supporting_analysis": workflow_results.get("supporting_analysis", []),
                "recommendations": workflow_results.get("recommendations", []),
                "next_steps": workflow_results.get("next_steps", [])
            },
            "quality_metrics": {
                "overall_score": workflow_results.get("quality_score", 0.0),
                "confidence_distribution": workflow_results.get("confidence_scores", []),
                "validation_results": workflow_results.get("validation_results", {}),
                "improvement_suggestions": workflow_results.get("improvement_suggestions", [])
            },
            "metadata": {
                "processing_metadata": workflow_results.get("processing_metadata", {}),
                "performance_metrics": workflow_results.get("performance_metrics", {}),
                "system_info": {
                    "version": "2.0",
                    "capabilities": "Enhanced multi-agent workflow with evaluation"
                }
            }
        }

class EvaluationAgentOrchestrator:
    """Orchestrates evaluation agents for different specialized roles"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.evaluation_agent = EvaluationAgent(api_key)
        
        # Specialized evaluation configurations
        self.evaluation_configs = {
            "project_management": {
                "criteria": {
                    "planning_quality": "How well structured and comprehensive is the planning?",
                    "resource_allocation": "How effectively are resources allocated?",
                    "risk_management": "How well are risks identified and mitigated?",
                    "stakeholder_engagement": "How well are stakeholders considered?",
                    "timeline_feasibility": "How realistic and achievable are the timelines?"
                },
                "scoring_scale": "1-10",
                "weight_factors": {"planning_quality": 0.25, "resource_allocation": 0.2, "risk_management": 0.2, "stakeholder_engagement": 0.15, "timeline_feasibility": 0.2}
            },
            "technical_solution": {
                "criteria": {
                    "technical_feasibility": "How technically feasible is the solution?",
                    "scalability": "How well will the solution scale?",
                    "maintainability": "How maintainable is the proposed solution?",
                    "security": "How secure is the solution design?",
                    "performance": "How well will the solution perform?"
                },
                "scoring_scale": "1-10",
                "weight_factors": {"technical_feasibility": 0.3, "scalability": 0.2, "maintainability": 0.2, "security": 0.15, "performance": 0.15}
            },
            "action_plan": {
                "criteria": {
                    "completeness": "How complete and comprehensive is the action plan?",
                    "clarity": "How clear and understandable are the action items?",
                    "sequencing": "How well are actions sequenced and prioritized?",
                    "resource_requirements": "How well defined are resource requirements?",
                    "success_metrics": "How well defined are success criteria?"
                },
                "scoring_scale": "1-10",
                "weight_factors": {"completeness": 0.25, "clarity": 0.2, "sequencing": 0.2, "resource_requirements": 0.15, "success_metrics": 0.2}
            }
        }
    
    def evaluate_project_management_output(self, content: str, context: str = "") -> Dict[str, Any]:
        """Evaluate project management specific output"""
        config = self.evaluation_configs["project_management"]
        response = self.evaluation_agent.custom_evaluation(content, config["criteria"], config["scoring_scale"])
        
        return {
            "evaluation_type": "project_management",
            "response": response,
            "specialized_metrics": self._calculate_weighted_score(response.metadata.get("individual_scores", {}), config["weight_factors"]),
            "context": context
        }
    
    def evaluate_technical_solution(self, content: str, context: str = "") -> Dict[str, Any]:
        """Evaluate technical solution output"""
        config = self.evaluation_configs["technical_solution"]
        response = self.evaluation_agent.custom_evaluation(content, config["criteria"], config["scoring_scale"])
        
        return {
            "evaluation_type": "technical_solution",
            "response": response,
            "specialized_metrics": self._calculate_weighted_score(response.metadata.get("individual_scores", {}), config["weight_factors"]),
            "context": context
        }
    
    def evaluate_action_plan(self, content: str, context: str = "") -> Dict[str, Any]:
        """Evaluate action plan output"""
        config = self.evaluation_configs["action_plan"]
        response = self.evaluation_agent.custom_evaluation(content, config["criteria"], config["scoring_scale"])
        
        return {
            "evaluation_type": "action_plan",
            "response": response,
            "specialized_metrics": self._calculate_weighted_score(response.metadata.get("individual_scores", {}), config["weight_factors"]),
            "context": context
        }
    
    def _calculate_weighted_score(self, scores: Dict[str, float], weights: Dict[str, float]) -> Dict[str, Any]:
        """Calculate weighted score based on criteria weights"""
        if not scores or not weights:
            return {"weighted_score": 0.0, "breakdown": {}}
        
        weighted_sum = 0.0
        total_weight = 0.0
        breakdown = {}
        
        for criterion, weight in weights.items():
            if criterion in scores:
                weighted_contribution = scores[criterion] * weight
                weighted_sum += weighted_contribution
                total_weight += weight
                breakdown[criterion] = {
                    "score": scores[criterion],
                    "weight": weight,
                    "contribution": weighted_contribution
                }
        
        weighted_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return {
            "weighted_score": weighted_score,
            "breakdown": breakdown,
            "total_weight": total_weight
        }

class AgenticProjectManagementWorkflow:
    """
    Enhanced main workflow orchestrator that coordinates multiple AI agents
    with comprehensive support functions and evaluation capabilities.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the enhanced workflow with all required agents and support systems"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize all agents
        self.project_manager = ProjectManagerAgent(self.api_key)
        self.augmented_prompt = AugmentedPromptAgent(self.api_key)
        self.knowledge_augmented = KnowledgeAugmentedPromptAgent(self.api_key)
        self.rag_knowledge = RAGKnowledgePromptAgent(self.api_key)
        self.evaluation = EvaluationAgent(self.api_key)
        self.routing = RoutingAgent(self.api_key)
        self.action_planning = ActionPlanningAgent(self.api_key)
        
        # Initialize support systems
        self.support_functions = WorkflowSupportFunctions()
        self.evaluation_orchestrator = EvaluationAgentOrchestrator(self.api_key)
        
        # Workflow state and configuration
        self.workflow_history = []
        self.current_project = None
        self.workflow_config = {
            "enable_evaluation": True,
            "enable_routing": True,
            "enable_knowledge_augmentation": True,
            "output_format": "structured_json",
            "quality_threshold": 0.7
        }
        
        logger.info("AgenticProjectManagementWorkflow initialized with enhanced capabilities")
    
    def process_project_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Enhanced main entry point for processing project management requests.
        Uses comprehensive routing, evaluation, and support functions.
        """
        logger.info(f"Processing project request: {request[:100]}...")
        
        # Validate input
        is_valid, missing_fields = self.support_functions.validate_input(
            {"request": request}, ["request"]
        )
        if not is_valid:
            return self._create_error_response(f"Missing required fields: {missing_fields}")
        
        context = context or {}
        workflow_start_time = datetime.now()
        
        try:
            # Step 1: Enhanced routing with comprehensive analysis
            routing_response = self._perform_enhanced_routing(request, context)
            
            # Step 2: Execute workflow based on routing decision
            workflow_results = self._execute_routed_workflow(request, context, routing_response)
            
            # Step 3: Comprehensive evaluation of results
            if self.workflow_config["enable_evaluation"]:
                evaluation_results = self._perform_comprehensive_evaluation(workflow_results)
                workflow_results["evaluation_results"] = evaluation_results
            
            # Step 4: Generate structured output
            structured_output = self._generate_final_structured_output(workflow_results, workflow_start_time)
            
            # Step 5: Log and store workflow execution
            self._log_workflow_execution(structured_output)
            
            return structured_output
            
        except Exception as e:
            logger.error(f"Workflow execution error: {str(e)}")
            return self._create_error_response(f"Workflow execution failed: {str(e)}")
    
    def _perform_enhanced_routing(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform enhanced routing with comprehensive analysis"""
        logger.info("Performing enhanced routing analysis")
        
        routing_response = self.routing.route_task(
            request, 
            json.dumps(context),
            context.get("priority", "medium")
        )
        
        routing_analysis = {
            "primary_agent": routing_response.metadata["primary_agent"],
            "confidence": routing_response.metadata["routing_confidence"],
            "alternatives": routing_response.metadata["alternative_agents"],
            "task_analysis": routing_response.metadata["task_analysis"],
            "workflow_recommendations": routing_response.metadata.get("workflow_recommendations", {}),
            "routing_reasoning": routing_response.reasoning
        }
        
        logger.info(f"Routing decision: {routing_analysis['primary_agent']} (confidence: {routing_analysis['confidence']:.2f})")
        return routing_analysis
    
    def _execute_routed_workflow(self, request: str, context: Dict[str, Any], routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow based on routing decision"""
        primary_agent = routing_analysis["primary_agent"]
        task_analysis = routing_analysis["task_analysis"]
        
        logger.info(f"Executing {primary_agent} workflow")
        
        # Determine workflow pattern based on complexity and multi-agent requirements
        if task_analysis.get("multi_agent_required", False) or routing_analysis["confidence"] < 0.8:
            return self._execute_comprehensive_multi_agent_workflow(request, context, routing_analysis)
        elif primary_agent == 'ProjectManagerAgent':
            return self._execute_enhanced_project_management_workflow(request, context, routing_analysis)
        elif primary_agent == 'ActionPlanningAgent':
            return self._execute_enhanced_action_planning_workflow(request, context, routing_analysis)
        elif primary_agent == 'EvaluationAgent':
            return self._execute_enhanced_evaluation_workflow(request, context, routing_analysis)
        else:
            return self._execute_comprehensive_multi_agent_workflow(request, context, routing_analysis)
    
    def _execute_enhanced_project_management_workflow(self, request: str, context: Dict[str, Any], routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enhanced project management focused workflow"""
        logger.info("Executing enhanced project management workflow")
        
        results = {
            'workflow_type': 'enhanced_project_management',
            'timestamp': datetime.now().isoformat(),
            'request': request,
            'context': context,
            'routing_analysis': routing_analysis,
            'steps': [],
            'agents_used': [],
            'confidence_scores': []
        }
        
        # Step 1: Knowledge-enhanced prompt preparation
        if self.workflow_config["enable_knowledge_augmentation"]:
            knowledge_enhanced = self.knowledge_augmented.add_project_management_knowledge(request)
            enhanced_request = knowledge_enhanced.content
            results['steps'].append(self._create_step_record('knowledge_enhancement', 'KnowledgeAugmentedPromptAgent', knowledge_enhanced))
            results['agents_used'].append('KnowledgeAugmentedPromptAgent')
            results['confidence_scores'].append(knowledge_enhanced.confidence_score)
        else:
            enhanced_request = request
        
        # Step 2: RAG knowledge retrieval for additional context
        rag_enhanced = self.rag_knowledge.enhance_with_project_knowledge(enhanced_request)
        results['steps'].append(self._create_step_record('rag_knowledge_retrieval', 'RAGKnowledgePromptAgent', rag_enhanced))
        results['agents_used'].append('RAGKnowledgePromptAgent')
        results['confidence_scores'].append(rag_enhanced.confidence_score)
        
        # Step 3: Comprehensive project management analysis
        pm_response = self.project_manager.process({
            'task_type': 'comprehensive_planning',
            'project_details': rag_enhanced.content,
            'requirements': json.dumps(context),
            'timeline': context.get('timeline', 'flexible'),
            'resources': context.get('resources', 'to_be_determined')
        })
        results['steps'].append(self._create_step_record('project_management_analysis', 'ProjectManagerAgent', pm_response))
        results['agents_used'].append('ProjectManagerAgent')
        results['confidence_scores'].append(pm_response.confidence_score)
        
        # Step 4: Detailed action plan creation
        action_plan = self.action_planning.create_project_plan(
            pm_response.content,
            context.get('project_type', 'project_management'),
            context
        )
        results['steps'].append(self._create_step_record('action_planning', 'ActionPlanningAgent', action_plan))
        results['agents_used'].append('ActionPlanningAgent')
        results['confidence_scores'].append(action_plan.confidence_score)
        
        # Calculate overall confidence and prepare results
        results['overall_confidence'] = self.support_functions.calculate_workflow_confidence(results['confidence_scores'])
        results['primary_output'] = pm_response.content
        results['supporting_analysis'] = [step['output'] for step in results['steps']]
        results['success'] = True
        
        return results
    
    def _execute_enhanced_action_planning_workflow(self, request: str, context: Dict[str, Any], routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enhanced action planning focused workflow"""
        logger.info("Executing enhanced action planning workflow")
        
        results = {
            'workflow_type': 'enhanced_action_planning',
            'timestamp': datetime.now().isoformat(),
            'request': request,
            'context': context,
            'routing_analysis': routing_analysis,
            'steps': [],
            'agents_used': [],
            'confidence_scores': []
        }
        
        # Step 1: Prompt enhancement for better planning
        enhanced_prompt = self.augmented_prompt.enhance_for_project_management(request)
        results['steps'].append(self._create_step_record('prompt_enhancement', 'AugmentedPromptAgent', enhanced_prompt))
        results['agents_used'].append('AugmentedPromptAgent')
        results['confidence_scores'].append(enhanced_prompt.confidence_score)
        
        # Step 2: Knowledge augmentation with planning expertise
        knowledge_enhanced = self.knowledge_augmented.add_project_management_knowledge(enhanced_prompt.content)
        results['steps'].append(self._create_step_record('knowledge_enhancement', 'KnowledgeAugmentedPromptAgent', knowledge_enhanced))
        results['agents_used'].append('KnowledgeAugmentedPromptAgent')
        results['confidence_scores'].append(knowledge_enhanced.confidence_score)
        
        # Step 3: Comprehensive action plan creation
        action_plan = self.action_planning.process({
            'goal': knowledge_enhanced.content,
            'project_type': context.get('project_type', 'general'),
            'timeline': context.get('timeline', 'flexible'),
            'resources': context.get('resources', 'to_be_determined'),
            'constraints': context.get('constraints', {}),
            'complexity': context.get('complexity', 'medium')
        })
        results['steps'].append(self._create_step_record('action_plan_creation', 'ActionPlanningAgent', action_plan))
        results['agents_used'].append('ActionPlanningAgent')
        results['confidence_scores'].append(action_plan.confidence_score)
        
        # Step 4: Project management validation and enhancement
        pm_validation = self.project_manager.process({
            'task_type': 'plan_validation',
            'project_details': action_plan.content,
            'requirements': 'Validate and enhance the action plan with project management best practices'
        })
        results['steps'].append(self._create_step_record('pm_validation', 'ProjectManagerAgent', pm_validation))
        results['agents_used'].append('ProjectManagerAgent')
        results['confidence_scores'].append(pm_validation.confidence_score)
        
        # Calculate results
        results['overall_confidence'] = self.support_functions.calculate_workflow_confidence(results['confidence_scores'])
        results['primary_output'] = action_plan.content
        results['supporting_analysis'] = [pm_validation.content]
        results['success'] = True
        
        return results
    
    def _execute_enhanced_evaluation_workflow(self, request: str, context: Dict[str, Any], routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enhanced evaluation focused workflow"""
        logger.info("Executing enhanced evaluation workflow")
        
        results = {
            'workflow_type': 'enhanced_evaluation',
            'timestamp': datetime.now().isoformat(),
            'request': request,
            'context': context,
            'routing_analysis': routing_analysis,
            'steps': [],
            'agents_used': [],
            'confidence_scores': []
        }
        
        # Step 1: Enhanced evaluation prompt creation
        evaluation_criteria = context.get('evaluation_criteria', [
            'completeness', 'quality', 'feasibility', 'clarity', 'usability'
        ])
        enhanced_eval_prompt = self.augmented_prompt.create_evaluation_prompt(
            evaluation_criteria, 
            context.get('scoring_scale', '1-10')
        )
        results['steps'].append(self._create_step_record('evaluation_prompt_enhancement', 'AugmentedPromptAgent', enhanced_eval_prompt))
        results['agents_used'].append('AugmentedPromptAgent')
        results['confidence_scores'].append(enhanced_eval_prompt.confidence_score)
        
        # Step 2: Comprehensive evaluation
        evaluation_type = context.get('evaluation_type', 'project_deliverable')
        evaluation_response = self.evaluation.process({
            'item_to_evaluate': request,
            'evaluation_type': evaluation_type,
            'scoring_scale': context.get('scoring_scale', '1-10'),
            'context': json.dumps(context)
        })
        results['steps'].append(self._create_step_record('comprehensive_evaluation', 'EvaluationAgent', evaluation_response))
        results['agents_used'].append('EvaluationAgent')
        results['confidence_scores'].append(evaluation_response.confidence_score)
        
        # Step 3: Improvement action plan based on evaluation
        improvement_plan = self.action_planning.break_down_task(
            f"Address evaluation findings and improve based on: {evaluation_response.content}",
            f"Evaluation context: {json.dumps(context)}"
        )
        results['steps'].append(self._create_step_record('improvement_planning', 'ActionPlanningAgent', improvement_plan))
        results['agents_used'].append('ActionPlanningAgent')
        results['confidence_scores'].append(improvement_plan.confidence_score)
        
        # Calculate results
        results['overall_confidence'] = self.support_functions.calculate_workflow_confidence(results['confidence_scores'])
        results['primary_output'] = evaluation_response.content
        results['supporting_analysis'] = [improvement_plan.content]
        results['quality_score'] = evaluation_response.metadata.get('overall_score', 0.0)
        results['success'] = True
        
        return results
    
    def _execute_comprehensive_multi_agent_workflow(self, request: str, context: Dict[str, Any], routing_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute comprehensive multi-agent workflow for complex tasks"""
        logger.info("Executing comprehensive multi-agent workflow")
        
        results = {
            'workflow_type': 'comprehensive_multi_agent',
            'timestamp': datetime.now().isoformat(),
            'request': request,
            'context': context,
            'routing_analysis': routing_analysis,
            'steps': [],
            'agents_used': [],
            'confidence_scores': [],
            'coordination_pattern': 'orchestrated'
        }
        
        # Step 1: Prompt enhancement and structure optimization
        enhanced_prompt = self.augmented_prompt.enhance_for_project_management(request)
        results['steps'].append(self._create_step_record('prompt_enhancement', 'AugmentedPromptAgent', enhanced_prompt))
        results['agents_used'].append('AugmentedPromptAgent')
        results['confidence_scores'].append(enhanced_prompt.confidence_score)
        
        # Step 2: Domain knowledge integration
        knowledge_enhanced = self.knowledge_augmented.add_project_management_knowledge(enhanced_prompt.content)
        results['steps'].append(self._create_step_record('knowledge_enhancement', 'KnowledgeAugmentedPromptAgent', knowledge_enhanced))
        results['agents_used'].append('KnowledgeAugmentedPromptAgent')
        results['confidence_scores'].append(knowledge_enhanced.confidence_score)
        
        # Step 3: RAG knowledge retrieval
        rag_enhanced = self.rag_knowledge.enhance_with_project_knowledge(knowledge_enhanced.content)
        results['steps'].append(self._create_step_record('rag_knowledge_retrieval', 'RAGKnowledgePromptAgent', rag_enhanced))
        results['agents_used'].append('RAGKnowledgePromptAgent')
        results['confidence_scores'].append(rag_enhanced.confidence_score)
        
        # Step 4: Project management analysis
        pm_response = self.project_manager.process({
            'task_type': 'comprehensive_analysis',
            'project_details': rag_enhanced.content,
            'requirements': json.dumps(context),
            'timeline': context.get('timeline', 'flexible')
        })
        results['steps'].append(self._create_step_record('project_management_analysis', 'ProjectManagerAgent', pm_response))
        results['agents_used'].append('ProjectManagerAgent')
        results['confidence_scores'].append(pm_response.confidence_score)
        
        # Step 5: Detailed action planning
        action_plan = self.action_planning.create_project_plan(pm_response.content, context.get('project_type', 'general'), context)
        results['steps'].append(self._create_step_record('action_planning', 'ActionPlanningAgent', action_plan))
        results['agents_used'].append('ActionPlanningAgent')
        results['confidence_scores'].append(action_plan.confidence_score)
        
        # Step 6: Comprehensive evaluation
        combined_output = f"Project Analysis: {pm_response.content}\n\nAction Plan: {action_plan.content}"
        evaluation = self.evaluation.evaluate_project_deliverable(combined_output)
        results['steps'].append(self._create_step_record('quality_evaluation', 'EvaluationAgent', evaluation))
        results['agents_used'].append('EvaluationAgent')
        results['confidence_scores'].append(evaluation.confidence_score)
        
        # Calculate comprehensive results
        results['overall_confidence'] = self.support_functions.calculate_workflow_confidence(results['confidence_scores'])
        results['primary_output'] = pm_response.content
        results['supporting_analysis'] = [action_plan.content, evaluation.content]
        results['quality_score'] = evaluation.metadata.get('overall_score', 0.0)
        results['recommendations'] = self._extract_recommendations(results['steps'])
        results['next_steps'] = self._extract_next_steps(results['steps'])
        results['success'] = True
        
        return results
    
    def _perform_comprehensive_evaluation(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive evaluation of workflow results"""
        logger.info("Performing comprehensive workflow evaluation")
        
        evaluation_results = {
            "workflow_evaluation": {},
            "output_evaluation": {},
            "specialized_evaluations": []
        }
        
        # Evaluate overall workflow performance
        workflow_summary = f"""
        Workflow Type: {workflow_results['workflow_type']}
        Agents Used: {', '.join(workflow_results.get('agents_used', []))}
        Steps Completed: {len(workflow_results.get('steps', []))}
        Overall Confidence: {workflow_results.get('overall_confidence', 0.0)}
        Primary Output Length: {len(workflow_results.get('primary_output', ''))}
        """
        
        workflow_eval = self.evaluation.evaluate_project_deliverable(workflow_summary, "Workflow execution assessment")
        evaluation_results["workflow_evaluation"] = {
            "response": workflow_eval,
            "score": workflow_eval.metadata.get('overall_score', 0.0)
        }
        
        # Evaluate primary output quality
        if workflow_results.get('primary_output'):
            output_eval = self.evaluation.evaluate_project_deliverable(
                workflow_results['primary_output'], 
                f"Primary output from {workflow_results['workflow_type']} workflow"
            )
            evaluation_results["output_evaluation"] = {
                "response": output_eval,
                "score": output_eval.metadata.get('overall_score', 0.0)
            }
        
        # Specialized evaluations based on workflow type
        if workflow_results['workflow_type'] in ['enhanced_project_management', 'comprehensive_multi_agent']:
            pm_eval = self.evaluation_orchestrator.evaluate_project_management_output(
                workflow_results.get('primary_output', ''),
                f"Project management output evaluation"
            )
            evaluation_results["specialized_evaluations"].append(pm_eval)
        
        if 'action_planning' in [step.get('step') for step in workflow_results.get('steps', [])]:
            action_plan_content = next((step['output'] for step in workflow_results.get('steps', []) if step.get('step') == 'action_planning'), '')
            if action_plan_content:
                ap_eval = self.evaluation_orchestrator.evaluate_action_plan(
                    action_plan_content,
                    "Action plan quality evaluation"
                )
                evaluation_results["specialized_evaluations"].append(ap_eval)
        
        return evaluation_results
    
    def _generate_final_structured_output(self, workflow_results: Dict[str, Any], start_time: datetime) -> Dict[str, Any]:
        """Generate final structured output for the workflow"""
        logger.info("Generating final structured output")
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare comprehensive structured output
        structured_output = self.support_functions.format_structured_output(workflow_results)
        
        # Add execution timing
        structured_output["workflow_execution"]["execution_time_seconds"] = execution_time
        structured_output["workflow_execution"]["performance_category"] = (
            "fast" if execution_time < 30 else "normal" if execution_time < 60 else "slow"
        )
        
        # Add comprehensive metadata
        structured_output["metadata"]["processing_metadata"] = self.support_functions.merge_agent_metadata(
            [step.get('metadata', {}) for step in workflow_results.get('steps', [])]
        )
        
        # Add quality assessment
        if workflow_results.get('evaluation_results'):
            structured_output["quality_metrics"]["evaluation_details"] = workflow_results['evaluation_results']
        
        # Add recommendations and next steps
        structured_output["deliverables"]["recommendations"] = workflow_results.get('recommendations', [])
        structured_output["deliverables"]["next_steps"] = workflow_results.get('next_steps', [])
        
        return structured_output
    
    def _create_step_record(self, step_name: str, agent_name: str, agent_response) -> Dict[str, Any]:
        """Create standardized step record"""
        return {
            'step': step_name,
            'agent': agent_name,
            'output': agent_response.content,
            'confidence': agent_response.confidence_score,
            'metadata': agent_response.metadata,
            'reasoning': agent_response.reasoning,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_recommendations(self, steps: List[Dict[str, Any]]) -> List[str]:
        """Extract recommendations from workflow steps"""
        recommendations = []
        for step in steps:
            content = step.get('output', '').lower()
            if 'recommend' in content or 'suggest' in content:
                # Simple extraction - in production, this would be more sophisticated
                lines = step.get('output', '').split('\n')
                for line in lines:
                    if any(word in line.lower() for word in ['recommend', 'suggest', 'should', 'consider']):
                        recommendations.append(line.strip())
        return recommendations[:5]  # Limit to top 5
    
    def _extract_next_steps(self, steps: List[Dict[str, Any]]) -> List[str]:
        """Extract next steps from workflow steps"""
        next_steps = []
        for step in steps:
            content = step.get('output', '').lower()
            if 'next step' in content or 'action' in content:
                lines = step.get('output', '').split('\n')
                for line in lines:
                    if any(word in line.lower() for word in ['next', 'action', 'implement', 'execute']):
                        next_steps.append(line.strip())
        return next_steps[:5]  # Limit to top 5
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "workflow_execution": {
                "id": f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error_message": error_message
            },
            "success": False
        }
    
    def _log_workflow_execution(self, structured_output: Dict[str, Any]):
        """Log workflow execution for monitoring and improvement"""
        execution_summary = {
            "workflow_id": structured_output["workflow_execution"]["id"],
            "type": structured_output["workflow_execution"]["type"],
            "status": structured_output["workflow_execution"]["status"],
            "confidence": structured_output["workflow_execution"]["overall_confidence"],
            "agents_used": structured_output["agent_coordination"]["agents_involved"],
            "execution_time": structured_output["workflow_execution"].get("execution_time_seconds", 0)
        }
        
        self.workflow_history.append(execution_summary)
        logger.info(f"Workflow execution logged: {execution_summary}")
    
    def handle_email_router_project(self) -> Dict[str, Any]:
        """
        Handle the specific Email Router project as mentioned in the requirements.
        This demonstrates the enhanced workflow with comprehensive capabilities.
        """
        logger.info("Processing Email Router Project for InnovateNext Solutions")
        
        email_router_request = """
        InnovateNext Solutions needs to implement an advanced Email Router system for their project management workflow.
        
        Project Requirements:
        - Automatically route incoming project-related emails to appropriate team members based on content analysis
        - Categorize emails by project type, priority, urgency, and department using AI classification
        - Integrate seamlessly with existing project management tools (Jira, Asana, Microsoft Project)
        - Provide comprehensive analytics and reporting on email routing patterns and efficiency
        - Ensure enterprise-level security and compliance with GDPR, SOX, and company data policies
        - Support high volume email processing (10,000+ emails/day) with real-time routing decisions
        - Include machine learning capabilities for continuous improvement of routing accuracy
        - Provide user-friendly dashboard for monitoring and manual override capabilities
        
        Technical Specifications:
        - Cloud-native architecture with microservices design
        - RESTful APIs for integration with existing systems
        - Real-time processing with sub-second response times
        - Scalable infrastructure supporting future growth
        - Comprehensive logging and monitoring capabilities
        
        Success Criteria:
        - 95%+ routing accuracy within 3 months of deployment
        - 50% reduction in manual email sorting time
        - Seamless integration with zero downtime
        - User satisfaction score of 4.5/5 or higher
        
        Timeline: 3 months for MVP, 6 months for full implementation with advanced features.
        Team: 5 senior developers, 2 project managers, 1 product manager, 1 DevOps engineer, 2 QA engineers.
        Budget: $500,000 for development and first year operations.
        """
        
        context = {
            'project_type': 'software_development',
            'complexity': 'high',
            'team_size': 11,
            'timeline': '6 months',
            'budget': '$500,000',
            'company': 'InnovateNext Solutions',
            'priority': 'high',
            'evaluation_criteria': ['technical_feasibility', 'scalability', 'security', 'user_experience', 'integration_complexity'],
            'constraints': {
                'compliance_requirements': ['GDPR', 'SOX'],
                'performance_requirements': ['10,000+ emails/day', 'sub-second response'],
                'integration_requirements': ['Jira', 'Asana', 'Microsoft Project']
            }
        }
        
        return self.process_project_request(email_router_request, context)
    
    def generate_workflow_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive report of the workflow execution"""
        if not results.get("workflow_execution"):
            return "Error: Invalid workflow results provided"
        
        workflow_exec = results["workflow_execution"]
        agent_coord = results.get("agent_coordination", {})
        deliverables = results.get("deliverables", {})
        quality_metrics = results.get("quality_metrics", {})
        
        report = f"""
# Enhanced AI-Powered Agentic Workflow Report
**Generated:** {workflow_exec.get('timestamp', 'Unknown')}
**Workflow ID:** {workflow_exec.get('id', 'Unknown')}
**Workflow Type:** {workflow_exec.get('type', 'Unknown')}
**Status:** {workflow_exec.get('status', 'Unknown')}
**Overall Confidence:** {workflow_exec.get('overall_confidence', 0.0):.2f}
**Execution Time:** {workflow_exec.get('execution_time_seconds', 0):.1f} seconds

## Request Analysis
**Original Request:** {results.get('request_analysis', {}).get('original_request', 'Not available')[:200]}...

**Complexity Assessment:** {results.get('request_analysis', {}).get('complexity_assessment', 'Unknown')}

## Agent Coordination Summary
**Agents Involved:** {', '.join(agent_coord.get('agents_involved', []))}
**Processing Steps:** {agent_coord.get('processing_steps', 0)}
**Coordination Pattern:** {agent_coord.get('coordination_pattern', 'Unknown')}

## Primary Deliverables
{deliverables.get('primary_output', 'No primary output available')[:1000]}...

## Quality Assessment
**Overall Quality Score:** {quality_metrics.get('overall_score', 0.0):.1f}/10
**Confidence Distribution:** {quality_metrics.get('confidence_distribution', [])}

## Key Recommendations
"""
        
        recommendations = deliverables.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations[:5], 1):
                report += f"{i}. {rec}\n"
        else:
            report += "No specific recommendations generated.\n"
        
        report += f"""
## Next Steps
"""
        
        next_steps = deliverables.get('next_steps', [])
        if next_steps:
            for i, step in enumerate(next_steps[:5], 1):
                report += f"{i}. {step}\n"
        else:
            report += "No specific next steps identified.\n"
        
        report += f"""
## Workflow Performance Metrics
- **Processing Efficiency:** {workflow_exec.get('performance_category', 'Unknown')}
- **Agent Utilization:** {len(agent_coord.get('agents_involved', []))} agents coordinated
- **Success Rate:** {'100%' if workflow_exec.get('status') == 'completed' else 'Failed'}

## System Information
- **Workflow Version:** {results.get('metadata', {}).get('system_info', {}).get('version', 'Unknown')}
- **Capabilities:** {results.get('metadata', {}).get('system_info', {}).get('capabilities', 'Unknown')}

---
*This report was generated by the Enhanced AI-Powered Agentic Workflow System*
"""
        
        return report

def convert_to_json_serializable(obj):
    """Convert AgentResponse objects and other non-serializable objects to JSON serializable format"""
    if hasattr(obj, '__dict__'):
        # Convert objects with __dict__ to dictionary
        return {key: convert_to_json_serializable(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        # For other types, convert to string representation
        return str(obj)

def main():
    """Main function to demonstrate the enhanced agentic workflow"""
    print("🤖 Initializing Enhanced AI-Powered Agentic Workflow for Project Management")
    print("=" * 80)
    
    # Initialize the enhanced workflow
    workflow = AgenticProjectManagementWorkflow()
    
    # Process the Email Router project with comprehensive capabilities
    print("📧 Processing Email Router Project with Enhanced Workflow...")
    results = workflow.handle_email_router_project()
    
    # Generate and display comprehensive report
    print("\n📊 Generating Comprehensive Workflow Report...")
    report = workflow.generate_workflow_report(results)
    
    # Save results in multiple formats
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save structured JSON output (convert AgentResponse objects to dicts)
    json_filename = f'enhanced_workflow_results_{timestamp}.json'
    json_serializable_results = convert_to_json_serializable(results)
    with open(json_filename, 'w') as f:
        json.dump(json_serializable_results, f, indent=2)
    
    # Save comprehensive report
    report_filename = f'enhanced_workflow_report_{timestamp}.md'
    with open(report_filename, 'w') as f:
        f.write(report)
    
    # Display summary
    print(f"\n✅ Enhanced Workflow completed successfully!")
    print(f"📊 Overall confidence: {results['workflow_execution']['overall_confidence']:.2f}")
    print(f"⏱️  Execution time: {results['workflow_execution'].get('execution_time_seconds', 0):.1f} seconds")
    print(f"🤖 Agents coordinated: {len(results['agent_coordination']['agents_involved'])}")
    print(f"📁 Structured results saved to: {json_filename}")
    print(f"📄 Comprehensive report saved to: {report_filename}")
    
    # Display quality metrics if available
    if results.get('quality_metrics', {}).get('overall_score'):
        print(f"🎯 Quality score: {results['quality_metrics']['overall_score']:.1f}/10")
    
    print("\n🎉 Enhanced Agentic Workflow demonstration completed!")
    return results

if __name__ == "__main__":
    main()
