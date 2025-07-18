
"""
Test suite for DirectPromptAgent
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from workflow_agents import DirectPromptAgent

class TestDirectPromptAgent(unittest.TestCase):
    """Test DirectPromptAgent functionality"""
    
    def setUp(self):
        self.agent = DirectPromptAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.agent_name, "DirectPromptAgent")
        self.assertIn("direct_llm_access", self.agent.capabilities)
        self.assertIn("unfiltered_prompting", self.agent.capabilities)
    
    def test_direct_prompt_processing(self):
        """Test direct prompt processing"""
        response = self.agent.direct_prompt(
            "What is the capital of France?",
            context="Geography question"
        )
        
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, str)
        self.assertGreater(len(response.content), 0)
        self.assertEqual(response.metadata["agent_type"], "DirectPromptAgent")
        self.assertTrue(response.metadata["direct_processing"])
        self.assertGreater(response.confidence_score, 0.8)
    
    def test_process_method(self):
        """Test process method with input data"""
        response = self.agent.process({
            'prompt': 'Explain machine learning in simple terms',
            'context': 'Educational content',
            'temperature': 0.5
        })
        
        self.assertTrue(response.success)
        self.assertIsInstance(response.content, str)
        self.assertEqual(response.metadata["temperature"], 0.5)
        self.assertIn("machine learning", response.content.lower())
    
    def test_empty_prompt_handling(self):
        """Test handling of empty prompts"""
        response = self.agent.process({
            'prompt': '',
            'context': 'Test context'
        })
        
        self.assertFalse(response.success)
        self.assertIn("No prompt provided", response.content)
        self.assertEqual(response.confidence_score, 0.0)
    
    def test_context_integration(self):
        """Test context integration with prompt"""
        response = self.agent.process({
            'prompt': 'Answer this question',
            'context': 'Context: This is about Python programming'
        })
        
        self.assertTrue(response.success)
        self.assertGreater(response.metadata["prompt_length"], len('Answer this question'))
    
    def test_temperature_parameter(self):
        """Test temperature parameter handling"""
        response = self.agent.process({
            'prompt': 'Generate creative text',
            'temperature': 0.9,
            'max_tokens': 100
        })
        
        self.assertTrue(response.success)
        self.assertEqual(response.metadata["temperature"], 0.9)
        self.assertEqual(response.metadata["max_tokens"], 100)

if __name__ == '__main__':
    unittest.main()
