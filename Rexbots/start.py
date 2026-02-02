# Developed by: LastPerson07 × RexBots
# Telegram: @RexBots_Official | @THEUPDATEDGUYS
import os
import asyncio
import random
import time
import shutil
import pyrogram
import requests
import hashlib 
from pyrogram import Client, filters, enums
from pyrogram.errors import (
    FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant,
    InviteHashExpired, UsernameNotOccupied, AuthKeyUnregistered, UserDeactivated, UserDeactivatedBan
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, InputMediaPhoto
from pyrogram.storage import MemoryStorage
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db
import math
from logger import LOGGER

logger = LOGGER(__name__)

SUBSCRIPTION = os.environ.get('SUBSCRIPTION', 'https://graph.org/file/242b7f1b52743938d81f1.jpg')
FREE_LIMIT_SIZE = 2 * 1024 * 1024 * 1024
FREE_LIMIT_DAILY = 10
UPI_ID = os.environ.get("UPI_ID", "your_upi@oksbi")
QR_CODE = os.environ.get("QR_CODE", "https://graph.org/file/242b7f1b52743938d81f1.jpg")

REACTIONS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬",
    "😢", "🎉", "🤩", "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱",
    "🥴", "😍", "🐳", "❤️‍🔥", "🌚", "🌭", "💯", "🤣", "⚡", "🍌",
    "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "🖕", "😈", "😴",
    "😭", "🤓", "👻", "👨‍💻", "👀", "🎃", "🙈", "😇", "😨", "🤝",
    "✍", "🤗", "🫡", "🎅", "🎄", "☃", "💅", "🤪", "🗿", "🆒",
    "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾", "🤷‍♂️", "🤷‍♀️",
    "😡"
]

# ========== HASH CHECK REMOVED ==========
dev_text = """👨‍💻 Mind Behind This Bot:
• @Divyanshshukla7
• @Divyanshshukla7"""

channels_text = """📢 Official Channels:
• @Divyanshshukla7
• @Divyanshshukla7

Stay updated for new features!"""

BATCH_STATE = {}  # User ID -> {step, link, destination, dump_chat_id}
ACTIVE_CLIENTS = {}  # Track active clients for cleanup

class script(object):

    START_TXT = """<b>👋 Hello {},</b>
<b>🤖 I am <a href=https://t.me/{}>{}</a></b>
<i>Your Professional Restricted Content Saver Bot.</i>
<blockquote><b>🚀 System Status: 🟢 Online</b>
<b>⚡ Performance: 10x High-Speed Processing</b>
<b>🔐 Security: End-to-End Encrypted</b>
<b>📊 Uptime: 99.9% Guaranteed</b></blockquote>
<b>👇 Select an Option Below to Get Started:</b>
"""
    HELP_TXT = """<b>📚 Comprehensive Help & User Guide</b>
<blockquote><b>1️⃣ Public Channels (No Login Required)</b></blockquote>
• Forward or send the post link directly.
• Compatible with any public channel or group.
• <i>Example Link:</i> <code>https://t.me/channel/123</code>
<blockquote><b>2️⃣ Private/Restricted Channels (Login Required)</b></blockquote>
• Use <code>/login</code> to securely connect your Telegram account.
• Send the private link (e.g., <code>t.me/c/123...</code>).
• Bot accesses content using your authenticated session.
<blockquote><b>3️⃣ Batch Downloading Mode ⭐ NEW</b></blockquote>
• Use <code>/batch</code> command for multiple files.
• <b>Choose destination:</b> Chat or Channel
• Send link like: <code>https://t.me/channel/100-110</code>
• Supports ALL media: Video, Document, Photo, Audio
• <b>Preserves original filename & extension</b>
<blockquote><b>🛑 Free User Limitations:</b></blockquote>
• <b>Daily Quota:</b> 10 Files / 24 Hours
• <b>Batch Limit:</b> 5 Files per batch (Free)
• <b>File Size Cap:</b> 2GB Maximum
<blockquote><b>💎 Premium Membership Benefits:</b></blockquote>
• Unlimited Downloads & No Restrictions.
• Unlimited batch size.
• Priority Support & Advanced Features.
"""
    ABOUT_TXT = """<b>ℹ️ About This Bot</b>
<blockquote><b>╭────[ 🧩 Technical Stack ]────⍟</b>
<b>├⍟ 🤖 Bot Name : <a href=http://t.me/@Divyanshshukla7>Save Content</a></b>
<b>├⍟ 👨‍💻 Developer : <a href=https://t.me/Divyanshshukla7>Ⓜ️ark X Rexbots</a></b>
<b>├⍟ 📚 Library : <a href='https://docs.pyrogram.org/'>Pyrogram Async</a></b>
<b>├⍟ 🐍 Language : <a href='https://www.python.org/'>Python 3.11+</a></b>
<b>├⍟ 🗄 Database : <a href='https://www.mongodb.com/'>MongoDB Atlas Cluster</a></b>
<b>├⍟ 📡 Hosting : Dedicated High-Speed VPS</b>
<b>╰───────────────⍟</b></blockquote>
"""
    PREMIUM_TEXT = """<b>💎 Premium Membership Plans</b>
<b>Unlock Unlimited Access & Advanced Features!</b>
<blockquote><b>✨ Key Benefits:</b>
<b>♾️ Unlimited Daily Downloads</b>
<b>📂 Support for 4GB+ File Sizes</b>
<b>⚡ Instant Processing (Zero Delay)</b>
<b>🖼 Customizable Thumbnails</b>
<b>📝 Personalized Captions</b>
<b>🛂 24/7 Priority Support</b></blockquote>
<blockquote><b>💳 Pricing Options:</b></blockquote>
• <b>1 Month Plan:</b> ₹50 / $1 (Billed Monthly)
• <b>3 Month Plan:</b> ₹120 / $2.5 (Save 20%)
• <b>Lifetime Access:</b> ₹200 / $4 (One-Time Payment)
<blockquote><b>👇 Secure Payment:</b></blockquote>
<b>💸 UPI ID:</b> <code>{}</code>
<b>📸 QR Code:</b> <a href='{}'>Scan to Pay</a>
<i>After Payment: Send Screenshot to Admin for Instant Activation.</i>
"""
    PROGRESS_BAR = """<b>⚡ Processing Task...</b>
<blockquote>
<b>Progress: {bar} {percentage:.1f}%</b>
<b>🚀 Speed:</b> <code>{speed}/s</code>
<b>💾 Size:</b> <code>{current} of {total}</code>
<b>⏱ Elapsed:</b> <code>{elapsed}</code>
<b>⏳ ETA:</b> <code>{eta}</code>
</blockquote>
"""
    CAPTION = """<b><a href="https://t.me/Divyanshshukla7">⚜️ Powered By : 💫『 𝒟𝒾𝓋𝓎𝒶𝓃𝓈𝒽 𝓈𝒽𝓊𝓀𝓁𝒶 』💫😎</a></b>"""
    LIMIT_REACHED = """<b>🚫 Daily Limit Exceeded</b>
<b>Your 10 free saves for today have been used.</b>
<i>Quota resets automatically after 24 hours from first download.</i>
<blockquote><b>🔓 Upgrade to Premium for Unlimited Access!</b></blockquote>
Remove all restrictions and enjoy seamless downloading.
"""
    SIZE_LIMIT = """<b>⚠️ File Size Exceeded</b>
<b>Free tier limited to 2GB per file.</b>
<blockquote><b>🔓 Upgrade to Premium</b></blockquote>
Download files up to 4GB and beyond with no limits!
"""

def humanbytes(size):
    if not size:
        return "0B"
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + ((str(hours) + "h, ") if hours else "") + ((str(minutes) + "m, ") if minutes else "") + ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2] if tmp else "0s"

class batch_temp(object):
    IS_BATCH = {}

def get_message_type(msg):
    if getattr(msg, 'document', None): return "Document"
    if getattr(msg, 'video', None): return "Video"
    if getattr(msg, 'photo', None): return "Photo"
    if getattr(msg, 'audio', None): return "Audio"
    if getattr(msg, 'text', None): return "Text"
    return None

def get_file_extension(filename):
    """Get file extension from filename"""
    if not filename:
        return ""
    return os.path.splitext(filename)[1]

def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    if not filename:
        return "unknown_file"
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

async def cleanup_client(client, session_name):
    """Safely cleanup client and remove session files"""
    try:
        if client:
            await client.disconnect()
            await client.stop()
    except Exception as e:
        logger.error(f"Error stopping client: {e}")

    # Remove session files
    try:
        session_file = f"{session_name}.session"
        journal_file = f"{session_name}.session-journal"
        if os.path.exists(session_file):
            os.remove(session_file)
        if os.path.exists(journal_file):
            os.remove(journal_file)
    except Exception as e:
        logger.error(f"Error removing session files: {e}")

# ========== PROGRESS FUNCTIONS ==========
async def progress_for_pyrogram(current, total, client, status_file, file_size, type):
    """Progress callback for pyrogram downloads/uploads"""
    now = time.time()
    if not hasattr(progress_for_pyrogram, "start_time"):
        progress_for_pyrogram.start_time = {}

    task_id = f"{status_file}_{type}"
    if task_id not in progress_for_pyrogram.start_time:
        progress_for_pyrogram.start_time[task_id] = now

    start_time = progress_for_pyrogram.start_time[task_id]
    elapsed = now - start_time

    percentage = current * 100 / total if total > 0 else 0
    speed = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / speed if speed > 0 else 0

    filled_length = int(percentage / 5)
    bar = '█' * filled_length + '░' * (20 - filled_length)

    status = f"""<b>⚡ Processing Task...</b>
<blockquote>
<b>Progress: {bar} {percentage:.1f}%</b>
<b>🚀 Speed:</b> <code>{humanbytes(speed)}/s</code>
<b>💾 Size:</b> <code>{humanbytes(current)} of {humanbytes(total)}</code>
<b>⏱ Elapsed:</b> <code>{TimeFormatter(elapsed * 1000)}</code>
<b>⏳ ETA:</b> <code>{TimeFormatter(eta * 1000)}</code>
</blockquote>"""

    try:
        with open(status_file, "w", encoding='utf-8') as f:
            f.write(status)
    except Exception as e:
        logger.error(f"Error writing status file: {e}")

async def update_batch_progress(client, message, status_file, current_idx, total, operation):
    """Update progress message for batch operations"""
    while True:
        try:
            if os.path.exists(status_file):
                with open(status_file, "r", encoding='utf-8') as f:
                    content = f.read()

                batch_info = f"\n<b>📦 Batch:</b> <code>{current_idx}/{total}</code> ({(current_idx/total)*100:.1f}%)"
                full_text = content + batch_info

                if message:
                    await message.edit_text(full_text, parse_mode=enums.ParseMode.HTML)
            await asyncio.sleep(3)
        except Exception:
            await asyncio.sleep(3)

async def upload_with_progress_caption(client, chat_id, file_path, caption, file_id, file_type, 
                                       status_file, file_size, **kwargs):
    """Upload file with progress tracking and caption"""
    if os.path.exists(status_file):
        os.remove(status_file)

    upload_status_file = status_file.replace("down", "up")

    try:
        if file_type == "document":
            await client.send_document(
                chat_id, file_path, caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(client, upload_status_file, file_size, "up")
            )
        elif file_type == "video":
            await client.send_video(
                chat_id, file_path, caption=caption,
                duration=kwargs.get('duration'),
                width=kwargs.get('width'),
                height=kwargs.get('height'),
                progress=progress_for_pyrogram,
                progress_args=(client, upload_status_file, file_size, "up")
            )
        elif file_type == "audio":
            await client.send_audio(
                chat_id, file_path, caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(client, upload_status_file, file_size, "up")
            )
    finally:
        if os.path.exists(upload_status_file):
            os.remove(upload_status_file)
        if os.path.exists(file_path):
            os.remove(file_path)

@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
    api_url = random.choice(apis)
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        photo_url = response.json()["url"]
    except Exception as e:
        logger.error(f"Failed to fetch image from API: {e}")
        photo_url = "https://i.postimg.cc/kX9tjGXP/16.png"
    buttons = [
        [
            InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
            InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
        ],
        [
            InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
            InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
        ],
        [
            InlineKeyboardButton('📢 Channels', callback_data="channels_info"),
            InlineKeyboardButton('👨‍💻 Developers', callback_data="dev_info")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    bot = await client.get_me()
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=script.START_TXT.format(message.from_user.mention, bot.username, bot.first_name),
        reply_markup=reply_markup,
        reply_to_message_id=message.id,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    buttons = [[InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]]
    await client.send_message(
        chat_id=message.chat.id,
        text=script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command(["plan", "myplan", "premium"]))
async def send_plan(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/Divyanshshukla7")],
        [InlineKeyboardButton("❌ Close Menu", callback_data="close_btn")]
    ]
    await client.send_photo(
        chat_id=message.chat.id,
        photo=SUBSCRIPTION,
        caption=script.PREMIUM_TEXT.format(UPI_ID, QR_CODE),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
    )

# ========== BATCH COMMAND WITH DESTINATION SELECTION ==========
@Client.on_message(filters.command("batch") & filters.private)
async def batch_start(client: Client, message: Message):
    """Start batch download process with destination selection"""
    user_id = message.from_user.id

    if user_id in BATCH_STATE:
        return await message.reply_text(
            "<b>⚠️ Batch already in progress!</b>\n\nUse /cancel to stop current batch.",
            parse_mode=enums.ParseMode.HTML
        )

    is_premium = await db.check_premium(user_id)
    if not is_premium:
        user_data = await db.col.find_one({'id': user_id})
        daily_usage = user_data.get('daily_usage', 0)
        if daily_usage >= 10:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.LIMIT_REACHED,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )

    dump_chat_id = await db.get_dump_chat(user_id)

    BATCH_STATE[user_id] = {
        "step": "waiting_destination",
        "link": None,
        "destination": None,
        "dump_chat_id": dump_chat_id
    }

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📱 Chat (Default)", callback_data="dest_chat"),
            InlineKeyboardButton("📢 Channel", callback_data="dest_channel")
        ],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_batch")]
    ])

    dest_text = "<b>📦 Batch Download Mode</b>\n\n"
    if dump_chat_id:
        dest_text += f"<b>Available Destinations:</b>\n"
        dest_text += f"📱 <b>Chat</b> - Send to you\n"
        dest_text += f"📢 <b>Channel</b> - Send to channel\n\n"
    else:
        dest_text += f"<b>⚠️ No Channel Set!</b>\n"
        dest_text += f"Use <code>/setchat &lt;channel_id&gt;</code> to set a channel.\n\n"

    dest_text += f"<b>⏱ Auto-start in Chat after 20 seconds...</b>\n\n"
    dest_text += f"<i>Choose where to upload:</i>"

    msg = await message.reply_text(
        dest_text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

    asyncio.create_task(batch_auto_timer(client, message.chat.id, msg.id, user_id))

async def batch_auto_timer(client, chat_id, msg_id, user_id):
    """20 second auto-timer for batch destination"""
    await asyncio.sleep(20)

    if user_id in BATCH_STATE and BATCH_STATE[user_id]["step"] == "waiting_destination":
        BATCH_STATE[user_id]["destination"] = "chat"
        BATCH_STATE[user_id]["step"] = "waiting_link"

        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text="<b>📦 Batch Download Mode</b>\n\n"
                     "<b>✅ Destination:</b> 📱 Chat (Auto-selected)\n\n"
                     "<b>Send me the link with range:</b>\n"
                     "<code>https://t.me/channel/100-200</code>\n\n"
                     "❌ Send /cancel to stop",
                parse_mode=enums.ParseMode.HTML
            )
        except:
            pass

@Client.on_callback_query(filters.regex("^dest_"))
async def batch_destination_callback(client: Client, callback_query: CallbackQuery):
    """Handle destination selection"""
    user_id = callback_query.from_user.id
    data = callback_query.data

    if user_id not in BATCH_STATE:
        return await callback_query.answer("Session expired! Start again with /batch", show_alert=True)

    if data == "dest_chat":
        BATCH_STATE[user_id]["destination"] = "chat"
        BATCH_STATE[user_id]["step"] = "waiting_link"

        await callback_query.edit_message_text(
            "<b>📦 Batch Download Mode</b>\n\n"
            "<b>✅ Destination:</b> 📱 Chat\n\n"
            "<b>Send me the link with range:</b>\n"
            "<code>https://t.me/channel/100-200</code>\n\n"
            "❌ Send /cancel to stop",
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "dest_channel":
        dump_chat_id = BATCH_STATE[user_id].get("dump_chat_id")

        if not dump_chat_id:
            await callback_query.answer("❌ No channel set! Use /setchat first", show_alert=True)
            return

        BATCH_STATE[user_id]["destination"] = "channel"
        BATCH_STATE[user_id]["step"] = "waiting_link"

        await callback_query.edit_message_text(
            f"<b>📦 Batch Download Mode</b>\n\n"
            f"<b>✅ Destination:</b> 📢 Channel\n"
            f"<code>{dump_chat_id}</code>\n\n"
            f"<b>Send me the link with range:</b>\n"
            f"<code>https://t.me/channel/100-200</code>\n\n"
            f"❌ Send /cancel to stop",
            parse_mode=enums.ParseMode.HTML
        )

    await callback_query.answer()

@Client.on_callback_query(filters.regex("^cancel_batch$"))
async def cancel_batch_callback(client: Client, callback_query: CallbackQuery):
    """Cancel batch from button"""
    user_id = callback_query.from_user.id

    if user_id in BATCH_STATE:
        del BATCH_STATE[user_id]

    await callback_query.edit_message_text(
        "<b>❌ Batch cancelled.</b>",
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer()

# ========== CANCEL COMMAND (Batch Only) ==========
@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in BATCH_STATE:
        del BATCH_STATE[user_id]
        batch_temp.IS_BATCH[user_id] = True  # Mark as cancelled
        await message.reply_text(
            "<b>❌ Batch process cancelled.</b>",
            parse_mode=enums.ParseMode.HTML
        )
        return

    await message.reply_text(
        "<b>⚠️ No active batch process found.</b>\nUse /stop to cancel all tasks.",
        parse_mode=enums.ParseMode.HTML
    )

# ========== STOP COMMAND (Everything) ==========
@Client.on_message(filters.command(["stop"]))
async def send_stop(client: Client, message: Message):
    user_id = message.from_user.id

    cancelled = []

    # Stop batch if active
    if user_id in BATCH_STATE:
        del BATCH_STATE[user_id]
        batch_temp.IS_BATCH[user_id] = True
        cancelled.append("Batch Download")

    # Stop any single download
    if user_id in batch_temp.IS_BATCH:
        batch_temp.IS_BATCH[user_id] = True
        cancelled.append("Single Download")

    # Cleanup any active clients
    if user_id in ACTIVE_CLIENTS:
        for client_info in ACTIVE_CLIENTS[user_id]:
            try:
                await cleanup_client(client_info['client'], client_info['session_name'])
            except:
                pass
        del ACTIVE_CLIENTS[user_id]

    if cancelled:
        await message.reply_text(
            f"<b>🛑 Stopped:</b> <code>{', '.join(cancelled)}</code>\n\n"
            f"<i>All active tasks have been cancelled.</i>",
            parse_mode=enums.ParseMode.HTML
        )
    else:
        await message.reply_text(
            "<b>✅ No active tasks to stop.</b>",
            parse_mode=enums.ParseMode.HTML
        )

async def settings_panel(client, callback_query):
    user_id = callback_query.from_user.id
    is_premium = await db.check_premium(user_id)
    badge = "💎 Premium Member" if is_premium else "👤 Standard User"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📜 Command List", callback_data="cmd_list_btn")],
        [InlineKeyboardButton("📊 Usage Stats", callback_data="user_stats_btn")],
        [InlineKeyboardButton("🗑 Dump Chat Settings", callback_data="dump_chat_btn")],
        [InlineKeyboardButton("🖼 Manage Thumbnail", callback_data="thumb_btn")],
        [InlineKeyboardButton("📝 Edit Caption", callback_data="caption_btn")],
        [InlineKeyboardButton("⬅️ Return to Home", callback_data="start_btn")]
    ])

    text = f"<b>⚙️ Settings Dashboard</b>\n\n<b>Account Status:</b> {badge}\n<b>User ID:</b> <code>{user_id}</code>\n\n<i>Customize and manage your bot preferences below for an optimized experience:</i>"

    await callback_query.edit_message_caption(
        caption=text,
        reply_markup=buttons,
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.text & filters.private & ~filters.regex("^/"))
async def save(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in BATCH_STATE and BATCH_STATE[user_id]["step"] == "waiting_link":
        return await process_batch_with_destination(client, message)

    if "https://t.me/" in message.text:

        is_limit_reached = await db.check_limit(message.from_user.id)
        if is_limit_reached:
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            return await message.reply_photo(
                photo=SUBSCRIPTION,
                caption=script.LIMIT_REACHED,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )

        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text("<b>⚠️ A Task is Currently Processing.</b>\n<i>Please wait for completion or use /stop to cancel.</i>", parse_mode=enums.ParseMode.HTML)

        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        batch_temp.IS_BATCH[message.from_user.id] = False
        is_private_link = "https://t.me/c/" in message.text
        is_batch = "https://t.me/b/" in message.text
        is_public_link = not is_private_link and not is_batch

        for msgid in range(fromID, toID + 1):

            if batch_temp.IS_BATCH.get(message.from_user.id):
                break

            if is_public_link:
                username = datas[3]
                try:
                    msg = await client.get_messages(username, msgid)
                    if msg:
                        # Add watermark to caption
                        original_caption = msg.caption or ""
                        watermark = script.CAPTION
                        final_caption = f"{original_caption}\n\n{watermark}" if original_caption else watermark

                        if msg.document:
                            await client.send_document(message.chat.id, msg.document.file_id, caption=final_caption)
                        elif msg.video:
                            await client.send_video(message.chat.id, msg.video.file_id, caption=final_caption)
                        elif msg.photo:
                            await client.send_photo(message.chat.id, msg.photo.file_id, caption=final_caption)
                        elif msg.audio:
                            await client.send_audio(message.chat.id, msg.audio.file_id, caption=final_caption)
                        elif msg.text:
                            text_with_watermark = f"{msg.text}\n\n{watermark}"
                            await client.send_message(message.chat.id, text_with_watermark)

                        await db.add_traffic(message.from_user.id)
                        await asyncio.sleep(1)
                        continue
                except Exception as e:
                    logger.error(f"Public copy error: {e}")
                    pass

            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply(
                    "<b>🔒 Authentication Required</b>\n\n"
                    "<i>Access to this content requires login.</i>\n"
                    "<i>Use /login to securely authorize your account.</i>",
                    parse_mode=enums.ParseMode.HTML
                )
                batch_temp.IS_BATCH[message.from_user.id] = True
                return

            # Create unique session for each download
            session_name = f"saverestricted_{message.from_user.id}_{int(time.time())}_{msgid}"

            acc = Client(
                session_name,
                session_string=user_data,
                api_hash=API_HASH,
                api_id=API_ID,
                in_memory=True,
                max_concurrent_transmissions=10,
                storage=MemoryStorage()
            )

            try:
                await acc.connect()
            except Exception as e:
                logger.error(f"Connection error: {e}")
                await cleanup_client(acc, session_name)
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply(f"<b>❌ Authentication Failed</b>\n\n<i>Your session may have expired. Please /logout and /login again.</i>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)

            try:
                if is_private_link:
                    chatid = int("-100" + datas[4])
                    await handle_restricted_content(client, acc, message, chatid, msgid)
                elif is_batch:
                    username = datas[4]
                    await handle_restricted_content(client, acc, message, username, msgid)
                else:
                    username = datas[3]
                    await handle_restricted_content(client, acc, message, username, msgid)
            finally:
                await cleanup_client(acc, session_name)

            await asyncio.sleep(2)

        batch_temp.IS_BATCH[message.from_user.id] = True

# ========== BATCH PROCESSING WITH PROGRESS TRACKING ==========
async def process_batch_with_destination(client: Client, message: Message):
    """Process batch with user-selected destination - PRESERVES ORIGINAL FILENAME + PROGRESS + CAPTION"""
    user_id = message.from_user.id
    text = message.text.strip()
    state = BATCH_STATE[user_id]
    destination = state["destination"]
    dump_chat_id = state.get("dump_chat_id")

    if "https://t.me/" not in text:
        return await message.reply_text(
            "❌ <b>Invalid link!</b>\n\nPlease send a valid Telegram link.",
            parse_mode=enums.ParseMode.HTML
        )

    try:
        datas = text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        start_id = int(temp[0].strip())
        end_id = int(temp[1].strip()) if len(temp) > 1 else start_id

        if end_id < start_id:
            return await message.reply_text(
                "❌ <b>Invalid range!</b>\nEnd ID should be greater than start ID.",
                parse_mode=enums.ParseMode.HTML
            )

        is_premium = await db.check_premium(user_id)
        total_files = end_id - start_id + 1

        if not is_premium:
            if total_files > 5:
                return await message.reply_text(
                    "<b>🚫 Batch too large!</b>\n\n"
                    "Free users: Max 5 files per batch\n"
                    "Premium users: Unlimited batch size\n\n"
                    "<i>Upgrade to premium for unlimited downloads!</i>",
                    parse_mode=enums.ParseMode.HTML
                )

            user_data = await db.col.find_one({'id': user_id})
            daily_usage = user_data.get('daily_usage', 0)
            if daily_usage + total_files > 10:
                remaining = 10 - daily_usage
                return await message.reply_text(
                    f"<b>🚫 Insufficient quota!</b>\n\n"
                    f"You have only <code>{remaining}</code> saves left today.\n"
                    f"This batch requires <code>{total_files}</code> saves.\n\n"
                    f"Try a smaller range or upgrade to premium.",
                    parse_mode=enums.ParseMode.HTML
                )

        del BATCH_STATE[user_id]

        if destination == "channel" and dump_chat_id:
            target_chat = dump_chat_id
            dest_text = f"📢 Channel"
        else:
            target_chat = message.chat.id
            dest_text = "📱 Chat"

        # Progress message for overall batch
        batch_progress_msg = await message.reply_text(
            f"<b>📦 Starting Batch Download</b>\n\n"
            f"<b>Destination:</b> {dest_text}\n"
            f"<b>Total Files:</b> <code>{total_files}</code>\n"
            f"<b>Range:</b> <code>{start_id}</code> to <code>{end_id}</code>\n\n"
            f"<i>Initializing...</i>",
            parse_mode=enums.ParseMode.HTML
        )

        success_count = 0
        failed_count = 0
        is_private = "https://t.me/c/" in text
        is_public = not is_private
        username = datas[3] if is_public else datas[4]

        for idx, msgid in enumerate(range(start_id, end_id + 1), 1):
            # Check for cancellation
            if batch_temp.IS_BATCH.get(user_id) == True:
                await batch_progress_msg.edit_text(
                    f"<b>❌ Batch Cancelled by User</b>\n\n"
                    f"<b>Processed:</b> <code>{idx-1}/{total_files}</code>\n"
                    f"<b>✅ Success:</b> <code>{success_count}</code>\n"
                    f"<b>❌ Failed:</b> <code>{failed_count}</code>",
                    parse_mode=enums.ParseMode.HTML
                )
                return

            # Update overall progress every file
            try:
                await batch_progress_msg.edit_text(
                    f"<b>📦 Batch Download Progress</b>\n\n"
                    f"<b>Overall:</b> <code>{idx}/{total_files}</code> ({(idx/total_files)*100:.1f}%)\n"
                    f"<b>✅ Success:</b> <code>{success_count}</code>\n"
                    f"<b>❌ Failed:</b> <code>{failed_count}</code>\n"
                    f"<b>Current:</b> Processing message {msgid}...",
                    parse_mode=enums.ParseMode.HTML
                )
            except:
                pass

            try:
                if is_public:
                    await download_upload_public_with_progress(
                        client, message, username, msgid, target_chat, 
                        batch_progress_msg, idx, total_files, is_premium
                    )
                    await db.add_traffic(user_id)
                    success_count += 1
                else:
                    user_session = await db.get_session(user_id)
                    if not user_session:
                        await message.reply_text(
                            "<b>🔒 Login Required!</b>\nUse /login first for private channels.",
                            parse_mode=enums.ParseMode.HTML
                        )
                        failed_count += (total_files - idx + 1)
                        break

                    await download_upload_private_with_progress(
                        client, message, user_id, msgid, datas, target_chat, 
                        batch_progress_msg, idx, total_files, is_premium
                    )
                    await db.add_traffic(user_id)
                    success_count += 1

            except Exception as e:
                logger.error(f"Batch error for {msgid}: {e}")
                failed_count += 1

            await asyncio.sleep(2)

        await batch_progress_msg.edit_text(
            f"<b>✅ Batch Download Complete!</b>\n\n"
            f"<b>📊 Summary:</b>\n"
            f"• <b>Destination:</b> {dest_text}\n"
            f"• <b>Total:</b> <code>{total_files}</code>\n"
            f"• <b>✅ Success:</b> <code>{success_count}</code>\n"
            f"• <b>❌ Failed:</b> <code>{failed_count}</code>\n\n"
            f"<i>Use /batch for more downloads.</i>",
            parse_mode=enums.ParseMode.HTML
        )

    except ValueError:
        await message.reply_text(
            "❌ <b>Invalid format!</b>\n\n"
            "Please use: <code>https://t.me/channel/100-200</code>",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Batch error: {e}")
        await message.reply_text(
            f"❌ <b>Error:</b> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML
        )
        if user_id in BATCH_STATE:
            del BATCH_STATE[user_id]

# ========== PUBLIC DOWNLOAD WITH PROGRESS & CAPTION ==========
async def download_upload_public_with_progress(client, message, username, msgid, target_chat, 
                                               progress_msg, current_idx, total, is_premium):
    """Download from public channel with detailed progress tracking and caption"""
    # Create unique session name
    session_name = f"public_temp_{message.from_user.id}_{int(time.time())}_{msgid}"

    temp_client = Client(
        session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True,
        storage=MemoryStorage()
    )

    try:
        await temp_client.connect()
    except Exception as e:
        logger.error(f"Connection error: {e}")
        await cleanup_client(temp_client, session_name)
        raise

    try:
        msg = await temp_client.get_messages(username, msgid)
        if not msg or msg.empty:
            raise Exception("Message not found or empty")

        # Create status files for this download
        status_file = f"batch_{message.id}_{msgid}_status.txt"

        # Start progress tracking task
        progress_task = asyncio.create_task(
            update_batch_progress(client, progress_msg, status_file, current_idx, total, "down")
        )

        try:
            # Prepare caption with watermark
            original_caption = msg.caption or ""
            watermark = script.CAPTION
            final_caption = f"{original_caption}\n\n{watermark}" if original_caption else watermark

            if msg.document:
                original_name = msg.document.file_name or f"document_{msgid}"
                safe_name = sanitize_filename(original_name)
                file_size = msg.document.file_size

                # Check 4GB limit for non-premium
                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    await client.send_message(
                        target_chat,
                        f"⚠️ <b>File too large (>{humanbytes(FREE_LIMIT_SIZE)})</b>\n"
                        f"Skipped: <code>{safe_name}</code>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

                file_path = await temp_client.download_media(
                    msg.document.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                # Upload with progress and caption
                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption, 
                    msg.document.file_id, "document", status_file, file_size
                )

            elif msg.video:
                file_size = msg.video.file_size
                if msg.video.file_name:
                    original_name = msg.video.file_name
                else:
                    ext = ".mp4"
                    if msg.video.mime_type:
                        if "mp4" in msg.video.mime_type: ext = ".mp4"
                        elif "mkv" in msg.video.mime_type: ext = ".mkv"
                        elif "avi" in msg.video.mime_type: ext = ".avi"
                    original_name = f"video_{msgid}{ext}"

                safe_name = sanitize_filename(original_name)

                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    await client.send_message(
                        target_chat,
                        f"⚠️ <b>Video too large (>{humanbytes(FREE_LIMIT_SIZE)})</b>\n"
                        f"Skipped: <code>{safe_name}</code>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

                file_path = await temp_client.download_media(
                    msg.video.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption,
                    msg.video.file_id, "video", status_file, file_size,
                    duration=msg.video.duration, width=msg.video.width, height=msg.video.height
                )

            elif msg.photo:
                file_path = await temp_client.download_media(
                    msg.photo.file_id,
                    file_name=f"downloads/photo_{msgid}.jpg"
                )
                await client.send_photo(target_chat, file_path, caption=final_caption)
                if os.path.exists(file_path):
                    os.remove(file_path)

            elif msg.audio:
                original_name = msg.audio.file_name or f"audio_{msgid}.mp3"
                safe_name = sanitize_filename(original_name)
                file_size = msg.audio.file_size

                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    return

                file_path = await temp_client.download_media(
                    msg.audio.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption,
                    msg.audio.file_id, "audio", status_file, file_size
                )

            elif msg.text:
                text_with_watermark = f"{msg.text}\n\n{watermark}"
                await client.send_message(target_chat, text_with_watermark)

        finally:
            if os.path.exists(status_file):
                os.remove(status_file)
            if 'progress_task' in locals():
                progress_task.cancel()
                try:
                    await progress_task
                except asyncio.CancelledError:
                    pass

    finally:
        await cleanup_client(temp_client, session_name)

# ========== PRIVATE DOWNLOAD WITH PROGRESS & CAPTION ==========
async def download_upload_private_with_progress(client, message, user_id, msgid, datas, target_chat, 
                                                progress_msg, current_idx, total, is_premium):
    """Download from private channel with detailed progress tracking and caption"""
    user_session = await db.get_session(user_id)
    if not user_session:
        raise Exception("No session")

    # Create unique session name
    session_name = f"saverestricted_{user_id}_{int(time.time())}_{msgid}"

    acc = Client(
        session_name,
        session_string=user_session,
        api_hash=API_HASH,
        api_id=API_ID,
        in_memory=True,
        max_concurrent_transmissions=10,
        storage=MemoryStorage()
    )

    try:
        await acc.connect()
    except Exception as e:
        logger.error(f"Connection error: {e}")
        await cleanup_client(acc, session_name)
        raise

    try:
        chatid = int("-100" + datas[4])
        msg = await acc.get_messages(chatid, msgid)

        if not msg or msg.empty:
            raise Exception("Message not found or empty")

        status_file = f"batch_{message.id}_{msgid}_status.txt"
        progress_task = asyncio.create_task(
            update_batch_progress(client, progress_msg, status_file, current_idx, total, "down")
        )

        try:
            # Prepare caption with watermark
            original_caption = msg.caption or ""
            watermark = script.CAPTION
            final_caption = f"{original_caption}\n\n{watermark}" if original_caption else watermark

            if msg.document:
                original_name = msg.document.file_name or f"document_{msgid}"
                safe_name = sanitize_filename(original_name)
                file_size = msg.document.file_size

                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    await client.send_message(
                        target_chat,
                        f"⚠️ <b>File too large (>{humanbytes(FREE_LIMIT_SIZE)})</b>\n"
                        f"Skipped: <code>{safe_name}</code>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

                file_path = await acc.download_media(
                    msg.document.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption,
                    msg.document.file_id, "document", status_file, file_size
                )

            elif msg.video:
                file_size = msg.video.file_size
                if msg.video.file_name:
                    original_name = msg.video.file_name
                else:
                    ext = ".mp4"
                    if msg.video.mime_type:
                        if "mp4" in msg.video.mime_type: ext = ".mp4"
                        elif "mkv" in msg.video.mime_type: ext = ".mkv"
                        elif "avi" in msg.video.mime_type: ext = ".avi"
                    original_name = f"video_{msgid}{ext}"

                safe_name = sanitize_filename(original_name)

                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    await client.send_message(
                        target_chat,
                        f"⚠️ <b>Video too large (>{humanbytes(FREE_LIMIT_SIZE)})</b>\n"
                        f"Skipped: <code>{safe_name}</code>",
                        parse_mode=enums.ParseMode.HTML
                    )
                    return

                file_path = await acc.download_media(
                    msg.video.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption,
                    msg.video.file_id, "video", status_file, file_size,
                    duration=msg.video.duration, width=msg.video.width, height=msg.video.height
                )

            elif msg.photo:
                file_path = await acc.download_media(
                    msg.photo.file_id,
                    file_name=f"downloads/photo_{msgid}.jpg"
                )
                await client.send_photo(target_chat, file_path, caption=final_caption)
                if os.path.exists(file_path):
                    os.remove(file_path)

            elif msg.audio:
                original_name = msg.audio.file_name or f"audio_{msgid}.mp3"
                safe_name = sanitize_filename(original_name)
                file_size = msg.audio.file_size

                if file_size > FREE_LIMIT_SIZE and not is_premium:
                    return

                file_path = await acc.download_media(
                    msg.audio.file_id,
                    file_name=f"downloads/{safe_name}",
                    progress=progress_for_pyrogram,
                    progress_args=(client, status_file, file_size, "down")
                )

                await upload_with_progress_caption(
                    client, target_chat, file_path, final_caption,
                    msg.audio.file_id, "audio", status_file, file_size
                )

            elif msg.text:
                text_with_watermark = f"{msg.text}\n\n{watermark}"
                await client.send_message(target_chat, text_with_watermark)

        finally:
            if os.path.exists(status_file):
                os.remove(status_file)
            if 'progress_task' in locals():
                progress_task.cancel()
                try:
                    await progress_task
                except asyncio.CancelledError:
                    pass

    finally:
        await cleanup_client(acc, session_name)

async def handle_restricted_content(client: Client, acc, message: Message, chat_target, msgid):
    try:
        msg = await acc.get_messages(chat_target, msgid)
    except Exception as e:
        logger.error(f"Error fetching message: {e}")
        return

    if msg.empty:
        return

    msg_type = get_message_type(msg)
    if not msg_type:
        return

    file_size = 0
    if msg_type == "Document": file_size = msg.document.file_size
    elif msg_type == "Video": file_size = msg.video.file_size
    elif msg_type == "Audio": file_size = msg.audio.file_size

    if file_size > FREE_LIMIT_SIZE:
        if not await db.check_premium(message.from_user.id):
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Upgrade to Premium", callback_data="buy_premium")]])
            await client.send_message(
                message.chat.id,
                script.SIZE_LIMIT,
                reply_markup=btn,
                parse_mode=enums.ParseMode.HTML
            )
            return

    # Prepare caption with watermark
    original_caption = msg.caption or ""
    watermark = script.CAPTION
    final_caption = f"{original_caption}\n\n{watermark}" if original_caption else watermark

    if msg_type == "Text":
        try:
            text_with_watermark = f"{msg.text}\n\n{watermark}"
            await client.send_message(message.chat.id, text_with_watermark, entities=msg.entities, parse_mode=enums.ParseMode.HTML)
            return
        except:
            return

    await db.add_traffic(message.from_user.id)
    smsg = await client.send_message(message.chat.id, '<b>⬇️ Starting Download...</b>', reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)

    temp_dir = f"downloads/{message.id}"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    try:
        # Create status file for progress
        status_file = f"{temp_dir}/status.txt"

        # Get original filename for single download too
        original_name = None
        if msg_type == "Document" and msg.document.file_name:
            original_name = sanitize_filename(msg.document.file_name)
        elif msg_type == "Video":
            if msg.video.file_name:
                original_name = sanitize_filename(msg.video.file_name)
            else:
                ext = ".mp4"
                if msg.video.mime_type:
                    if "mp4" in msg.video.mime_type:
                        ext = ".mp4"
                    elif "mkv" in msg.video.mime_type:
                        ext = ".mkv"
                original_name = f"video_{msgid}{ext}"
        elif msg_type == "Audio" and msg.audio.file_name:
            original_name = sanitize_filename(msg.audio.file_name)

        if original_name:
            file_path = await acc.download_media(
                msg,
                file_name=f"{temp_dir}/{original_name}",
                progress=progress_for_pyrogram,
                progress_args=(client, status_file, file_size, "down")
            )
        else:
            file_path = await acc.download_media(
                msg,
                file_name=f"{temp_dir}/",
                progress=progress_for_pyrogram,
                progress_args=(client, status_file, file_size, "down")
            )

        if os.path.exists(status_file): os.remove(status_file)
    except Exception as e:
        if batch_temp.IS_BATCH.get(message.from_user.id) or "Cancelled" in str(e):
            if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
            return await smsg.edit("❌ **Task Cancelled**")
        return await smsg.delete()

    try:
        ph_path = None
        thumb_id = await db.get_thumbnail(message.from_user.id)

        if thumb_id:
            try:
                ph_path = await client.download_media(thumb_id, file_name=f"{temp_dir}/custom_thumb.jpg")
            except Exception as e:
                logger.error(f"Failed to download custom thumb: {e}")

        if not ph_path:
            try:
                if msg_type == "Video" and msg.video.thumbs:
                    ph_path = await acc.download_media(msg.video.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
                elif msg_type == "Document" and msg.document.thumbs:
                    ph_path = await acc.download_media(msg.document.thumbs[0].file_id, file_name=f"{temp_dir}/thumb.jpg")
            except:
                pass

        if msg_type == "Document":
            await client.send_document(message.chat.id, file_path, thumb=ph_path, caption=final_caption)
        elif msg_type == "Video":
            await client.send_video(message.chat.id, file_path, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=final_caption)
        elif msg_type == "Audio":
            await client.send_audio(message.chat.id, file_path, thumb=ph_path, caption=final_caption)
        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file_path, caption=final_caption)

    except Exception as e:
         await smsg.edit(f"Upload Failed: {e}")

    if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
    await client.delete_messages(message.chat.id, [smsg.id])

@Client.on_callback_query()
async def button_callbacks(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message
    if not message: return

    if data == "dev_info":
        await callback_query.answer(
            text=dev_text,
            show_alert=True
        )
    elif data == "channels_info":
        await callback_query.answer(
            text=channels_text,
            show_alert=True
        )
    elif data == "settings_btn":
        await settings_panel(client, callback_query)
    elif data == "buy_premium":
        buttons = [
            [InlineKeyboardButton("📸 Send Payment Proof", url="https://t.me/Divyanshshukla7")],
            [InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]
        ]
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=SUBSCRIPTION,
                caption=script.PREMIUM_TEXT.format(UPI_ID, QR_CODE)
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "help_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.HELP_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "about_btn":
        buttons = [[InlineKeyboardButton("⬅️ Back to Home", callback_data="start_btn")]]
        await client.edit_message_caption(
            chat_id=message.chat.id,
            message_id=message.id,
            caption=script.ABOUT_TXT,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    elif data == "start_btn":
        bot = await client.get_me()
        apis = ["https://api.waifu.pics/sfw/waifu", "https://nekos.life/api/v2/img/waifu"]
        api_url = random.choice(apis)
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            photo_url = response.json()["url"]
        except Exception as e:
            logger.error(f"Failed to fetch image from API: {e}")
            photo_url = "https://i.postimg.cc/cC7txyhz/15.png"
        buttons = [
            [
                InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
                InlineKeyboardButton("🆘 Help & Guide", callback_data="help_btn")
            ],
            [
                InlineKeyboardButton("⚙️ Settings Panel", callback_data="settings_btn"),
                InlineKeyboardButton("ℹ️ About Bot", callback_data="about_btn")
            ],
            [
                InlineKeyboardButton('📢 Channels', callback_data="channels_info"),
                InlineKeyboardButton('👨‍💻 Developers', callback_data="dev_info")
            ]
        ]
        await client.edit_message_media(
            chat_id=message.chat.id,
            message_id=message.id,
            media=InputMediaPhoto(
                media=photo_url,
                caption=script.START_TXT.format(callback_query.from_user.mention, bot.username, bot.first_name)
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif data == "close_btn":
        await message.delete()
    elif data in ["cmd_list_btn", "user_stats_btn", "dump_chat_btn", "thumb_btn", "caption_btn"]:
        pass
    await callback_query.answer()
