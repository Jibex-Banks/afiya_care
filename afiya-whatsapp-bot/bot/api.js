const axios = require('axios');

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000/api/v1';
const API_TIMEOUT = 30000; // 30 seconds

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Get diagnosis from FastAPI backend
async function getDiagnosis(symptoms, language = 'en') {
  try {
    console.log(`🔄 API Call: POST /diagnose`);
    console.log(`   Symptoms: ${symptoms.substring(0, 50)}...`);
    console.log(`   Language: ${language}`);
    
    const response = await apiClient.post('/diagnose', {
      symptoms: symptoms,
      language: language
    });
    
    console.log(`✅ API Response: ${response.status} ${response.statusText}`);
    return response.data;
    
  } catch (error) {
    console.error('❌ API Error:', error.message);
    
    if (error.response) {
      console.error(`   Status: ${error.response.status}`);
      console.error(`   Data:`, error.response.data);
    } else if (error.request) {
      console.error('   No response received from server');
    }
    
    throw new Error('Failed to get diagnosis from backend');
  }
}

// Get supported languages
async function getLanguages() {
  try {
    const response = await apiClient.get('/languages');
    return response.data;
  } catch (error) {
    console.error('❌ Error getting languages:', error.message);
    return {
      'en': 'English',
      'yo': 'Yoruba',
      'ha': 'Hausa',
      'ig': 'Igbo',
      'pcm': 'Nigerian Pidgin'
    };
  }
}

// Health check
async function healthCheck() {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'unhealthy' };
  }
}

module.exports = {
  getDiagnosis,
  getLanguages,
  healthCheck
};