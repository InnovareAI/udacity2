
"""
Fixed Enhanced AI-Powered Agentic Workflow for Project Management
Complete implementation with proper step-wise routing pattern and completed_steps list
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
    ActionPlanningAgent,
    DirectPromptAgent
)
from support_functions import product_manager, program_manager, development_engineer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedAgenticWorkflow:
    """
    Enhanced agentic workflow with proper step-wise routing pattern and completed_steps tracking
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', 'dummy-key')
        
        # Initialize agents with specialized parameters
        self.agents = {
            'ProjectManagerAgent': ProjectManagerAgent(self.api_key),
            'AugmentedPromptAgent': AugmentedPromptAgent(self.api_key),
            'KnowledgeAugmentedPromptAgent': KnowledgeAugmentedPromptAgent(self.api_key),
            'RAGKnowledgePromptAgent': RAGKnowledgePromptAgent(self.api_key),
            'EvaluationAgent': EvaluationAgent(self.api_key, max_interactions=3),
            'ActionPlanningAgent': ActionPlanningAgent(self.api_key, knowledge_action_planning={
                "planning_methodologies": ["Agile", "Waterfall", "Hybrid"],
                "best_practices": ["SMART goals", "Risk assessment", "Stakeholder analysis"]
            }),
            'DirectPromptAgent': DirectPromptAgent(self.api_key)
        }
        
        # Initialize routing agent with agents reference
        self.routing_agent = RoutingAgent(self.api_key, agents=self.agents)
        self.agents['RoutingAgent'] = self.routing_agent
        
        # Support functions
        self.support_functions = {
            'product_manager': product_manager,
            'program_manager': program_manager,
            'development_engineer': development_engineer
        }
        
        # Workflow state tracking
        self.completed_steps = []
        self.workflow_state = {
            "current_step": 0,
            "total_steps": 0,
            "step_results": [],
            "overall_confidence": 0.0
        }
    
    def execute_workflow(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute complete workflow with step-wise routing pattern
        """
        context = context or {}
        self.completed_steps = []  # Reset for new workflow
        
        logger.info(f"Starting enhanced workflow execution for request: {request[:100]}...")
        
        try:
            # Step 1: Initial routing analysis
            routing_result = self._execute_step("routing_analysis", {
                'task_description': request,
                'context': json.dumps(context),
                'priority': context.get('priority', 'medium')
            })
            
            # Step 2: Primary agent processing
            primary_agent = routing_result.metadata.get('primary_agent', 'DirectPromptAgent')
            primary_result = self._execute_step("primary_processing", {
                'agent': primary_agent,
                'request': request,
                'context': context,
                'routing_guidance': routing_result.content
            })
            
            # Step 3: Quality evaluation with corrections
            evaluation_result = self._execute_step("quality_evaluation", {
                'item_to_evaluate': primary_result.content,
                'evaluation_type': 'project_deliverable',
                'enable_corrections': True,
                'correction_threshold': 7.0
            })
            
            # Step 4: Support function integration (if needed)
            support_result = self._execute_step("support_integration", {
                'primary_output': primary_result.content,
                'evaluation_feedback': evaluation_result.content,
                'request_type': self._classify_request_type(request)
            })
            
            # Step 5: Final structured output generation
            final_result = self._execute_step("output_structuring", {
                'workflow_results': {
                    'request': request,
                    'context': context,
                    'routing_analysis': routing_result.metadata,
                    'primary_output': primary_result.content,
                    'evaluation_results': evaluation_result.metadata,
                    'support_analysis': support_result,
                    'agents_used': [step['agent_used'] for step in self.completed_steps],
                    'steps': self.completed_steps,
                    'overall_confidence': self._calculate_overall_confidence(),
                    'success': True
                }
            })
            
            return self._format_final_output(final_result, request, context)
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return self._handle_workflow_error(e, request, context)
    
    def _execute_step(self, step_name: str, step_data: Dict[str, Any]) -> Any:
        """
        Execute a single workflow step with proper tracking
        """
        step_start_time = datetime.now()
        logger.info(f"Executing step: {step_name}")
        
        try:
            if step_name == "routing_analysis":
                result = self.routing_agent.process(step_data)
                agent_used = "RoutingAgent"
                
            elif step_name == "primary_processing":
                agent_name = step_data['agent']
                agent = self.agents.get(agent_name, self.agents['DirectPromptAgent'])
                
                if agent_name == 'ActionPlanningAgent':
                    result = agent.process({
                        'goal': step_data['request'],
                        'user_prompt': step_data['request'],
                        'context': step_data.get('context', {})
                    })
                elif agent_name == 'EvaluationAgent':
                    result = agent.process({
                        'item_to_evaluate': step_data['request'],
                        'evaluation_type': 'project_deliverable'
                    })
                else:
                    result = agent.process({
                        'request': step_data['request'],
                        'context': step_data.get('context', {})
                    })
                agent_used = agent_name
                
            elif step_name == "quality_evaluation":
                result = self.agents['EvaluationAgent'].process(step_data)
                agent_used = "EvaluationAgent"
                
            elif step_name == "support_integration":
                result = self._integrate_support_functions(step_data)
                agent_used = "SupportFunctions"
                
            elif step_name == "output_structuring":
                result = self._structure_final_output(step_data['workflow_results'])
                agent_used = "WorkflowOrchestrator"
                
            else:
                raise ValueError(f"Unknown step: {step_name}")
            
            # Track completed step
            step_duration = (datetime.now() - step_start_time).total_seconds()
            completed_step = {
                "step_name": step_name,
                "agent_used": agent_used,
                "duration_seconds": step_duration,
                "timestamp": step_start_time.isoformat(),
                "success": True,
                "confidence": getattr(result, 'confidence_score', 0.8) if hasattr(result, 'confidence_score') else 0.8
            }
            
            self.completed_steps.append(completed_step)
            logger.info(f"Step {step_name} completed successfully in {step_duration:.2f}s")
            
            return result
            
        except Exception as e:
            # Track failed step
            step_duration = (datetime.now() - step_start_time).total_seconds()
            failed_step = {
                "step_name": step_name,
                "agent_used": "Unknown",
                "duration_seconds": step_duration,
                "timestamp": step_start_time.isoformat(),
                "success": False,
                "error": str(e),
                "confidence": 0.0
            }
            
            self.completed_steps.append(failed_step)
            logger.error(f"Step {step_name} failed: {str(e)}")
            raise
    
    def _integrate_support_functions(self, step_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate support functions based on request type
        """
        request_type = step_data.get('request_type', 'general')
        primary_output = step_data.get('primary_output', '')
        evaluation_feedback = step_data.get('evaluation_feedback', '')
        
        support_results = {}
        
        if request_type in ['product_development', 'product_management']:
            support_results['product_manager'] = self.support_functions['product_manager']({
                'task_type': 'product_planning',
                'requirements': primary_output,
                'context': evaluation_feedback,
                'stakeholders': ['Product Owner', 'Development Team', 'Users'],
                'timeline': 'flexible'
            })
        
        if request_type in ['program_coordination', 'multi_team']:
            support_results['program_manager'] = self.support_functions['program_manager']({
                'program_scope': primary_output,
                'teams_involved': ['Development', 'QA', 'DevOps'],
                'resources': {'budget': 'TBD', 'timeline': 'flexible'},
                'timeline': 'flexible',
                'dependencies': []
            })
        
        if request_type in ['technical_implementation', 'software_development']:
            support_results['development_engineer'] = self.support_functions['development_engineer']({
                'technical_requirements': primary_output,
                'architecture_type': 'microservices',
                'technology_stack': ['JavaScript', 'Python', 'React'],
                'scalability_needs': 'medium',
                'integration_points': []
            })
        
        return support_results
    
    def _classify_request_type(self, request: str) -> str:
        """
        Classify request type for support function selection
        """
        request_lower = request.lower()
        
        if any(keyword in request_lower for keyword in ['product', 'feature', 'user story', 'requirements']):
            return 'product_development'
        elif any(keyword in request_lower for keyword in ['program', 'coordinate', 'teams', 'resources']):
            return 'program_coordination'
        elif any(keyword in request_lower for keyword in ['technical', 'implement', 'code', 'architecture']):
            return 'technical_implementation'
        else:
            return 'general'
    
    def _calculate_overall_confidence(self) -> float:
        """
        Calculate overall workflow confidence from completed steps
        """
        if not self.completed_steps:
            return 0.0
        
        successful_steps = [step for step in self.completed_steps if step.get('success', False)]
        if not successful_steps:
            return 0.0
        
        confidences = [step.get('confidence', 0.0) for step in successful_steps]
        return sum(confidences) / len(confidences)
    
    def _structure_final_output(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure the final workflow output in required format
        """
        return {
            "workflow_execution": {
                "id": f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "timestamp": datetime.now().isoformat(),
                "type": "enhanced_agentic_workflow",
                "status": "completed" if workflow_results.get("success", False) else "failed",
                "duration_info": f"Completed in {len(self.completed_steps)} steps",
                "overall_confidence": workflow_results.get("overall_confidence", 0.0)
            },
            "request_analysis": {
                "original_request": workflow_results.get("request", ""),
                "processed_context": workflow_results.get("context", {}),
                "routing_decision": workflow_results.get("routing_analysis", {}),
                "complexity_assessment": "medium"
            },
            "agent_coordination": {
                "agents_involved": workflow_results.get("agents_used", []),
                "processing_steps": len(workflow_results.get("steps", [])),
                "coordination_pattern": "step_wise_routing",
                "completed_steps": self.completed_steps
            },
            "deliverables": {
                "primary_output": workflow_results.get("primary_output", ""),
                "user_stories": self._extract_user_stories(workflow_results.get("primary_output", "")),
                "product_features": self._extract_product_features(workflow_results.get("primary_output", "")),
                "engineering_tasks": self._extract_engineering_tasks(workflow_results.get("support_analysis", {})),
                "evaluation_results": workflow_results.get("evaluation_results", {}),
                "support_analysis": workflow_results.get("support_analysis", {})
            },
            "quality_metrics": {
                "overall_score": workflow_results.get("evaluation_results", {}).get("overall_score", 0.0),
                "confidence_distribution": [step.get('confidence', 0.0) for step in self.completed_steps],
                "validation_results": workflow_results.get("evaluation_results", {}),
                "step_success_rate": len([s for s in self.completed_steps if s.get('success')]) / len(self.completed_steps) if self.completed_steps else 0
            },
            "metadata": {
                "processing_metadata": {
                    "total_steps": len(self.completed_steps),
                    "successful_steps": len([s for s in self.completed_steps if s.get('success')]),
                    "agents_used": list(set([s.get('agent_used') for s in self.completed_steps]))
                },
                "system_info": {
                    "version": "2.0",
                    "capabilities": "Enhanced multi-agent workflow with step-wise routing and support functions"
                }
            }
        }
    
    def _extract_user_stories(self, content: str) -> List[str]:
        """Extract user stories from content"""
        # Simple extraction - in real implementation would use more sophisticated NLP
        stories = []
        lines = content.split('\n')
        for line in lines:
            if 'user' in line.lower() and ('want' in line.lower() or 'need' in line.lower()):
                stories.append(line.strip())
        
        # Add default stories if none found
        if not stories:
            stories = [
                "As a user, I want to access the system efficiently",
                "As an admin, I want to manage system configurations",
                "As a stakeholder, I want to view progress reports"
            ]
        
        return stories[:5]  # Limit to 5 stories
    
    def _extract_product_features(self, content: str) -> List[str]:
        """Extract product features from content"""
        features = []
        lines = content.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['feature', 'functionality', 'capability', 'component']):
                features.append(line.strip())
        
        # Add default features if none found
        if not features:
            features = [
                "Core system functionality",
                "User interface components",
                "Data management features",
                "Integration capabilities",
                "Security and authentication"
            ]
        
        return features[:5]  # Limit to 5 features
    
    def _extract_engineering_tasks(self, support_analysis: Dict[str, Any]) -> List[str]:
        """Extract engineering tasks from support analysis"""
        tasks = []
        
        # Extract from development engineer analysis
        dev_analysis = support_analysis.get('development_engineer', {})
        if dev_analysis:
            tech_tasks = dev_analysis.get('technical_tasks', [])
            for task in tech_tasks:
                if isinstance(task, dict):
                    tasks.append(task.get('task', str(task)))
                else:
                    tasks.append(str(task))
        
        # Add default tasks if none found
        if not tasks:
            tasks = [
                "Set up development environment",
                "Implement core business logic",
                "Develop user interface components",
                "Create database schema and models",
                "Implement API endpoints",
                "Set up testing framework",
                "Configure deployment pipeline"
            ]
        
        return tasks[:7]  # Limit to 7 tasks
    
    def _format_final_output(self, structured_result: Dict[str, Any], request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the final workflow output
        """
        return {
            "success": True,
            "workflow_id": structured_result["workflow_execution"]["id"],
            "timestamp": structured_result["workflow_execution"]["timestamp"],
            "request": request,
            "context": context,
            "results": structured_result,
            "completed_steps": self.completed_steps,
            "overall_confidence": structured_result["workflow_execution"]["overall_confidence"],
            "summary": f"Workflow completed successfully with {len(self.completed_steps)} steps and {structured_result['workflow_execution']['overall_confidence']:.2f} confidence"
        }
    
    def _handle_workflow_error(self, error: Exception, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle workflow execution errors
        """
        return {
            "success": False,
            "workflow_id": f"failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "context": context,
            "error": str(error),
            "completed_steps": self.completed_steps,
            "overall_confidence": 0.0,
            "summary": f"Workflow failed after {len(self.completed_steps)} steps: {str(error)}"
        }

# Main execution function
def main():
    """
    Main execution function for testing the enhanced workflow
    """
    # Initialize workflow
    workflow = EnhancedAgenticWorkflow()
    
    # Test request
    test_request = """
    Create a comprehensive project plan for developing an email routing system that can:
    1. Automatically categorize incoming emails
    2. Route emails to appropriate departments
    3. Provide analytics and reporting
    4. Integrate with existing CRM systems
    
    The system should handle high volume email processing and include proper security measures.
    """
    
    test_context = {
        "priority": "high",
        "timeline": "3 months",
        "budget": "flexible",
        "stakeholders": ["IT Department", "Customer Service", "Management"]
    }
    
    # Execute workflow
    result = workflow.execute_workflow(test_request, test_context)
    
    # Print results
    print("=" * 80)
    print("ENHANCED AGENTIC WORKFLOW EXECUTION RESULTS")
    print("=" * 80)
    print(f"Success: {result['success']}")
    print(f"Workflow ID: {result['workflow_id']}")
    print(f"Overall Confidence: {result['overall_confidence']:.2f}")
    print(f"Completed Steps: {len(result['completed_steps'])}")
    print("\nStep Summary:")
    for i, step in enumerate(result['completed_steps'], 1):
        print(f"  {i}. {step['step_name']} ({step['agent_used']}) - {'✓' if step['success'] else '✗'}")
    
    print(f"\nSummary: {result['summary']}")
    
    # Save results to file
    output_file = f"enhanced_workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return result

if __name__ == "__main__":
    main()
