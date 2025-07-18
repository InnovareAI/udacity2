
"""
Support Functions for Enhanced Agentic Workflow
Implements the three required support functions: product_manager, program_manager, development_engineer
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

def product_manager(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Product Manager support function - handles product strategy, requirements, and roadmap planning
    
    Args:
        request: Dictionary containing:
            - task_type: Type of product management task
            - requirements: Product requirements or specifications
            - context: Additional context about the product
            - stakeholders: List of stakeholders involved
            - timeline: Project timeline information
    
    Returns:
        Dictionary with product management analysis and recommendations
    """
    task_type = request.get('task_type', 'general')
    requirements = request.get('requirements', '')
    context = request.get('context', '')
    stakeholders = request.get('stakeholders', [])
    timeline = request.get('timeline', 'flexible')
    
    # Product management analysis
    analysis = {
        "product_strategy": {
            "market_analysis": "Analyze target market and competitive landscape",
            "value_proposition": "Define unique value proposition and key differentiators",
            "user_personas": "Identify and define target user personas",
            "success_metrics": "Define key performance indicators and success metrics"
        },
        "requirements_analysis": {
            "functional_requirements": _extract_functional_requirements(requirements),
            "non_functional_requirements": _extract_non_functional_requirements(requirements),
            "user_stories": _generate_user_stories(requirements, context),
            "acceptance_criteria": _define_acceptance_criteria(requirements)
        },
        "roadmap_planning": {
            "phases": _define_product_phases(task_type, timeline),
            "milestones": _identify_key_milestones(requirements, timeline),
            "dependencies": _analyze_dependencies(requirements),
            "risk_assessment": _assess_product_risks(requirements, context)
        },
        "stakeholder_management": {
            "stakeholder_mapping": _map_stakeholders(stakeholders),
            "communication_plan": _create_communication_plan(stakeholders),
            "feedback_loops": _design_feedback_mechanisms(stakeholders)
        }
    }
    
    return {
        "function": "product_manager",
        "timestamp": datetime.now().isoformat(),
        "task_type": task_type,
        "analysis": analysis,
        "recommendations": _generate_product_recommendations(analysis),
        "next_steps": _define_product_next_steps(analysis),
        "confidence": 0.85
    }

def program_manager(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Program Manager support function - handles program coordination, resource management, and cross-team alignment
    
    Args:
        request: Dictionary containing:
            - program_scope: Scope of the program
            - teams_involved: List of teams or departments involved
            - resources: Available resources and constraints
            - timeline: Program timeline and milestones
            - dependencies: Cross-team dependencies
    
    Returns:
        Dictionary with program management coordination and planning
    """
    program_scope = request.get('program_scope', '')
    teams_involved = request.get('teams_involved', [])
    resources = request.get('resources', {})
    timeline = request.get('timeline', 'flexible')
    dependencies = request.get('dependencies', [])
    
    # Program management coordination
    coordination = {
        "program_structure": {
            "work_breakdown": _create_program_wbs(program_scope),
            "team_alignment": _align_teams(teams_involved, program_scope),
            "governance_model": _define_governance_model(teams_involved),
            "communication_framework": _establish_communication_framework(teams_involved)
        },
        "resource_management": {
            "resource_allocation": _allocate_resources(resources, teams_involved),
            "capacity_planning": _plan_capacity(resources, timeline),
            "resource_optimization": _optimize_resource_usage(resources),
            "conflict_resolution": _identify_resource_conflicts(resources, teams_involved)
        },
        "timeline_coordination": {
            "master_schedule": _create_master_schedule(timeline, teams_involved),
            "milestone_alignment": _align_milestones(timeline, teams_involved),
            "dependency_management": _manage_dependencies(dependencies, teams_involved),
            "risk_mitigation": _mitigate_program_risks(dependencies, timeline)
        },
        "performance_tracking": {
            "kpi_framework": _define_program_kpis(program_scope),
            "progress_monitoring": _setup_progress_monitoring(teams_involved),
            "reporting_structure": _create_reporting_structure(teams_involved),
            "quality_assurance": _establish_qa_processes(program_scope)
        }
    }
    
    return {
        "function": "program_manager",
        "timestamp": datetime.now().isoformat(),
        "program_scope": program_scope,
        "coordination": coordination,
        "recommendations": _generate_program_recommendations(coordination),
        "action_items": _define_program_action_items(coordination),
        "confidence": 0.88
    }

def development_engineer(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Development Engineer support function - handles technical implementation, architecture, and engineering best practices
    
    Args:
        request: Dictionary containing:
            - technical_requirements: Technical specifications and requirements
            - architecture_type: Type of architecture (microservices, monolithic, etc.)
            - technology_stack: Preferred or required technology stack
            - scalability_needs: Scalability and performance requirements
            - integration_points: External systems and integration requirements
    
    Returns:
        Dictionary with technical implementation plan and engineering recommendations
    """
    technical_requirements = request.get('technical_requirements', '')
    architecture_type = request.get('architecture_type', 'modular')
    technology_stack = request.get('technology_stack', [])
    scalability_needs = request.get('scalability_needs', 'medium')
    integration_points = request.get('integration_points', [])
    
    # Technical implementation analysis
    implementation = {
        "architecture_design": {
            "system_architecture": _design_system_architecture(architecture_type, technical_requirements),
            "component_breakdown": _break_down_components(technical_requirements),
            "data_architecture": _design_data_architecture(technical_requirements),
            "security_architecture": _design_security_architecture(technical_requirements)
        },
        "technology_recommendations": {
            "tech_stack_analysis": _analyze_tech_stack(technology_stack, technical_requirements),
            "framework_selection": _recommend_frameworks(technology_stack, architecture_type),
            "tool_recommendations": _recommend_development_tools(technology_stack),
            "library_dependencies": _identify_key_libraries(technical_requirements, technology_stack)
        },
        "implementation_plan": {
            "development_phases": _plan_development_phases(technical_requirements),
            "coding_standards": _define_coding_standards(technology_stack),
            "testing_strategy": _create_testing_strategy(architecture_type),
            "deployment_strategy": _plan_deployment_strategy(scalability_needs)
        },
        "integration_strategy": {
            "api_design": _design_api_strategy(integration_points),
            "data_integration": _plan_data_integration(integration_points),
            "third_party_integrations": _analyze_third_party_integrations(integration_points),
            "integration_testing": _plan_integration_testing(integration_points)
        }
    }
    
    return {
        "function": "development_engineer",
        "timestamp": datetime.now().isoformat(),
        "technical_requirements": technical_requirements,
        "implementation": implementation,
        "recommendations": _generate_engineering_recommendations(implementation),
        "technical_tasks": _define_technical_tasks(implementation),
        "confidence": 0.90
    }

# Helper functions for product_manager
def _extract_functional_requirements(requirements: str) -> List[str]:
    """Extract functional requirements from requirements text"""
    # Simple extraction - in real implementation would use NLP
    functional_keywords = ['user can', 'system shall', 'application must', 'feature should']
    return [req.strip() for req in requirements.split('.') if any(kw in req.lower() for kw in functional_keywords)]

def _extract_non_functional_requirements(requirements: str) -> List[str]:
    """Extract non-functional requirements"""
    nfr_keywords = ['performance', 'security', 'scalability', 'availability', 'usability']
    return [req.strip() for req in requirements.split('.') if any(kw in req.lower() for kw in nfr_keywords)]

def _generate_user_stories(requirements: str, context: str) -> List[Dict[str, str]]:
    """Generate user stories from requirements"""
    return [
        {"story": "As a user, I want to access the system easily", "priority": "high"},
        {"story": "As an admin, I want to manage user permissions", "priority": "medium"},
        {"story": "As a stakeholder, I want to view progress reports", "priority": "medium"}
    ]

def _define_acceptance_criteria(requirements: str) -> List[str]:
    """Define acceptance criteria for requirements"""
    return [
        "All functional requirements are implemented and tested",
        "System meets performance benchmarks",
        "Security requirements are validated",
        "User acceptance testing is completed successfully"
    ]

def _define_product_phases(task_type: str, timeline: str) -> List[Dict[str, str]]:
    """Define product development phases"""
    return [
        {"phase": "Discovery", "duration": "2 weeks", "focus": "Requirements and research"},
        {"phase": "Design", "duration": "3 weeks", "focus": "Product design and prototyping"},
        {"phase": "Development", "duration": "8 weeks", "focus": "Implementation and testing"},
        {"phase": "Launch", "duration": "2 weeks", "focus": "Deployment and go-to-market"}
    ]

def _identify_key_milestones(requirements: str, timeline: str) -> List[Dict[str, str]]:
    """Identify key project milestones"""
    return [
        {"milestone": "Requirements Finalized", "target": "Week 2"},
        {"milestone": "Design Approved", "target": "Week 5"},
        {"milestone": "MVP Completed", "target": "Week 10"},
        {"milestone": "Product Launch", "target": "Week 15"}
    ]

def _analyze_dependencies(requirements: str) -> List[Dict[str, str]]:
    """Analyze project dependencies"""
    return [
        {"dependency": "External API integration", "type": "technical", "impact": "high"},
        {"dependency": "Stakeholder approval", "type": "business", "impact": "medium"},
        {"dependency": "Resource availability", "type": "resource", "impact": "high"}
    ]

def _assess_product_risks(requirements: str, context: str) -> List[Dict[str, str]]:
    """Assess product development risks"""
    return [
        {"risk": "Technical complexity", "probability": "medium", "impact": "high", "mitigation": "Proof of concept development"},
        {"risk": "Market changes", "probability": "low", "impact": "high", "mitigation": "Regular market analysis"},
        {"risk": "Resource constraints", "probability": "medium", "impact": "medium", "mitigation": "Flexible resource planning"}
    ]

def _map_stakeholders(stakeholders: List) -> Dict[str, Any]:
    """Map stakeholders and their interests"""
    return {
        "primary": ["Product Owner", "Development Team", "End Users"],
        "secondary": ["Marketing", "Sales", "Support"],
        "influence_matrix": {"high_influence_high_interest": ["Product Owner"], "high_influence_low_interest": ["Executive Sponsor"]}
    }

def _create_communication_plan(stakeholders: List) -> Dict[str, Any]:
    """Create stakeholder communication plan"""
    return {
        "weekly_updates": ["Development Team", "Product Owner"],
        "monthly_reviews": ["All Stakeholders"],
        "milestone_reports": ["Executive Sponsors", "Key Stakeholders"]
    }

def _design_feedback_mechanisms(stakeholders: List) -> List[str]:
    """Design feedback collection mechanisms"""
    return [
        "Weekly sprint reviews with development team",
        "Monthly stakeholder feedback sessions",
        "User testing and feedback collection",
        "Continuous feedback through product analytics"
    ]

def _generate_product_recommendations(analysis: Dict) -> List[str]:
    """Generate product management recommendations"""
    return [
        "Prioritize user stories based on business value and technical complexity",
        "Establish regular feedback loops with key stakeholders",
        "Implement agile development methodology for flexibility",
        "Create comprehensive testing strategy including user acceptance testing"
    ]

def _define_product_next_steps(analysis: Dict) -> List[str]:
    """Define next steps for product development"""
    return [
        "Finalize product requirements and user stories",
        "Create detailed project timeline and resource allocation",
        "Set up development environment and team structure",
        "Begin discovery phase with stakeholder interviews"
    ]

# Helper functions for program_manager
def _create_program_wbs(program_scope: str) -> Dict[str, Any]:
    """Create work breakdown structure for program"""
    return {
        "level_1": ["Planning", "Execution", "Monitoring", "Closure"],
        "level_2": {
            "Planning": ["Requirements", "Design", "Resource Planning"],
            "Execution": ["Development", "Testing", "Integration"],
            "Monitoring": ["Progress Tracking", "Quality Assurance", "Risk Management"],
            "Closure": ["Deployment", "Documentation", "Handover"]
        }
    }

def _align_teams(teams: List, scope: str) -> Dict[str, Any]:
    """Align teams with program objectives"""
    return {
        "team_responsibilities": {team: f"Responsible for {team.lower()} related tasks" for team in teams},
        "collaboration_points": ["Weekly sync meetings", "Milestone reviews", "Cross-team workshops"],
        "escalation_paths": "Team Lead -> Program Manager -> Executive Sponsor"
    }

def _define_governance_model(teams: List) -> Dict[str, Any]:
    """Define program governance model"""
    return {
        "steering_committee": ["Program Manager", "Team Leads", "Executive Sponsor"],
        "decision_making": "Consensus with Program Manager final authority",
        "meeting_cadence": {"weekly": "Team sync", "monthly": "Steering committee", "quarterly": "Executive review"}
    }

def _establish_communication_framework(teams: List) -> Dict[str, Any]:
    """Establish communication framework"""
    return {
        "communication_channels": ["Email", "Slack", "Video conferences", "Project management tool"],
        "reporting_structure": "Teams -> Program Manager -> Stakeholders",
        "escalation_procedures": "Standard -> Urgent -> Critical escalation paths defined"
    }

def _allocate_resources(resources: Dict, teams: List) -> Dict[str, Any]:
    """Allocate resources across teams"""
    return {
        "resource_distribution": {team: f"Allocated based on {team} workload" for team in teams},
        "shared_resources": ["Infrastructure", "Testing environments", "Documentation tools"],
        "resource_conflicts": "Managed through priority matrix and program manager oversight"
    }

def _plan_capacity(resources: Dict, timeline: str) -> Dict[str, Any]:
    """Plan resource capacity"""
    return {
        "capacity_analysis": "Current vs required capacity analysis",
        "bottleneck_identification": "Identify potential resource bottlenecks",
        "scaling_strategy": "Plan for resource scaling during peak periods"
    }

def _optimize_resource_usage(resources: Dict) -> List[str]:
    """Optimize resource usage"""
    return [
        "Cross-train team members for flexibility",
        "Implement resource sharing across teams",
        "Use automation to reduce manual effort",
        "Regular capacity reviews and adjustments"
    ]

def _identify_resource_conflicts(resources: Dict, teams: List) -> List[Dict[str, str]]:
    """Identify potential resource conflicts"""
    return [
        {"conflict": "Shared infrastructure", "teams": "Development, Testing", "resolution": "Time-based allocation"},
        {"conflict": "Subject matter expert", "teams": "Multiple teams", "resolution": "Scheduled consultation hours"}
    ]

def _create_master_schedule(timeline: str, teams: List) -> Dict[str, Any]:
    """Create master program schedule"""
    return {
        "program_timeline": timeline,
        "team_schedules": {team: f"{team} specific timeline" for team in teams},
        "integration_points": "Defined integration and synchronization points",
        "buffer_time": "Built-in buffer for risk mitigation"
    }

def _align_milestones(timeline: str, teams: List) -> Dict[str, Any]:
    """Align milestones across teams"""
    return {
        "program_milestones": ["Planning Complete", "Development Phase 1", "Integration Complete", "Go-Live"],
        "team_milestones": {team: f"{team} specific milestones" for team in teams},
        "milestone_dependencies": "Cross-team milestone dependencies mapped"
    }

def _manage_dependencies(dependencies: List, teams: List) -> Dict[str, Any]:
    """Manage program dependencies"""
    return {
        "dependency_mapping": "Visual mapping of all dependencies",
        "critical_path": "Identified critical path and dependencies",
        "mitigation_strategies": "Strategies for each high-risk dependency"
    }

def _mitigate_program_risks(dependencies: List, timeline: str) -> List[Dict[str, str]]:
    """Mitigate program risks"""
    return [
        {"risk": "Timeline delays", "mitigation": "Buffer time and parallel work streams"},
        {"risk": "Resource unavailability", "mitigation": "Cross-training and backup resources"},
        {"risk": "Technical challenges", "mitigation": "Proof of concepts and expert consultation"}
    ]

def _define_program_kpis(scope: str) -> List[Dict[str, str]]:
    """Define program KPIs"""
    return [
        {"kpi": "Schedule Performance Index", "target": ">0.95", "frequency": "Weekly"},
        {"kpi": "Budget Performance Index", "target": ">0.95", "frequency": "Monthly"},
        {"kpi": "Quality Metrics", "target": "<5% defect rate", "frequency": "Continuous"},
        {"kpi": "Stakeholder Satisfaction", "target": ">90%", "frequency": "Monthly"}
    ]

def _setup_progress_monitoring(teams: List) -> Dict[str, Any]:
    """Setup progress monitoring"""
    return {
        "monitoring_tools": ["Project management software", "Dashboards", "Automated reports"],
        "reporting_frequency": {"daily": "Team level", "weekly": "Program level", "monthly": "Executive level"},
        "escalation_triggers": "Defined triggers for escalation based on performance metrics"
    }

def _create_reporting_structure(teams: List) -> Dict[str, Any]:
    """Create program reporting structure"""
    return {
        "report_types": ["Status reports", "Risk reports", "Financial reports", "Quality reports"],
        "audience_mapping": {"teams": "Detailed reports", "executives": "Summary dashboards"},
        "reporting_schedule": "Weekly, monthly, and milestone-based reporting"
    }

def _establish_qa_processes(scope: str) -> Dict[str, Any]:
    """Establish quality assurance processes"""
    return {
        "quality_standards": "Defined quality standards and criteria",
        "review_processes": "Code reviews, design reviews, process reviews",
        "testing_strategy": "Unit, integration, system, and acceptance testing",
        "continuous_improvement": "Regular retrospectives and process improvements"
    }

def _generate_program_recommendations(coordination: Dict) -> List[str]:
    """Generate program management recommendations"""
    return [
        "Establish clear governance structure with defined roles and responsibilities",
        "Implement robust communication framework across all teams",
        "Create comprehensive risk management and mitigation strategies",
        "Set up automated monitoring and reporting systems"
    ]

def _define_program_action_items(coordination: Dict) -> List[Dict[str, str]]:
    """Define program action items"""
    return [
        {"action": "Set up program governance structure", "owner": "Program Manager", "due": "Week 1"},
        {"action": "Establish team communication channels", "owner": "Team Leads", "due": "Week 1"},
        {"action": "Create master program schedule", "owner": "Program Manager", "due": "Week 2"},
        {"action": "Implement monitoring and reporting tools", "owner": "PMO", "due": "Week 3"}
    ]

# Helper functions for development_engineer
def _design_system_architecture(arch_type: str, requirements: str) -> Dict[str, Any]:
    """Design system architecture"""
    return {
        "architecture_pattern": arch_type,
        "system_components": ["Frontend", "Backend", "Database", "Integration Layer"],
        "scalability_design": "Horizontal scaling with load balancers",
        "reliability_patterns": "Circuit breakers, retry mechanisms, failover"
    }

def _break_down_components(requirements: str) -> List[Dict[str, str]]:
    """Break down system into components"""
    return [
        {"component": "User Interface", "responsibility": "User interaction and presentation"},
        {"component": "Business Logic", "responsibility": "Core business rules and processing"},
        {"component": "Data Layer", "responsibility": "Data persistence and retrieval"},
        {"component": "Integration Layer", "responsibility": "External system communication"}
    ]

def _design_data_architecture(requirements: str) -> Dict[str, Any]:
    """Design data architecture"""
    return {
        "data_model": "Relational with NoSQL for specific use cases",
        "data_flow": "ETL processes for data integration",
        "data_security": "Encryption at rest and in transit",
        "backup_strategy": "Automated backups with point-in-time recovery"
    }

def _design_security_architecture(requirements: str) -> Dict[str, Any]:
    """Design security architecture"""
    return {
        "authentication": "Multi-factor authentication with SSO",
        "authorization": "Role-based access control",
        "data_protection": "Encryption and data masking",
        "security_monitoring": "SIEM and automated threat detection"
    }

def _analyze_tech_stack(stack: List, requirements: str) -> Dict[str, Any]:
    """Analyze technology stack"""
    return {
        "frontend": "React/Angular for web, React Native for mobile",
        "backend": "Node.js/Python for API services",
        "database": "PostgreSQL for relational, MongoDB for document storage",
        "infrastructure": "Docker containers on Kubernetes"
    }

def _recommend_frameworks(stack: List, arch_type: str) -> List[Dict[str, str]]:
    """Recommend development frameworks"""
    return [
        {"framework": "Express.js", "purpose": "Backend API development", "justification": "Lightweight and flexible"},
        {"framework": "React", "purpose": "Frontend development", "justification": "Component-based architecture"},
        {"framework": "Jest", "purpose": "Testing framework", "justification": "Comprehensive testing capabilities"}
    ]

def _recommend_development_tools(stack: List) -> List[Dict[str, str]]:
    """Recommend development tools"""
    return [
        {"tool": "VS Code", "purpose": "IDE", "justification": "Excellent extension ecosystem"},
        {"tool": "Git", "purpose": "Version control", "justification": "Industry standard"},
        {"tool": "Docker", "purpose": "Containerization", "justification": "Consistent environments"},
        {"tool": "Jenkins", "purpose": "CI/CD", "justification": "Automated deployment pipeline"}
    ]

def _identify_key_libraries(requirements: str, stack: List) -> List[Dict[str, str]]:
    """Identify key libraries and dependencies"""
    return [
        {"library": "Lodash", "purpose": "Utility functions", "version": "^4.17.21"},
        {"library": "Axios", "purpose": "HTTP client", "version": "^0.24.0"},
        {"library": "Moment.js", "purpose": "Date manipulation", "version": "^2.29.0"}
    ]

def _plan_development_phases(requirements: str) -> List[Dict[str, str]]:
    """Plan development phases"""
    return [
        {"phase": "Setup", "duration": "1 week", "activities": "Environment setup, tool configuration"},
        {"phase": "Core Development", "duration": "6 weeks", "activities": "Feature implementation"},
        {"phase": "Integration", "duration": "2 weeks", "activities": "System integration and testing"},
        {"phase": "Deployment", "duration": "1 week", "activities": "Production deployment and monitoring"}
    ]

def _define_coding_standards(stack: List) -> Dict[str, Any]:
    """Define coding standards"""
    return {
        "style_guide": "ESLint for JavaScript, PEP 8 for Python",
        "naming_conventions": "camelCase for variables, PascalCase for classes",
        "documentation": "JSDoc for JavaScript, docstrings for Python",
        "code_review": "All code must be reviewed before merge"
    }

def _create_testing_strategy(arch_type: str) -> Dict[str, Any]:
    """Create comprehensive testing strategy"""
    return {
        "unit_testing": "Jest for JavaScript, pytest for Python",
        "integration_testing": "API testing with Postman/Newman",
        "end_to_end_testing": "Cypress for web application testing",
        "performance_testing": "Load testing with JMeter",
        "security_testing": "OWASP ZAP for security scanning"
    }

def _plan_deployment_strategy(scalability: str) -> Dict[str, Any]:
    """Plan deployment strategy"""
    return {
        "deployment_model": "Blue-green deployment for zero downtime",
        "infrastructure": "Kubernetes for container orchestration",
        "monitoring": "Prometheus and Grafana for metrics",
        "logging": "ELK stack for centralized logging",
        "scaling": "Auto-scaling based on CPU and memory metrics"
    }

def _design_api_strategy(integration_points: List) -> Dict[str, Any]:
    """Design API strategy"""
    return {
        "api_design": "RESTful APIs with OpenAPI specification",
        "authentication": "OAuth 2.0 for secure API access",
        "rate_limiting": "API rate limiting to prevent abuse",
        "versioning": "Semantic versioning for API compatibility"
    }

def _plan_data_integration(integration_points: List) -> Dict[str, Any]:
    """Plan data integration"""
    return {
        "integration_patterns": "ETL for batch, streaming for real-time",
        "data_formats": "JSON for APIs, CSV for bulk data",
        "error_handling": "Retry mechanisms and dead letter queues",
        "monitoring": "Data quality monitoring and alerting"
    }

def _analyze_third_party_integrations(integration_points: List) -> List[Dict[str, str]]:
    """Analyze third-party integrations"""
    return [
        {"integration": "Payment Gateway", "method": "REST API", "complexity": "Medium"},
        {"integration": "Email Service", "method": "SMTP/API", "complexity": "Low"},
        {"integration": "Analytics Platform", "method": "JavaScript SDK", "complexity": "Low"}
    ]

def _plan_integration_testing(integration_points: List) -> Dict[str, Any]:
    """Plan integration testing"""
    return {
        "test_environments": "Dedicated integration testing environment",
        "test_data": "Synthetic test data for integration scenarios",
        "automation": "Automated integration test suite",
        "monitoring": "Integration health checks and monitoring"
    }

def _generate_engineering_recommendations(implementation: Dict) -> List[str]:
    """Generate engineering recommendations"""
    return [
        "Implement comprehensive testing strategy from the beginning",
        "Use infrastructure as code for consistent environments",
        "Establish CI/CD pipeline for automated deployments",
        "Implement monitoring and logging from day one",
        "Follow security best practices throughout development"
    ]

def _define_technical_tasks(implementation: Dict) -> List[Dict[str, str]]:
    """Define technical implementation tasks"""
    return [
        {"task": "Set up development environment", "priority": "High", "estimate": "2 days"},
        {"task": "Implement core business logic", "priority": "High", "estimate": "2 weeks"},
        {"task": "Develop API endpoints", "priority": "High", "estimate": "1 week"},
        {"task": "Implement database schema", "priority": "High", "estimate": "3 days"},
        {"task": "Set up CI/CD pipeline", "priority": "Medium", "estimate": "1 week"},
        {"task": "Implement monitoring and logging", "priority": "Medium", "estimate": "3 days"}
    ]
