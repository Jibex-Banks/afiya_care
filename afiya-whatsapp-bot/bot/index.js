const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
require('dotenv').config();

const api = require('./api');
const messages = require('./messages');
const { detectLanguage, formatPhoneNumber } = require('./utils');

// Initialize Express (for health checks)
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    bot: client ? 'connected' : 'disconnected' 
  });
});

app.listen(PORT, () => {
  console.log(`🌐 Health check server running on port ${PORT}`);
});

// Initialize WhatsApp Client
const client = new Client({
  authStrategy: new LocalAuth({
    clientId: 'afiya-care-bot'
  }),
  puppeteer: {
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--single-process',
      '--disable-gpu'
    ]
  }
});

// Store user sessions (in production, use Redis)
const userSessions = new Map();

// QR Code for authentication
client.on('qr', (qr) => {
  console.log('\n🔐 Scan this QR code with WhatsApp:');
  qrcode.generate(qr, { small: true });
  console.log('\n📱 Open WhatsApp → Settings → Linked Devices → Link a Device');
});

// Client ready
client.on('ready', () => {
  console.log('✅ WhatsApp Bot is ready!');
  console.log('🇳🇬 Afiya Care - N-ATLaS Powered Health Assistant');
  console.log('📱 Waiting for messages...\n');
});

// Authentication success
client.on('authenticated', () => {
  console.log('🔓 Authentication successful!');
});

// Authentication failure
client.on('auth_failure', (msg) => {
  console.error('❌ Authentication failed:', msg);
});

// Disconnected
client.on('disconnected', (reason) => {
  console.log('⚠️ Client was disconnected:', reason);
});

// Handle incoming messages
client.on('message', async (message) => {
  try {
    const from = message.from;
    const name = message._data.notifyName || 'User';
    const text = message.body.trim();
    
    console.log(`\n📩 Message from ${name} (${from})`);
    console.log(`💬 Text: ${text.substring(0, 50)}...`);
    
    // Ignore group messages
    if (message.from.includes('@g.us')) {
      console.log('⏭️ Ignoring group message');
      return;
    }
    
    // Get or create user session
    if (!userSessions.has(from)) {
      userSessions.set(from, {
        name: name,
        language: 'en',
        messageCount: 0,
        lastMessage: Date.now()
      });
    }
    
    const session = userSessions.get(from);
    session.messageCount++;
    session.lastMessage = Date.now();
    
    // Detect language from message
    const detectedLang = detectLanguage(text);
    session.language = detectedLang;
    
    console.log(`🌍 Detected language: ${detectedLang}`);
    
    // Handle commands
    if (text.toLowerCase() === '/start' || 
        text.toLowerCase() === 'hi' || 
        text.toLowerCase() === 'hello' ||
        text.toLowerCase() === 'bawo' ||
        text.toLowerCase() === 'sannu') {
      
      await message.reply(messages.getWelcomeMessage(detectedLang, name));
      return;
    }
    
    if (text.toLowerCase() === '/help') {
      await message.reply(messages.getHelpMessage(detectedLang));
      return;
    }
    
    if (text.toLowerCase() === '/languages') {
      await message.reply(messages.getLanguagesMessage());
      return;
    }
    
    // Show typing indicator
    await message.reply('⏳ Analyzing your symptoms...');
    
    // Call FastAPI backend for diagnosis
    console.log('🔄 Calling FastAPI backend...');
    const diagnosis = await api.getDiagnosis(text, detectedLang);
    
    // Format and send response
    const response = formatDiagnosisResponse(diagnosis, detectedLang);
    await message.reply(response);
    
    console.log('✅ Response sent successfully\n');
    
  } catch (error) {
    console.error('❌ Error handling message:', error.message);
    
    try {
      await message.reply(
        '😔 Sorry, I encountered an error. Please try again.\n\n' +
        'Gafara, na sami matsala. Don Allah a sake gwada.'
      );
    } catch (replyError) {
      console.error('❌ Error sending error message:', replyError);
    }
  }
});

// Format diagnosis response for WhatsApp
function formatDiagnosisResponse(diagnosis, language) {
  let response = '';
  
  // Red flags (URGENT)
  if (diagnosis.red_flags && diagnosis.red_flags.length > 0) {
    response += '🚨 *URGENT ALERT / SANARWA MAI MUHIMMANCI*\n\n';
    diagnosis.red_flags.forEach(flag => {
      response += `${flag}\n\n`;
    });
    response += '━━━━━━━━━━━━━━━━━\n\n';
  }
  
  // Possible conditions
  if (diagnosis.conditions && diagnosis.conditions.length > 0) {
    response += '🔍 *Possible Conditions:*\n\n';
    
    diagnosis.conditions.slice(0, 3).forEach((condition, index) => {
      response += `*${index + 1}. ${condition.title}*\n`;
      response += `📊 Confidence: ${Math.round(condition.confidence * 100)}%\n`;
      response += `📝 ${condition.description.substring(0, 150)}...\n`;
      
      // Show treatments for top condition
      if (index === 0 && condition.treatments && condition.treatments.length > 0) {
        response += `\n💊 *Suggested Care:*\n`;
        condition.treatments.slice(0, 3).forEach(treatment => {
          response += `  • ${treatment}\n`;
        });
      }
      response += '\n';
    });
    
    response += '━━━━━━━━━━━━━━━━━\n\n';
  }
  
  // N-ATLaS Analysis
  if (diagnosis.natlas_analysis) {
    response += `💡 *AI Analysis:*\n${diagnosis.natlas_analysis.substring(0, 200)}...\n\n`;
    response += '━━━━━━━━━━━━━━━━━\n\n';
  }
  
  // Recommendations
  if (diagnosis.recommendations && diagnosis.recommendations.length > 0) {
    response += '📋 *Recommendations:*\n';
    diagnosis.recommendations.forEach(rec => {
      response += `  • ${rec}\n`;
    });
    response += '\n━━━━━━━━━━━━━━━━━\n\n';
  }
  
  // Disclaimer
  response += `⚕️ ${diagnosis.disclaimer}\n\n`;
  
  // Language detected
  if (diagnosis.detected_language) {
    const langNames = {
      'en': 'English',
      'yo': 'Yoruba',
      'ha': 'Hausa',
      'ig': 'Igbo',
      'pcm': 'Pidgin'
    };
    response += `🌍 Language: ${langNames[diagnosis.detected_language] || 'Auto'}\n`;
  }
  
  // Response time
  if (diagnosis.processing_time_ms) {
    response += `⚡ Response time: ${diagnosis.processing_time_ms}ms\n`;
  }
  
  response += '\n💬 Send another message to describe different symptoms!';
  
  return response;
}

// Initialize the client
console.log('🚀 Starting Afiya Care WhatsApp Bot...');
console.log('🇳🇬 Powered by N-ATLaS (NCAIR1/N-ATLaS)');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

client.initialize();

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n\n🛑 Shutting down bot...');
  await client.destroy();
  process.exit(0);
});