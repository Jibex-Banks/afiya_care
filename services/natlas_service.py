from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Optional, Dict
from core.config import settings


class NATLaSService:
    """
    N-ATLaS Language Model Service
    Nigerian Atlas for Languages & AI at Scale
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.supported_languages = {
            'en': 'English (Nigerian accent)',
            'yo': 'Yoruba',
            'ha': 'Hausa',
            'ig': 'Igbo',
            'pcm': 'Nigerian Pidgin'
        }
        
    async def initialize(self):
        """Load N-ATLaS model and tokenizer"""
        print(f"🇳🇬 Loading N-ATLaS model: {settings.NATLAS_MODEL}")
        print(f"🔧 Using device: {self.device}")
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.NATLAS_MODEL,
                trust_remote_code=True,
                use_fast=False, 
                token=settings.HF_TOKEN,
            )
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.NATLAS_MODEL,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            print("✅ N-ATLaS model loaded successfully")
            print(f"📊 Model size: ~8B parameters (Llama-3 based)")
            print(f"🌍 Languages: {', '.join(self.supported_languages.values())}")
            
        except Exception as e:
            print(f"❌ Error loading N-ATLaS: {e}")
            raise RuntimeError(f"Failed to load N-ATLaS model: {e}")
    
    async def generate_response(
        self,
        prompt: str,
        language: Optional[str] = "en",
        max_length: int = None,
        temperature: float = None,
        top_p: float = None
    ) -> str:
        """
        Generate response using N-ATLaS
        
        Args:
            prompt: Input prompt/question
            language: Language code (en, yo, ha, ig, pcm)
            max_length: Maximum response length
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("N-ATLaS service not initialized")
        
        # Set defaults
        max_length = max_length or settings.NATLAS_MAX_LENGTH
        temperature = temperature or settings.NATLAS_TEMPERATURE
        top_p = top_p or settings.NATLAS_TOP_P
        
        # Format prompt for N-ATLaS
        formatted_prompt = self._format_prompt(prompt, language)
        
        # Tokenize
        inputs = self.tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=max_length
        ).to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from response
        response = response.replace(formatted_prompt, "").strip()
        
        return response
    
    def _format_prompt(self, prompt: str, language: str) -> str:
        """
        Format prompt for N-ATLaS based on language
        """
        lang_prefixes = {
            'en': '',  # Default
            'yo': '[Yoruba] ',
            'ha': '[Hausa] ',
            'ig': '[Igbo] ',
            'pcm': '[Pidgin] '
        }
        
        prefix = lang_prefixes.get(language, '')
        return f"{prefix}{prompt}"
    
    async def analyze_symptoms_natlas(
        self,
        symptoms: str,
        language: str = "en"
    ) -> Dict:
        """
        Use N-ATLaS to analyze symptoms in local languages
        
        Args:
            symptoms: Patient symptom description
            language: Language of the symptoms
        """
        # Create medical analysis prompt
        prompt = f"""As a medical assistant, analyze these symptoms and provide:
1. Possible conditions
2. Severity level
3. Recommendations

Symptoms: {symptoms}

Provide a clear, helpful response."""
        
        # Generate response
        response = await self.generate_response(
            prompt=prompt,
            language=language,
            max_length=1024,
            temperature=0.7
        )
        
        return {
            "analysis": response,
            "language": language,
            "model": "N-ATLaS"
        }
    
    async def translate_medical_info(
        self,
        text: str,
        target_language: str
    ) -> str:
        """
        Translate medical information to local language
        
        Args:
            text: Text to translate
            target_language: Target language code
        """
        prompt = f"Translate the following medical information to {self.supported_languages.get(target_language, 'English')}:\n\n{text}"
        
        translation = await self.generate_response(
            prompt=prompt,
            language=target_language,
            max_length=512
        )
        
        return translation
    
    def get_model_info(self) -> Dict:
        """Get N-ATLaS model information"""
        return {
            "model_name": settings.NATLAS_MODEL,
            "architecture": "Llama-3 8B (Fine-tuned)",
            "device": self.device,
            "supported_languages": self.supported_languages,
            "developer": "Awarri Technologies + FMCIDE Nigeria",
            "training_tokens": "391M+ multilingual tokens",
            "release": "September 2025"
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text (basic implementation)
        """
        text_lower = text.lower()
        
        # Yoruba markers
        yoruba_markers = ['ẹ', 'ọ', 'ṣ', 'bawo', 'e se', 'omo']
        if any(marker in text_lower for marker in yoruba_markers):
            return 'yo'
        
        # Hausa markers
        hausa_markers = ['sannu', 'yaya', 'ina', 'ƙ', 'ɗ']
        if any(marker in text_lower for marker in hausa_markers):
            return 'ha'
        
        # Igbo markers
        igbo_markers = ['kedu', 'ndewo', 'ị', 'ụ']
        if any(marker in text_lower for marker in igbo_markers):
            return 'ig'
        
        # Pidgin markers
        pidgin_markers = ['wetin', 'dey', 'no', 'go', 'fit']
        pidgin_count = sum(1 for marker in pidgin_markers if marker in text_lower.split())
        if pidgin_count >= 2:
            return 'pcm'
        
        return 'en'  # Default to English