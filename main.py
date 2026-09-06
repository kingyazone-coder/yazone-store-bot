import telebot
from telebot import types
import json
import os
API_TOKEN = '8742155499:AAEPQ7Ju-AgEDM6RXaarhDlEL3Kh7wm-rcU'
SUPPORT_GROUP_ID = -1004391403638
CHANNEL_USERNAME = '@yazone_store3'

bot = telebot.TeleBot(API_TOKEN)

# ቋሚ የዳታቤዝ ፋይል መጫኛ
DB_FILE = 'database.json'

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"merchants": {}, "products": {}, "orders": {}, "languages": {}}

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_db()
merchants_db = db["merchants"]
products_db = db["products"]
orders_db = db["orders"]
user_language = db["languages"]
user_states = {}

STRINGS = {
    'am': {
        'welcome': "እንኳን ወደ Yazone Store ቦት በደህና መጡ! ለመገበያየት ወይም ምርት ለመለጠፍ ከታች ካሉት ቁልፎች ይምረጡ።",
        'welcome_merchant': "እንኳን ደህና መጡ ነጋዴ! መለያ ቁጥርዎ፦ {}",
        'btn_order': "🛒 ምርት ለማዘዝ",
        'btn_channel': "📢 ምርቶችን በቻናል ይመልከቱ",
        'btn_settings': "⚙️ ማስተካከያ / Settings",
        'btn_support': "💬 ሐሳብ አስተያየት",
        'btn_post': "➕ አዲስ ምርት ለመለጠፍ",
        'btn_received': "📥 የመጡ ትዕዛዞች",
        'btn_my_ads': "📋 የኔ ማስታወቂያዎች",
        'btn_register': "🔐 ነጋዴ ለመሆን መመዝገቢያ",
        'btn_cancel': "❌ ለመሰረዝ",
        'btn_back': "⬅️ ወደ ዋናው ማውጫ",
        'msg_cancel': "ሂደቱ ተሰርዟል ወደ ዋናው ማውጫ ተመልሰዋል።",
        'msg_support': "እባክዎ ለእኛ ማጋራት የሚፈልጉትን ሐሳብ ወይም አስተያየት ይጻፉ፦",
        'msg_support_sent': "🙏 አመሰግናለሁ! አስተያየትዎ በተሳካ ሁኔታ ተልኳል።",
        'ask_shop': "እባክዎ የሱቅዎን ወይም የድርጅትዎን ስም ያስገቡ፦",
        'ask_phone': "በመቀጠል የስልክ ቁጥርዎን ያስገቡ፦",
        'reg_success': "🎉 ምዝገባዎ ተጠናቋል! የእርስዎ መለያ ቁጥር (Merchant ID)፦ `{}`",
        'ask_prod_photo': "እባክዎ የምርቱን ፎቶ ይላኩ፦",
        'ask_prod_title': "የምርቱን ስም (ርዕስ) ያስገቡ፦",
        'ask_prod_price': "የምርቱን ዋጋ ያስገቡ፦",
        'ask_prod_desc': "ስለምርቱ ሙሉ መግለጫ (መጠን፣ ከለር ወዘተ) ያብራሩ፦",
        'prod_post_confirm': "ምርቱ በተሳካ ሁኔታ ቻናል ላይ ተለጥፏል! 👍",
        'btn_order_now': "🛒 አሁኑኑ እዘዝ",
        'ask_order_name': "እባክዎ የእርስዎን ሙሉ ስም ያስገቡ፦",
        'ask_order_phone': "የስልክ ቁጥርዎን ያስገቡ፦",
        'ask_order_addr': "ምርቱ የሚረከቡበትን ሙሉ አድራሻ ያስገቡ፦",
        'ask_order_date': "ምርቱን የሚፈልጉበትን ቀን (ለምሳሌ፡ ነገ፣ ማክሰኞ) ያስገቡ፦",
        'order_success': "🙏 እናመሰግናለን! ትዕዛዝዎ በተሳካ ሁኔታ ለሻጩ ተልኳል። ሻጩ በቅርቡ ያነጋግርዎታል።",
        'no_orders': "እስካሁን ምንም የመጣ ትዕዛዝ የለም።",
        'no_ads': "እስካሁን ምንም የለጠፉት ምርት የለም።"
    },
    'en': {
        'welcome': "Welcome to Yazone Store Bot!",
        'welcome_merchant': "Welcome Merchant! Your ID: {}",
        'btn_order': "🛒 Order Now",
        'btn_channel': "📢 View Channel",
        'btn_settings': "⚙️ Settings",
        'btn_support': "💬 Support",
        'btn_post': "➕ Post an Ad",
        'btn_received': "📥 Received Orders",
        'btn_my_ads': "📋 My Ads",
        'btn_register': "🔐 Register as Merchant",
        'btn_cancel': "❌ Cancel",
        'btn_back': "⬅️ Back to Menu",
        'msg_cancel': "Process cancelled. Returned to main menu.",
        'msg_support': "Please write your feedback/support message:",
        'msg_support_sent': "🙏 Thank you! Your feedback has been sent.",
        'ask_shop': "Please enter your shop/business name:",
        'ask_phone': "Please enter your phone number:",
        'reg_success': "🎉 Registration complete! Your Merchant ID: `{}`",
        'ask_prod_photo': "Please send a photo of the product:",
        'ask_prod_title': "Enter product title:",
        'ask_prod_price': "Enter product price:",
        'ask_prod_desc': "Enter full product description (size, color etc):",
        'prod_post_confirm': "Product successfully posted to channel! 👍",
        'btn_order_now': "🛒 Order Now",
        'ask_order_name': "Enter your full name:",
        'ask_order_phone': "Enter your phone number:",
        'ask_order_addr': "Enter delivery address:",
        'ask_order_date': "Enter preferred delivery date:",
        'order_success': "Thank you! Your order has been sent to the seller.",
        'no_orders': "No orders received yet.",
        'no_ads': "No ads posted yet."
def sync_db
    save_db({"merchants": merchants_db, "products": products_db, "orders": orders_db, "languages": user_language})

def get_text(user_id, key):
    lang = user_language.get(str(user_id), 'am')
    if lang not in STRINGS or key not in STRINGS[lang]:
        return STRINGS['am'][key]
    return STRINGS[lang][key]

def build_main_menu(user_id):
    u_str = str(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_order = types.KeyboardButton(get_text(user_id, 'btn_order'))
    btn_channel = types.KeyboardButton(get_text(user_id, 'btn_channel'))
    btn_settings = types.KeyboardButton(get_text(user_id, 'btn_settings'))
    btn_support = types.KeyboardButton(get_text(user_id, 'btn_support'))
    
    if u_str in merchants_db:
        btn_post = types.KeyboardButton(get_text(user_id, 'btn_post'))
        btn_received = types.KeyboardButton(get_text(user_id, 'btn_received'))
        btn_my_ads = types.KeyboardButton(get_text(user_id, 'btn_my_ads'))
        markup.add(btn_post)
        markup.add(btn_received, btn_my_ads)
        markup.add(btn_order, btn_channel, btn_settings, btn_support)
    else:
        btn_register = types.KeyboardButton(get_text(user_id, 'btn_register'))
        markup.add(btn_register)
        markup.add(btn_order, btn_channel)
        markup.add(btn_settings, btn_support)
    return markup

def build_cancel_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(get_text(user_id, 'btn_cancel')))
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    u_str = str(user_id)
    if u_str not in user_language:
        user_language[u_str] = 'am'
        sync_db()
        
    if len(message.text.split()) > 1:
        param = message.text.split()[1]
        if param.startswith('order_'):
            prod_id = param.replace('order_', '')
            if prod_id in products_db:
                user_states[user_id] = {'state': 'ORDER_NAME', 'prod_id': prod_id}
                bot.send_message(user_id, get_text(user_id, 'ask_order_name'), reply_markup=build_cancel_menu(user_id))
                return

    if u_str in merchants_db:
        m_id = merchants_db[u_str]['merchant_id']
        bot.send_message(user_id, get_text(user_id, 'welcome_merchant').format(m_id), reply_markup=build_main_menu(user_id))
    else:
        bot.send_message(user_id, get_text(user_id, 'welcome'), reply_markup=build_main_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["❌ ለመሰረዝ", "❌ Cancel"])
def cancel_action(message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    bot.send_message(user_id, get_text(user_id, 'msg_cancel'), reply_markup=build_main_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["⚙️ ማስተካከያ / Settings", "⚙️ Settings"])
def settings_menu(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("አማርኛ 🇪🇹", callback_data="lang_am"),
        types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    )
    bot.send_message(user_id, "እባክዎ የቦቱን ቋንቋ ይምረጡ / Please choose bot language:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    user_id = call.from_user.id
    lang = call.data.split('_')[1]
    user_language[str(user_id)] = lang
    sync_db()
    bot.answer_callback_query(call.id, "Language Updated!")
    bot.send_message(user_id, get_text(user_id, 'welcome'), reply_markup=build_main_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["💬 ሐሳብ አስተያየት", "💬 Support"])
def support_init(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'SUPPORT_MSG'}
    bot.send_message(user_id, get_text(user_id, 'msg_support'), reply_markup=build_cancel_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["🔐 ነጋዴ ለመሆን መመዝገቢያ", "🔐 Register as Merchant"])
def register_init(message):
    user_id = message.from_user.id
    user_states[user_id] = {'state': 'REG_SHOP'}
    bot.send_message(user_id, get_text(user_id, 'ask_shop'), reply_markup=build_cancel_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["➕ አዲስ ምርት ለመለጠፍ", "➕ Post an Ad"])
def post_init(message):
    user_id = message.from_user.id
    if str(user_id) not in merchants_db: return
    user_states[user_id] = {'state': 'POST_PHOTO'}
    bot.send_message(user_id, get_text(user_id, 'ask_prod_photo'), reply_markup=build_cancel_menu(user_id))

@bot.message_handler(func=lambda m: m.text in ["📥 የመጡ ትዕዛዞች", "📥 Received Orders"])
def view_orders(message):
    user_id = message.from_user.id
    u_str = str(user_id)
    if u_str not in merchants_db: return
    m_id = merchants_db[u_str]['merchant_id']
    
    merchant_orders = [o_id for o_id, o in orders_db.items() if o['merchant_id'] == m_id]
    if not merchant_orders:
        bot.send_message(user_id, get_text(user_id, 'no_orders'))
        return
        
    for o_id in merchant_orders:
        o = orders_db[o_id]
        status = o['status']
        text = f"📦 **ትዕዛዝ ቁጥር፦** `{o_id}`\n\n{o['details']}\nស្ថានភាព፦ {status}"
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ እቀበላለሁ", callback_data=f"ord_acc_{o_id}"),
            types.InlineKeyboardButton("❌ እሰርዛለሁ", callback_data=f"ord_rej_{o_id}")
        )
        bot.send_message(user_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith('ord_'))
def handle_order_status(call):
    data = call.data.split('_')
    action, o_id = data[1], data[2]if o_id in orders_db:
buyer_id = orders_db[o_id]['buyer_id']if action == 'acc':orders_db[o_id]['status'] = "ተቀባይነት አግኝቷል (Accepted)"bot.send_message(buyer_id, f"🎉 ማሳሰቢያ፦ ትዕዛዝ ቁጥር {o_id} በሻጩ ተቀባይነት አግኝቷል!")elif action == 'rej':orders_db[o_id]['status'] = "ተሰርዟል (Cancelled)"bot.send_message(buyer_id, f"❌ ማሳሰቢያ፦ ትዕዛዝ ቁጥር {o_id} በሻጩ በኩል ተሰርዟል።")sync_db()bot.answer_callback_query(call.id, "ምላሽዎ ተልኳል!")@bot.message_handler(func=lambda m: m.text in ["📋 የኔ ማስታወቂያዎች", "📋 My Ads"])def view_my_ads(message):user_id = message.from_user.idu_str = str(user_id)if u_str not in merchants_db: returnm_id = merchants_db[u_str]['merchant_id']my_prods = [p_id for p_id, p in products_db.items() if p['merchant_id'] == m_id]if not my_prods:bot.send_message(user_id, get_text(user_id, 'no_ads'))returnfor p_id in my_prods:p = products_db[p_id]text = f"📌 {p['title']}\nዋጋ: {p['price']}\nመግለጫ: {p['desc']}"markup = types.InlineKeyboardMarkup()markup.add(types.InlineKeyboardButton("🗑 ሰርዝ", callback_data=f"del_{p_id}"))bot.send_photo(user_id, p['photo'], caption=text, reply_markup=markup)@bot.callback_query_handler(func=lambda call: call.data.startswith('del_'))def delete_product(call):p_id = call.data.replace('del_', '')if p_id in products_db:products_db.pop(p_id, None)sync_db()bot.answer_callback_query(call.id, "ተሰርዟል!")bot.delete_message(call.message.chat.id , call.message.message_id) @bot.message_handler(func=lambda m: m.text in ["🛒 ምርት ለማዘዝ", "🛒 Order Now"])def general_order_init(message):user_id = message.from_user.iduser_states[user_id] = {'state': 'ORDER_NAME', 'prod_id': 'GENERAL'}bot.send_message(user_id, get_text(user_id, 'ask_order_name'), reply_markup=build_cancel_menu(user_id))@bot.message_handler(func=lambda m: m.text in ["📢 ምርቶችን በቻናል ይመልከቱ", "📢 View Channel"])def channel_redirect(message):bot.send_message(message.from_user.id, f"ወደ Yazone Store ቻናል ለመግባት ሊንኩን ይጫኑ፦ t.me")@bot.message_handler(content_types=['text', 'photo'])def handle_all_steps(message):user_id = message.from_user.idu_str = str(user_id)if user_id not in user_states: returnstate = user_states[user_id]['state']if state == 'SUPPORT_MSG':feedback = message.textbot.send_message(SUPPORT_GROUP_ID, f"💬 አዲስ አስተያየት ከቦቱ መጥቷል፦\n\nከአሳታሚ (ID: {user_id}):\n{feedback}")user_states.pop(user_id, None)bot.send_message(user_id, get_text(user_id, 'msg_support_sent'), reply_markup=build_main_menu(user_id))elif state == 'REG_SHOP':user_states[user_id]['shop_name'] = message.textuser_states[user_id]['state'] = 'REG_PHONE'bot.send_message(user_id, get_text(user_id, 'ask_phone')elif state == 'REG_PHONE':shop_name = user_states[user_id]['shop_name']phone = message.textm_id = f"YZ-{user_id}"merchants_db[u_str] = {'shop_name': shop_name, 'phone': phone, 'merchant_id': m_id}sync_db()user_states.pop(user_id, None)bot.send_message(user_id, get_text(user_id, 'reg_success').format(m_id), parse_mode="Markdown", reply_markup=build_main_menu(user_id))elif state == 'POST_PHOTO':if not message.photo: returnuser_states[user_id]['photo'] = message.photo[-1].file_iduser_states[user_id]['state'] = 'POST_TITLE'bot.send_message(user_id, get_text(user_id, 'ask_prod_title'))elif state == 'POST_TITLE':user_states[user_id]['title'] = message.textuser_states[user_id]['state'] = 'POST_PRICE'bot.send_message(user_id, get_text(user_id, 'ask_prod_price'))elif state == 'POST_PRICE':user_states[user_id]['price'] = message.textuser_states[user_id]['state'] = 'POST_DESC'bot.send_message(user_id, get_text(user_id, 'ask_prod_desc'))elif state == 'POST_DESC':photo = user_states[user_id]['photo']title = user_states[user_id]['title']price = user_states[user_id]['price']desc = message.textm_id = merchants_db[u_str]['merchant_id']p_id = str(len(products_db) + 1001)products_db[p_id] = {'merchant_id': m_id, 'photo': photo, 'title': title, 'price': price, 'desc': desc, 'seller_id': user_id}sync_db()user_states.pop(user_id, None)caption_text = f"🛍 {title}\n\n💵 ዋጋ: {price}\n📝 መግለጫ: {desc}\n\n🔢 መለያ ቁጥር: #{m_id}"inline_markup = types.InlineKeyboardMarkup()inline_markup.add(types.InlineKeyboardButton("🛒 ለማዘዝ እዚህ ይጫኑ", url=f"t.me_{p_id}"))bot.send_photo(CHANNEL_USERNAME, photo, caption=caption_text, reply_markup=inline_markup, parse_mode="Markdown")bot.send_message(user_id, get_text(user_id, 'prod_post_confirm'), reply_markup=build_main_menu(user_id))elif state == 'ORDER_NAME':user_states[user_id]['name'] = message.textuser_states[user_id]['state'] = 'ORDER_PHONE'bot.send_message(user_id, get_text(user_id, 'ask_order_phone'))elif state == 'ORDER_PHONE':user_states[user_id]['phone'] = message.textuser_states[user_id]['state'] = 'ORDER_ADDR'bot.send_message(user_id, get_text(user_id, 'ask_order_addr'))elif state == 'ORDER_ADDR':user_states[user_id]['addr'] = message.textuser_states[user_id]['state'] = 'ORDER_DATE'bot.send_message(user_id, get_text(user_id, 'ask_order_date'))elif state == 'ORDER_DATE':prod_id = user_states[user_id]['prod_id']name = user_states[user_id]['name']phone = user_states[user_id]['phone']addr = user_states[user_id]['addr']date = message.texto_id = str(len(orders_db) + 5001)details = f"👤 ገዢ: {name}\n📞 ስልክ: {phone}\n📍 አድራሻ: {addr}\n📅 የሚፈልጉበት ቀን: {date}" if prod_id != 'GENERAL' and prod_id in products_db:p = products_db[prod_id]m_id = p['merchant_id']seller_id = p['seller_id']details += f"\n\n🛍 ያዘዙት ምርት: {p['title']}\n💵 ዋጋ: {p['price']}"orders_db[o_id] = {'merchant_id': m_id, 'buyer_id': user_id, 'product_id': prod_id, 'details': details, 'status': 'በሂደት ላይ'}sync_db()bot.send_message(seller_id, f"🔔 አዲስ ትዕዛዝ መጥቶልዎታል!\n\n📥 የመጡ ትዕዛዞች ቁልፍን ይጫኑ።")else:bot.send_message(SUPPORT_GROUP_ID, f"🛒 አዲስ ጠቅላላ ትዕዛዝ መጥቷል፦\n\n{details}")user_states.pop(user_id, None)bot.send_message(user_id, get_text(user_id, 'order_success'), reply_markup=build_main_menu(user_id))bot.polling(none_stop=True) 
