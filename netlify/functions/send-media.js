exports.handler = async function(event, context) {
  const BOT_TOKEN = process.env.BOT_TOKEN;
  // هنا بتحط الـ API Key بتاع خدمة التحميل اللي انت مشترك فيها
  // مثال: const DOWNLOAD_API_KEY = process.env.DOWNLOAD_API_KEY;
  // const DOWNLOAD_API_URL = process.env.DOWNLOAD_API_URL;

  if (!BOT_TOKEN) {
    return { statusCode: 500, body: JSON.stringify({ success: false, error: "Bot token not configured" }) };
  }

  try {
    const { chatId, url, type, quality } = JSON.parse(event.body);
    if (!chatId || !url || !type) {
      return { statusCode: 400, body: JSON.stringify({ success: false, error: "Missing parameters" }) };
    }

    // ===== مكان ربط خدمة التحميل بتاعتك =====
    // انت هنا هتعمل fetch لخدمة التحميل اللي معاك الـ Key بتاعها
    // والخدمة دي هي اللي هترجعلك رابط ملف مباشر mp4 او mp3
    // مثال للشكل اللي المفروض ترجعه الخدمة:
    // const downloadRes = await fetch(DOWNLOAD_API_URL, { method:'POST', headers:{ Authorization: `Bearer ${DOWNLOAD_API_KEY}` }, body: JSON.stringify({ url, type, quality }) });
    // const downloadData = await downloadRes.json();
    // const fileUrl = downloadData.fileUrl; // رابط مباشر
    // =========================================

    // لو لسه مركبتش خدمة تحميل، هنبعت رسالة تأكيد مؤقتة عشان تتأكد ان الربط شغال
    const fileUrl = null; // خليها null لحد ما تربط خدمتك، وبعدها حط fileUrl اللي جاي من الخدمة

    if (fileUrl) {
      // لو فيه ملف فعلي، ابعته كـ Document
      const caption = type === 'video' ? `فيديو بجودة ${quality}p 🎬` : `صوت فقط 🎵`;
      const sendRes = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendDocument`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, document: fileUrl, caption: caption })
      });
      const sendData = await sendRes.json();
      if (!sendRes.ok) {
        return { statusCode: 500, body: JSON.stringify({ success: false, error: sendData.description || "Telegram API error" }) };
      }
    } else {
      // وضع الاختبار: بيبعت رسالة تأكيد بس
      const caption = type === 'video'
        ? `تم استلام طلبك 🎬\nالرابط: ${url}\nالجودة: ${quality}p\n\nاربط خدمة التحميل في الـ Function عشان يوصلك الملف نفسه.`
        : `تم استلام طلبك 🎵\nالرابط: ${url}\nالنوع: صوت فقط\n\nاربط خدمة التحميل في الـ Function عشان يوصلك الملف نفسه.`;

      const sendRes = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text: caption })
      });
      const sendData = await sendRes.json();
      if (!sendRes.ok) {
        return { statusCode: 500, body: JSON.stringify({ success: false, error: sendData.description || "Telegram API error" }) };
      }
    }

    // بنرجع success عشان الصفحة تقفل لوحدها
    return { statusCode: 200, body: JSON.stringify({ success: true }) };

  } catch (error) {
    return { statusCode: 500, body: JSON.stringify({ success: false, error: error.message }) };
  }
};
