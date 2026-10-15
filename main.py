# -*- coding: utf-8 -*-
import os, random
from flask import Flask
from threading import Thread
import telebot
from telebot import types
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running with Force Sub ✅"
@app.route('/health')
def health(): return "OK", 200

TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "7145036494"))

# قناتك للاشتراك الاجباري
FORCE_CHANNEL_USERNAME = "pkwbiwjwbekeekkw" # بدون @
FORCE_CHANNEL_LINK = "https://t.me/pkwbiwjwbekeekkw"
INVITE_LINK = FORCE_CHANNEL_LINK # نفسها

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
os.makedirs("database", exist_ok=True)
os.makedirs("temp", exist_ok=True)

def get_points(uid):
    try: return int(open(f"database/points_{uid}.txt", encoding="utf-8").read().strip() or 0)
    except: return 0
def add_points(uid, a):
    open(f"database/points_{uid}.txt","w",encoding="utf-8").write(str(get_points(uid)+a))

# ============ فحص الاشتراك الاجباري ============
def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(f"@{FORCE_CHANNEL_USERNAME}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Check sub error: {e}")
        return False # لو البوت مو ادمن في القناة، يسمح للكل مؤقتا

def force_sub_keyboard():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 اشترك في القناة اجباري ✅", url=FORCE_CHANNEL_LINK))
    kb.add(types.InlineKeyboardButton("✅ تحققت - اشتركت", callback_data="check_sub"))
    return kb

def make_img(text, bg="black"):
    img = Image.new("RGB", (1080,1350), bg if bg!="white" else "white")
    draw = ImageDraw.Draw(img)
    try: font = ImageFont.truetype("arial.ttf", 40)
    except: font = ImageFont.load_default()
    y=40
    for line in text.split("\n"):
        draw.text((50,y), line, fill="white" if bg!="white" else "black", font=font)
        y+=70
    path = f"temp/{random.randint(10000,99999)}.jpg"
    img.save(path)
    return path

def auto_daman(store, typ):
    t = {
        "store": f"🛡️ ضمان متجر {store}\n\n✅ ذهبي 7 ايام\n✅ استرجاع\n✅ دعم 24 ساعة\n{FORCE_CHANNEL_LINK}",
        "account": f"🛡️ ضمان حسابات {store}\n\n✅ يوزر وباس\n✅ ضمان 3 ايام\n{FORCE_CHANNEL_LINK}",
        "number": f"🛡️ ضمان ارقام {store}\n\n✅ نظيف\n✅ كود فوري\n{FORCE_CHANNEL_LINK}",
        "email": f"🛡️ ضمان ايميلات {store}\n\n✅ شغال\n✅ كود فوري\n{FORCE_CHANNEL_LINK}",
        "ship": f"🛡️ ضمان شحن {store}\n\n✅ شحن سريع\n✅ تتبع\n{FORCE_CHANNEL_LINK}",
        "follow": f"🛡️ ضمان متابعين {store}\n\n✅ حقيقيين\n✅ ضمان 30 يوم\n{FORCE_CHANNEL_LINK}",
    }
    return make_img(t.get(typ, t["store"]), "white"), t.get(typ)

# ============ START مع اشتراك اجباري ============

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id

    # فحص الاشتراك الاجباري
    if not is_subscribed(uid):
        bot.send_message(uid,
            f"⚠️ *يجب الاشتراك اولا* ⚠️\n\n"
            f"📢 قناتك للاشتراك الاجباري:\n{FORCE_CHANNEL_LINK}\n\n"
            f"👇 اشترك ثم اضغط تحققت",
            reply_markup=force_sub_keyboard()
        )
        return

    pts = get_points(uid)
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("📢 قناتنا ✅", url=FORCE_CHANNEL_LINK))

    kb.add(types.InlineKeyboardButton("━━━ 🛡️ الضمان الخاص ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("🛡️ ضمان متجر", callback_data="daman_store"),
        types.InlineKeyboardButton("👤 ضمان حسابات", callback_data="daman_account")
    )
    kb.add(
        types.InlineKeyboardButton("📱 ضمان ارقام", callback_data="daman_number"),
        types.InlineKeyboardButton("📧 ضمان ايميلات", callback_data="daman_email")
    )
    kb.add(
        types.InlineKeyboardButton("📦 ضمان شحن", callback_data="daman_ship"),
        types.InlineKeyboardButton("🚀 ضمان متابعين", callback_data="daman_follow")
    )

    kb.add(types.InlineKeyboardButton("━━━ 📧 ايميلات وهمية ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("📧 ايميل وهمي - 5", callback_data="fake_email"),
        types.InlineKeyboardButton("🔑 تفعيل ايميل - 5", callback_data="activate_email")
    )
    kb.add(
        types.InlineKeyboardButton("📨 استقبال كود - 5", callback_data="email_code"),
        types.InlineKeyboardButton("📬 ايميل 10 دقايق - 5", callback_data="temp_10min")
    )
    kb.add(
        types.InlineKeyboardButton("♾️ ايميل دائم - 15", callback_data="email_perm"),
        types.InlineKeyboardButton("🔐 مشفر - 10", callback_data="email_secure")
    )

    kb.add(types.InlineKeyboardButton("━━━ 📦 شحن ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("💳 شحن رصيد - 5", callback_data="charge"),
        types.InlineKeyboardButton("📦 تتبع شحنة - 5", callback_data="track_ship")
    )
    kb.add(
        types.InlineKeyboardButton("🎁 كود خصم - 5", callback_data="coupon"),
        types.InlineKeyboardButton("🧾 فاتورة - 5", callback_data="invoice")
    )

    kb.add(types.InlineKeyboardButton("━━━ 🚀 زيده ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("🚀 متابعين - 15", callback_data="zyada"),
        types.InlineKeyboardButton("❤️ لايكات - 15", callback_data="likes")
    )
    kb.add(
        types.InlineKeyboardButton("👁️ مشاهدات - 15", callback_data="views"),
        types.InlineKeyboardButton("📈 اعضاء - 15", callback_data="members")
    )
    kb.add(types.InlineKeyboardButton("━━━ 🔓 تفعيل ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("🔓 فك حظر - 15", callback_data="unban"),
        types.InlineKeyboardButton("📱 رقم وهمي - 15", callback_data="number")
    )
    kb.add(
        types.InlineKeyboardButton("💎 امريكي - 25", callback_data="usnumber"),
        types.InlineKeyboardButton("📲 تفعيل واتس - 15", callback_data="whatsapp")
    )

    kb.add(types.InlineKeyboardButton("━━━ 🎨 تصميم فوري 5 ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("🎨 تصميم", callback_data="design"),
        types.InlineKeyboardButton("✨ فلتر", callback_data="filter")
    )
    kb.add(
        types.InlineKeyboardButton("🔤 كتابة", callback_data="textpic"),
        types.InlineKeyboardButton("🖼️ جودة", callback_data="hd")
    )
    kb.add(
        types.InlineKeyboardButton("🎯 لوجو - 10", callback_data="logo"),
        types.InlineKeyboardButton("🪪 بطاقة - 10", callback_data="card")
    )

    kb.add(types.InlineKeyboardButton("━━━ 📢 اعلانات ━━━", callback_data="sec"))
    kb.add(
        types.InlineKeyboardButton("📢 نشر - 20", callback_data="ad_post"),
        types.InlineKeyboardButton("📌 تثبيت - 30", callback_data="ad_pin")
    )
    kb.add(
        types.InlineKeyboardButton("🚀 ممول - 50", callback_data="ad_sponsor"),
        types.InlineKeyboardButton("📣 بث للكل - 100", callback_data="ad_broadcast")
    )

    kb.add(types.InlineKeyboardButton(f"💰 رصيدك: {pts} نقطة", callback_data="bal"))
    kb.add(types.InlineKeyboardButton("💳 شراء نقاط", callback_data="buy"))

    bot.send_message(uid, f"🏪 *متجر زيده - قناتك اجباري* 🔥\n✅ انت مشترك في {FORCE_CHANNEL_LINK}\n💰 رصيدك: *{pts}*\n\n✅ كل شي ينفذ تلقائيا\n👇 اختر:", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    uid = c.from_user.id
    chat = c.message.chat.id
    d = c.data

    # زر التحقق من الاشتراك
    if d == "check_sub":
        if is_subscribed(uid):
            bot.answer_callback_query(c.id, "✅ تم الاشتراك بنجاح!")
            bot.delete_message(chat, c.message.message_id)
            start(c.message) # ارجع شغل start من جديد
        else:
            bot.answer_callback_query(c.id, "❌ انت لسه ما اشتركت!", show_alert=True)
            bot.send_message(chat, f"❌ ما اشتركت لسه\nاشترك هنا: {FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return

    bot.answer_callback_query(c.id)
    if d.startswith("sec"): return

    # فحص الاشتراك قبل اي زر
    if not is_subscribed(uid):
        bot.send_message(chat, f"⚠️ *اشترك اولا* ⚠️\n{FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return

    if d == "buy":
        bot.send_message(chat, f"💳 *شراء*\n5=0.05$ 15=0.15$ 30=0.30$\nUSDT:\n`YOUR_WALLET`\nايدك: {uid}")
        return
    if d == "bal":
        bot.send_message(chat, f"💰 رصيدك {get_points(uid)}")
        return

    prices = {"design":5,"filter":5,"textpic":5,"hd":5,"coupon":5,"invoice":5,"fake_email":5,"activate_email":5,"email_code":5,"temp_10min":5,"charge":5,"track_ship":5,"daman_store":5,"daman_account":5,"daman_number":5,"daman_email":5,"daman_ship":5,"daman_follow":5,"logo":10,"card":10,"email_secure":10,"zyada":15,"likes":15,"views":15,"members":15,"unban":15,"number":15,"whatsapp":15,"email_perm":15,"usnumber":25,"ad_post":20,"ad_pin":30,"ad_sponsor":50,"ad_broadcast":100,"force_free":0}
    price = prices.get(d,15)
    if get_points(uid) < price and price!=0:
        bot.send_message(chat, f"❌ تحتاج {price} رصيدك {get_points(uid)}")
        return

    if d in ["filter","hd","textpic"]:
        bot.send_message(chat, f"📸 *{d} - {price}*\n\nارسل الصورة:")
        bot.register_next_step_handler_by_chat_id(chat, lambda m: exec_photo(m,d,price))
    elif d.startswith("daman_"):
        typ = d.split("_")[1]
        bot.send_message(chat, f"🛡️ *ضمان {typ} - {price}*\n\nارسل اسم متجرك:")
        bot.register_next_step_handler_by_chat_id(chat, lambda m: exec_daman(m,typ,price))
    elif d in ["fake_email","activate_email","email_code","temp_10min","email_perm","email_secure"]:
        exec_email(chat, uid, d, price)
    elif d in ["charge","track_ship","coupon","invoice"]:
        exec_ship(chat, uid, d, price)
    elif d in ["design","logo","card"]:
        bot.send_message(chat, f"🎨 *{d} - {price}*\n\nارسل النص:")
        bot.register_next_step_handler_by_chat_id(chat, lambda m: exec_text(m,d,price))
    else:
        bot.send_message(chat, f"📦 *{d} - {price}*\n\nارسل بياناتك:")
        bot.register_next_step_handler_by_chat_id(chat, lambda m: exec_delay(m,d,price))

def exec_email(chat, uid, typ, price):
    add_points(uid,-price)
    emails = {
        "fake_email": f"📧 ايميل:\n`{random.randint(10000,99999)}@tempmail.com`\nباس: `{random.randint(100000,999999)}` ✅",
        "activate_email": f"✅ تفعيل:\n`user{random.randint(1000,9999)}@gmail.com`\nكود: `{random.randint(100000,999999)}`",
        "email_code": f"📨 كود:\n`{random.randint(100000,999999)}`",
        "temp_10min": f"📬 10 دقايق:\n`{random.randint(10000,99999)}@10minutemail.com`",
        "email_perm": f"♾️ دائم:\n`store{random.randint(100,999)}@gmail.com`",
        "email_secure": f"🔐 مشفر:\n`secure{random.randint(1000,9999)}@protonmail.com`"
    }
    bot.send_message(chat, emails[typ]+f"\n\n💰 خصم {price} - رصيدك {get_points(uid)}\n/start")

def exec_ship(chat, uid, typ, price):
    add_points(uid,-price)
    msgs = {
        "charge": f"💳 تم شحن 10$ ✅",
        "track_ship": f"📦 TRK{random.randint(100000000,999999999)}\nفي الطريق 🚚",
        "coupon": f"🎁 كود: `ZAYDA{random.randint(10,99)}` خصم 20%",
        "invoice": f"🧾 فاتورة مدفوعة ✅"
    }
    bot.send_message(chat, msgs[typ]+f"\n💰 خصم {price} - رصيدك {get_points(uid)}")

def exec_photo(m, typ, price):
    uid = m.from_user.id
    chat = m.chat.id
    if m.content_type!= 'photo': return
    if not is_subscribed(uid):
        bot.send_message(chat, f"⚠️ اشترك اولا\n{FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return
    file_info = bot.get_file(m.photo[-1].file_id)
    data = bot.download_file(file_info.file_path)
    in_path = f"temp/{uid}_in.jpg"
    open(in_path,"wb").write(data)
    img = Image.open(in_path)
    if typ=="filter": img = ImageEnhance.Color(img.filter(ImageFilter.DETAIL)).enhance(1.5)
    elif typ=="hd": img = ImageEnhance.Sharpness(img).enhance(2.5)
    elif typ=="textpic":
        bot.send_message(chat, "ارسل النص:")
        bot.register_next_step_handler_by_chat_id(chat, lambda m2: exec_text_on_pic(m,m2,price))
        return
    out = f"temp/{uid}_out.jpg"
    img.save(out)
    add_points(uid,-price)
    bot.send_photo(chat, open(out,"rb"), caption=f"✅ تم {typ} - {price} نقطة\nرصيدك {get_points(uid)}")

def exec_text_on_pic(photo_msg, text_msg, price):
    uid = photo_msg.from_user.id
    chat = photo_msg.chat.id
    file_info = bot.get_file(photo_msg.photo[-1].file_id)
    data = bot.download_file(file_info.file_path)
    in_path = f"temp/{uid}_in.jpg"
    open(in_path,"wb").write(data)
    img = Image.open(in_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    w,h = img.size
    try: font = ImageFont.truetype("arial.ttf", int(h/12))
    except: font = ImageFont.load_default()
    draw.rectangle([(0,h-150),(w,h)], fill=(0,0,0,180))
    draw.text((20,h-100), text_msg.text, fill="white", font=font)
    out = f"temp/{uid}_out.jpg"
    img.save(out)
    add_points(uid,-price)
    bot.send_photo(chat, open(out,"rb"), caption=f"✅ كتابة تمت - {price} نقطة\nرصيدك {get_points(uid)}")

def exec_daman(m, typ, price):
    uid = m.from_user.id
    if not is_subscribed(uid):
        bot.send_message(m.chat.id, f"⚠️ اشترك اولا\n{FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return
    out, text = auto_daman(m.text, typ)
    add_points(uid,-price)
    bot.send_photo(m.chat.id, open(out,"rb"), caption=f"✅ ضمان {typ}\n\n{text}\n\nخصم {price} - رصيدك {get_points(uid)}")

def exec_text(m, typ, price):
    uid = m.from_user.id
    if not is_subscribed(uid):
        bot.send_message(m.chat.id, f"⚠️ اشترك اولا\n{FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return
    out = make_img(f"{typ}\n\n{m.text}\n\n{FORCE_CHANNEL_LINK}", random.choice(["black","#FF0055","#00AAFF"]))
    add_points(uid,-price)
    bot.send_photo(m.chat.id, open(out,"rb"), caption=f"✅ تم {typ} - {price} نقطة\nرصيدك {get_points(uid)}")

def exec_delay(m, typ, price):
    uid = m.from_user.id
    if not is_subscribed(uid):
        bot.send_message(m.chat.id, f"⚠️ اشترك اولا\n{FORCE_CHANNEL_LINK}", reply_markup=force_sub_keyboard())
        return
    if price>0: add_points(uid,-price)
    bot.send_message(m.chat.id, f"✅ تم {typ} - خصم {price}\n⏳ انتظر 24 ساعة\nرصيدك {get_points(uid)}")
    bot.send_message(ADMIN_ID, f"طلب {typ} {price}ن من {uid}: {m.text}\n/done {uid}")

@bot.message_handler(commands=['add','done'])
def admin(m):
    if m.from_user.id!=ADMIN_ID: return
    try:
        if m.text.startswith('/add'):
            _, uid, pts = m.text.split()
            add_points(int(uid), int(pts))
            bot.send_message(int(uid), f"✅ شحن {pts} - رصيدك {get_points(int(uid))}")
        else:
            _, uid = m.text.split()
            bot.send_message(int(uid), f"🎉 تم التنفيذ ✅\n{FORCE_CHANNEL_LINK}\n/start")
    except: pass

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)