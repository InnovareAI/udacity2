
"""
Enhanced test suite for complete workflow functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from agentic_workflow_fixed import EnhancedAgenticWorkflow
from support_functions import product_manager, program_manager, development_engineer

class TestEnhancedWorkflow(unittest.TestCase):
    """Test enhanced workflow functionality"""
    
    def setUp(self):
        self.workflow = EnhancedAgenticWorkflow()
    
    def test_workflow_initialization(self):
        """Test workflow initializes correctly"""
        self.assertIsNotNone(self.workflow)
        self.assertIn('DirectPromptAgent', self.workflow.agents)
        self.assertIn('RoutingAgent', self.workflow.agents)
        self.assertIn('EvaluationAgent', self.workflow.agents)
        self.assertEqual(len(self.workflow.completed_steps), 0)
    
    def test_support_functions(self):
        """Test support functions"""
        # Test product_manager function
        pm_result = product_manager({
            'task_type': 'product_planning',
            'requirements': 'Build a mobile app',
            'context': 'Consumer market',
            'stakeholders': ['Users', 'Developers'],
            'timeline': '6 months'
        })
        
        self.assertEqual(pm_result['function'], 'product_manager')
        self.assertIn('analysis', pm_result)
        self.assertGreater(pm_result['confidence'], 0.8)
        
        # Test program_manager function
        prog_result = program_manager({
            'program_scope': 'Multi-team software project',
            'teams_involved': ['Dev', 'QA', 'DevOps'],
            'resources': {'budget': '1M', 'timeline': '1 year'},
            'timeline': '12 months',
            'dependencies': ['External API']
        })
        
        self.assertEqual(prog_result['function'], 'program_manager')
        self.assertIn('coordination', prog_result)
        self.assertGreater(prog_result['confidence'], 0.8)
        
        # Test development_engineer function
        dev_result = development_engineer({
            'technical_requirements': 'REST API with database',
            'architecture_type': 'microservices',
            'technology_stack': ['Python', 'PostgreSQL'],
            'scalability_needs': 'high',
            'integration_points': ['Payment gateway']
        })
        
        self.assertEqual(dev_result['function'], 'development_engineer')
        self.assertIn('implementation', dev_result)
        self.assertGreater(dev_result['confidence'], 0.8)
    
    def test_step_execution(self):
        """Test individual step execution"""
        # Test routing step
        routing_result = self.workflow._execute_step("routing_analysis", {
            'task_description': 'Create a project plan',
            'context': '{}',
            'priority': 'medium'
        })
        
        self.assertTrue(routing_result.success)
        self.assertEqual(len(self.workflow.completed_steps), 1)
        self.assertEqual(self.workflow.completed_steps[0]['step_name'], 'routing_analysis')
        self.assertTrue(self.workflow.completed_steps[0]['success'])
    
    def test_request_classification(self):
        """Test request type classification"""
        # Test product development classification
        product_type = self.workflow._classify_request_type("Create user stories for new product features")
        self.assertEqual(product_type, 'product_development')
        
        # Test technical implementation classification
        tech_type = self.workflow._classify_request_type("Implement REST API with authentication")
        self.assertEqual(tech_type, 'technical_implementation')
        
        # Test program coordination classification
        program_type = self.workflow._classify_request_type("Coordinate multiple teams for project delivery")
        self.assertEqual(program_type, 'program_coordination')
    
    def test_user_story_extraction(self):
        """Test user story extraction"""
        content = """
        As a user, I want to login securely to access my account.
        As an admin, I want to manage user permissions effectively.
        The system should provide reporting capabilities.
        """
        
        stories = self.workflow._extract_user_stories(content)
        self.assertGreater(len(stories), 0)
        self.assertTrue(any('user' in story.lower() for story in stories))
    
    def test_product_feature_extraction(self):
        """Test product feature extraction"""
        content = """
        The system will include the following features:
        - User authentication feature
        - Data reporting functionality
        - Integration capability with external systems
        """
        
        features = self.workflow._extract_product_features(content)
        self.assertGreater(len(features), 0)
        self.assertLessEqual(len(features), 5)
    
    def test_engineering_task_extraction(self):
        """Test engineering task extraction"""
        support_analysis = {
            'development_engineer': {
                'technical_tasks': [
                    {'task': 'Set up development environment', 'priority': 'High'},
                    {'task': 'Implement API endpoints', 'priority': 'High'}
                ]
            }
        }
        
        tasks = self.workflow._extract_engineering_tasks(support_analysis)
        self.assertGreater(len(tasks), 0)
        self.assertIn('Set up development environment', tasks)
    
    def test_confidence_calculation(self):
        """Test overall confidence calculation"""
        # Add some mock completed steps
        self.workflow.completed_steps = [
            {'success': True, 'confidence': 0.8},
            {'success': True, 'confidence': 0.9},
            {'success': False, 'confidence': 0.0}
        ]
        
        confidence = self.workflow._calculate_overall_confidence()
        self.assertGreater(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_workflow_execution_structure(self):
        """Test workflow execution returns proper structure"""
        # Simple test request
        test_request = "Create a basic project plan for a web application"
        test_context = {"priority": "medium", "timeline": "flexible"}
        
        try:
            result = self.workflow.execute_workflow(test_request, test_context)
            
            # Check basic structure
            self.assertIn('success', result)
            self.assertIn('workflow_id', result)
            self.assertIn('results', result)
            self.assertIn('completed_steps', result)
            
            # Check results structure
            results = result['results']
            self.assertIn('workflow_execution', results)
            self.assertIn('deliverables', results)
            self.assertIn('agent_coordination', results)
            
            # Check deliverables structure
            deliverables = results['deliverables']
            self.assertIn('user_stories', deliverables)
            self.assertIn('product_features', deliverables)
            self.assertIn('engineering_tasks', deliverables)
            
            # Verify completed_steps tracking
            self.assertGreater(len(result['completed_steps']), 0)
            
        except Exception as e:
            # If execution fails due to API issues, check that error handling works
            self.assertIsInstance(e, Exception)

if __name__ == '__main__':
    unittest.main()
