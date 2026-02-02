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
• Auto-download and upload for restricted content
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
    CAPTION = """<b><a href="https://t.me/Divyanshshukla7"></a></b>

<b>⚜️ Powered By 💫『 𝒟𝒾𝓋𝓎𝒶𝓃𝓈𝒽 𝓈𝒽𝓊𝓀𝓁𝒶 』💫 : <a href="https://t.me/Divyanshshukla7">THE UPDATED GUYS 😎</a></b>"""
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
    tmp = ((str(days) + "d, ") if days else "") +         ((str(hours) + "h, ") if hours else "") +         ((str(minutes) + "m, ") if minutes else "") +         ((str(seconds) + "s, ") if seconds else "")
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

async def downstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as downread:
                txt = downread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)

async def upstatus(client, statusfile, message, chat):
    while not os.path.exists(statusfile):
        await asyncio.sleep(3)
    while os.path.exists(statusfile):
        try:
            with open(statusfile, "r", encoding='utf-8') as upread:
                txt = upread.read()
            await client.edit_message_text(chat, message.id, f"{txt}")
            await asyncio.sleep(5)
        except:
            await asyncio.sleep(5)

def progress(current, total, message, type):
    if batch_temp.IS_BATCH.get(message.from_user.id):
        raise Exception("Cancelled")
    if not hasattr(progress, "cache"):
        progress.cache = {}

    now = time.time()
    task_id = f"{message.id}{type}"
    last_time = progress.cache.get(task_id, 0)

    if not hasattr(progress, "start_time"):
        progress.start_time = {}
    if task_id not in progress.start_time:
        progress.start_time[task_id] = now

    if (now - last_time) > 5 or current == total:
        try:
            percentage = current * 100 / total
            speed = current / (now - progress.start_time[task_id]) if (now - progress.start_time[task_id]) > 0 else 0
            eta = (total - current) / speed if speed > 0 else 0
            elapsed = now - progress.start_time[task_id]

            filled_length = int(percentage / 5)
            bar = '█' * filled_length + ' ' * (20 - filled_length)

            status = script.PROGRESS_BAR.format(
                bar=bar,
                percentage=percentage,
                current=humanbytes(current),
                total=humanbytes(total),
                speed=humanbytes(speed),
                elapsed=TimeFormatter(elapsed * 1000),
                eta=TimeFormatter(eta * 1000)
            )

            with open(f'{message.id}{type}status.txt', "w", encoding='utf-8') as fileup:
                fileup.write(status)

            progress.cache[task_id] = now

            if current == total:
                progress.start_time.pop(task_id, None)
                progress.cache.pop(task_id, None)
        except:
            pass

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

@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in BATCH_STATE:
        del BATCH_STATE[user_id]
        await message.reply_text(
            "<b>❌ Batch process cancelled.</b>",
            parse_mode=enums.ParseMode.HTML
        )
        return

    batch_temp.IS_BATCH[user_id] = True
    await message.reply_text("❌ Current task cancelled.")

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

    # Check if in batch mode waiting for link
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
            return await message.reply_text("<b>⚠️ A Task is Currently Processing.</b>\n<i>Please wait for completion or use /cancel to stop.</i>", parse_mode=enums.ParseMode.HTML)

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
                    await client.copy_message(
                        chat_id=message.chat.id,
                        from_chat_id=username,
                        message_id=msgid,
                        reply_to_message_id=message.id
                    )
                    await db.add_traffic(message.from_user.id)
                    await asyncio.sleep(1)
                    continue
                except Exception as e:
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

            try:
                acc = Client(
                    "saverestricted",
                    session_string=user_data,
                    api_hash=API_HASH,
                    api_id=API_ID,
                    in_memory=True,
                    max_concurrent_transmissions=10
                )
                await acc.connect()
            except Exception as e:
                batch_temp.IS_BATCH[message.from_user.id] = True
                return await message.reply(f"<b>❌ Authentication Failed</b>\n\n<i>Your session may have expired. Please /logout and /login again.</i>\n<code>{e}</code>", parse_mode=enums.ParseMode.HTML)

            if is_private_link:
                chatid = int("-100" + datas[4])
                await handle_restricted_content(client, acc, message, chatid, msgid)
            elif is_batch:
                username = datas[4]
                await handle_restricted_content(client, acc, message, username, msgid)
            else:
                username = datas[3]
                await handle_restricted_content(client, acc, message, username, msgid)

            await asyncio.sleep(2)

        batch_temp.IS_BATCH[message.from_user.id] = True

# ========== MAIN BATCH PROCESSING WITH FULL MEDIA SUPPORT ==========
async def process_batch_with_destination(client: Client, message: Message):
    """Process batch with user-selected destination - FULL MEDIA SUPPORT"""
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

        # Determine target chat
        if destination == "channel" and dump_chat_id:
            target_chat = dump_chat_id
            dest_text = f"📢 Channel ({dump_chat_id})"
        else:
            target_chat = message.chat.id
            dest_text = "📱 Chat"

        progress_msg = await message.reply_text(
            f"<b>📦 Starting Batch Download</b>\n\n"
            f"<b>Destination:</b> {dest_text}\n"
            f"<b>Total Files:</b> <code>{total_files}</code>\n"
            f"<b>Range:</b> <code>{start_id}</code> to <code>{end_id}</code>\n\n"
            f"<i>Processing...</i>",
            parse_mode=enums.ParseMode.HTML
        )

        success_count = 0
        failed_count = 0
        is_private = "https://t.me/c/" in text
        is_public = not is_private

        for idx, msgid in enumerate(range(start_id, end_id + 1), 1):
            if idx % 2 == 0 or idx == 1:
                try:
                    await progress_msg.edit_text(
                        f"<b>📦 Batch Download Progress</b>\n\n"
                        f"<b>Destination:</b> {dest_text}\n"
                        f"<b>Progress:</b> <code>{idx}/{total_files}</code>\n"
                        f"<b>✅ Success:</b> <code>{success_count}</code>\n"
                        f"<b>❌ Failed:</b> <code>{failed_count}</code>\n\n"
                        f"<i>Processing message {msgid}...</i>",
                        parse_mode=enums.ParseMode.HTML
                    )
                except:
                    pass

            try:
                if is_public:
                    username = datas[3]
                    # Try copy first (fast), if fails then download+upload
                    try:
                        await client.copy_message(
                            chat_id=target_chat,
                            from_chat_id=username,
                            message_id=msgid
                        )
                        await db.add_traffic(user_id)
                        success_count += 1
                    except Exception as copy_error:
                        # Copy failed (restricted), try download+upload
                        logger.warning(f"Copy failed for {msgid}, trying download: {copy_error}")
                        try:
                            await download_upload_public(
                                client, message, username, msgid, target_chat
                            )
                            await db.add_traffic(user_id)
                            success_count += 1
                        except Exception as dl_error:
                            logger.error(f"Download also failed for {msgid}: {dl_error}")
                            failed_count += 1
                else:
                    # Private channel - must use download+upload
                    user_session = await db.get_session(user_id)
                    if not user_session:
                        await message.reply_text(
                            "<b>🔒 Login Required!</b>\nUse /login first for private channels.",
                            parse_mode=enums.ParseMode.HTML
                        )
                        failed_count += (total_files - idx + 1)
                        break

                    try:
                        await download_upload_private(
                            client, message, user_id, msgid, datas, target_chat
                        )
                        await db.add_traffic(user_id)
                        success_count += 1
                    except Exception as e:
                        logger.error(f"Private download failed for {msgid}: {e}")
                        failed_count += 1

            except Exception as e:
                logger.error(f"Batch error for {msgid}: {e}")
                failed_count += 1

            await asyncio.sleep(3)  # Prevent flood

        await progress_msg.edit_text(
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

async def download_upload_public(client, message, username, msgid, target_chat):
    """Download and upload from public channel (when copy fails)"""
    # Create temporary client for public channel
    temp_client = Client(
        "public_temp",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    await temp_client.connect()

    try:
        # Get message
        msg = await temp_client.get_messages(username, msgid)
        if not msg or msg.empty:
            raise Exception("Message not found or empty")

        # Handle different media types
        if msg.document:
            file_path = await temp_client.download_media(msg.document.file_id)
            await client.send_document(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.video:
            file_path = await temp_client.download_media(msg.video.file_id)
            await client.send_video(
                target_chat, 
                file_path, 
                duration=msg.video.duration,
                width=msg.video.width,
                height=msg.video.height,
                caption=msg.caption
            )
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.photo:
            file_path = await temp_client.download_media(msg.photo.file_id)
            await client.send_photo(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.audio:
            file_path = await temp_client.download_media(msg.audio.file_id)
            await client.send_audio(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.text:
            await client.send_message(target_chat, msg.text)
        else:
            raise Exception("Unsupported message type")

    finally:
        await temp_client.disconnect()

async def download_upload_private(client, message, user_id, msgid, datas, target_chat):
    """Download and upload from private channel"""
    user_session = await db.get_session(user_id)
    if not user_session:
        raise Exception("No session")

    acc = Client(
        "saverestricted",
        session_string=user_session,
        api_hash=API_HASH,
        api_id=API_ID,
        in_memory=True,
        max_concurrent_transmissions=10
    )
    await acc.connect()

    try:
        chatid = int("-100" + datas[4])
        msg = await acc.get_messages(chatid, msgid)

        if not msg or msg.empty:
            raise Exception("Message not found or empty")

        # Handle different media types with download
        if msg.document:
            file_path = await acc.download_media(msg.document.file_id)
            if not file_path:
                raise Exception("Download failed")
            await client.send_document(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.video:
            file_path = await acc.download_media(msg.video.file_id)
            if not file_path:
                raise Exception("Download failed")
            await client.send_video(
                target_chat, 
                file_path,
                duration=msg.video.duration,
                width=msg.video.width,
                height=msg.video.height,
                caption=msg.caption
            )
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.photo:
            file_path = await acc.download_media(msg.photo.file_id)
            if not file_path:
                raise Exception("Download failed")
            await client.send_photo(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.audio:
            file_path = await acc.download_media(msg.audio.file_id)
            if not file_path:
                raise Exception("Download failed")
            await client.send_audio(target_chat, file_path, caption=msg.caption)
            if os.path.exists(file_path):
                os.remove(file_path)

        elif msg.text:
            await client.send_message(target_chat, msg.text)
        else:
            raise Exception("Unsupported message type")

    finally:
        await acc.disconnect()

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

    if msg_type == "Text":
        try:
            await client.send_message(message.chat.id, msg.text, entities=msg.entities, parse_mode=enums.ParseMode.HTML)
            return
        except:
            return

    await db.add_traffic(message.from_user.id)
    smsg = await client.send_message(message.chat.id, '<b>⬇️ Starting Download...</b>', reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)

    temp_dir = f"downloads/{message.id}"
    if not os.path.exists(temp_dir): os.makedirs(temp_dir)

    try:
        asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, message.chat.id))

        file = await acc.download_media(
            msg,
            file_name=f"{temp_dir}/",
            progress=progress,
            progress_args=[message, "down"]
        )

        if os.path.exists(f'{message.id}downstatus.txt'): os.remove(f'{message.id}downstatus.txt')
    except Exception as e:
        if batch_temp.IS_BATCH.get(message.from_user.id) or "Cancelled" in str(e):
            if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
            return await smsg.edit("❌ **Task Cancelled**")
        return await smsg.delete()

    try:
        asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, message.chat.id))

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

        custom_caption = await db.get_caption(message.from_user.id)
        if custom_caption:
            final_caption = custom_caption.format(filename=file.split("/")[-1], size=humanbytes(file_size))
        else:
            final_caption = script.CAPTION.format(file_name=file.split("/")[-1])
            if msg.caption:
                final_caption += f"\n\n{msg.caption}"

        if msg_type == "Document":
            await client.send_document(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Video":
            await client.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Audio":
            await client.send_audio(message.chat.id, file, thumb=ph_path, caption=final_caption, progress=progress, progress_args=[message, "up"])
        elif msg_type == "Photo":
            await client.send_photo(message.chat.id, file, caption=final_caption)

    except Exception as e:
         await smsg.edit(f"Upload Failed: {e}")

    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
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
