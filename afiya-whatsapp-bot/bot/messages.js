// Welcome messages in different languages
function getWelcomeMessage(language, name = 'Friend') {
  const messages = {
    'en': `👋 Hello ${name}! Welcome to *Afiya Care*

I'm your AI health assistant powered by N-ATLaS 🤖

🌍 *I speak 5 languages:*
- English
- Yoruba (Yorùbá)
- Hausa
- Igbo
- Nigerian Pidgin

💬 *How to use me:*
Just describe your symptoms in any language!

Example:
"I have a headache and fever"
"Mo ni irora ori ati iba" (Yoruba)
"Ina da ciwon kai" (Hausa)

⚕️ Type /help for more commands

Let's get started! What symptoms are you experiencing?`,

    'yo': `👋 Ẹ káàbọ̀ ${name}! Káàbọ̀ sí *Afiya Care*

Èmi ni olùrànlọ́wọ́ ìlera AI tí N-ATLaS ń darí 🤖

🌍 *Mo lè sọ èdè márùn-ún:*
- English
- Yorùbá
- Hausa
- Igbo
- Nigerian Pidgin

💬 *Bí o ṣe lè lò mi:*
Sọ àwọn àmì àìsàn rẹ ní èdè èyíkéyìí!

Àpẹẹrẹ:
"Mo ní irora orí àti ibà"

⚕️ Tẹ /help fún àwọn àṣẹ míràn

Jẹ́ ká bẹ̀rẹ̀! Kí ni àwọn àmì àìsàn tí ó ń ní?`,

    'ha': `👋 Sannu ${name}! Barka da zuwa *Afiya Care*

Ni ne mai taimaka lafiya AI wanda N-ATLaS ke gudanarwa 🤖

🌍 *Ina iya magana da harsuna biyar:*
- Turanci
- Yoruba
- Hausa
- Igbo
- Nigerian Pidgin

💬 *Yadda za ku yi amfani da ni:*
Ku bayyana alamun rashin lafiyar ku da kowace harshe!

Misali:
"Ina da ciwon kai da zazzabi"

⚕️ Rubuta /help don ƙarin umarni

Mu fara! Wane irin alamun rashin lafiya kuke da su?`,

    'ig': `👋 Nnọọ ${name}! Nnọọ na *Afiya Care*

Abụ m onye inyeaka ahụ ike AI nke N-ATLaS na-eduzi 🤖

🌍 *Enwere m ike ịsụ asụsụ ise:*
- Bekee
- Yoruba
- Hausa
- Igbo
- Nigerian Pidgin

💬 *Otu ị ga-esi jiri m:*
Kọwaa mgbaàmà gị n'asụsụ ọ bụla!

Ọmụmaatụ:
"Enwere m isi ọwụwa na ahụ ọkụ"

⚕️ Pịa /help maka iwu ndị ọzọ

Ka anyị malite! Kedu mgbaàmà ị nwere?`,

    'pcm': `👋 How far ${name}! Welcome to *Afiya Care*

I be your AI health helper wey N-ATLaS dey power 🤖

🌍 *I fit speak 5 languages:*
- English
- Yoruba
- Hausa
- Igbo
- Nigerian Pidgin

💬 *How to use me:*
Just tell me wetin dey pain you for any language!

Example:
"My head dey pain me and I get fever"

⚕️ Type /help for more commands

Make we start! Wetin dey pain you?`
  };
  
  return messages[language] || messages['en'];
}

// Help message
function getHelpMessage(language) {
  return `📖 *Afiya Care Commands*

/start - Start or restart conversation
/help - Show this help message
/languages - Show all supported languages

💬 *How to get help:*
Just describe your symptoms naturally in any of these languages:
- English
- Yoruba (Yorùbá)
- Hausa
- Igbo
- Nigerian Pidgin

Example messages:
"I have fever and cough"
"Mo ni ibà àti ikó"
"Ina da zazzabi da tari"
"Enwere m ahụ ọkụ na ụkwara"
"I get fever and cough"

⚠️ *IMPORTANT DISCLAIMER:*
This bot provides health information only. It is NOT a substitute for professional medical advice. Always consult a qualified healthcare provider for diagnosis and treatment.

🚨 In case of emergency, call your local emergency services immediately!

━━━━━━━━━━━━━━━━━
Powered by N-ATLaS (NCAIR1/N-ATLaS)
Built for Awarri Hackathon 2024`;
}

// Languages list
function getLanguagesMessage() {
  return `🌍 *Supported Languages*

I can understand and respond in:

🇬🇧 *English*
Example: "I have a headache"

🇳🇬 *Yoruba (Yorùbá)*
Example: "Mo ni irora ori"

🇳🇬 *Hausa*
Example: "Ina da ciwon kai"

🇳🇬 *Igbo*
Example: "Enwere m isi ọwụwa"

🇳🇬 *Nigerian Pidgin*
Example: "My head dey pain me"

━━━━━━━━━━━━━━━━━
Just send your message in any of these languages and I'll automatically detect it! 🚀`;
}

module.exports = {
  getWelcomeMessage,
  getHelpMessage,
  getLanguagesMessage
};