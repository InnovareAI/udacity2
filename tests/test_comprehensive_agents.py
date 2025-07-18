
"""
Comprehensive test suite for all workflow agents
Tests functionality, integration, and edge cases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from workflow_agents import (
    ProjectManagerAgent,
    AugmentedPromptAgent,
    KnowledgeAugmentedPromptAgent,
    RAGKnowledgePromptAgent,
    EvaluationAgent,
    RoutingAgent,
    ActionPlanningAgent
)

class TestProjectManagerAgent(unittest.TestCase):
    """Test ProjectManagerAgent functionality"""
    
    def setUp(self):
        self.agent = ProjectManagerAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "ProjectManagerAgent")
        self.assertIn("project_planning", self.agent.capabilities)
    
    def test_create_project_plan(self):
        """Test project plan creation"""
        response = self.agent.create_project_plan(
            "Develop a mobile app for task management",
            {"timeline": "3 months", "team_size": 4}
        )
        
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, str)
        self.assertGreater(len(response.content), 100)
        self.assertGreater(response.confidence_score, 0)
        self.assertEqual(response.metadata["agent_type"], "ProjectManagerAgent")
    
    def test_assess_project_risks(self):
        """Test risk assessment functionality"""
        response = self.agent.assess_project_risks(
            "Complex enterprise software integration with tight deadline"
        )
        
        self.assertTrue(response.success)
        self.assertIn("risk", response.content.lower())
        self.assertEqual(response.metadata["task_type"], "risk_assessment")
    
    def test_methodology_recommendation(self):
        """Test methodology recommendation logic"""
        # Test Agile recommendation
        agile_project = "Innovative mobile app with changing requirements"
        response = self.agent.create_project_plan(agile_project)
        self.assertIn("Agile", response.metadata.get("methodology_recommended", ""))
        
        # Test Waterfall recommendation
        waterfall_project = "Regulatory compliance system with fixed requirements"
        response = self.agent.create_project_plan(waterfall_project)
        # Should recommend Waterfall or Hybrid for regulatory projects

class TestEvaluationAgent(unittest.TestCase):
    """Test EvaluationAgent functionality"""
    
    def setUp(self):
        self.agent = EvaluationAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "EvaluationAgent")
        self.assertIn("quality_assessment", self.agent.capabilities)
    
    def test_evaluate_project_deliverable(self):
        """Test project deliverable evaluation"""
        deliverable = """
        Project Plan for Mobile App Development
        - Timeline: 12 weeks
        - Team: 5 developers, 2 designers, 1 PM
        - Features: User authentication, task management, notifications
        - Technology: React Native, Node.js, MongoDB
        """
        
        response = self.agent.evaluate_project_deliverable(deliverable)
        
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, str)
        self.assertGreater(len(response.content), 200)
        self.assertIn("evaluation", response.content.lower())
        self.assertEqual(response.metadata["evaluation_type"], "project_deliverable")
        self.assertIn("individual_scores", response.metadata)
    
    def test_custom_evaluation(self):
        """Test custom evaluation with specific criteria"""
        criteria = {
            "innovation": "How innovative is the solution?",
            "feasibility": "How feasible is the implementation?",
            "impact": "What is the expected business impact?"
        }
        
        response = self.agent.custom_evaluation(
            "AI-powered customer service chatbot",
            criteria,
            "1-5"
        )
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["scoring_scale"], "1-5")
        self.assertEqual(response.metadata["evaluation_type"], "custom")
    
    def test_evaluation_criteria_access(self):
        """Test access to evaluation criteria"""
        criteria = self.agent.get_evaluation_criteria("project_deliverable")
        self.assertIsInstance(criteria, dict)
        self.assertIn("completeness", criteria)
        self.assertIn("quality", criteria)

class TestRoutingAgent(unittest.TestCase):
    """Test RoutingAgent functionality"""
    
    def setUp(self):
        self.agent = RoutingAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "RoutingAgent")
        self.assertIn("intelligent_task_routing", self.agent.capabilities)
    
    def test_route_evaluation_task(self):
        """Test routing of evaluation task"""
        response = self.agent.route_task(
            "I need to evaluate the quality of our project documentation",
            "The documentation includes technical specs and user guides"
        )
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["primary_agent"], "EvaluationAgent")
        self.assertGreater(response.metadata["routing_confidence"], 0.5)
        self.assertIn("alternative_agents", response.metadata)
    
    def test_route_planning_task(self):
        """Test routing of planning task"""
        response = self.agent.route_task(
            "Create a detailed action plan for implementing a new CRM system"
        )
        
        self.assertTrue(response.success)
        # Should route to ActionPlanningAgent or ProjectManagerAgent
        self.assertIn(response.metadata["primary_agent"], 
                     ["ActionPlanningAgent", "ProjectManagerAgent"])
    
    def test_agent_capabilities_access(self):
        """Test access to agent capabilities"""
        capabilities = self.agent.get_agent_capabilities()
        self.assertIsInstance(capabilities, dict)
        self.assertIn("ProjectManagerAgent", capabilities)
        self.assertIn("EvaluationAgent", capabilities)
    
    def test_task_analysis(self):
        """Test comprehensive task analysis"""
        response = self.agent.route_task(
            "Comprehensive project management for enterprise software development with quality assurance"
        )
        
        self.assertTrue(response.success)
        task_analysis = response.metadata["task_analysis"]
        self.assertIn("classification", task_analysis)
        self.assertIn("complexity", task_analysis)
        self.assertIn("multi_agent_required", task_analysis)

class TestActionPlanningAgent(unittest.TestCase):
    """Test ActionPlanningAgent functionality"""
    
    def setUp(self):
        self.agent = ActionPlanningAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "ActionPlanningAgent")
        self.assertIn("action_plan_creation", self.agent.capabilities)
    
    def test_create_project_plan(self):
        """Test project plan creation"""
        response = self.agent.create_project_plan(
            "Implement a customer feedback system",
            "software_development"
        )
        
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, str)
        self.assertGreater(len(response.content), 300)
        self.assertEqual(response.metadata["project_type"], "software_development")
        self.assertIn("planning_metadata", response.metadata)
    
    def test_break_down_task(self):
        """Test task breakdown functionality"""
        response = self.agent.break_down_task(
            "Launch a new product marketing campaign",
            "B2B software product with 6-month timeline"
        )
        
        self.assertTrue(response.success)
        self.assertTrue("step" in response.content.lower() or "phase" in response.content.lower())
        self.assertIn("phase", response.content.lower())
    
    def test_planning_templates(self):
        """Test access to planning templates"""
        templates = self.agent.get_planning_templates()
        self.assertIsInstance(templates, dict)
        self.assertIn("software_development", templates)
        self.assertIn("project_management", templates)

class TestAugmentedPromptAgent(unittest.TestCase):
    """Test AugmentedPromptAgent functionality"""
    
    def setUp(self):
        self.agent = AugmentedPromptAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "AugmentedPromptAgent")
        self.assertIn("prompt_enhancement", self.agent.capabilities)
    
    def test_enhance_for_project_management(self):
        """Test project management prompt enhancement"""
        original_prompt = "Create a project plan"
        response = self.agent.enhance_for_project_management(original_prompt)
        
        self.assertTrue(response.success)
        self.assertGreater(len(response.content), len(original_prompt))
        self.assertEqual(response.metadata["task_domain"], "project_management")
        self.assertIn("improvement_metrics", response.metadata)
    
    def test_optimize_for_clarity(self):
        """Test clarity optimization"""
        unclear_prompt = "Do something with the project stuff maybe"
        response = self.agent.optimize_for_clarity(unclear_prompt)
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["enhancement_type"], "clarity_focused")
    
    def test_create_evaluation_prompt(self):
        """Test evaluation prompt creation"""
        criteria = ["accuracy", "completeness", "usability"]
        response = self.agent.create_evaluation_prompt(criteria, "1-10")
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["task_domain"], "evaluation")

class TestKnowledgeAugmentedPromptAgent(unittest.TestCase):
    """Test KnowledgeAugmentedPromptAgent functionality"""
    
    def setUp(self):
        self.agent = KnowledgeAugmentedPromptAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "KnowledgeAugmentedPromptAgent")
        self.assertIn("domain_knowledge_integration", self.agent.capabilities)
    
    def test_add_project_management_knowledge(self):
        """Test project management knowledge integration"""
        content = "How to manage project risks effectively?"
        response = self.agent.add_project_management_knowledge(content)
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["domain"], "project_management")
        self.assertIn("integration_analysis", response.metadata)
        self.assertGreater(response.metadata["best_practices_count"], 0)
    
    def test_apply_framework(self):
        """Test framework application"""
        content = "Project planning approach"
        response = self.agent.apply_framework(content, "Agile", "project_management")
        
        self.assertTrue(response.success)
        self.assertIn("Agile", response.metadata["frameworks_applied"])
    
    def test_knowledge_base_access(self):
        """Test knowledge base access"""
        kb = self.agent.get_knowledge_base("project_management")
        self.assertIsInstance(kb, dict)
        self.assertIn("frameworks", kb)
        self.assertIn("best_practices", kb)

class TestRAGKnowledgePromptAgent(unittest.TestCase):
    """Test RAGKnowledgePromptAgent functionality"""
    
    def setUp(self):
        self.agent = RAGKnowledgePromptAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "RAGKnowledgePromptAgent")
        self.assertIn("information_retrieval", self.agent.capabilities)
    
    def test_enhance_with_project_knowledge(self):
        """Test project knowledge enhancement"""
        content = "What are the best practices for project planning?"
        response = self.agent.enhance_with_project_knowledge(content)
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["domain"], "project_management")
        self.assertIn("retrieval_metrics", response.metadata)
        self.assertGreaterEqual(response.metadata["sources_retrieved"], 0)
    
    def test_research_technical_solution(self):
        """Test technical solution research"""
        query = "Microservices architecture best practices"
        response = self.agent.research_technical_solution(query, "microservices")
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["domain"], "software_development")
    
    def test_knowledge_search(self):
        """Test direct knowledge search"""
        results = self.agent.search_knowledge("agile methodology")
        self.assertIsInstance(results, dict)
    
    def test_knowledge_repository_access(self):
        """Test knowledge repository access"""
        repo = self.agent.get_knowledge_repository("project_management")
        self.assertIsInstance(repo, dict)
        self.assertIn("methodologies", repo)

class TestAgentIntegration(unittest.TestCase):
    """Test agent integration and workflow"""
    
    def setUp(self):
        self.routing_agent = RoutingAgent()
        self.pm_agent = ProjectManagerAgent()
        self.eval_agent = EvaluationAgent()
    
    def test_routing_to_evaluation_workflow(self):
        """Test complete routing to evaluation workflow"""
        # Step 1: Route task
        routing_response = self.routing_agent.route_task(
            "Evaluate our project management processes"
        )
        
        self.assertTrue(routing_response.success)
        recommended_agent = routing_response.metadata["primary_agent"]
        
        # Step 2: Execute with recommended agent (should be EvaluationAgent)
        if recommended_agent == "EvaluationAgent":
            eval_response = self.eval_agent.evaluate_project_deliverable(
                "Project management processes including planning, execution, and monitoring"
            )
            self.assertTrue(eval_response.success)
    
    def test_multi_agent_coordination(self):
        """Test coordination between multiple agents"""
        # Step 1: Create project plan
        pm_response = self.pm_agent.create_project_plan(
            "Develop customer portal",
            {"timeline": "4 months", "complexity": "medium"}
        )
        
        self.assertTrue(pm_response.success)
        
        # Step 2: Evaluate the plan
        eval_response = self.eval_agent.evaluate_project_deliverable(
            pm_response.content
        )
        
        self.assertTrue(eval_response.success)
        self.assertIn("overall_score", eval_response.metadata)

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("🧪 Running Comprehensive Agent Test Suite")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProjectManagerAgent,
        TestEvaluationAgent,
        TestRoutingAgent,
        TestActionPlanningAgent,
        TestAugmentedPromptAgent,
        TestKnowledgeAugmentedPromptAgent,
        TestRAGKnowledgePromptAgent,
        TestAgentIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n⚠️  Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Error:')[-1].strip()}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Excellent! All agents are working correctly.")
    elif success_rate >= 75:
        print("✅ Good! Most agents are working correctly.")
    else:
        print("⚠️  Some issues detected. Please review failed tests.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_comprehensive_tests()
