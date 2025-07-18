
"""
Test script for individual agents to ensure they work correctly
"""

import os
from workflow_agents import (
    ProjectManagerAgent,
    AugmentedPromptAgent,
    KnowledgeAugmentedPromptAgent,
    RAGKnowledgePromptAgent,
    EvaluationAgent,
    RoutingAgent,
    ActionPlanningAgent
)

def test_project_manager_agent():
    """Test ProjectManagerAgent"""
    print("🧪 Testing ProjectManagerAgent...")
    agent = ProjectManagerAgent()
    
    response = agent.create_project_plan(
        "Develop a mobile app for task management",
        {"timeline": "3 months", "team_size": 4}
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_augmented_prompt_agent():
    """Test AugmentedPromptAgent"""
    print("\n🧪 Testing AugmentedPromptAgent...")
    agent = AugmentedPromptAgent()
    
    response = agent.enhance_for_project_management(
        "Create a project plan for software development"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_knowledge_augmented_prompt_agent():
    """Test KnowledgeAugmentedPromptAgent"""
    print("\n🧪 Testing KnowledgeAugmentedPromptAgent...")
    agent = KnowledgeAugmentedPromptAgent()
    
    response = agent.add_project_management_knowledge(
        "How to manage project risks effectively?"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_rag_knowledge_prompt_agent():
    """Test RAGKnowledgePromptAgent"""
    print("\n🧪 Testing RAGKnowledgePromptAgent...")
    agent = RAGKnowledgePromptAgent()
    
    response = agent.enhance_with_project_knowledge(
        "What are the best practices for project planning?"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_evaluation_agent():
    """Test EvaluationAgent"""
    print("\n🧪 Testing EvaluationAgent...")
    agent = EvaluationAgent()
    
    response = agent.evaluate_project_deliverable(
        "A comprehensive project plan with timeline, resources, and risk assessment"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_routing_agent():
    """Test RoutingAgent"""
    print("\n🧪 Testing RoutingAgent...")
    agent = RoutingAgent()
    
    response = agent.route_task(
        "I need to evaluate the quality of our project documentation",
        "The documentation includes technical specs and user guides"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"🎯 Recommended agent: {response.metadata.get('primary_agent', 'Unknown')}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def test_action_planning_agent():
    """Test ActionPlanningAgent"""
    print("\n🧪 Testing ActionPlanningAgent...")
    agent = ActionPlanningAgent()
    
    response = agent.create_project_plan(
        "Implement a customer feedback system",
        "software_development"
    )
    
    print(f"✅ Success: {response.success}")
    print(f"📊 Confidence: {response.confidence_score:.2f}")
    print(f"📝 Content preview: {response.content[:200]}...")
    return response.success

def main():
    """Run all agent tests"""
    print("🚀 Starting Agent Testing Suite")
    print("=" * 50)
    
    tests = [
        test_project_manager_agent,
        test_augmented_prompt_agent,
        test_knowledge_augmented_prompt_agent,
        test_rag_knowledge_prompt_agent,
        test_evaluation_agent,
        test_routing_agent,
        test_action_planning_agent
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! Agents are working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return all(results)

if __name__ == "__main__":
    main()
