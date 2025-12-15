from typing import List, Dict
import re

class SafetyService:
    """Medical safety and red flag detection service"""
    
    # Critical red flags that require immediate medical attention
    RED_FLAGS = {
        "chest_pain": {
            "patterns": [
                r"chest pain",
                r"heart pain",
                r"tightness in chest",
                r"crushing sensation",
                r"pressure in chest"
            ],
            "severity": "EMERGENCY",
            "message": "Chest pain may indicate a heart attack. Call emergency services immediately."
        },
        "breathing": {
            "patterns": [
                r"can't breathe",
                r"difficulty breathing",
                r"shortness of breath",
                r"gasping for air",
                r"unable to breathe"
            ],
            "severity": "EMERGENCY",
            "message": "Severe breathing difficulty requires immediate medical attention."
        },
        "consciousness": {
            "patterns": [
                r"unconscious",
                r"passed out",
                r"losing consciousness",
                r"fainting repeatedly",
                r"blacking out"
            ],
            "severity": "EMERGENCY",
            "message": "Loss of consciousness is a medical emergency. Call 911/emergency services."
        },
        "severe_bleeding": {
            "patterns": [
                r"heavy bleeding",
                r"won't stop bleeding",
                r"bleeding profusely",
                r"blood won't clot"
            ],
            "severity": "EMERGENCY",
            "message": "Uncontrolled bleeding requires immediate medical attention."
        },
        "stroke": {
            "patterns": [
                r"face drooping",
                r"arm weakness",
                r"speech difficulty",
                r"sudden confusion",
                r"vision loss sudden"
            ],
            "severity": "EMERGENCY",
            "message": "These symptoms may indicate a stroke. Call emergency services immediately. Remember FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911."
        },
        "mental_health_crisis": {
            "patterns": [
                r"want to die",
                r"kill myself",
                r"end my life",
                r"suicide",
                r"not worth living"
            ],
            "severity": "CRISIS",
            "message": "Please contact a crisis helpline immediately. National Suicide Prevention Lifeline: 988. You're not alone, and help is available."
        },
        "severe_abdominal_pain": {
            "patterns": [
                r"severe abdominal pain",
                r"intense stomach pain",
                r"sharp belly pain",
                r"vomiting blood"
            ],
            "severity": "URGENT",
            "message": "Severe abdominal pain may indicate a serious condition. Seek medical attention promptly."
        },
        "head_injury": {
            "patterns": [
                r"head injury",
                r"hit my head hard",
                r"concussion",
                r"severe headache after trauma"
            ],
            "severity": "URGENT",
            "message": "Head injuries should be evaluated by a medical professional."
        }
    }
    
    def detect_red_flags(self, symptoms_text: str) -> List[Dict]:
        """Detect emergency red flags in symptom text"""
        detected_flags = []
        symptoms_lower = symptoms_text.lower()
        
        for flag_category, flag_data in self.RED_FLAGS.items():
            for pattern in flag_data["patterns"]:
                if re.search(pattern, symptoms_lower):
                    detected_flags.append({
                        "category": flag_category,
                        "severity": flag_data["severity"],
                        "message": f"⚠️ {flag_data['severity']}: {flag_data['message']}"
                    })
                    break  # Only add once per category
        
        return detected_flags
    
    def get_disclaimer(self) -> str:
        """Get medical disclaimer"""
        return (
            "⚕️ IMPORTANT MEDICAL DISCLAIMER: This AI-powered tool is for "
            "informational and educational purposes only. It does NOT provide "
            "medical advice, diagnosis, or treatment. Always consult with a "
            "qualified healthcare professional for medical concerns. In case of "
            "emergency, call your local emergency services immediately."
        )
    
    def get_recommendations(self, red_flags: List[Dict]) -> List[str]:
        """Get safety recommendations based on detected red flags"""
        recommendations = []
        
        if any(flag["severity"] == "EMERGENCY" for flag in red_flags):
            recommendations.append("🚨 CALL EMERGENCY SERVICES IMMEDIATELY")
            recommendations.append("Do not wait - this could be life-threatening")
        elif any(flag["severity"] == "CRISIS" for flag in red_flags):
            recommendations.append("📞 Contact a crisis helpline now - help is available 24/7")
            recommendations.append("National Suicide Prevention Lifeline: 988")
        elif any(flag["severity"] == "URGENT" for flag in red_flags):
            recommendations.append("⏰ Seek medical attention within 24 hours")
            recommendations.append("Consider visiting urgent care or emergency department")
        else:
            recommendations.append("✅ Monitor your symptoms")
            recommendations.append("Consult a healthcare provider if symptoms worsen")
            recommendations.append("Keep a symptom diary to share with your doctor")
        
        return recommendations