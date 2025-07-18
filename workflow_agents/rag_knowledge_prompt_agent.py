
"""
RAG Knowledge Prompt Agent - Retrieval-Augmented Generation for knowledge enhancement
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
import json

class RAGKnowledgePromptAgent(BaseAgent):
    """
    Specialized agent for retrieval-augmented generation and knowledge search:
    - Information retrieval and knowledge search
    - Source integration and fact verification
    - Research augmentation and data gathering
    - Knowledge base querying and synthesis
    - Evidence-based response generation
    """
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.capabilities = [
            "information_retrieval", "knowledge_search", "source_integration",
            "fact_verification", "research_augmentation", "data_synthesis"
        ]
        self.specialties = [
            "project_knowledge_retrieval", "technical_documentation_search",
            "best_practices_research", "industry_standards_lookup",
            "case_studies_analysis", "evidence_based_recommendations"
        ]
        
        # Simulated knowledge repositories for different domains
        self.knowledge_repositories = {
            "project_management": {
                "methodologies": {
                    "Agile": {
                        "description": "Iterative and incremental approach to project management",
                        "key_principles": ["Individuals over processes", "Working software over documentation", "Customer collaboration", "Responding to change"],
                        "best_practices": ["Daily standups", "Sprint planning", "Retrospectives", "Continuous delivery"],
                        "tools": ["Jira", "Trello", "Azure DevOps", "Scrum boards"],
                        "success_factors": ["Team collaboration", "Customer involvement", "Adaptive planning", "Regular feedback"]
                    },
                    "Waterfall": {
                        "description": "Sequential approach to project management with distinct phases",
                        "key_principles": ["Sequential phases", "Comprehensive documentation", "Formal reviews", "Change control"],
                        "best_practices": ["Detailed planning", "Phase gate reviews", "Risk management", "Quality assurance"],
                        "tools": ["MS Project", "Gantt charts", "WBS", "Risk registers"],
                        "success_factors": ["Clear requirements", "Stable scope", "Experienced team", "Formal processes"]
                    }
                },
                "risk_management": {
                    "common_risks": ["Scope creep", "Resource constraints", "Technical challenges", "Stakeholder conflicts"],
                    "mitigation_strategies": ["Regular monitoring", "Contingency planning", "Stakeholder engagement", "Risk registers"],
                    "assessment_methods": ["Probability-impact matrix", "Risk scoring", "Qualitative analysis", "Monte Carlo simulation"]
                },
                "stakeholder_management": {
                    "identification_methods": ["Stakeholder mapping", "Power-interest grid", "Influence diagrams"],
                    "engagement_strategies": ["Regular communication", "Involvement in decisions", "Feedback loops", "Expectation management"],
                    "communication_tools": ["Status reports", "Dashboards", "Meetings", "Collaboration platforms"]
                }
            },
            "software_development": {
                "architectures": {
                    "Microservices": {
                        "description": "Architectural style that structures an application as a collection of loosely coupled services",
                        "benefits": ["Scalability", "Technology diversity", "Team autonomy", "Fault isolation"],
                        "challenges": ["Complexity", "Network latency", "Data consistency", "Monitoring"],
                        "best_practices": ["Service boundaries", "API design", "Data management", "Monitoring and logging"]
                    },
                    "Monolithic": {
                        "description": "Traditional unified model for designing software applications",
                        "benefits": ["Simplicity", "Easy deployment", "Performance", "Testing"],
                        "challenges": ["Scalability", "Technology lock-in", "Team coordination", "Maintenance"],
                        "best_practices": ["Modular design", "Clear interfaces", "Automated testing", "Continuous integration"]
                    }
                },
                "testing_strategies": {
                    "unit_testing": ["Test individual components", "Fast execution", "High coverage", "Automated"],
                    "integration_testing": ["Test component interactions", "API testing", "Database testing", "Service testing"],
                    "system_testing": ["End-to-end testing", "Performance testing", "Security testing", "User acceptance testing"]
                },
                "deployment_patterns": {
                    "blue_green": "Two identical production environments for zero-downtime deployment",
                    "canary": "Gradual rollout to subset of users for risk mitigation",
                    "rolling": "Sequential update of instances in production environment"
                }
            },
            "quality_assurance": {
                "standards": {
                    "ISO_9001": {
                        "description": "International standard for quality management systems",
                        "principles": ["Customer focus", "Leadership", "People engagement", "Process approach"],
                        "requirements": ["Quality policy", "Documented procedures", "Management review", "Continuous improvement"],
                        "benefits": ["Improved efficiency", "Customer satisfaction", "Risk management", "Competitive advantage"]
                    },
                    "Six_Sigma": {
                        "description": "Data-driven methodology for eliminating defects and improving processes",
                        "phases": ["Define", "Measure", "Analyze", "Improve", "Control"],
                        "tools": ["Statistical analysis", "Process mapping", "Root cause analysis", "Control charts"],
                        "benefits": ["Defect reduction", "Cost savings", "Process improvement", "Customer satisfaction"]
                    }
                },
                "testing_methodologies": {
                    "risk_based_testing": "Prioritize testing based on risk assessment",
                    "exploratory_testing": "Simultaneous learning, test design, and execution",
                    "automated_testing": "Use of software tools to execute tests automatically"
                }
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> AgentResponse:
        """
        Process RAG knowledge requests
        
        Args:
            input_data: Dictionary containing:
                - query: Search query or knowledge request
                - domain: Domain to search within
                - search_depth: Depth of search (surface, moderate, deep)
                - source_types: Types of sources to include
                - context: Additional context for search
        """
        query = input_data.get('query', '')
        domain = input_data.get('domain', 'project_management')
        search_depth = input_data.get('search_depth', 'moderate')
        source_types = input_data.get('source_types', ['methodologies', 'best_practices', 'tools'])
        context = input_data.get('context', '')
        
        # Perform knowledge retrieval
        retrieved_knowledge = self._retrieve_knowledge(query, domain, search_depth, source_types)
        
        # Synthesize and integrate knowledge
        knowledge_synthesis = self._synthesize_knowledge(retrieved_knowledge, query, context)
        
        system_prompt = """You are an expert knowledge researcher and information synthesis specialist with advanced capabilities in:

- Comprehensive information retrieval and knowledge discovery
- Multi-source research and evidence gathering
- Knowledge synthesis and integration across domains
- Fact verification and source validation
- Research methodology and systematic analysis
- Evidence-based recommendation development

Your RAG approach should be:
- Research-driven with comprehensive knowledge retrieval
- Evidence-based with credible sources and references
- Synthesized with integrated insights across sources
- Contextual with relevant application to specific situations
- Analytical with critical evaluation of information
- Actionable with practical recommendations and guidance
- Authoritative with expert-level knowledge integration

Always provide source attribution, evidence quality assessment, and confidence levels for retrieved information."""
        
        user_prompt = f"""
        RAG KNOWLEDGE REQUEST
        
        Query: {query}
        Domain: {domain}
        Search Depth: {search_depth}
        Source Types: {source_types}
        Context: {context}
        
        Retrieved Knowledge:
        {json.dumps(retrieved_knowledge, indent=2)}
        
        Knowledge Synthesis:
        {json.dumps(knowledge_synthesis, indent=2)}
        
        Please provide comprehensive knowledge-enhanced response including:
        
        1. KNOWLEDGE-ENHANCED RESPONSE
           - Query response enhanced with retrieved knowledge
           - Multi-source information integration
           - Evidence-based insights and analysis
           - Contextual application of knowledge
           - Expert-level synthesis and interpretation
        
        2. SOURCE ANALYSIS
           - Retrieved sources and their relevance
           - Source quality and credibility assessment
           - Knowledge gaps and limitations identified
           - Conflicting information reconciliation
           - Additional research recommendations
        
        3. EVIDENCE-BASED INSIGHTS
           - Key findings from knowledge retrieval
           - Patterns and trends identified
           - Best practices and proven approaches
           - Success factors and critical considerations
           - Risk factors and mitigation strategies
        
        4. PRACTICAL APPLICATIONS
           - How to apply retrieved knowledge
           - Implementation strategies and approaches
           - Real-world examples and case studies
           - Adaptation for specific contexts
           - Success metrics and measurement
        
        5. KNOWLEDGE SYNTHESIS
           - Integration of multiple knowledge sources
           - Comprehensive understanding development
           - Holistic perspective and analysis
           - Cross-domain insights and connections
           - Emergent patterns and implications
        
        6. RECOMMENDATIONS
           - Evidence-based recommendations
           - Prioritized action items
           - Implementation roadmap
           - Resource requirements
           - Success probability assessment
        
        7. KNOWLEDGE GAPS
           - Areas requiring additional research
           - Missing information and data
           - Uncertainty factors and assumptions
           - Future research directions
           - Knowledge validation needs
        
        8. CONFIDENCE ASSESSMENT
           - Confidence levels for different aspects
           - Evidence quality indicators
           - Reliability and validity assessment
           - Limitations and caveats
           - Recommendation strength levels
        
        Ensure all information is properly attributed and evidence-based with clear confidence indicators.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_content = self._call_openai(messages)
        confidence_score = self._calculate_confidence(response_content)
        
        # Calculate retrieval metrics
        retrieval_metrics = self._calculate_retrieval_metrics(retrieved_knowledge, query)
        
        return AgentResponse(
            success=True,
            content=response_content,
            metadata={
                "agent_type": "RAGKnowledgePromptAgent",
                "domain": domain,
                "search_depth": search_depth,
                "sources_retrieved": len(retrieved_knowledge),
                "knowledge_synthesis": knowledge_synthesis,
                "retrieval_metrics": retrieval_metrics,
                "source_types_used": source_types,
                "knowledge_coverage": self._assess_knowledge_coverage(retrieved_knowledge, query)
            },
            confidence_score=confidence_score,
            reasoning=f"Retrieved and synthesized knowledge from {len(retrieved_knowledge)} sources in {domain} domain with {search_depth} depth analysis"
        )
    
    def enhance_with_project_knowledge(self, content: str, specific_area: str = "") -> AgentResponse:
        """Enhance content with project management knowledge"""
        return self.process({
            'query': content,
            'domain': 'project_management',
            'search_depth': 'deep',
            'source_types': ['methodologies', 'risk_management', 'stakeholder_management'],
            'context': f'Project management enhancement focusing on: {specific_area}' if specific_area else 'General project management enhancement'
        })
    
    def research_technical_solution(self, technical_query: str, technology: str = "") -> AgentResponse:
        """Research technical solutions and best practices"""
        return self.process({
            'query': technical_query,
            'domain': 'software_development',
            'search_depth': 'deep',
            'source_types': ['architectures', 'testing_strategies', 'deployment_patterns'],
            'context': f'Technical research for {technology}' if technology else 'General technical research'
        })
    
    def lookup_quality_standards(self, quality_query: str, standard: str = "") -> AgentResponse:
        """Lookup quality assurance standards and practices"""
        return self.process({
            'query': quality_query,
            'domain': 'quality_assurance',
            'search_depth': 'moderate',
            'source_types': ['standards', 'testing_methodologies'],
            'context': f'Quality standards research for {standard}' if standard else 'General quality standards research'
        })
    
    def find_best_practices(self, practice_query: str, domain: str = "project_management") -> AgentResponse:
        """Find best practices for specific domain"""
        return self.process({
            'query': practice_query,
            'domain': domain,
            'search_depth': 'moderate',
            'source_types': ['best_practices', 'methodologies', 'tools'],
            'context': 'Best practices research and recommendations'
        })
    
    def _retrieve_knowledge(self, query: str, domain: str, search_depth: str, source_types: List[str]) -> Dict[str, Any]:
        """Retrieve knowledge from repositories based on query"""
        retrieved = {}
        
        domain_repo = self.knowledge_repositories.get(domain, {})
        query_lower = query.lower()
        
        for source_type in source_types:
            if source_type in domain_repo:
                source_data = domain_repo[source_type]
                relevant_items = {}
                
                # Search through source data
                for key, value in source_data.items():
                    relevance_score = self._calculate_relevance(query_lower, key, value)
                    if relevance_score > 0.3:  # Relevance threshold
                        relevant_items[key] = {
                            'data': value,
                            'relevance_score': relevance_score,
                            'source_type': source_type
                        }
                
                if relevant_items:
                    retrieved[source_type] = relevant_items
        
        # Adjust retrieval based on search depth
        if search_depth == 'surface':
            # Limit to top 2 items per source type
            for source_type in retrieved:
                items = list(retrieved[source_type].items())[:2]
                retrieved[source_type] = dict(items)
        elif search_depth == 'deep':
            # Include additional context and related information
            retrieved = self._expand_knowledge_retrieval(retrieved, query_lower, domain_repo)
        
        return retrieved
    
    def _calculate_relevance(self, query: str, key: str, value: Any) -> float:
        """Calculate relevance score between query and knowledge item"""
        relevance_score = 0.0
        
        # Check key relevance
        key_lower = key.lower()
        query_words = query.split()
        key_words = key_lower.split('_')
        
        # Word overlap scoring
        common_words = set(query_words) & set(key_words)
        if common_words:
            relevance_score += len(common_words) / max(len(query_words), len(key_words))
        
        # Content relevance (if value is dict with searchable content)
        if isinstance(value, dict):
            content_text = ' '.join(str(v).lower() for v in value.values() if isinstance(v, (str, list)))
            content_words = content_text.split()
            content_overlap = set(query_words) & set(content_words)
            if content_overlap:
                relevance_score += len(content_overlap) / len(query_words) * 0.5
        
        # Substring matching
        if any(word in key_lower for word in query_words):
            relevance_score += 0.3
        
        return min(relevance_score, 1.0)
    
    def _expand_knowledge_retrieval(self, retrieved: Dict[str, Any], query: str, domain_repo: Dict[str, Any]) -> Dict[str, Any]:
        """Expand knowledge retrieval for deep search"""
        expanded = retrieved.copy()
        
        # Add related concepts and cross-references
        for source_type, items in retrieved.items():
            for item_key, item_data in items.items():
                # Look for related items in other source types
                for other_source_type, other_source_data in domain_repo.items():
                    if other_source_type != source_type and other_source_type not in expanded:
                        for other_key, other_value in other_source_data.items():
                            if self._calculate_relevance(item_key, other_key, other_value) > 0.4:
                                if other_source_type not in expanded:
                                    expanded[other_source_type] = {}
                                expanded[other_source_type][other_key] = {
                                    'data': other_value,
                                    'relevance_score': self._calculate_relevance(query, other_key, other_value),
                                    'source_type': other_source_type,
                                    'related_to': item_key
                                }
        
        return expanded
    
    def _synthesize_knowledge(self, retrieved_knowledge: Dict[str, Any], query: str, context: str) -> Dict[str, Any]:
        """Synthesize retrieved knowledge into coherent insights"""
        synthesis = {
            'key_themes': [],
            'common_patterns': [],
            'conflicting_information': [],
            'knowledge_gaps': [],
            'synthesis_confidence': 0.0
        }
        
        # Extract key themes
        all_items = []
        for source_type, items in retrieved_knowledge.items():
            for item_key, item_data in items.items():
                all_items.append({
                    'key': item_key,
                    'source_type': source_type,
                    'relevance': item_data['relevance_score'],
                    'data': item_data['data']
                })
        
        # Identify themes based on frequency and relevance
        theme_candidates = {}
        for item in all_items:
            key_words = item['key'].lower().split('_')
            for word in key_words:
                if len(word) > 3:  # Skip short words
                    if word not in theme_candidates:
                        theme_candidates[word] = {'count': 0, 'relevance_sum': 0}
                    theme_candidates[word]['count'] += 1
                    theme_candidates[word]['relevance_sum'] += item['relevance']
        
        # Select top themes
        sorted_themes = sorted(theme_candidates.items(), 
                             key=lambda x: x[1]['count'] * x[1]['relevance_sum'], 
                             reverse=True)
        synthesis['key_themes'] = [theme[0] for theme in sorted_themes[:5]]
        
        # Identify common patterns
        if len(all_items) > 1:
            synthesis['common_patterns'] = self._identify_patterns(all_items)
        
        # Calculate synthesis confidence
        if retrieved_knowledge:
            avg_relevance = sum(
                item['relevance_score'] 
                for source_items in retrieved_knowledge.values() 
                for item in source_items.values()
            ) / sum(len(items) for items in retrieved_knowledge.values())
            synthesis['synthesis_confidence'] = avg_relevance
        
        return synthesis
    
    def _identify_patterns(self, items: List[Dict[str, Any]]) -> List[str]:
        """Identify common patterns across retrieved items"""
        patterns = []
        
        # Look for common data structures or attributes
        common_attributes = set()
        for item in items:
            if isinstance(item['data'], dict):
                common_attributes.update(item['data'].keys())
        
        # Find attributes that appear in multiple items
        attribute_counts = {}
        for attr in common_attributes:
            count = sum(1 for item in items 
                       if isinstance(item['data'], dict) and attr in item['data'])
            if count > 1:
                attribute_counts[attr] = count
        
        # Convert to patterns
        for attr, count in sorted(attribute_counts.items(), key=lambda x: x[1], reverse=True):
            if count >= len(items) * 0.5:  # Appears in at least 50% of items
                patterns.append(f"Common attribute: {attr}")
        
        return patterns[:3]  # Return top 3 patterns
    
    def _calculate_retrieval_metrics(self, retrieved_knowledge: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Calculate metrics for knowledge retrieval quality"""
        metrics = {
            'total_sources': len(retrieved_knowledge),
            'total_items': sum(len(items) for items in retrieved_knowledge.values()),
            'average_relevance': 0.0,
            'coverage_score': 0.0,
            'diversity_score': 0.0
        }
        
        if retrieved_knowledge:
            # Calculate average relevance
            all_relevances = [
                item['relevance_score']
                for source_items in retrieved_knowledge.values()
                for item in source_items.values()
            ]
            if all_relevances:
                metrics['average_relevance'] = sum(all_relevances) / len(all_relevances)
            
            # Calculate coverage score (how well query is covered)
            query_words = set(query.lower().split())
            covered_words = set()
            for source_items in retrieved_knowledge.values():
                for item_key, item_data in source_items.items():
                    item_words = set(item_key.lower().split('_'))
                    covered_words.update(item_words & query_words)
            
            if query_words:
                metrics['coverage_score'] = len(covered_words) / len(query_words)
            
            # Calculate diversity score (variety of source types)
            metrics['diversity_score'] = len(retrieved_knowledge) / 3  # Assuming max 3 source types
        
        return metrics
    
    def _assess_knowledge_coverage(self, retrieved_knowledge: Dict[str, Any], query: str) -> str:
        """Assess how well the retrieved knowledge covers the query"""
        if not retrieved_knowledge:
            return 'none'
        
        total_items = sum(len(items) for items in retrieved_knowledge.values())
        source_diversity = len(retrieved_knowledge)
        
        if total_items >= 5 and source_diversity >= 2:
            return 'comprehensive'
        elif total_items >= 3 and source_diversity >= 2:
            return 'good'
        elif total_items >= 2:
            return 'moderate'
        else:
            return 'limited'
    
    def get_knowledge_repository(self, domain: str) -> Dict[str, Any]:
        """Get knowledge repository for specific domain"""
        return self.knowledge_repositories.get(domain, {})
    
    def add_knowledge_source(self, domain: str, source_type: str, knowledge_data: Dict[str, Any]):
        """Add knowledge source to repository"""
        if domain not in self.knowledge_repositories:
            self.knowledge_repositories[domain] = {}
        
        if source_type not in self.knowledge_repositories[domain]:
            self.knowledge_repositories[domain][source_type] = {}
        
        self.knowledge_repositories[domain][source_type].update(knowledge_data)
    
    def search_knowledge(self, query: str, domain: str = None) -> Dict[str, Any]:
        """Direct knowledge search across domains"""
        domains_to_search = [domain] if domain else list(self.knowledge_repositories.keys())
        
        results = {}
        for search_domain in domains_to_search:
            domain_results = self._retrieve_knowledge(
                query, search_domain, 'moderate', 
                list(self.knowledge_repositories.get(search_domain, {}).keys())
            )
            if domain_results:
                results[search_domain] = domain_results
        
        return results
