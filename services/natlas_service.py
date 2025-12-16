from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
from typing import Dict, Optional
from core.config import settings

class NATLaSService:
    """
    N-ATLaS Language Model Service with 4-bit Quantization
    Reduces memory usage from 16GB to ~4GB
    """
    
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
        """Load N-ATLaS model with 4-bit quantization"""
        print(f"🇳🇬 Loading N-ATLaS with 4-bit quantization: {settings.NATLAS_MODEL}")
        print(f"🔧 Device: {self.device}")
        print(f"💾 Using 4-bit quantization to reduce memory usage")
        
        try:
            # Load tokenizer
            print("📝 Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                settings.NATLAS_MODEL,
                trust_remote_code=True,
                token=settings.HUGGINGFACE_HUB_TOKEN,
                force_download=True
            )
            print("✅ Tokenizer loaded")
            
            # Configure 4-bit quantization
            print("⚙️ Configuring 4-bit quantization...")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,                          # Enable 4-bit loading
                bnb_4bit_compute_dtype=torch.float16,       # Compute in float16
                bnb_4bit_quant_type="nf4",                  # Normal Float 4-bit
                bnb_4bit_use_double_quant=True,             # Double quantization
            )
            
            # Load model with quantization
            print("🤖 Loading N-ATLaS model (this may take 2-3 minutes)...")
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.NATLAS_MODEL,
                quantization_config=quantization_config,
                token=settings.HUGGINGFACE_HUB_TOKEN,
                device_map="auto",                           # Auto device placement
                trust_remote_code=True,
                low_cpu_mem_usage=True,                      # Optimize CPU memory
                torch_dtype=torch.float16,                   # Use float16
                force_download=True
            )
            
            print("✅ N-ATLaS model loaded successfully!")
            print(f"💾 Memory usage: ~4-5GB (vs ~16GB unquantized)")
            print(f"🌍 Languages: {', '.join(self.supported_languages.values())}")
            
        except Exception as e:
            print(f"❌ Error loading N-ATLaS: {e}")
            print(f"💡 Tip: Make sure bitsandbytes is installed: pip install bitsandbytes")
            raise RuntimeError(f"Failed to load N-ATLaS model: {e}")
    
    async def analyze_symptoms(self, symptoms: str, language: str = "en") -> str:
        """
        Analyze symptoms using quantized N-ATLaS
        
        Args:
            symptoms: Patient symptom description
            language: Language code (en, yo, ha, ig, pcm)
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("N-ATLaS service not initialized")
        
        # Create medical analysis prompt
        prompt = f"""As a medical assistant, analyze these symptoms briefly:

Symptoms: {symptoms}

Provide a concise analysis with possible conditions and recommendations."""
        
        # Tokenize with reduced context (saves memory)
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512  # Reduced from 2048 to save memory
        ).to(self.device)
        
        # Generate response with reduced length
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,      # Reduced from 512
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove prompt from response
        response = response.replace(prompt, "").strip()
        
        return response
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text using pattern matching
        
        Args:
            text: Input text
            
        Returns:
            Language code (en, yo, ha, ig, pcm)
        """
        text_lower = text.lower()
        
        # Yoruba markers (special characters and common words)
        yoruba_markers = ['ẹ', 'ọ', 'ṣ', 'bawo', 'se', 'ni', 'mo', 'ti']
        if any(marker in text_lower for marker in yoruba_markers):
            return 'yo'
        
        # Hausa markers
        hausa_markers = ['sannu', 'yaya', 'ina', 'da', 'ciwon', 'kai']
        if any(marker in text_lower for marker in hausa_markers):
            return 'ha'
        
        # Igbo markers
        igbo_markers = ['kedu', 'ndewo', 'enwere', 'nwere']
        if any(marker in text_lower for marker in igbo_markers):
            return 'ig'
        
        # Pidgin markers (need at least 2 for confidence)
        pidgin_markers = ['wetin', 'dey', 'fit', 'no', 'go', 'make', 'dem']
        pidgin_count = sum(1 for marker in pidgin_markers if marker in text_lower.split())
        if pidgin_count >= 2:
            return 'pcm'
        
        # Default to English
        return 'en'
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        return {
            "model_name": settings.NATLAS_MODEL,
            "architecture": "Llama-3 8B (4-bit quantized)",
            "device": self.device,
            "quantization": "4-bit NF4",
            "memory_usage": "~4-5GB",
            "supported_languages": self.supported_languages,
            "developer": "Awarri Technologies + FMCIDE Nigeria"
        }