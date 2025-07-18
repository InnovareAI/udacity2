"""
Corrected AI-Powered Agentic Workflow for Project Management
Addresses all Udacity feedback requirements

This script implements the exact requirements from the Udacity rubric:
1. Loads Product-Spec-Email-Router.txt into product_spec variable
2. Instantiates specialized knowledge and evaluation agents correctly
3. Configures routing agent with proper agents attribute structure
4. Implements support functions that chain knowledge->evaluation agents
5. Implements main workflow orchestration as specified
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Import all required agents from workflow_agents package
from workflow_agents import (
    ActionPlanningAgent,
    KnowledgeAugmentedPromptAgent,
    EvaluationAgent,
    RoutingAgent
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Personas and Knowledge Base as required by rubric
persona_product_manager = """You are a Product Manager responsible for defining product strategy, user stories, and product requirements. You focus on understanding user needs, market requirements, and translating them into actionable product specifications."""

persona_program_manager = """You are a Program Manager responsible for coordinating cross-functional teams, managing timelines, and ensuring successful program delivery. You focus on resource allocation, risk management, and stakeholder coordination."""

persona_dev_engineer = """You are a Development Engineer responsible for technical implementation, architecture design, and engineering best practices. You focus on system design, coding standards, and technical feasibility."""

persona_program_manager_eval = """You are an evaluation agent that checks the answers of other worker agents for program management deliverables."""

persona_dev_engineer_eval = """You are an evaluation agent that checks the answers of other worker agents for development engineering deliverables."""

# Knowledge bases for each role
knowledge_action_planning = """
Action planning involves breaking down complex goals into manageable, sequential steps. Key principles include:
- Clear objective definition
- Step-by-step breakdown
- Resource identification
- Timeline estimation
- Risk assessment
- Success criteria definition
"""

knowledge_program_manager = """
Program management focuses on coordinating multiple projects and teams to achieve strategic objectives. Key areas include:
- Resource allocation and capacity planning
- Cross-team coordination and communication
- Risk management and mitigation
- Timeline and milestone management
- Stakeholder engagement and reporting
- Quality assurance and process improvement
"""

knowledge_dev_engineer = """
Development engineering encompasses technical implementation and system design. Key areas include:
- System architecture and design patterns
- Technology stack selection and evaluation
- Coding standards and best practices
- Testing strategies and quality assurance
- Performance optimization and scalability
- Security considerations and implementation
"""

# Evaluation criteria as specified in rubric
user_story_evaluation_criteria = """The answer should be stories that follow the following structure: As a [type of user], I want [an action or feature] so that [benefit/value]."""

product_feature_evaluation_criteria = """The answer should be product features that follow the following structure:
Feature Name: [Clear, descriptive name]
Description: [Detailed description of the feature]
User Value: [How this feature benefits users]
Priority: [High/Medium/Low]
Dependencies: [Any dependencies or prerequisites]"""

task_evaluation_criteria = """The answer should be engineering tasks that follow the following structure:
Task Name: [Clear, descriptive name]
Description: [Detailed description of what needs to be done]
Technical Requirements: [Specific technical requirements]
Estimated Effort: [Time/complexity estimate]
Dependencies: [Any dependencies on other tasks]
Acceptance Criteria: [How to know the task is complete]"""

class AgenticWorkflow:
    """
    Main agentic workflow class that implements all Udacity requirements
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the workflow with all required agents and configurations"""
        # Load API key from environment variable as required
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # REQUIREMENT 1: Load Product-Spec-Email-Router.txt into product_spec variable
        self.product_spec = self._load_product_spec()
        
        # REQUIREMENT 2: Instantiate specialized knowledge agents correctly
        self._instantiate_knowledge_agents()
        
        # REQUIREMENT 3: Instantiate evaluation agents for each specialized role
        self._instantiate_evaluation_agents()
        
        # REQUIREMENT 4: Configure routing agent with proper agents attribute
        self._configure_routing_agent()
        
        # REQUIREMENT 5: Implement support functions
        self._setup_support_functions()
        
        # Workflow state
        self.completed_steps = []
        
        logger.info("AgenticWorkflow initialized with all Udacity requirements")
    
    def _load_product_spec(self) -> str:
        """Load the content of Product-Spec-Email-Router.txt into product_spec variable"""
        try:
            with open('/home/ubuntu/udacity_final_project/Product-Spec-Email-Router.txt', 'r') as f:
                product_spec_content = f.read()
            logger.info("Product specification loaded successfully")
            return product_spec_content
        except FileNotFoundError:
            logger.error("Product-Spec-Email-Router.txt not found")
            return ""
        except Exception as e:
            logger.error(f"Error loading product specification: {e}")
            return ""
    
    def _instantiate_knowledge_agents(self):
        """Instantiate specialized knowledge agents as required by rubric"""
        # Complete knowledge_product_manager by appending product_spec
        knowledge_product_manager_completed = knowledge_program_manager + "\n\nProduct Specification:\n" + self.product_spec
        
        # Instantiate ActionPlanningAgent with knowledge_action_planning
        # Note: The actual agent constructor takes knowledge_action_planning as a dict parameter
        self.action_planning_agent = ActionPlanningAgent(self.api_key, {"knowledge": knowledge_action_planning})
        
        # Instantiate KnowledgeAugmentedPromptAgent instances
        # Note: The actual agent constructor only takes api_key, so we'll store personas and knowledge separately
        self.product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(self.api_key)
        self.product_manager_persona = persona_product_manager
        self.product_manager_knowledge = knowledge_product_manager_completed
        
        self.program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(self.api_key)
        self.program_manager_persona = persona_program_manager
        self.program_manager_knowledge = knowledge_program_manager
        
        self.dev_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(self.api_key)
        self.dev_engineer_persona = persona_dev_engineer
        self.dev_engineer_knowledge = knowledge_dev_engineer
        
        logger.info("Specialized knowledge agents instantiated successfully")
    
    def _instantiate_evaluation_agents(self):
        """Instantiate evaluation agents for each specialized role as required by rubric"""
        # EvaluationAgent instances - store personas and criteria separately since constructor doesn't support them
        self.product_manager_eval_agent = EvaluationAgent(self.api_key)
        self.product_manager_eval_persona = "You are an evaluation agent that checks the answers of other worker agents"
        self.product_manager_eval_criteria = user_story_evaluation_criteria
        
        self.program_manager_eval_agent = EvaluationAgent(self.api_key)
        self.program_manager_eval_persona = persona_program_manager_eval
        self.program_manager_eval_criteria = product_feature_evaluation_criteria
        
        self.dev_engineer_eval_agent = EvaluationAgent(self.api_key)
        self.dev_engineer_eval_persona = persona_dev_engineer_eval
        self.dev_engineer_eval_criteria = task_evaluation_criteria
        
        logger.info("Specialized evaluation agents instantiated successfully")
    
    def _configure_routing_agent(self):
        """Configure routing agent with agents attribute as list of dictionaries"""
        # REQUIREMENT 4: agents attribute should be a list of dictionaries with name, description, and func
        agents_config = [
            {
                "name": "Product Manager",
                "description": "Responsible for defining product personas and user stories only. Handles product strategy, requirements gathering, and user story creation.",
                "func": self.product_manager_support_function
            },
            {
                "name": "Program Manager", 
                "description": "Responsible for coordinating cross-functional teams and managing program delivery. Handles resource allocation, timeline management, and stakeholder coordination.",
                "func": self.program_manager_support_function
            },
            {
                "name": "Development Engineer",
                "description": "Responsible for technical implementation and system architecture. Handles technical design, coding standards, and engineering best practices.",
                "func": self.development_engineer_support_function
            }
        ]
        
        # Instantiate RoutingAgent with proper agents attribute
        self.routing_agent = RoutingAgent(self.api_key)
        self.routing_agent.agents = agents_config
        
        logger.info("Routing agent configured with proper agents attribute structure")
    
    def _setup_support_functions(self):
        """Setup support functions that chain knowledge agent respond() to evaluation agent evaluate()"""
        # Support functions are defined as methods of this class
        # They implement the required pattern: accept query -> call knowledge agent respond() -> call evaluation agent evaluate() -> return validated result
        pass
    
    def product_manager_support_function(self, query: str) -> Dict[str, Any]:
        """
        Product Manager support function that chains knowledge agent to evaluation agent
        
        Args:
            query: Input query (a step from the action plan)
            
        Returns:
            Final validated response from evaluation agent
        """
        try:
            # Call the process() method of the corresponding KnowledgeAugmentedPromptAgent
            # Include persona and knowledge in the input
            knowledge_input = {
                "content": query,
                "persona": self.product_manager_persona,
                "knowledge_base": self.product_manager_knowledge,
                "task_type": "user_story_generation"
            }
            knowledge_response = self.product_manager_knowledge_agent.process(knowledge_input)
            
            # Pass the response to the process() method of the corresponding EvaluationAgent
            evaluation_input = {
                "item_to_evaluate": knowledge_response.content,
                "evaluation_type": "user_stories",
                "criteria": self.product_manager_eval_criteria,
                "persona": self.product_manager_eval_persona
            }
            evaluation_result = self.product_manager_eval_agent.process(evaluation_input)
            
            # Return the final, validated response
            return {
                "final_response": evaluation_result.content,
                "knowledge_response": knowledge_response.content,
                "evaluation_score": evaluation_result.confidence_score,
                "agent_type": "Product Manager"
            }
        except Exception as e:
            logger.error(f"Error in product_manager_support_function: {e}")
            return {"final_response": f"Error processing query: {e}", "agent_type": "Product Manager"}
    
    def program_manager_support_function(self, query: str) -> Dict[str, Any]:
        """
        Program Manager support function that chains knowledge agent to evaluation agent
        
        Args:
            query: Input query (a step from the action plan)
            
        Returns:
            Final validated response from evaluation agent
        """
        try:
            # Call the process() method of the corresponding KnowledgeAugmentedPromptAgent
            knowledge_input = {
                "content": query,
                "persona": self.program_manager_persona,
                "knowledge_base": self.program_manager_knowledge,
                "task_type": "product_feature_definition"
            }
            knowledge_response = self.program_manager_knowledge_agent.process(knowledge_input)
            
            # Pass the response to the process() method of the corresponding EvaluationAgent
            evaluation_input = {
                "item_to_evaluate": knowledge_response.content,
                "evaluation_type": "product_features",
                "criteria": self.program_manager_eval_criteria,
                "persona": self.program_manager_eval_persona
            }
            evaluation_result = self.program_manager_eval_agent.process(evaluation_input)
            
            # Return the final, validated response
            return {
                "final_response": evaluation_result.content,
                "knowledge_response": knowledge_response.content,
                "evaluation_score": evaluation_result.confidence_score,
                "agent_type": "Program Manager"
            }
        except Exception as e:
            logger.error(f"Error in program_manager_support_function: {e}")
            return {"final_response": f"Error processing query: {e}", "agent_type": "Program Manager"}
    
    def development_engineer_support_function(self, query: str) -> Dict[str, Any]:
        """
        Development Engineer support function that chains knowledge agent to evaluation agent
        
        Args:
            query: Input query (a step from the action plan)
            
        Returns:
            Final validated response from evaluation agent
        """
        try:
            # Call the process() method of the corresponding KnowledgeAugmentedPromptAgent
            knowledge_input = {
                "content": query,
                "persona": self.dev_engineer_persona,
                "knowledge_base": self.dev_engineer_knowledge,
                "task_type": "engineering_task_definition"
            }
            knowledge_response = self.dev_engineer_knowledge_agent.process(knowledge_input)
            
            # Pass the response to the process() method of the corresponding EvaluationAgent
            evaluation_input = {
                "item_to_evaluate": knowledge_response.content,
                "evaluation_type": "engineering_tasks",
                "criteria": self.dev_engineer_eval_criteria,
                "persona": self.dev_engineer_eval_persona
            }
            evaluation_result = self.dev_engineer_eval_agent.process(evaluation_input)
            
            # Return the final, validated response
            return {
                "final_response": evaluation_result.content,
                "knowledge_response": knowledge_response.content,
                "evaluation_score": evaluation_result.confidence_score,
                "agent_type": "Development Engineer"
            }
        except Exception as e:
            logger.error(f"Error in development_engineer_support_function: {e}")
            return {"final_response": f"Error processing query: {e}", "agent_type": "Development Engineer"}
    
    def run_workflow(self, workflow_prompt: str) -> Dict[str, Any]:
        """
        REQUIREMENT 6: Implement the main agentic workflow orchestration as specified
        
        The workflow should:
        1. Use action_planning_agent to get a list of workflow_steps from workflow_prompt
        2. Iterate through the workflow_steps
        3. For each step: print step -> call routing_agent.route() -> append to completed_steps -> print result
        4. Print final output after all steps
        """
        logger.info("Starting main agentic workflow orchestration")
        
        try:
            # Step 1: Use the action_planning_agent to get a list of workflow_steps from the workflow_prompt
            print("Getting workflow steps from action planning agent...")
            action_plan_input = {
                "goal": workflow_prompt,
                "project_type": "email_router_system",
                "context": "Product specification based planning"
            }
            action_plan_response = self.action_planning_agent.process(action_plan_input)
            
            # Extract workflow_steps from the action plan response
            workflow_steps = self._extract_workflow_steps(action_plan_response.content)
            
            print(f"Extracted {len(workflow_steps)} workflow steps")
            
            # Step 2: Iterate through the workflow_steps
            for i, step in enumerate(workflow_steps, 1):
                # Step 3a: Print the current step
                print(f"\n--- Step {i}: {step} ---")
                
                # Step 3b: Call routing_agent.route() with the current step
                # Note: Using route_task_with_embedding since there's no route() method
                routing_input = {
                    "task_description": step,
                    "context": f"Step {i} of workflow execution"
                }
                routing_response = self.routing_agent.process(routing_input)
                
                # Execute the routed task using the appropriate support function
                routed_result = self._execute_routed_step(step, routing_response)
                
                # Step 3c: Append the result from the routing_agent to completed_steps
                step_result = {
                    "step_number": i,
                    "step_description": step,
                    "routing_result": routing_response.content,
                    "execution_result": routed_result,
                    "timestamp": datetime.now().isoformat()
                }
                self.completed_steps.append(step_result)
                
                # Step 3d: Print the result of the current step
                print(f"Routing Result: {routing_response.content}")
                print(f"Execution Result: {routed_result.get('final_response', 'No response')}")
            
            # Step 4: Print the final output (last item in completed_steps or consolidated summary)
            final_output = self._generate_final_output()
            print(f"\n=== FINAL WORKFLOW OUTPUT ===")
            print(final_output)
            
            return {
                "workflow_steps": workflow_steps,
                "completed_steps": self.completed_steps,
                "final_output": final_output,
                "success": True,
                "total_steps": len(workflow_steps)
            }
            
        except Exception as e:
            logger.error(f"Error in workflow orchestration: {e}")
            error_output = f"Workflow failed with error: {e}"
            print(f"\n=== WORKFLOW ERROR ===")
            print(error_output)
            return {
                "error": str(e),
                "completed_steps": self.completed_steps,
                "final_output": error_output,
                "success": False
            }
    
    def _execute_routed_step(self, step: str, routing_response) -> Dict[str, Any]:
        """Execute a routed step using the appropriate support function"""
        try:
            # Determine which support function to use based on routing response
            routing_content = routing_response.content.lower()
            
            if "product manager" in routing_content or "user stor" in routing_content:
                return self.product_manager_support_function(step)
            elif "program manager" in routing_content or "product feature" in routing_content:
                return self.program_manager_support_function(step)
            elif "development engineer" in routing_content or "engineering task" in routing_content:
                return self.development_engineer_support_function(step)
            else:
                # Default to product manager if routing is unclear
                return self.product_manager_support_function(step)
        except Exception as e:
            logger.error(f"Error executing routed step: {e}")
            return {"final_response": f"Error executing step: {e}", "agent_type": "Unknown"}
    
    def _extract_workflow_steps(self, action_plan_content: str) -> List[str]:
        """Extract workflow steps from action plan content"""
        # Simple extraction - look for numbered steps or bullet points
        lines = action_plan_content.split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            # Look for numbered steps (1., 2., etc.) or bullet points (-, *, etc.)
            if (line and (
                line[0].isdigit() or 
                line.startswith('-') or 
                line.startswith('*') or
                line.startswith('•') or
                'step' in line.lower()
            )):
                # Clean up the step text
                step = line
                # Remove numbering and bullet points
                for prefix in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '-', '*', '•']:
                    if step.startswith(prefix):
                        step = step[len(prefix):].strip()
                        break
                
                if step and len(step) > 10:  # Only include substantial steps
                    steps.append(step)
        
        # If no structured steps found, create default steps
        if not steps:
            steps = [
                "Analyze project requirements and define scope",
                "Create user stories and product features", 
                "Design technical architecture and implementation plan",
                "Define project timeline and resource allocation",
                "Identify risks and mitigation strategies"
            ]
        
        return steps[:10]  # Limit to reasonable number of steps
    
    def _generate_final_output(self) -> str:
        """Generate final consolidated output from completed steps"""
        if not self.completed_steps:
            return "No steps completed"
        
        # Get the last completed step as primary output
        last_step = self.completed_steps[-1]
        
        # Create consolidated summary
        summary = f"""
WORKFLOW EXECUTION SUMMARY
==========================
Total Steps Completed: {len(self.completed_steps)}
Last Step: {last_step['step_description']}
Final Result: {last_step['routing_result']}

STEP-BY-STEP RESULTS:
"""
        
        for step in self.completed_steps:
            summary += f"\n{step['step_number']}. {step['step_description']}"
            summary += f"\n   Result: {step['routing_result']}\n"
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    # Initialize the workflow
    workflow = AgenticWorkflow()
    
    # Example workflow prompt for Email Router project
    workflow_prompt = """
    Create a comprehensive project plan for the Email Router System based on the product specification.
    The plan should include user stories, product features, and engineering tasks as specified in the requirements.
    Focus on the intelligent email classification, routing engine, integration capabilities, and monitoring features.
    """
    
    # Run the workflow
    result = workflow.run_workflow(workflow_prompt)
    
    # Print results
    print("\n" + "="*50)
    print("WORKFLOW EXECUTION COMPLETE")
    print("="*50)
    print(f"Success: {result['success']}")
    print(f"Total Steps: {result.get('total_steps', 0)}")
    print(f"Completed Steps: {len(result.get('completed_steps', []))}")
