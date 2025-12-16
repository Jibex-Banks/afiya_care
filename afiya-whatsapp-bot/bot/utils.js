// Detect language from text
function detectLanguage(text) {
  const textLower = text.toLowerCase();
  
  // Yoruba markers
  const yorubaMarkers = ['ẹ', 'ọ', 'ṣ', 'bawo', 'ni', 'mo', 'ti'];
  if (yorubaMarkers.some(marker => textLower.includes(marker))) {
    return 'yo';
  }
  
  // Hausa markers
  const hausaMarkers = ['sannu', 'yaya', 'ina', 'da', 'ciwon'];
  if (hausaMarkers.some(marker => textLower.includes(marker))) {
    return 'ha';
  }
  
  // Igbo markers
  const igboMarkers = ['kedu', 'ndewo', 'enwere', 'ọ'];
  if (igboMarkers.some(marker => textLower.includes(marker))) {
    return 'ig';
  }
  
  // Pidgin markers (need at least 2 matches)
  const pidginMarkers = ['wetin', 'dey', 'fit', 'no', 'go', 'make'];
  const pidginCount = pidginMarkers.filter(marker => 
    textLower.split(' ').includes(marker)
  ).length;
  if (pidginCount >= 2) {
    return 'pcm';
  }
  
  // Default to English
  return 'en';
}

// Format phone number
function formatPhoneNumber(number) {
  return number.replace(/[^\d+]/g, '');
}

// Clean text for processing
function cleanText(text) {
  return text.trim().replace(/\s+/g, ' ');
}

// Truncate text
function truncate(text, maxLength = 100) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

module.exports = {
  detectLanguage,
  formatPhoneNumber,
  cleanText,
  truncate
};