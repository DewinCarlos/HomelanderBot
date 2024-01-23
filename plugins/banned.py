from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'<b>‼️Sorry Dude, You are Banned to use Me.‼️</b> \n\nBan Reason: {ban["ban_reason"]}')

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('🧬 𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/https://t.me/raixchat')
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"𝗧𝗵𝗶𝘀 𝗖𝗵𝗮𝘁 𝗜𝘀 𝗡𝗼𝘁 𝗔𝗹𝗹𝗼𝘄𝗱𝗲𝗱.!\n\n𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖬𝗒 𝖬𝖺𝗌𝗍𝖾𝗋.\nReason : <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
