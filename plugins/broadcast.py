import datetime, time, os, asyncio,logging 
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton
from pyrogram import Client, filters, enums
from database.users_chats_db import db
from info import ADMINS
        
@Client.on_message(filters.command(["bb", "broadcast"]) & filters.user(ADMINS) & filters.reply)
async def broadcast(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(text='🚀')
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌 {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {blocked}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await bot.send_message(message.chat.id, f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇:\n𝖳𝗂𝗆𝖾 𝖳𝖺𝗄𝖾𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌ꜱ: {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {blocked}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {deleted}")

@Client.on_message(filters.command(["cb", "clean_broadcast"]) & filters.user(ADMINS))
async def remove_junkuser__db(bot, message):
    users = await db.get_all_users()
    b_msg = message 
    sts = await message.reply_text(text='🚀') 
    start_time = time.time()
    total_users = await db.total_users_count()
    blocked = 0
    deleted = 0
    failed = 0
    done = 0
    async for user in users:
        pti, sh = await clear_junk(int(user['id']), b_msg)
        if pti == False:
            if sh == "Blocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌 {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {blocked}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await bot.send_message(message.chat.id, f"𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌 {total_users}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_users}\n𝖡𝗅𝗈𝖼𝗄𝖾𝖽: {blocked}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")

@Client.on_message(filters.command(["gg", "group_broadcast"]) & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message.reply_to_message
    sts = await message.reply_text(text='🚀')
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed = ""
    success = 0
    deleted = 0
    async for group in groups:
        pti, sh, ex = await broadcast_messages_group(int(group['id']), b_msg)
        if pti == True:
            if sh == "Succes":
                success += 1
        elif pti == False:
            if sh == "deleted":
                deleted+=1 
                failed += ex 
                try:
                    await bot.leave_chat(int(group['id']))
                except Exception as e:
                    print(f"{e} > {group['id']}")  
        done += 1
        if not done % 20:
            await sts.edit(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    try:
        await message.reply_text(f"𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}\n\n𝖱𝖾𝖺𝗌𝗈𝗇:- {failed}")
    except MessageTooLong:
        with open('reason.txt', 'w+') as outfile:
            outfile.write(failed)
        await message.reply_document('reason.txt', caption=f"𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: {success}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")
        os.remove("reason.txt")
    
@Client.on_message(filters.command(["cg", "clean_gbroadcast"]) & filters.user(ADMINS))
async def junk_clear_group(bot, message):
    groups = await db.get_all_chats()
    b_msg = message
    sts = await message.reply_text(text='🚀')
    start_time = time.time()
    total_groups = await db.total_chat_count()
    done = 0
    failed = ""
    deleted = 0
    async for group in groups:
        pti, sh, ex = await junk_group(int(group['id']), b_msg)        
        if pti == False:
            if sh == "deleted":
                deleted+=1 
                failed += ex 
                try:
                    await bot.leave_chat(int(group['id']))
                except Exception as e:
                    print(f"{e} > {group['id']}")  
        done += 1
        if not done % 20:
            await sts.edit(f"𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    try:
        await bot.send_message(message.chat.id, f"𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}\n\n𝖱𝖾𝖺𝗌𝗈𝗇:- {failed}")    
    except MessageTooLong:
        with open('junk.txt', 'w+') as outfile:
            outfile.write(failed)
        await message.reply_document('junk.txt', caption=f"𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽:\𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖨𝗇 {time_taken} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌.\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌 {total_groups}\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: {done} / {total_groups}\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽: {deleted}")
        os.remove("junk.txt")

async def broadcast_messages_group(chat_id, message):
    try:
        await message.copy(chat_id=chat_id)
        return True, "Succes", 'mm'
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages_group(chat_id, message)
    except Exception as e:
        await db.delete_chat(int(chat_id))       
        logging.info(f"{chat_id} - PeerIdInvalid")
        return False, "deleted", f'{e}\n\n'
    
async def junk_group(chat_id, message):
    try:
        kk = await message.copy(chat_id=chat_id)
        await kk.delete(True)
        return True, "Succes", 'mm'
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await junk_group(chat_id, message)
    except Exception as e:
        await db.delete_chat(int(chat_id))       
        logging.info(f"{chat_id} - PeerIdInvalid")
        return False, "deleted", f'{e}\n\n'
    
async def clear_junk(user_id, message):
    try:
        key = await message.copy(chat_id=user_id)
        await key.delete(True)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await clear_junk(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"