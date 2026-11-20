const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const VIDEO_API_KEY = process.env.VIDEO_API_KEY; // حط هنا مفتاح videodownloadapi في Netlify

async function sleep(ms){ return new Promise(r=>setTimeout(r,ms)); }

exports.handler = async (event) => {
  try{
    const { url, format, quality, chatId } = JSON.parse(event.body || '{}');
    if(!url || !chatId) return { statusCode:400, body: JSON.stringify({ok:false, error:'ناقص لينك او chatId'}) };

    const isAudio = format === 'audio';

    // 1. ابدأ التحميل في videodownloadapi
    const start = await fetch('https://videodownloadapi.com/api/v1/downloads', {
      method:'POST',
      headers:{
        'Authorization': `Bearer ${VIDEO_API_KEY}`,
        'Content-Type':'application/json'
      },
      body: JSON.stringify({
        url,
        format: isAudio ? 'MP3' : 'MP4',
        quality: isAudio ? 'best' : quality
      })
    });
    const startData = await start.json();
    const download_id = startData.download_id || startData.id || startData.data?.download_id;
    if(!download_id) return { statusCode:500, body: JSON.stringify({ok:false, error:'الـ API مردش بـ download_id: ' + JSON.stringify(startData).slice(0,300)}) };

    // 2. استنى لحد ما يجهز - poll كل 3 ثواني لحد 3 دقايق
    let download_url = null;
    for(let i=0;i<60;i++){
      await sleep(3000);
      const check = await fetch(`https://videodownloadapi.com/api/v1/downloads/${download_id}`, {
        headers:{ 'Authorization': `Bearer ${VIDEO_API_KEY}` }
      });
      const j = await check.json();
      const status = j.status || j.data?.status;
      const fileUrl = j.download_url || j.data?.download_url;
      if(status === 'ready' && fileUrl){ download_url = fileUrl; break; }
      if(status === 'failed') return { statusCode:500, body: JSON.stringify({ok:false, error:'فشل التحميل من الـ API'}) };
    }
    if(!download_url) return { statusCode:500, body: JSON.stringify({ok:false, error:'التحميل طول اكتر من اللازم'}) };

    // 3. نزل الملف وابعتو في تيليجرام كملف حقيقي مش لينك
    const fileRes = await fetch(download_url);
    const buffer = Buffer.from(await fileRes.arrayBuffer());
    const filename = isAudio ? 'audio.mp3' : 'video.mp4';

    const form = new FormData();
    form.append('chat_id', String(chatId));
    form.append('caption', 'تم التحميل ✅');
    form.append(isAudio ? 'audio' : 'video', new Blob([buffer], {type: isAudio ? 'audio/mpeg' : 'video/mp4'}), filename);

    const tgRes = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/${isAudio ? 'sendAudio' : 'sendVideo'}`, {
      method:'POST',
      body: form
    });
    const tgData = await tgRes.json();
    if(!tgData.ok) return { statusCode:500, body: JSON.stringify({ok:false, error: tgData.description}) };

    return { statusCode:200, body: JSON.stringify({ok:true}) };
  }catch(e){
    return { statusCode:500, body: JSON.stringify({ok:false, error: e.message}) };
  }
};
