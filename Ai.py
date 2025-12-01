import os
import json
from typing import List, Dict, Optional
from anthropic import Anthropic


class AIProcessor:
    """Handles all AI-powered features using the Claude API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI processor.
        
        Args:
            api_key: Anthropic API key. If None, will try to read from ANTHROPIC_API_KEY env variable.
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def categorize_card(self, question: str, answer: str) -> List[str]:
        """
        Categorize a flashcard using Claude API.
        
        Args:
            question: The flashcard question
            answer: The flashcard answer
            
        Returns:
            List of hierarchical category strings (e.g., ["Biology > Cell Biology", "Science > Life Sciences"])
        """
        prompt = f"""Analyze this flashcard and provide 1-3 hierarchical categories that best describe its content.

Question: {question}
Answer: {answer}

Return ONLY a JSON array of category strings in the format "MainCategory > Subcategory > SpecificTopic".
Use standard academic/professional categories when applicable.

Examples:
- ["Mathematics > Algebra > Linear Equations"]
- ["History > World History > Ancient Rome", "Social Studies > Civilizations"]
- ["Programming > Python > Data Structures"]

Return only the JSON array, no other text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract text from response
            response_text = response.content[0].text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else response_text
            
            # Parse JSON response
            categories = json.loads(response_text)
            
            # Validate that we got a list of strings
            if not isinstance(categories, list):
                raise ValueError("API did not return a list")
            
            # Filter and validate categories
            valid_categories = [
                cat.strip() for cat in categories 
                if isinstance(cat, str) and cat.strip()
            ]
            
            return valid_categories[:3]  # Limit to 3 categories max
            
        except json.JSONDecodeError as e:
            print(f"Error parsing API response: {e}")
            print(f"Response was: {response_text}")
            return ["General > Uncategorized"]
        except Exception as e:
            print(f"Error calling Claude API for categorization: {e}")
            return ["General > Uncategorized"]
    
    def generate_report(self, performance_data: Dict) -> str:
        if not performance_data:
            return "No performance data available yet. Start reviewing cards to see your progress!"
        
        # Format performance data for the prompt
        performance_summary = []
        for category_path, perf in performance_data.items():
            accuracy = (perf.correct / perf.attempts * 100) if perf.attempts > 0 else 0
            performance_summary.append({
                "category": category_path,
                "attempts": perf.attempts,
                "correct": perf.correct,
                "accuracy": f"{accuracy:.1f}%",
                "multiplier": f"{perf.multiplier}x"
            })
        
        # Sort by attempts (most practiced first)
        performance_summary.sort(key=lambda x: x["attempts"], reverse=True)
        
        prompt = f"""Analyze this student's flashcard performance data and provide a comprehensive report.

Performance Data:
{json.dumps(performance_summary, indent=2)}

Please provide:
1. **Strengths**: Which categories/topics the student is performing well in (>80% accuracy)
2. **Areas for Improvement**: Which categories need more practice (<70% accuracy)
3. **Study Recommendations**: Specific, actionable advice based on the patterns you see
4. **Progress Insights**: Any notable patterns or trends in their learning

Format your response in clear sections with markdown formatting. Be encouraging but honest. Keep it concise (300-400 words)."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract text from response
            report = response.content[0].text.strip()
            return report
            
        except Exception as e:
            print(f"Error calling Claude API for report generation: {e}")
            return f"Unable to generate report at this time. Error: {str(e)}"


# Convenience functions for module-level usage
_processor_instance: Optional[AIProcessor] = None


def initialize_ai_processor(api_key: Optional[str] = None):
    """Initialize the global AI processor instance."""
    global _processor_instance
    _processor_instance = AIProcessor(api_key)


def categorize_card(question: str, answer: str) -> List[str]:
    if _processor_instance is None:
        raise RuntimeError("AI Processor not initialized. Call initialize_ai_processor() first.")
    return _processor_instance.categorize_card(question, answer)


def generate_report(performance_data: Dict) -> str:
    if _processor_instance is None:
        raise RuntimeError("AI Processor not initialized. Call initialize_ai_processor() first.")
    return _processor_instance.generate_report(performance_data)
