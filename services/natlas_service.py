from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoConfig,
    BitsAndBytesConfig
)
import torch
from typing import Dict
from core.config import settings

class NATLaSService:
    """N-ATLaS Language Model Service with compatibility fixes"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.supported_languages = {
            'en': 'English',
            'yo': 'Yoruba',
            'ha': 'Hausa',
            'ig': 'Igbo',
            'pcm': 'Nigerian Pidgin'
        }

    async def initialize(self):
        """Load N-ATLaS model safely with rope_scaling patch"""
        print(f"🇳🇬 Loading N-ATLaS: {settings.NATLAS_MODEL}")
        print(f"🔧 Device: {self.device}")

        token = settings.HUGGINGFACE_HUB_TOKEN

        try:
            # Load tokenizer
            print("📝 Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.NATLAS_MODEL,
                trust_remote_code=True,
                use_auth_token=token,
                use_fast=False
            )

            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            print("✅ Tokenizer loaded")

            # Load config and patch rope_scaling
            print("⚙️ Loading model config...")
            config = AutoConfig.from_pretrained(
                settings.NATLAS_MODEL,
                trust_remote_code=True,
                use_auth_token=token
            )

            # Patch rope_scaling for LLaMA3 compatibility
            if hasattr(config, "rope_scaling") and isinstance(config.rope_scaling, dict):
                config.rope_scaling = {
                    "type": config.rope_scaling.get("type", "dynamic"),
                    "factor": config.rope_scaling.get("factor", 8.0)
                }

            print(f"✅ Config loaded: {config.model_type}")

            # 4-bit quantization config
            print("💾 Configuring 4-bit quantization...")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            # Load model
            print("🤖 Loading N-ATLaS model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.NATLAS_MODEL,
                config=config,
                quantization_config=quantization_config,
                device_map="auto",
                trust_remote_code=True,
                use_auth_token=token,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float16
            )

            print("✅ N-ATLaS loaded successfully!")
            print(f"💾 Approx. memory usage: 4-5GB")

        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"🔍 Error type: {type(e).__name__}")
            print("🔄 Attempting fallback load without quantization...")
            await self._load_fallback(token)

    async def _load_fallback(self, token: str):
        """Fallback loading without quantization"""
        try:
            print("⚠️ Loading without quantization (more memory)...")
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.NATLAS_MODEL,
                device_map="auto",
                trust_remote_code=True,
                use_auth_token=token,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float16,
                offload_folder="offload"
            )
            print("✅ Fallback loading successful")
        except Exception as e:
            print(f"❌ Fallback failed: {e}")
            raise RuntimeError(f"Cannot load N-ATLaS: {e}")

    async def analyze_symptoms(self, symptoms: str, language: str = "en") -> str:
        """Analyze symptoms"""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("N-ATLaS not initialized")

        prompt = f"""As a medical assistant, analyze these symptoms:

Symptoms: {symptoms}

Provide a brief analysis."""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.replace(prompt, "").strip()

    def detect_language(self, text: str) -> str:
        """Detect language"""
        text_lower = text.lower()

        if any(m in text_lower for m in ['ẹ', 'ọ', 'ṣ', 'bawo']):
            return 'yo'
        if any(m in text_lower for m in ['sannu', 'yaya', 'ina']):
            return 'ha'
        if any(m in text_lower for m in ['kedu', 'ndewo']):
            return 'ig'
        if sum(1 for m in ['wetin', 'dey', 'fit'] if m in text_lower.split()) >= 2:
            return 'pcm'
        return 'en'

    def get_model_info(self) -> Dict:
        """Return model info"""
        return {
            "model_name": settings.NATLAS_MODEL,
            "device": self.device,
            "quantization": "4-bit NF4" if hasattr(self.model, 'quantization_config') else "None",
            "supported_languages": self.supported_languages
        }
