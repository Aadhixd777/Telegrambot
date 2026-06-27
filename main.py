# ============================================
# MAFYA OTP BOT - FULL FIXED VERSION
# Channel: @NEXT_DYS
# Owner: LuciFer
# ============================================

import time
import requests
import json
import re
import os
from datetime import datetime, date, timedelta
from urllib.parse import quote_plus
from pathlib import Path
import sqlite3
import telebot
from telebot import types
import threading
import traceback
import random
import itertools
import logging
import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ============================================
# DASHBOARD CONFIGURATION (iVasms)
# ============================================

IVASMS_DASHBOARD = {
    "name": "iVasms",
    "type": "ivasms",
    "login_url": "https://ivas.tempnum.qzz.io/login",
    "base_url": "https://ivas.tempnum.qzz.io",
    "sms_api_endpoint": "https://ivas.tempnum.qzz.io/portal/sms/received/getsms",
    "username": "لوحه",
    "password": "اي شيء",
    "session": requests.Session(),
    "is_logged_in": False,
    "cookies": None,
    "csrf_token": None,
    "last_check": None
}

# ============================================
# GENERAL SETTINGS
# ============================================

USERNAME = "MAFYA123"
PASSWORD = "Bn_1411"
BOT_TOKEN = "8239745105:AAHcCzGLxhHK8VDw9mSQUqal-dZA7ICrA4E"  # Replace with your bot token
CHAT_IDS = [
    "-1004456953335",  # Replace with your group chat ID
]

REFRESH_INTERVAL = 3
TIMEOUT = 100
MAX_RETRIES = 5
RETRY_DELAY = 5

SENT_MESSAGES_FILE = "sent_messages.json"
ADMIN_IDS = [1305766743]  # Your Telegram user ID
DB_PATH = "bot.db"
FORCE_SUB_CHANNEL = None
FORCE_SUB_ENABLED = False
BOT_ACTIVE = True
CHANNEL_USERNAME = "@NEXT_DYS"

if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN must be set!")

# ============================================
# COUNTRY CODES DATABASE (COMPLETE)
# ============================================

COUNTRY_CODES = {
    "1": ("USA/Canada", "🇺🇸", "US"),
    "7": ("Russia", "🇷🇺", "RU"),
    "20": ("Egypt", "🇪🇬", "EG"),
    "27": ("South Africa", "🇿🇦", "ZA"),
    "30": ("Greece", "🇬🇷", "GR"),
    "31": ("Netherlands", "🇳🇱", "NL"),
    "32": ("Belgium", "🇧🇪", "BE"),
    "33": ("France", "🇫🇷", "FR"),
    "34": ("Spain", "🇪🇸", "ES"),
    "36": ("Hungary", "🇭🇺", "HU"),
    "39": ("Italy", "🇮🇹", "IT"),
    "40": ("Romania", "🇷🇴", "RO"),
    "41": ("Switzerland", "🇨🇭", "CH"),
    "43": ("Austria", "🇦🇹", "AT"),
    "44": ("United Kingdom", "🇬🇧", "UK"),
    "45": ("Denmark", "🇩🇰", "DK"),
    "46": ("Sweden", "🇸🇪", "SE"),
    "47": ("Norway", "🇳🇴", "NO"),
    "48": ("Poland", "🇵🇱", "PL"),
    "49": ("Germany", "🇩🇪", "DE"),
    "51": ("Peru", "🇵🇪", "PE"),
    "52": ("Mexico", "🇲🇽", "MX"),
    "53": ("Cuba", "🇨🇺", "CU"),
    "54": ("Argentina", "🇦🇷", "AR"),
    "55": ("Brazil", "🇧🇷", "BR"),
    "56": ("Chile", "🇨🇱", "CL"),
    "57": ("Colombia", "🇨🇴", "CO"),
    "58": ("Venezuela", "🇻🇪", "VE"),
    "60": ("Malaysia", "🇲🇾", "MY"),
    "61": ("Australia", "🇦🇺", "AU"),
    "62": ("Indonesia", "🇮🇩", "ID"),
    "63": ("Philippines", "🇵🇭", "PH"),
    "64": ("New Zealand", "🇳🇿", "NZ"),
    "65": ("Singapore", "🇸🇬", "SG"),
    "66": ("Thailand", "🇹🇭", "TH"),
    "81": ("Japan", "🇯🇵", "JP"),
    "82": ("South Korea", "🇰🇷", "KR"),
    "84": ("Vietnam", "🇻🇳", "VN"),
    "86": ("China", "🇨🇳", "CN"),
    "90": ("Turkey", "🇹🇷", "TR"),
    "91": ("India", "🇮🇳", "IN"),
    "92": ("Pakistan", "🇵🇰", "PK"),
    "93": ("Afghanistan", "🇦🇫", "AF"),
    "94": ("Sri Lanka", "🇱🇰", "LK"),
    "95": ("Myanmar", "🇲🇲", "MM"),
    "98": ("Iran", "🇮🇷", "IR"),
    "212": ("Morocco", "🇲🇦", "MA"),
    "213": ("Algeria", "🇩🇿", "DZ"),
    "216": ("Tunisia", "🇹🇳", "TN"),
    "218": ("Libya", "🇱🇾", "LY"),
    "220": ("Gambia", "🇬🇲", "GM"),
    "221": ("Senegal", "🇸🇳", "SN"),
    "222": ("Mauritania", "🇲🇷", "MR"),
    "223": ("Mali", "🇲🇱", "ML"),
    "224": ("Guinea", "🇬🇳", "GN"),
    "225": ("Ivory Coast", "🇨🇮", "CI"),
    "226": ("Burkina Faso", "🇧🇫", "BF"),
    "227": ("Niger", "🇳🇪", "NE"),
    "228": ("Togo", "🇹🇬", "TG"),
    "229": ("Benin", "🇧🇯", "BJ"),
    "230": ("Mauritius", "🇲🇺", "MU"),
    "231": ("Liberia", "🇱🇷", "LR"),
    "232": ("Sierra Leone", "🇸🇱", "SL"),
    "233": ("Ghana", "🇬🇭", "GH"),
    "234": ("Nigeria", "🇳🇬", "NG"),
    "235": ("Chad", "🇹🇩", "TD"),
    "236": ("Central African Rep", "🇨🇫", "CF"),
    "237": ("Cameroon", "🇨🇲", "CM"),
    "238": ("Cape Verde", "🇨🇻", "CV"),
    "239": ("Sao Tome", "🇸🇹", "ST"),
    "240": ("Equatorial Guinea", "🇬🇶", "GQ"),
    "241": ("Gabon", "🇬🇦", "GA"),
    "242": ("Congo", "🇨🇬", "CG"),
    "243": ("DR Congo", "🇨🇩", "CD"),
    "244": ("Angola", "🇦🇴", "AO"),
    "245": ("Guinea-Bissau", "🇬🇼", "GW"),
    "248": ("Seychelles", "🇸🇨", "SC"),
    "249": ("Sudan", "🇸🇩", "SD"),
    "250": ("Rwanda", "🇷🇼", "RW"),
    "251": ("Ethiopia", "🇪🇹", "ET"),
    "252": ("Somalia", "🇸🇴", "SO"),
    "253": ("Djibouti", "🇩🇯", "DJ"),
    "254": ("Kenya", "🇰🇪", "KE"),
    "255": ("Tanzania", "🇹🇿", "TZ"),
    "256": ("Uganda", "🇺🇬", "UG"),
    "257": ("Burundi", "🇧🇮", "BI"),
    "258": ("Mozambique", "🇲🇿", "MZ"),
    "260": ("Zambia", "🇿🇲", "ZM"),
    "261": ("Madagascar", "🇲🇬", "MG"),
    "262": ("Reunion", "🇷🇪", "RE"),
    "263": ("Zimbabwe", "🇿🇼", "ZW"),
    "264": ("Namibia", "🇳🇦", "NA"),
    "265": ("Malawi", "🇲🇼", "MW"),
    "266": ("Lesotho", "🇱🇸", "LS"),
    "267": ("Botswana", "🇧🇼", "BW"),
    "268": ("Eswatini", "🇸🇿", "SZ"),
    "269": ("Comoros", "🇰🇲", "KM"),
    "350": ("Gibraltar", "🇬🇮", "GI"),
    "351": ("Portugal", "🇵🇹", "PT"),
    "352": ("Luxembourg", "🇱🇺", "LU"),
    "353": ("Ireland", "🇮🇪", "IE"),
    "354": ("Iceland", "🇮🇸", "IS"),
    "355": ("Albania", "🇦🇱", "AL"),
    "356": ("Malta", "🇲🇹", "MT"),
    "357": ("Cyprus", "🇨🇾", "CY"),
    "358": ("Finland", "🇫🇮", "FI"),
    "359": ("Bulgaria", "🇧🇬", "BG"),
    "370": ("Lithuania", "🇱🇹", "LT"),
    "371": ("Latvia", "🇱🇻", "LV"),
    "372": ("Estonia", "🇪🇪", "EE"),
    "373": ("Moldova", "🇲🇩", "MD"),
    "374": ("Armenia", "🇦🇲", "AM"),
    "375": ("Belarus", "🇧🇾", "BY"),
    "376": ("Andorra", "🇦🇩", "AD"),
    "377": ("Monaco", "🇲🇨", "MC"),
    "378": ("San Marino", "🇸🇲", "SM"),
    "380": ("Ukraine", "🇺🇦", "UA"),
    "381": ("Serbia", "🇷🇸", "RS"),
    "382": ("Montenegro", "🇲🇪", "ME"),
    "383": ("Kosovo", "🇽🇰", "XK"),
    "385": ("Croatia", "🇭🇷", "HR"),
    "386": ("Slovenia", "🇸🇮", "SI"),
    "387": ("Bosnia", "🇧🇦", "BA"),
    "389": ("North Macedonia", "🇲🇰", "MK"),
    "420": ("Czech Republic", "🇨🇿", "CZ"),
    "421": ("Slovakia", "🇸🇰", "SK"),
    "423": ("Liechtenstein", "🇱🇮", "LI"),
    "500": ("Falkland Islands", "🇫🇰", "FK"),
    "501": ("Belize", "🇧🇿", "BZ"),
    "502": ("Guatemala", "🇬🇹", "GT"),
    "503": ("El Salvador", "🇸🇻", "SV"),
    "504": ("Honduras", "🇭🇳", "HN"),
    "505": ("Nicaragua", "🇳🇮", "NI"),
    "506": ("Costa Rica", "🇨🇷", "CR"),
    "507": ("Panama", "🇵🇦", "PA"),
    "509": ("Haiti", "🇭🇹", "HT"),
    "591": ("Bolivia", "🇧🇴", "BO"),
    "592": ("Guyana", "🇬🇾", "GY"),
    "593": ("Ecuador", "🇪🇨", "EC"),
    "595": ("Paraguay", "🇵🇾", "PY"),
    "597": ("Suriname", "🇸🇷", "SR"),
    "598": ("Uruguay", "🇺🇾", "UY"),
    "670": ("Timor-Leste", "🇹🇱", "TL"),
    "673": ("Brunei", "🇧🇳", "BN"),
    "674": ("Nauru", "🇳🇷", "NR"),
    "675": ("Papua New Guinea", "🇵🇬", "PG"),
    "676": ("Tonga", "🇹🇴", "TO"),
    "677": ("Solomon Islands", "🇸🇧", "SB"),
    "678": ("Vanuatu", "🇻🇺", "VU"),
    "679": ("Fiji", "🇫🇯", "FJ"),
    "680": ("Palau", "🇵🇼", "PW"),
    "685": ("Samoa", "🇼🇸", "WS"),
    "686": ("Kiribati", "🇰🇮", "KI"),
    "687": ("New Caledonia", "🇳🇨", "NC"),
    "688": ("Tuvalu", "🇹🇻", "TV"),
    "689": ("French Polynesia", "🇵🇫", "PF"),
    "691": ("Micronesia", "🇫🇲", "FM"),
    "692": ("Marshall Islands", "🇲🇭", "MH"),
    "850": ("North Korea", "🇰🇵", "KP"),
    "852": ("Hong Kong", "🇭🇰", "HK"),
    "853": ("Macau", "🇲🇴", "MO"),
    "855": ("Cambodia", "🇰🇭", "KH"),
    "856": ("Laos", "🇱🇦", "LA"),
    "960": ("Maldives", "🇲🇻", "MV"),
    "961": ("Lebanon", "🇱🇧", "LB"),
    "962": ("Jordan", "🇯🇴", "JO"),
    "963": ("Syria", "🇸🇾", "SY"),
    "964": ("Iraq", "🇮🇶", "IQ"),
    "965": ("Kuwait", "🇰🇼", "KW"),
    "966": ("Saudi Arabia", "🇸🇦", "SA"),
    "967": ("Yemen", "🇾🇪", "YE"),
    "968": ("Oman", "🇴🇲", "OM"),
    "970": ("Palestine", "🇵🇸", "PS"),
    "971": ("UAE", "🇦🇪", "AE"),
    "972": ("Israel", "🇮🇱", "IL"),
    "973": ("Bahrain", "🇧🇭", "BH"),
    "974": ("Qatar", "🇶🇦", "QA"),
    "975": ("Bhutan", "🇧🇹", "BT"),
    "976": ("Mongolia", "🇲🇳", "MN"),
    "977": ("Nepal", "🇳🇵", "NP"),
    "992": ("Tajikistan", "🇹🇯", "TJ"),
    "993": ("Turkmenistan", "🇹🇲", "TM"),
    "994": ("Azerbaijan", "🇦🇿", "AZ"),
    "995": ("Georgia", "🇬🇪", "GE"),
    "996": ("Kyrgyzstan", "🇰🇬", "KG"),
    "998": ("Uzbekistan", "🇺🇿", "UZ"),
}

# ============================================
# DATABASE FUNCTIONS
# ============================================

def get_setting(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT value FROM bot_settings WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO bot_settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        country_code TEXT,
        assigned_number TEXT,
        is_banned INTEGER DEFAULT 0,
        private_combo_country TEXT DEFAULT NULL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS combos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_code TEXT,
        combo_index INTEGER DEFAULT 1,
        numbers TEXT,
        UNIQUE(country_code, combo_index)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS otp_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT,
        otp TEXT,
        full_message TEXT,
        timestamp TEXT,
        assigned_to INTEGER
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS dashboards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        base_url TEXT,
        ajax_path TEXT,
        login_page TEXT,
        login_post TEXT,
        username TEXT,
        password TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS bot_settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS private_combos (
        user_id INTEGER,
        country_code TEXT,
        numbers TEXT,
        PRIMARY KEY (user_id, country_code)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS force_sub_channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_url TEXT UNIQUE NOT NULL,
        description TEXT DEFAULT '',
        enabled INTEGER DEFAULT 1
    )''')

    c.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES ('force_sub_channel', '')")
    c.execute("INSERT OR IGNORE INTO bot_settings (key, value) VALUES ('force_sub_enabled', '0')")

    conn.commit()
    conn.close()
    print("✅ Database initialized")

init_db()

# ============================================
# USER DATABASE FUNCTIONS
# ============================================

def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def save_user(user_id, username="", first_name="", last_name="", country_code=None, assigned_number=None, private_combo_country=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    existing_data = get_user(user_id)
    if existing_data:
        if country_code is None:
            country_code = existing_data[4]
        if assigned_number is None:
            assigned_number = existing_data[5]
        if private_combo_country is None:
            private_combo_country = existing_data[7]

    c.execute("""
        REPLACE INTO users (user_id, username, first_name, last_name, country_code, assigned_number, is_banned, private_combo_country)
        VALUES (?, ?, ?, ?, ?, ?, COALESCE((SELECT is_banned FROM users WHERE user_id=?), 0), ?)
    """, (
        user_id,
        username,
        first_name,
        last_name,
        country_code,
        assigned_number,
        user_id,
        private_combo_country
    ))
    conn.commit()
    conn.close()

def ban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id):
    user = get_user(user_id)
    return user and user[6] == 1

def is_maintenance_mode():
    return not BOT_ACTIVE

def set_maintenance_mode(status):
    global BOT_ACTIVE
    BOT_ACTIVE = not status

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned=0")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

def get_combo(country_code, combo_index=1, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT numbers FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
        row = c.fetchone()
        if row:
            conn.close()
            return json.loads(row[0])
    c.execute("SELECT numbers FROM combos WHERE country_code=? AND combo_index=?", (country_code, combo_index))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else []

def save_combo(country_code, numbers, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if user_id:
        c.execute("REPLACE INTO private_combos (user_id, country_code, numbers) VALUES (?, ?, ?)",
                  (user_id, country_code, json.dumps(numbers)))
    else:
        c.execute("SELECT MAX(combo_index) FROM combos WHERE country_code=?", (country_code,))
        max_index = c.fetchone()[0]
        next_index = 1 if max_index is None else max_index + 1
        
        c.execute("INSERT INTO combos (country_code, combo_index, numbers) VALUES (?, ?, ?)",
                  (country_code, next_index, json.dumps(numbers)))
    
    conn.commit()
    conn.close()

def delete_combo(country_code, combo_index=None, user_id=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
        c = conn.cursor()
        
        if user_id:
            c.execute("DELETE FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
        elif combo_index:
            c.execute("DELETE FROM combos WHERE country_code=? AND combo_index=?", (country_code, combo_index))
        else:
            c.execute("DELETE FROM combos WHERE country_code=?", (country_code,))
        
        conn.commit()
        print(f"✅ Combo deleted: {country_code} (index: {combo_index})")
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite Error in delete_combo: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_all_combos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT country_code, combo_index FROM combos ORDER BY country_code, combo_index")
    combos = c.fetchall()
    conn.close()
    return combos

def assign_number_to_user(user_id, number):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=? WHERE user_id=?", (number, user_id))
    conn.commit()
    conn.close()

def get_user_by_number(number):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE assigned_number=?", (number,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def log_otp(number, otp, full_message, assigned_to=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO otp_logs (number, otp, full_message, timestamp, assigned_to) VALUES (?, ?, ?, ?, ?)",
              (number, otp, full_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), assigned_to))
    conn.commit()
    conn.close()

def release_number(old_number):
    if not old_number:
        return
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=NULL WHERE assigned_number=?", (old_number,))
    conn.commit()
    conn.close()

def get_otp_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM otp_logs")
    logs = c.fetchall()
    conn.close()
    return logs

def get_user_info(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_available_numbers(country_code, combo_index=1, user_id=None):
    all_numbers = get_combo(country_code, combo_index, user_id)
    if not all_numbers:
        return []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT assigned_number FROM users WHERE assigned_number IS NOT NULL AND assigned_number != ''")
    used_numbers = set(row[0] for row in c.fetchall())
    conn.close()
    available = [num for num in all_numbers if num not in used_numbers]
    return available

# ============================================
# FORCE SUBSCRIPTION FUNCTIONS (FIXED)
# ============================================

def get_all_force_sub_channels(enabled_only=True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if enabled_only:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels WHERE enabled = 1 ORDER BY id")
    else:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def add_force_sub_channel(channel_url, description=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO force_sub_channels (channel_url, description, enabled) VALUES (?, ?, 1)",
                  (channel_url.strip(), description.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM force_sub_channels WHERE id = ?", (channel_id,))
    changed = c.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def toggle_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE force_sub_channels SET enabled = 1 - enabled WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

def force_sub_check(user_id):
    """Check if user is subscribed to all channels - FIXED"""
    channels = get_all_force_sub_channels(True)
    if not channels:
        return True

    for _, url, _ in channels:
        try:
            # Extract channel username from URL
            channel_username = url
            if url.startswith("https://t.me/"):
                channel_username = "@" + url.split("/")[-1]
            elif url.startswith("@"):
                channel_username = url
            else:
                channel_username = f"@{url}"
            
            member = bot.get_chat_member(channel_username, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"[!] Error checking channel {url}: {e}")
            return False
    return True

def force_sub_markup():
    """Create force sub markup - FIXED"""
    channels = get_all_force_sub_channels(True)
    if not channels:
        return None

    markup = types.InlineKeyboardMarkup()
    for _, url, desc in channels:
        # Convert to proper URL for button
        button_url = url
        if url.startswith("@"):
            button_url = f"https://t.me/{url[1:]}"
        elif not url.startswith("http"):
            button_url = f"https://t.me/{url}"
        
        text = f"📢 {desc}" if desc else "📢 Subscribe"
        markup.add(types.InlineKeyboardButton(text, url=button_url))
    
    markup.add(types.InlineKeyboardButton("✅ Verify", callback_data="check_sub"))
    return markup

def is_admin(user_id):
    return user_id in ADMIN_IDS

def safe_html(text):
    if not text:
        return ""
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

# ============================================
# TELEGRAM BOT INITIALIZATION
# ============================================

bot = telebot.TeleBot(BOT_TOKEN)

# ============================================
# BOT COMMAND HANDLERS
# ============================================

user_states = {}

@bot.message_handler(commands=['start'])
def start_cmd(message):
    uid = message.from_user.id
    cid = message.chat.id
    
    if is_maintenance_mode() and not is_admin(uid):
        bot.send_message(cid, "<b>🔧 Bot under maintenance. Try later.</b>", parse_mode="HTML")
        return
    
    if is_banned(uid):
        bot.reply_to(message, "<b>🚫 You are banned.</b>", parse_mode="HTML")
        return
    
    if not force_sub_check(uid):
        mk = force_sub_markup()
        if mk:
            bot.send_message(cid, "<b>🔒 Subscribe to use bot.</b>", parse_mode="HTML", reply_markup=mk)
        return
    
    if not get_user(uid):
        save_user(uid, message.from_user.username or "", message.from_user.first_name or "", message.from_user.last_name or "")
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    user = get_user(uid)
    priv = user[7] if user else None
    combos = get_all_combos()
    
    ccs = {}
    for cc, ci in combos:
        if cc not in ccs:
            ccs[cc] = []
        ccs[cc].append(ci)
    
    if priv and priv in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[priv]
        btns.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{priv}_1"))
    
    for cc, idxs in ccs.items():
        if cc in COUNTRY_CODES and cc != priv:
            name, flag, _ = COUNTRY_CODES[cc]
            for i in idxs:
                txt = f"{flag} {name}" if len(idxs) == 1 else f"{flag} {name} ({i})"
                btns.append(types.InlineKeyboardButton(txt, callback_data=f"country_{cc}_{i}"))
    
    for i in range(0, len(btns), 2):
        markup.row(*btns[i:i+2])
    
    if is_admin(uid):
        markup.add(types.InlineKeyboardButton("🔐 Admin", callback_data="admin_panel"))
    
    bot.send_message(cid, "<b>Select country:</b>", parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "check_sub")
def check_sub_cb(call):
    if force_sub_check(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified", show_alert=True)
        start_cmd(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Not subscribed", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("country_"))
def country_cb(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    
    if is_banned(uid) or not force_sub_check(uid):
        return
    
    parts = call.data.split("_")
    cc = parts[1]
    ci = int(parts[2]) if len(parts) > 2 else 1
    
    avail = get_available_numbers(cc, ci, uid)
    if not avail:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="back_to_countries"))
        bot.edit_message_text("<b>❌ No numbers available.</b>", cid, mid, reply_markup=markup, parse_mode="HTML")
        return
    
    num = random.choice(avail)
    old = get_user(uid)
    if old and old[5]:
        release_number(old[5])
    assign_number_to_user(uid, num)
    save_user(uid, country_code=cc, assigned_number=num)
    
    name, flag, _ = COUNTRY_CODES.get(cc, ("Unknown", "🌍", ""))
    text = f"<b>◈ Number:</b> <code>+{num}</code>\n<b>◈ Country:</b> {flag} {name}\n<b>◈ Combo:</b> #{ci}\n<b>◈ Status:</b> ⏳ Waiting"
    
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🔄 Change", callback_data=f"change_num_{cc}_{ci}"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_countries")
    )
    bot.edit_message_text(text, cid, mid, reply_markup=markup, parse_mode="HTML")
    bot.answer_callback_query(call.id, "✅ Number assigned")

@bot.callback_query_handler(func=lambda c: c.data.startswith("change_num_"))
def change_cb(call):
    uid = call.from_user.id
    if is_banned(uid) or not force_sub_check(uid):
        return
    parts = call.data.split("_")
    cc = parts[2]
    ci = int(parts[3]) if len(parts) > 3 else 1
    avail = get_available_numbers(cc, ci, uid)
    if not avail:
        bot.answer_callback_query(call.id, "❌ No numbers", show_alert=True)
        return
    num = random.choice(avail)
    old = get_user(uid)
    if old and old[5]:
        release_number(old[5])
    assign_number_to_user(uid, num)
    save_user(uid, assigned_number=num)
    name, flag, _ = COUNTRY_CODES.get(cc, ("Unknown", "🌍", ""))
    text = f"<b>◈ Number:</b> <code>+{num}</code>\n<b>◈ Country:</b> {flag} {name}\n<b>◈ Combo:</b> #{ci}\n<b>◈ Status:</b> ⏳ Waiting"
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🔄 Change", callback_data=f"change_num_{cc}_{ci}"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_countries")
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
    bot.answer_callback_query(call.id, "✅ Changed")

@bot.callback_query_handler(func=lambda c: c.data == "back_to_countries")
def back_cb(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    markup = types.InlineKeyboardMarkup(row_width=2)
    btns = []
    user = get_user(uid)
    priv = user[7] if user else None
    combos = get_all_combos()
    ccs = {}
    for cc, ci in combos:
        if cc not in ccs:
            ccs[cc] = []
        ccs[cc].append(ci)
    if priv and priv in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[priv]
        btns.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{priv}_1"))
    for cc, idxs in ccs.items():
        if cc in COUNTRY_CODES and cc != priv:
            name, flag, _ = COUNTRY_CODES[cc]
            for i in idxs:
                txt = f"{flag} {name}" if len(idxs) == 1 else f"{flag} {name} ({i})"
                btns.append(types.InlineKeyboardButton(txt, callback_data=f"country_{cc}_{i}"))
    for i in range(0, len(btns), 2):
        markup.row(*btns[i:i+2])
    if is_admin(uid):
        markup.add(types.InlineKeyboardButton("🔐 Admin", callback_data="admin_panel"))
    bot.edit_message_text("<b>Select country:</b>", cid, mid, reply_markup=markup, parse_mode="HTML")
    bot.answer_callback_query(call.id)

# ============================================
# ADMIN PANEL
# ============================================

def admin_menu():
    mk = types.InlineKeyboardMarkup()
    st = "🟢 Online" if not is_maintenance_mode() else "🔴 Maintenance"
    mk.add(types.InlineKeyboardButton(f"{st}", callback_data="toggle_maintenance"))
    mk.row(
        types.InlineKeyboardButton("📥 Add Combo", callback_data="admin_add_combo"),
        types.InlineKeyboardButton("🗑️ Del Combo", callback_data="admin_del_combo")
    )
    mk.row(
        types.InlineKeyboardButton("📊 Stats", callback_data="admin_stats"),
        types.InlineKeyboardButton("📄 Report", callback_data="admin_full_report")
    )
    mk.row(
        types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast_all"),
        types.InlineKeyboardButton("📨 To User", callback_data="admin_broadcast_user")
    )
    mk.row(
        types.InlineKeyboardButton("🚫 Ban", callback_data="admin_ban"),
        types.InlineKeyboardButton("✅ Unban", callback_data="admin_unban"),
        types.InlineKeyboardButton("👤 Info", callback_data="admin_user_info")
    )
    mk.row(
        types.InlineKeyboardButton("🔗 Force Sub", callback_data="admin_force_sub"),
        types.InlineKeyboardButton("🔑 Private", callback_data="admin_private_combo")
    )
    mk.add(types.InlineKeyboardButton("🔙 Exit", callback_data="back_to_countries"))
    return mk

@bot.callback_query_handler(func=lambda c: c.data == "admin_panel")
def admin_panel_cb(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admins only", show_alert=True)
        return
    bot.edit_message_text("<b>🔐 Admin Panel</b>", call.message.chat.id, call.message.message_id,
                         parse_mode="HTML", reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda c: c.data == "toggle_maintenance")
def toggle_maint_cb(call):
    if not is_admin(call.from_user.id):
        return
    set_maintenance_mode(is_maintenance_mode())
    bot.answer_callback_query(call.id, "✅ Toggled", show_alert=True)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda c: c.data == "admin_force_sub")
def force_sub_menu_cb(call):
    if not is_admin(call.from_user.id):
        return
    chs = get_all_force_sub_channels(False)
    txt = f"⚙️ Force Sub Channels: {len(chs)}\n"
    mk = types.InlineKeyboardMarkup()
    for cid, url, desc in chs:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT enabled FROM force_sub_channels WHERE id=?", (cid,))
        en = cur.fetchone()[0]
        conn.close()
        st = "✅" if en else "❌"
        mk.add(types.InlineKeyboardButton(f"{st} {desc or url[:20]}", callback_data=f"edit_fc_{cid}"))
    mk.add(types.InlineKeyboardButton("➕ Add", callback_data="add_fc"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "add_fc")
def add_fc_step1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "add_fc_url"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_force_sub"))
    bot.edit_message_text("Send channel link (@ or https):", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "add_fc_url")
def add_fc_step2(msg):
    url = msg.text.strip()
    
    # Normalize URL - FIXED
    if url.startswith("https://t.me/"):
        pass
    elif url.startswith("@"):
        url = f"https://t.me/{url[1:]}"
    elif not url.startswith("http"):
        url = f"https://t.me/{url}"
    else:
        bot.reply_to(msg, "❌ Invalid link! Must be @channel or https://t.me/channel")
        return
    
    user_states[msg.from_user.id] = {"step": "add_fc_desc", "url": url}
    bot.reply_to(msg, "Enter description for the channel (or leave empty):")

@bot.message_handler(func=lambda m: isinstance(user_states.get(m.from_user.id), dict) and user_states[m.from_user.id].get("step") == "add_fc_desc")
def add_fc_step3(msg):
    data = user_states[msg.from_user.id]
    if add_force_sub_channel(data["url"], msg.text.strip()):
        bot.reply_to(msg, "✅ Channel added")
    else:
        bot.reply_to(msg, "❌ Already exists")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_fc_"))
def edit_fc_cb(call):
    if not is_admin(call.from_user.id):
        return
    cid = int(call.data.split("_")[2])
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT channel_url, description, enabled FROM force_sub_channels WHERE id=?", (cid,))
    url, desc, en = cur.fetchone()
    conn.close()
    txt = f"Link: {url}\nDesc: {desc or '-'}\nStatus: {'Enabled' if en else 'Disabled'}"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("✏️ Edit Desc", callback_data=f"edit_desc_{cid}"))
    mk.add(types.InlineKeyboardButton("❌ Disable" if en else "✅ Enable", callback_data=f"toggle_fc_{cid}"))
    mk.add(types.InlineKeyboardButton("🗑️ Delete", callback_data=f"del_fc_{cid}"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_force_sub"))
    bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("toggle_fc_"))
def toggle_fc_cb(call):
    cid = int(call.data.split("_")[2])
    toggle_force_sub_channel(cid)
    bot.answer_callback_query(call.id, "✅ Toggled", show_alert=True)
    force_sub_menu_cb(call)

@bot.callback_query_handler(func=lambda c: c.data.startswith("del_fc_"))
def del_fc_cb(call):
    cid = int(call.data.split("_")[2])
    if delete_force_sub_channel(cid):
        bot.answer_callback_query(call.id, "✅ Deleted", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ Failed", show_alert=True)
    force_sub_menu_cb(call)

@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_desc_"))
def edit_desc_cb(call):
    cid = int(call.data.split("_")[2])
    user_states[call.from_user.id] = f"edit_desc_{cid}"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data=f"edit_fc_{cid}"))
    bot.edit_message_text("Send new description:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: isinstance(user_states.get(m.from_user.id), str) and user_states[m.from_user.id].startswith("edit_desc_"))
def edit_desc_final(msg):
    try:
        cid = int(user_states[msg.from_user.id].split("_")[2])
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("UPDATE force_sub_channels SET description=? WHERE id=?", (msg.text.strip(), cid))
        conn.commit()
        conn.close()
        bot.reply_to(msg, "✅ Updated")
    except:
        bot.reply_to(msg, "❌ Error")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_add_combo")
def add_combo_cb(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "wait_combo"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("📤 Send TXT file", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(content_types=['document'])
def combo_file(msg):
    if not is_admin(msg.from_user.id) or user_states.get(msg.from_user.id) != "wait_combo":
        return
    try:
        fi = bot.get_file(msg.document.file_id)
        dat = bot.download_file(fi.file_path).decode('utf-8')
        lines = [l.strip() for l in dat.splitlines() if l.strip()]
        if not lines:
            bot.reply_to(msg, "❌ Empty file")
            return
        
        # Detect country from first 5 numbers
        detected_countries = set()
        for sample in lines[:5]:
            clean_num = re.sub(r'[\+\s\-\(\)]', '', sample)
            sorted_codes = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)
            for code in sorted_codes:
                if clean_num.startswith(code):
                    detected_countries.add(code)
                    break
        
        if len(detected_countries) == 1:
            cc = list(detected_countries)[0]
            save_combo(cc, lines)
            name, flag, _ = COUNTRY_CODES[cc]
            bot.reply_to(msg, f"✅ Combo saved for {flag} {name}\n📊 Numbers: {len(lines)}")
            del user_states[msg.from_user.id]
            
        elif len(detected_countries) > 1:
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for cc in detected_countries:
                name, flag, _ = COUNTRY_CODES[cc]
                buttons.append(types.InlineKeyboardButton(f"{flag} {name}", callback_data=f"choose_{cc}"))
            
            for i in range(0, len(buttons), 2):
                markup.row(*buttons[i:i+2])
            
            user_states[msg.from_user.id] = {"step": "choose_country", "numbers": lines, "file_msg": msg}
            bot.reply_to(msg, "📌 Multiple countries detected. Please select one:", reply_markup=markup)
            
        else:
            markup = types.InlineKeyboardMarkup(row_width=2)
            buttons = []
            for code, (name, flag, _) in list(COUNTRY_CODES.items())[:20]:
                buttons.append(types.InlineKeyboardButton(f"{flag} {name}", callback_data=f"manual_{code}"))
            
            for i in range(0, len(buttons), 2):
                markup.row(*buttons[i:i+2])
            
            user_states[msg.from_user.id] = {"step": "manual_country", "numbers": lines, "file_msg": msg}
            bot.reply_to(msg, "❌ Cannot detect country. Please select manually:", reply_markup=markup)
        
    except Exception as e:
        bot.reply_to(msg, f"❌ Error: {str(e)}")

@bot.callback_query_handler(func=lambda c: c.data.startswith("choose_") or c.data.startswith("manual_"))
def choose_country_cb(call):
    if not is_admin(call.from_user.id):
        return
    
    data = user_states.get(call.from_user.id)
    if not data or data.get("step") not in ["choose_country", "manual_country"]:
        bot.answer_callback_query(call.id, "❌ Session expired")
        return
    
    cc = call.data.split("_")[1]
    numbers = data["numbers"]
    
    save_combo(cc, numbers)
    name, flag, _ = COUNTRY_CODES[cc]
    
    bot.edit_message_text(
        f"✅ Combo saved for {flag} {name}\n📊 Numbers: {len(numbers)}",
        call.message.chat.id,
        call.message.message_id
    )
    
    if data.get("file_msg"):
        try:
            bot.reply_to(data["file_msg"], f"✅ Combo added for {flag} {name}")
        except:
            pass
    
    del user_states[call.from_user.id]
    bot.answer_callback_query(call.id, "✅ Saved!")

@bot.callback_query_handler(func=lambda c: c.data == "admin_del_combo")
def del_combo_cb(call):
    if not is_admin(call.from_user.id):
        return
    combos = get_all_combos()
    if not combos:
        bot.answer_callback_query(call.id, "No combos")
        return
    mk = types.InlineKeyboardMarkup()
    ccs = {}
    for cc, ci in combos:
        if cc not in ccs:
            ccs[cc] = []
        ccs[cc].append(ci)
    for cc, idxs in ccs.items():
        if cc in COUNTRY_CODES:
            name, flag, _ = COUNTRY_CODES[cc]
            for i in idxs:
                txt = f"{flag} {name}" if len(idxs) == 1 else f"{flag} {name} ({i})"
                mk.add(types.InlineKeyboardButton(txt, callback_data=f"delconf_{cc}_{i}"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Select combo:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("delconf_"))
def delconf_cb(call):
    if not is_admin(call.from_user.id):
        return
    parts = call.data.split("_")
    cc = parts[1]
    ci = int(parts[2])
    if delete_combo(cc, ci):
        name, flag, _ = COUNTRY_CODES.get(cc, ("Unknown", "🌍", ""))
        bot.answer_callback_query(call.id, f"✅ {flag} {name} deleted", show_alert=True)
    else:
        bot.answer_callback_query(call.id, "❌ Failed", show_alert=True)
    del_combo_cb(call)

@bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
def stats_cb(call):
    if not is_admin(call.from_user.id):
        return
    users = len(get_all_users())
    combos = get_all_combos()
    uc = len(set(c[0] for c in combos))
    tc = len(combos)
    tn = 0
    for cc, ci in combos:
        tn += len(get_combo(cc, ci))
    otp = len(get_otp_logs())
    txt = f"📊 Stats:\n👥 Users: {users}\n🌐 Countries: {uc}\n📦 Combos: {tc}\n📞 Numbers: {tn}\n🔑 OTPs: {otp}"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "admin_full_report")
def report_cb(call):
    if not is_admin(call.from_user.id):
        return
    try:
        txt = "📊 Full Report\n" + "="*40 + "\n\n"
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        for u in cur.fetchall():
            st = "Banned" if u[6] else "Active"
            txt += f"ID: {u[0]} | @{u[1] or 'N/A'} | Num: {u[5] or 'N/A'} | {st}\n"
        txt += "\n" + "="*40 + "\n\n"
        cur.execute("SELECT * FROM otp_logs")
        for log in cur.fetchall():
            ui = get_user_info(log[5]) if log[5] else None
            tag = f"@{ui[1]}" if ui and ui[1] else f"ID:{log[5] or 'N/A'}"
            txt += f"Num: {log[1]} | OTP: {log[2]} | User: {tag} | Time: {log[4]}\n"
        txt += "\n" + "="*40 + "\n\nCombos:\n"
        cur.execute("SELECT country_code, combo_index FROM combos")
        for cc, ci in cur.fetchall():
            name, flag, _ = COUNTRY_CODES.get(cc, ("Unknown", "🌍", ""))
            cnt = len(get_combo(cc, ci))
            txt += f"{flag} {name} ({ci}): {cnt} nums\n"
        conn.close()
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(txt)
        with open("report.txt", "rb") as f:
            bot.send_document(call.from_user.id, f)
        os.remove("report.txt")
        bot.answer_callback_query(call.id, "✅ Sent", show_alert=True)
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ {e}", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def ban1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "ban"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Enter user ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "ban")
def ban2(msg):
    try:
        uid = int(msg.text)
        ban_user(uid)
        bot.reply_to(msg, f"✅ Banned {uid}")
    except:
        bot.reply_to(msg, "❌ Invalid")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_unban")
def unban1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "unban"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Enter user ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "unban")
def unban2(msg):
    try:
        uid = int(msg.text)
        unban_user(uid)
        bot.reply_to(msg, f"✅ Unbanned {uid}")
    except:
        bot.reply_to(msg, "❌ Invalid")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast_all")
def bc1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "bc_all"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Send message:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "bc_all")
def bc2(msg):
    users = get_all_users()
    ok = 0
    for uid in users:
        try:
            bot.send_message(uid, msg.text)
            ok += 1
        except:
            pass
    bot.reply_to(msg, f"✅ Sent to {ok}/{len(users)}")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast_user")
def bcu1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "bcu_id"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Enter user ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "bcu_id")
def bcu2(msg):
    try:
        uid = int(msg.text)
        user_states[msg.from_user.id] = f"bcu_msg_{uid}"
        bot.reply_to(msg, "Send message:")
    except:
        bot.reply_to(msg, "❌ Invalid")

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id, "").startswith("bcu_msg_"))
def bcu3(msg):
    uid = int(user_states[msg.from_user.id].split("_")[2])
    try:
        bot.send_message(uid, msg.text)
        bot.reply_to(msg, f"✅ Sent to {uid}")
    except Exception as e:
        bot.reply_to(msg, f"❌ {e}")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_user_info")
def inf1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "info"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Enter user ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "info")
def inf2(msg):
    try:
        uid = int(msg.text)
        u = get_user_info(uid)
        if not u:
            bot.reply_to(msg, "❌ Not found")
            return
        st = "Banned" if u[6] else "Active"
        txt = f"ID: {u[0]}\n@: {u[1] or 'N/A'}\nName: {u[2]} {u[3]}\nNum: {u[5] or 'N/A'}\nStatus: {st}"
        bot.reply_to(msg, txt)
    except Exception as e:
        bot.reply_to(msg, f"❌ {e}")
    del user_states[msg.from_user.id]

@bot.callback_query_handler(func=lambda c: c.data == "admin_private_combo")
def priv_menu(call):
    if not is_admin(call.from_user.id):
        return
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("➕ Add", callback_data="add_priv"))
    mk.add(types.InlineKeyboardButton("🗑️ Delete", callback_data="del_priv"))
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("Private Combo:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data == "add_priv")
def add_priv1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "priv_uid"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_private_combo"))
    bot.edit_message_text("User ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "priv_uid")
def add_priv2(msg):
    try:
        uid = int(msg.text)
        user_states[msg.from_user.id] = f"priv_cc_{uid}"
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = []
        combos = get_all_combos()
        ccs = {}
        for cc, ci in combos:
            if cc not in ccs:
                ccs[cc] = []
            ccs[cc].append(ci)
        for cc, idxs in ccs.items():
            if cc in COUNTRY_CODES:
                name, flag, _ = COUNTRY_CODES[cc]
                for i in idxs:
                    txt = f"{flag} {name}" if len(idxs) == 1 else f"{flag} {name} ({i})"
                    btns.append(types.InlineKeyboardButton(txt, callback_data=f"setpriv_{uid}_{cc}"))
        for i in range(0, len(btns), 2):
            markup.row(*btns[i:i+2])
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_private_combo"))
        bot.reply_to(msg, "Select country:", reply_markup=markup)
    except:
        bot.reply_to(msg, "❌ Invalid")

@bot.callback_query_handler(func=lambda c: c.data.startswith("setpriv_"))
def setpriv_cb(call):
    parts = call.data.split("_")
    uid = int(parts[1])
    cc = parts[2]
    save_user(uid, private_combo_country=cc)
    name, flag, _ = COUNTRY_CODES[cc]
    bot.answer_callback_query(call.id, f"✅ {uid} -> {flag} {name}", show_alert=True)
    priv_menu(call)

@bot.callback_query_handler(func=lambda c: c.data == "del_priv")
def del_priv1(call):
    if not is_admin(call.from_user.id):
        return
    user_states[call.from_user.id] = "del_priv"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_private_combo"))
    bot.edit_message_text("User ID:", call.message.chat.id, call.message.message_id, reply_markup=mk)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == "del_priv")
def del_priv2(msg):
    try:
        uid = int(msg.text)
        save_user(uid, private_combo_country=None)
        bot.reply_to(msg, f"✅ Removed private combo for {uid}")
    except:
        bot.reply_to(msg, "❌ Invalid")
    del user_states[msg.from_user.id]

# ============================================
# OTP FUNCTIONS
# ============================================

def clean_number(num):
    return re.sub(r'\D', '', str(num)) if num else ""

def get_country_info(num):
    num = num.replace("+", "").replace(" ", "")
    for code, (name, flag, short) in COUNTRY_CODES.items():
        if num.startswith(code):
            return name, flag, short
    return "Unknown", "🌍", "UN"

def mask_number(num):
    num = num.strip()
    if len(num) > 8:
        return num[:4] + "••••" + num[-3:]
    return num

def extract_otp(msg):
    patterns = [
        r'(?:code|رمز|كود|verification|otp|pin)[:\s]+(\d{3,8})',
        r'\b(\d{4,8})\b'
    ]
    for p in patterns:
        m = re.search(p, msg, re.IGNORECASE)
        if m:
            return m.group(1)
    nums = re.findall(r'\d{4,8}', msg)
    return nums[0] if nums else "N/A"

def detect_service(msg):
    low = msg.lower()
    services = {
        "#WP": "whatsapp", "#FB": "facebook", "#IG": "instagram",
        "#TG": "telegram", "#TW": "twitter", "#GG": "google",
        "#AMZ": "amazon", "#APL": "apple"
    }
    for code, kw in services.items():
        if kw in low:
            return code
    return "Unknown"

def format_message(dt, num, sms):
    cn, cf, _ = get_country_info(num)
    mn = mask_number(num)
    sv = detect_service(sms)
    return f"╭───────────────╮\n│ {cf} {sv} {mn}\n╰───────────────╯"

def delete_message_after_delay(chat_id, msg_id, delay=150):
    time.sleep(delay)
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage",
                     data={"chat_id": chat_id, "message_id": msg_id})
    except:
        pass

def send_to_telegram_group(text, otp_code):
    """Send message to Telegram group"""
    success_count = 0
    
    # Create keyboard
    keyboard = {
        "inline_keyboard": [
            [{"text": f"✌🏻 {otp_code}", "callback_data": f"copy_{otp_code}"}],
            [
                {"text": "📢 CHANNEL", "url": f"https://t.me/{CHANNEL_USERNAME[1:]}"},
                {"text": "🤖 BOT", "url": f"https://t.me/MAFYA_Numbers1_bot"}
            ],
            [
                {"text": "👤 Owner", "url": f"tg://user?id={ADMIN_IDS[0]}"}
            ]
        ]
    }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    for chat_id in CHAT_IDS:
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_markup": json.dumps(keyboard)
            }
            resp = requests.post(url, data=payload, timeout=10)
            
            if resp.status_code == 200:
                print(f"[+] Message sent to: {chat_id}")
                success_count += 1

                msg_id = resp.json()["result"]["message_id"]
                threading.Thread(
                    target=delete_message_after_delay, 
                    args=(chat_id, msg_id, 150), 
                    daemon=True
                ).start()
            else:
                print(f"[!] Failed to send to {chat_id}: {resp.status_code}")
        except Exception as e:
            print(f"[!] Error sending to {chat_id}: {e}")

    return success_count > 0

def send_otp_to_user_and_group(date_str, number, sms):
    otp = extract_otp(sms)
    cn, cf, _ = get_country_info(number)
    sv = detect_service(sms)
    uid = get_user_by_number(number)
    log_otp(number, otp, sms, uid)
    
    if uid:
        try:
            mk = types.InlineKeyboardMarkup()
            mk.row(
                types.InlineKeyboardButton("👤 Owner", url=f"tg://user?id={ADMIN_IDS[0]}"),
                types.InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")
            )
            bot.send_message(uid,
                f"✨ <b>MAFYA BOT</b>\n🌍 Country: {cn} {cf}\n⚙ Service: {sv}\n☎ Number: {number}\n🕒 Time: {date_str}\n\n🔐 Code: {otp}",
                reply_markup=mk, parse_mode="HTML")
        except:
            pass
    
    send_to_telegram_group(format_message(date_str, number, sms), otp)

@bot.callback_query_handler(func=lambda c: c.data.startswith("copy_"))
def copy_cb(call):
    code = call.data.split("_", 1)[1]
    bot.answer_callback_query(call.id, f"✅ Code: {code}", show_alert=True)

# ============================================
# DASHBOARD FUNCTIONS
# ============================================

def login_ivasms():
    d = IVASMS_DASHBOARD
    try:
        r = d["session"].get(d["login_url"], timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        tok = soup.find('input', {'name': '_token'})
        tok = tok['value'] if tok else None
        data = {'email': d["username"], 'password': d["password"]}
        if tok:
            data['_token'] = tok
        r2 = d["session"].post(d["login_url"], data=data, timeout=30)
        if "login" not in r2.url.lower():
            print(f"[{d['name']}] ✅ Login OK")
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            meta = soup2.find('meta', {'name': 'csrf-token'})
            d['csrf_token'] = meta.get('content') if meta else None
            d['is_logged_in'] = True
            d['cookies'] = d["session"].cookies.get_dict()
            return True
    except Exception as e:
        print(f"[{d['name']}] ❌ Login error: {e}")
    return False

def fetch_ivasms():
    d = IVASMS_DASHBOARD
    if not d.get('is_logged_in') and not login_ivasms():
        return []
    try:
        sess = d["session"]
        base = d["base_url"]
        api = d["sms_api_endpoint"]
        tok = d.get('csrf_token')
        if not tok:
            return []
        
        end = datetime.utcnow().strftime('%m/%d/%Y %H:%M')
        start = (datetime.utcnow() - timedelta(hours=1)).strftime('%m/%d/%Y %H:%M')
        
        headers = {'Referer': f"{base}/portal/sms/received", 'X-Requested-With': 'XMLHttpRequest'}
        summ = sess.post(api, headers=headers, data={'from': start, 'to': end, '_token': tok}, timeout=30)
        soup = BeautifulSoup(summ.text, 'html.parser')
        groups = soup.find_all('div', {'class': 'pointer'})
        
        msgs = []
        for g in groups:
            onclick = g.get('onclick', '')
            m = re.search(r"getDetials\('(.+?)'\)", onclick)
            if not m:
                continue
            gid = m.group(1)
            
            nums_resp = sess.post(urljoin(base, "portal/sms/received/getsms/number"),
                                  headers=headers,
                                  data={'start': start, 'end': end, 'range': gid, '_token': tok},
                                  timeout=30)
            num_soup = BeautifulSoup(nums_resp.text, 'html.parser')
            phones = [d.text.strip() for d in num_soup.select("div[onclick*='getDetialsNumber']")]
            
            for ph in phones:
                sms_resp = sess.post(urljoin(base, "portal/sms/received/getsms/number/sms"),
                                     headers=headers,
                                     data={'start': start, 'end': end, 'Number': ph, 'Range': gid, '_token': tok},
                                     timeout=30)
                sms_soup = BeautifulSoup(sms_resp.text, 'html.parser')
                for card in sms_soup.find_all('div', class_='card-body'):
                    p = card.find('p', class_='mb-0')
                    if p:
                        txt = p.get_text(separator='\n').strip()
                        msgs.append({
                            'id': f"{ph}-{txt[:50]}",
                            'number': ph,
                            'text': txt,
                            'timestamp': datetime.utcnow().isoformat()
                        })
        print(f"[{d['name']}] ✅ Got {len(msgs)} msgs")
        return msgs
    except Exception as e:
        print(f"[{d['name']}] ❌ Fetch error: {e}")
        d['is_logged_in'] = False
        return []

# ============================================
# MAIN LOOP
# ============================================

def main_loop():
    global REFRESH_INTERVAL
    REFRESH_INTERVAL = 3
    
    SENT_FILE = "ivasms_sent.json"
    sent = set()
    try:
        if os.path.exists(SENT_FILE):
            with open(SENT_FILE) as f:
                sent = set(json.load(f))
    except:
        pass
    
    print("="*50)
    print("🚀 MAFYA OTP BOT RUNNING")
    print(f"📢 Channel: {CHANNEL_USERNAME}")
    print("="*50)
    
    errs = 0
    
    while True:
        try:
            msgs = fetch_ivasms()
            new = 0
            for m in msgs:
                if m['id'] not in sent:
                    send_otp_to_user_and_group(m['timestamp'], clean_number(m['number']), m['text'])
                    sent.add(m['id'])
                    new += 1
            if new:
                print(f"[+] New: {new}")
                with open(SENT_FILE, 'w') as f:
                    json.dump(list(sent)[-1000:], f)
            errs = 0
        except Exception as e:
            errs += 1
            print(f"[!] Error: {e}")
            if errs >= 5:
                IVASMS_DASHBOARD['is_logged_in'] = False
                errs = 0
        time.sleep(REFRESH_INTERVAL)

def run_bot():
    print("[*] Starting Telegram bot...")
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except:
        time.sleep(5)
        run_bot()

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════╗
    ║    AADHIXD OTP BOT       ║
    ║    Channel: @Aadhixdotp  ║
    ║    Owner: Aadhixd       ║
    ╚════════════════════════╝
    """)
    
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    main_loop()
