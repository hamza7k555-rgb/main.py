// netlify/functions/send.js
// التوكن هنا بيتاخد من Environment Variables في Netlify، مش مكتوب في الكود

exports.handler = async (event) => {
  try {
    const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN; // من المتغيرات بس
    if (!BOT_TOKEN) return { statusCode: 500, body: JSON.stringify({ ok: false, error: 'BOT_TOKEN مش موجود في المتغيرات' }) };

    // event.body جاي multipart من الـ JS
    // بنستخدم busboy عشان نقرا الملف
    const Busboy = require('busboy');
    const fields = {};
    let fileBuffer = null;
    let filename = 'video.mp4';
    let mime = 'video/mp4';

    await new Promise((resolve, reject) => {
      const busboy = Busboy({ headers: event.headers });
      busboy.on('field', (name, val) => fields[name] = val);
      busboy.on('file', (name, file, info) => {
        filename = info.filename;
        mime = info.mimeType;
        const chunks = [];
        file.on('data', d => chunks.push(d));
        file.on('end', () => fileBuffer = Buffer.concat(chunks));
      });
      busboy.on('finish', resolve);
      busboy.on('error', reject);
      busboy.end(Buffer.from(event.body, event.isBase64Encoded ? 'base64' : 'utf8'));
    });

    const chatId = fields.chatId;
    const format = fields.format || 'video';
    const method = format === 'audio' ? 'sendAudio' : 'sendVideo';
    const fieldName = format === 'audio' ? 'audio' : 'video';

    const form = new FormData();
    form.append('chat_id', String(chatId));
    form.append('caption', 'تم التحميل ✅');
    form.append(fieldName, new Blob([fileBuffer], { type: mime }), filename);

    const tgRes = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/${method}`, { method: 'POST', body: form });
    const tgData = await tgRes.json();
    if (!tgData.ok) return { statusCode: 500, body: JSON.stringify({ ok: false, error: tgData.description }) };

    return { statusCode: 200, body: JSON.stringify({ ok: true }) };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ ok: false, error: e.message }) };
  }
};
