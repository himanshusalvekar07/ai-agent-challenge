"""
Advanced tools and capabilities for the Karbon AI Agent
"""
import json
import re
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

class AgentTools:
    """Collection of tools that agents can use"""
    
    def __init__(self):
        self.tools = {
            "code_analyzer": self.analyze_code,
            "data_processor": self.process_data,
            "text_summarizer": self.summarize_text,
            "research_helper": self.research_helper,
            "creative_generator": self.creative_generator
        }
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze code for potential issues and improvements"""
        analysis = {
            "language": language,
            "lines_of_code": len(code.split('\n')),
            "complexity_score": 0,
            "suggestions": [],
            "issues": []
        }
        
        # Basic code analysis
        lines = code.split('\n')
        
        # Count complexity indicators
        complexity_indicators = ['if', 'for', 'while', 'try', 'except', 'with', 'def', 'class']
        complexity_score = 0
        
        for line in lines:
            line_stripped = line.strip().lower()
            for indicator in complexity_indicators:
                if indicator in line_stripped:
                    complexity_score += 1
        
        analysis["complexity_score"] = complexity_score
        
        # Basic suggestions based on patterns
        if language.lower() == "python":
            # Check for common Python issues
            if "import *" in code:
                analysis["issues"].append("Avoid wildcard imports (import *)")
            
            if re.search(r'except:', code):
                analysis["issues"].append("Use specific exception types instead of bare except")
            
            if len([line for line in lines if len(line) > 80]) > 0:
                analysis["suggestions"].append("Consider breaking long lines (>80 characters)")
            
            if code.count("print(") > 5:
                analysis["suggestions"].append("Consider using logging instead of multiple print statements")
        
        return analysis
    
    def process_data(self, data: Any, operation: str = "summary") -> Dict[str, Any]:
        """Process data and provide insights"""
        result = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "data_type": type(data).__name__,
            "result": None
        }
        
        try:
            if isinstance(data, (list, tuple)):
                if operation == "summary":
                    result["result"] = {
                        "count": len(data),
                        "data_types": list(set(type(item).__name__ for item in data)),
                        "sample": data[:5] if len(data) > 5 else data
                    }
                elif operation == "statistics" and all(isinstance(x, (int, float)) for x in data):
                    result["result"] = {
                        "mean": sum(data) / len(data),
                        "min": min(data),
                        "max": max(data),
                        "count": len(data)
                    }
            
            elif isinstance(data, dict):
                result["result"] = {
                    "keys": list(data.keys()),
                    "key_count": len(data),
                    "value_types": list(set(type(v).__name__ for v in data.values()))
                }
            
            elif isinstance(data, str):
                result["result"] = {
                    "length": len(data),
                    "word_count": len(data.split()),
                    "line_count": len(data.split('\n'))
                }
                
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> Dict[str, Any]:
        """Summarize text content"""
        sentences = text.split('. ')
        
        # Simple extractive summarization
        word_freq = {}
        words = text.lower().split()
        
        for word in words:
            word = re.sub(r'[^\w]', '', word)
            if word and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = sentence.lower().split()
            score = 0
            word_count = 0
            
            for word in sentence_words:
                word = re.sub(r'[^\w]', '', word)
                if word in word_freq:
                    score += word_freq[word]
                    word_count += 1
            
            if word_count > 0:
                sentence_scores[sentence] = score / word_count
        
        # Get top sentences
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        summary_sentences = [sent[0] for sent in top_sentences[:max_sentences]]
        
        return {
            "original_length": len(text),
            "summary_length": len('. '.join(summary_sentences)),
            "compression_ratio": len('. '.join(summary_sentences)) / len(text) if text else 0,
            "summary": '. '.join(summary_sentences),
            "key_words": list(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def research_helper(self, topic: str) -> Dict[str, Any]:
        """Help with research by providing structured information"""
        return {
            "topic": topic,
            "research_framework": {
                "key_questions": [
                    f"What is {topic}?",
                    f"Why is {topic} important?",
                    f"What are the current trends in {topic}?",
                    f"What are the challenges related to {topic}?",
                    f"What is the future outlook for {topic}?"
                ],
                "research_areas": [
                    "Background and definition",
                    "Current state and trends",
                    "Key players and stakeholders",
                    "Challenges and opportunities",
                    "Future predictions and implications"
                ],
                "suggested_sources": [
                    "Academic databases",
                    "Industry reports",
                    "Government publications",
                    "Expert interviews",
                    "Case studies"
                ]
            },
            "analysis_framework": {
                "strengths": [],
                "weaknesses": [], 
                "opportunities": [],
                "threats": []
            }
        }
    
    def creative_generator(self, prompt: str, creative_type: str = "ideas") -> Dict[str, Any]:
        """Generate creative content and ideas"""
        templates = {
            "story_outline": {
                "structure": ["Setup", "Inciting Incident", "Rising Action", "Climax", "Falling Action", "Resolution"],
                "elements": ["Character", "Setting", "Conflict", "Theme", "Plot Twist"]
            },
            "brainstorm": {
                "techniques": ["Mind Mapping", "SCAMPER", "Six Thinking Hats", "Random Word", "What If..."],
                "categories": ["Traditional", "Innovative", "Disruptive", "Improvement", "Combination"]
            },
            "content_ideas": {
                "formats": ["Blog Post", "Video", "Infographic", "Podcast", "Social Media", "Newsletter"],
                "angles": ["How-to", "List", "Case Study", "Interview", "Review", "Comparison"]
            }
        }
        
        result = {
            "prompt": prompt,
            "creative_type": creative_type,
            "timestamp": datetime.now().isoformat(),
            "suggestions": []
        }
        
        if creative_type in templates:
            result["framework"] = templates[creative_type]
        
        # Generate basic creative suggestions based on prompt
        keywords = prompt.lower().split()
        result["inspiration_points"] = [
            f"Explore the intersection of {keywords[0] if keywords else 'your topic'} and technology",
            f"Consider the human story behind {prompt}",
            f"What would happen if {prompt} didn't exist?",
            f"How might {prompt} evolve in the next 10 years?",
            f"What can we learn from failures in {prompt}?"
        ]
        
        return result

class TaskPlanner:
    """Plan and break down complex tasks"""
    
    def __init__(self):
        self.task_templates = {
            "coding_project": [
                "Define requirements",
                "Design architecture", 
                "Set up development environment",
                "Implement core features",
                "Add error handling",
                "Write tests",
                "Documentation",
                "Code review",
                "Deployment preparation"
            ],
            "research_project": [
                "Define research question",
                "Literature review",
                "Methodology selection",
                "Data collection",
                "Data analysis", 
                "Results interpretation",
                "Report writing",
                "Peer review",
                "Presentation preparation"
            ],
            "content_creation": [
                "Topic research",
                "Audience analysis",
                "Content outline",
                "First draft",
                "Review and edit",
                "Visual elements",
                "SEO optimization",
                "Proofreading",
                "Publishing and promotion"
            ]
        }
    
    def create_task_plan(self, task_description: str, task_type: str = "general") -> Dict[str, Any]:
        """Create a structured task plan"""
        plan = {
            "task": task_description,
            "type": task_type,
            "created": datetime.now().isoformat(),
            "estimated_duration": "To be determined",
            "priority": "Medium",
            "steps": []
        }
        
        if task_type in self.task_templates:
            plan["steps"] = [
                {
                    "step_number": i + 1,
                    "title": step,
                    "status": "Not Started",
                    "estimated_time": "TBD",
                    "dependencies": []
                }
                for i, step in enumerate(self.task_templates[task_type])
            ]
        else:
            # Generic task breakdown
            plan["steps"] = [
                {"step_number": 1, "title": "Analyze requirements", "status": "Not Started"},
                {"step_number": 2, "title": "Plan approach", "status": "Not Started"},
                {"step_number": 3, "title": "Execute main task", "status": "Not Started"},
                {"step_number": 4, "title": "Review and refine", "status": "Not Started"},
                {"step_number": 5, "title": "Finalize and deliver", "status": "Not Started"}
            ]
        
        return plan

# Initialize global tools instance
agent_tools = AgentTools()
task_planner = TaskPlanner()