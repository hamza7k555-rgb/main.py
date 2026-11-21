// app.js - مفيش توكن هنا خالص
const tg = window.Telegram.WebApp;
tg.ready(); tg.expand();

const BENSON_URL = 'https://dev-iii-iii.pantheonsite.io/server/download.php';

async function start(){
  const url = document.getElementById('url').value.trim();
  const format = document.getElementById('format').value; // video او audio
  const chatId = tg.initDataUnsafe?.user?.id;
  if(!url) return alert('حط اللينك الاول');
  if(!chatId) return alert('افتح من جوه البوت');

  document.getElementById('status').innerText = '1/3 - ببعت اللينك لبنسون...';
  try{
    // 1. JS ياخد الرابط من HTML ويوديه لـ PHP بنسون
    const res = await fetch(`${BENSON_URL}?url=${encodeURIComponent(url)}&format=${format}`);
    if(!res.ok) throw new Error('بنسون مردش');
    const blob = await res.blob();

    document.getElementById('status').innerText = '2/3 - الملف رجع من بنسون، ببعته لـ Netlify...';

    // 2. JS ياخد الملف اللي رجع من بنسون ويبعته لـ Netlify
    const form = new FormData();
    form.append('chatId', String(chatId));
    form.append('format', format);
    form.append('file', blob, format === 'audio' ? 'audio.mp3' : 'video.mp4');

    const send = await fetch('/.netlify/functions/send', { method: 'POST', body: form });
    const data = await send.json();
    if(!data.ok) throw new Error(data.error || 'فشل الارسال');

    document.getElementById('status').innerText = 'تم! الملف اتبعت ✅';
    setTimeout(()=> tg.close(), 1200);
  }catch(e){
    document.getElementById('status').innerText = 'حصل خطأ: ' + e.message;
  }
}
