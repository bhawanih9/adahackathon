
import os
import json
from google.genai import types
from google.genai import Client

# --- Sub-Agents ---

class ConceptAgent:
    """Specialized in explaining physics concepts and translation."""
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def analyze(self, question, age):
        prompt = f"""
        You are an expert Physics Tutor for a {age} year old student.
        Analyze the following question: "{question}"
        
        Identify the core physics topic.
        Provide a simplification explanation suitable for a {age} year old.
        Provide a standard physics formula related to it.
        Provide a real-life example suitable for a {age} year old.
        Translate the explanation to Kannada.
        
        Return ONLY valid JSON with this structure:
        {{
            "topic": "Topic Name",
            "explanation": "English explanation...",
            "kannada_explanation": "Kannada translation...",
            "formula": "Formula",
            "example": "Real life example..."
        }}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        try:
            parsed = json.loads(response.text)
            if isinstance(parsed, list):
                parsed = parsed[0] if len(parsed) > 0 else {}
            return parsed
        except:
             return {
                "topic": "Gravity",
                "explanation": "Gravity is the force that pulls things down.",
                "kannada_explanation": "ಗುರುತ್ವಾಕರ್ಷಣೆಯು ವಸ್ತುಗಳನ್ನು ಕೆಳಕ್ಕೆ ಎಳೆಯುವ ಶಕ್ತಿಯಾಗಿದೆ.",
                "formula": "F = mg",
                "example": "Dropping a ball."
            }

class ImageAgent:
    """Specialized in creating visual descriptions for diagrams."""
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def generate_prompt(self, topic, explanation):
        prompt = f"""
        create a description for a physics diagram about "{topic}".
        Context: {explanation}
        
        Return ONLY valid JSON:
        {{
            "diagram_description": "A short description...",
            "image_prompt": "A prompt for an image generator (e.g. concept physics diagram educational)"
        }}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
             config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        try:
            parsed = json.loads(response.text)
            if isinstance(parsed, list):
                parsed = parsed[0] if len(parsed) > 0 else {}
            
            # Sanitization
            if 'image_prompt' not in parsed:
                parsed['image_prompt'] = f"{topic} physics diagram"
            
            return parsed
        except:
            return {
                "diagram_description": "A diagram showing the concept.",
                "image_prompt": f"{topic} physics diagram"
            }

class QuizAgent:
    """Specialized in creating assessment quizzes."""
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def generate(self, topic, age):
        prompt = f"""
        Create 5 multiple choice questions about "{topic}" for a {age} year old student.
        Return ONLY valid JSON with this structure:
        {{
            "questions": [
                {{
                    "id": 1,
                    "question": "Question text",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": "Correct Option Text",
                    "feedback_correct": "Short praise in Kannada",
                    "feedback_incorrect": "Short hint in Kannada"
                }},
                ... (4 more)
            ]
        }}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
             config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        try:
            parsed = json.loads(response.text)
            if isinstance(parsed, list):
                parsed = parsed[0] if len(parsed) > 0 else {}
            
            if 'questions' not in parsed:
                 if isinstance(parsed, list) and len(parsed) > 0 and 'question' in parsed[0]:
                     parsed = {"questions": parsed}
                 else:
                     raise ValueError("Invalid format")
            return parsed
        except:
             return {
                "questions": [
                    { "id": 1, "question": "Fallback Q1", "options": ["A","B"], "correct": "A", "feedback_correct": "Sari", "feedback_incorrect": "Tappu" }
                ]
            }

# --- Coordinator Agent ---

class PhysicsTutor:
    def __init__(self, model_name='gemini-2.0-flash-exp'):
        self.client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = model_name
        
        # Initialize Sub-Agents
        self.concept_agent = ConceptAgent(self.client, self.model)
        self.image_agent = ImageAgent(self.client, self.model)
        self.quiz_agent = QuizAgent(self.client, self.model)
    
    def analyze_question(self, question, age):
        # Step 1: Get Concept Analysis
        concept_data = self.concept_agent.analyze(question, age)
        
        # Step 2: Get Image Prompt (using the topic from step 1)
        topic = concept_data.get('topic', 'Physics')
        explanation = concept_data.get('explanation', '')
        image_data = self.image_agent.generate_prompt(topic, explanation)
        
        # Merge Data
        result = {**concept_data, **image_data}
        return result

    def generate_quiz(self, topic, age):
        return self.quiz_agent.generate(topic, age)

    def chat(self, user_message, history, age):
        # Direct chat can be handled by Concept Agent logic or simple pass-through
        system_inst = f"You are a helpful physics tutor for a {age} year old. Answer briefly and encourage curiosity. Also provide a Kannada translation for your answer."
        prompt = f"""
        System: {system_inst}
        User: {user_message}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
