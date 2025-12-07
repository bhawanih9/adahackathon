
import os
import json
from google.genai import types
from google.genai import Client

# Assuming adk functionality wrapper or using GenAI directly if ADK is distinct.
# Since ADK docs are new, we will build a robust class that uses the standard Gemini API 
# which is the core of what ADK likely wraps, but structured as an 'Agent'.

class PhysicsTutor:
    def __init__(self, model_name='gemini-3.0-pro'):
        self.client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = model_name
    
    def analyze_question(self, question, age):
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
            "example": "Real life example...",
            "diagram_description": "A short, clear description of what a diagram for this concept would look like."
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        try:
            parsed = json.loads(response.text)
            if isinstance(parsed, list):
                if len(parsed) > 0:
                    return parsed[0]
                else:
                    return {} # Return empty dict if empty list
            return parsed
        except:
             # Fallback
            return {
                "topic": " gravity",
                "explanation": "Gravity is the force that pulls things down. (Fallback)",
                "kannada_explanation": "ಗುರುತ್ವಾಕರ್ಷಣೆಯು ವಸ್ತುಗಳನ್ನು ಕೆಳಕ್ಕೆ ಎಳೆಯುವ ಶಕ್ತಿಯಾಗಿದೆ.",
                "formula": "F = mg",
                "example": "Dropping a ball.",
                "diagram_description": "A diagram showing a ball falling towards the earth with an arrow pointing down."
            }

    def generate_quiz(self, topic, age):
        prompt = f"""
        Create a multiple choice question about "{topic}" for a {age} year old student.
        Return ONLY valid JSON:
        {{
            "question": "The question string",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": "The correct option text",
            "feedback_correct": "Short praise in Kannada",
            "feedback_incorrect": "Short hint in Kannada"
        }}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
             config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        try:
            return json.loads(response.text)
        except:
             return {
                "question": "What is Gravity? (Fallback)",
                "options": ["Force", "Energy", "Speed", "Time"],
                "correct": "Force",
                "feedback_correct": "Sari!",
                "feedback_incorrect": "Tappu."
            }

    def chat(self, user_message, history, age):
        # history is a list of {"role": "user"/"model", "parts": ["text"]}
        system_inst = f"You are a helpful physics tutor for a {age} year old. Answer briefly and encourage curiosity. Also provide a Kannada translation for your answer."
        
        # Simple non-streaming chat
        # Reconstruct chat for API if needed, or just send prompt with context
        # For simplicity in this demo, we'll just send the last message with instruction
        prompt = f"""
        System: {system_inst}
        User: {user_message}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
