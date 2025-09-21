import os
import json
from openai import OpenAI
import streamlit as st

class OpenAIClient:
    def __init__(self):
        # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
        # do not change this unless explicitly requested by the user
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
            return
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-5"
    
    def get_empathetic_response(self, user_message, persona="therapist", conversation_history=None):
        """Generate empathetic response based on selected persona"""
        
        persona_prompts = {
            "peer": """You are a supportive peer who understands youth struggles. Respond with empathy, 
                      shared experiences, and encouragement. Use casual, relatable language while being supportive.""",
            "mentor": """You are a wise mentor who provides guidance and perspective. Share insights and 
                        gentle advice while being understanding and non-judgmental.""",
            "therapist": """You are a compassionate therapist trained in CBT techniques. Provide professional 
                           but warm support, ask reflective questions, and suggest coping strategies."""
        }
        
        system_prompt = f"""
        {persona_prompts.get(persona, persona_prompts["therapist"])}
        
        IMPORTANT SAFETY PROTOCOLS:
        - If you detect ANY signs of crisis, suicidal thoughts, self-harm, or immediate danger, 
          immediately respond with crisis resources and encourage professional help
        - Always maintain boundaries - you are supportive but not a replacement for professional help
        - Be empathetic, non-judgmental, and culturally sensitive
        - Focus on evidence-based techniques and positive coping strategies
        - If unsure about safety, err on the side of caution and suggest professional resources
        
        Remember: You're talking to a young person who may be vulnerable. Be especially gentle and supportive.
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Keep last 10 messages for context
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Type conversion for OpenAI messages is handled by the library
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I'm having trouble connecting right now. Please try again, or if this is urgent, please contact crisis resources at 988."
    
    def analyze_sentiment_and_risk(self, text):
        """Analyze sentiment and assess crisis risk level"""
        
        system_prompt = """
        You are a mental health risk assessment tool. Analyze the text for:
        1. Overall sentiment (1-10, where 1 is very negative, 10 is very positive)
        2. Crisis risk level (low, moderate, high, critical)
        3. Key emotional indicators
        4. Suggested intervention level
        
        CRITICAL: Flag anything indicating suicidal ideation, self-harm, or immediate danger as "critical"
        
        Respond in JSON format:
        {
            "sentiment_score": number,
            "risk_level": "low|moderate|high|critical",
            "emotional_indicators": ["emotion1", "emotion2"],
            "intervention_needed": "none|support|professional|crisis",
            "confidence": number
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content or "{}")
            return result
            
        except Exception as e:
            # Default to moderate risk if analysis fails
            return {
                "sentiment_score": 5,
                "risk_level": "moderate",
                "emotional_indicators": ["unknown"],
                "intervention_needed": "support",
                "confidence": 0.1
            }
    
    def generate_cbt_insight(self, thought_record):
        """Generate CBT-based insights for thought records"""
        
        system_prompt = """
        You are a CBT-trained assistant. Analyze the thought record and provide:
        1. Identified cognitive distortions
        2. Balanced perspective suggestions
        3. Evidence-based challenges to negative thoughts
        4. Practical coping strategies
        
        Be supportive and educational. Format as JSON:
        {
            "cognitive_distortions": ["distortion1", "distortion2"],
            "balanced_thoughts": ["thought1", "thought2"],
            "evidence_challenges": ["challenge1", "challenge2"],
            "coping_strategies": ["strategy1", "strategy2"],
            "encouragement": "supportive message"
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Thought record: {json.dumps(thought_record)}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.6
            )
            
            return json.loads(response.choices[0].message.content or "{}")
            
        except Exception as e:
            return {
                "cognitive_distortions": ["Unable to analyze at this time"],
                "balanced_thoughts": ["Consider multiple perspectives on this situation"],
                "evidence_challenges": ["What evidence supports and contradicts this thought?"],
                "coping_strategies": ["Take deep breaths and practice self-compassion"],
                "encouragement": "Remember, thoughts are not facts. You're doing great by reflecting on them."
            }
    
    def generate_personalized_journal_prompt(self, mood_data, recent_entries):
        """Generate personalized journal prompt based on user's current state"""
        
        system_prompt = """
        Generate a personalized journal prompt based on the user's mood and recent entries.
        Make it supportive, relevant, and designed to promote self-reflection and growth.
        
        Consider:
        - Current emotional state
        - Recent patterns or themes
        - CBT principles
        - Age-appropriate language for youth
        
        Return as JSON:
        {
            "prompt": "The personalized journal prompt",
            "focus_area": "emotional_awareness|coping_skills|gratitude|goals|relationships",
            "follow_up_questions": ["question1", "question2"]
        }
        """
        
        context = f"Mood data: {mood_data}\nRecent entries themes: {recent_entries}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            
            return json.loads(response.choices[0].message.content or "{}")
            
        except Exception as e:
            return {
                "prompt": "What's one thing you're grateful for today, and how did it make you feel?",
                "focus_area": "gratitude",
                "follow_up_questions": [
                    "How can you create more moments like this?",
                    "What would you tell a friend feeling the same way?"
                ]
            }
