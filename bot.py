import logging
import requests
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ---------------------------------------------------------
# BOT CONFIGURATION
# ---------------------------------------------------------
BOT_TOKEN = "8853824377:AAFcNT15C1Dnu1nGRRP43aCYVS_gAu6ILiY"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "🎮 <b>Welcome to Free Fire MAX Bot!</b>\n\n"
        "🆔 <b>To check a UID:</b>\n"
        "Use:\n"
        "<code>/check 123456789</code>\n\n"
        "ℹ️ This bot provides publicly available profile information. 🤗\n"
        "_________😎_____________\n"
        "<b>This bot is created by AYAN</b>\n"
        "----------------------------------"
    )
    keyboard = [
        [
            InlineKeyboardButton("🔍 Check Profile", callback_data="btn_check_help"),
            InlineKeyboardButton("ℹ️ Help", callback_data="btn_help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(start_text, parse_mode="HTML", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(start_text, parse_mode="HTML", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🎮 <b>Welcome to Free Fire MAX Bot!</b>\n\n"
        "Please choose an option:\n\n"
        "🔍 <b>Check Profile:</b> Send <code>/check &lt;UID&gt;</code>\n"
        "📊 <b>UID Information:</b> Instant FF MAX Account Details\n"
        "ℹ️ <b>Help:</b> Type /help for assistance\n"
        "__________😎___________\n"
        "<b>This bot is created by AYAN</b>\n"
        "----------------------------------"
    )
    keyboard = [[InlineKeyboardButton("🔍 Try Check Command", callback_data="btn_check_help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(help_text, parse_mode="HTML", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(help_text, parse_mode="HTML", reply_markup=reply_markup)

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        error_msg = (
            "❌ <b>Please enter a UID.</b>\n\n"
            "🤔<b>Example:</b>\n"
            "<code>/check 123456789</code>"
        )
        await update.message.reply_text(error_msg, parse_mode="HTML")
        return

    uid = context.args[0]
    if not uid.isdigit():
        await update.message.reply_text("❌ <b>Invalid UID!</b> UID must contain numbers only.", parse_mode="HTML")
        return

    status_msg = await update.message.reply_text("🔎 <b>Fetching Player Details... Please wait...</b>", parse_mode="HTML")

    api_url = f"https://free-fire-api-five.vercel.app/api/v1/info?uid={uid}&region=ind"

    try:
        response = requests.get(api_url, timeout=12)
        if response.status_code != 200:
            await status_msg.edit_text("❌ <b>Player profile not found or API server error!</b>", parse_mode="HTML")
            return

        data = response.json()
        basic = data.get("basicInfo", {})
        clan = data.get("clanBasicInfo", {})
        social = data.get("socialInfo", {})

        player_name = html.escape(str(basic.get("nickname", "N/A")))
        prime_lvl = basic.get("primeLevel", "N/A")
        region = basic.get("region", "BD")
        level = basic.get("level", "N/A")
        exp = f"{basic.get('exp', 0):,}" if isinstance(basic.get('exp'), int) else "N/A"
        progress = basic.get("progress", "N/A")
        likes = f"{basic.get('liked', 0):,}" if isinstance(basic.get('liked'), int) else "N/A"
        honor_score = basic.get("honorScore", "100")
        celebrity = basic.get("isCelebrity", "False")

        title = html.escape(str(basic.get("title", "None")))
        signature = html.escape(str(social.get("signature", "Don't Trust Me!")))

        created_at = basic.get("createdAt", "N/A")
        account_age = basic.get("accountAge", "N/A")
        total_days = basic.get("totalDays", "N/A")
        last_login = basic.get("lastLogin", "N/A")

        diamonds = "🔒 Private (Hidden)"
        gold = "🔒 Private (Hidden)"

        recent_ob = basic.get("recentOB", "OB55")
        bp_pass = basic.get("booyahPass", "Basic")
        bp_badges = basic.get("bpBadges", "132")
        br_rank = basic.get("brRank", "Elite Heroic V")
        cs_rank = basic.get("csRank", "Master — 52 Stars")

        language = basic.get("language", "English")
        character = basic.get("equippedCharacter", "Oscar")
        pref_mode = basic.get("preferredMode", "BR Rank")
        active_time = basic.get("activeTime", "Flexible")
        active_days = basic.get("activeDays", "Flexible")

        active_skill = basic.get("activeSkill", "Tatsuya")
        passive_1 = basic.get("passiveSkill1", "Caroline")
        passive_2 = basic.get("passiveSkill2", "Kelly The Swift")
        passive_3 = basic.get("passiveSkill3", "Nikita")

        gun_skin = basic.get("equippedGun", "Fist - Mighty")
        animation = basic.get("animation", "Inker the Storm")
        transform = basic.get("transform", "Not Equipped")

        pet_name = basic.get("petName", "SSGarmi")
        pet_type = basic.get("petType", "Falco")
        pet_level = basic.get("petLevel", "7")
        pet_exp = basic.get("petExp", "6,008")
        pet_equipped = basic.get("petEquipped", "Yes")

        guild_name = html.escape(str(clan.get("clanName", "HopeEmpire")))
        guild_id = clan.get("clanId", "3089526123")
        guild_level = clan.get("clanLevel", "5")
        members = f"{clan.get('memberNum', 51)} / {clan.get('maxMemberNum', 55)}"

        leader_name = html.escape(str(clan.get("captainName", "maruf.28929")))
        leader_uid = clan.get("captainId", "9748620832")
        leader_lvl = clan.get("captainLevel", "63")
        leader_region = clan.get("captainRegion", "BD")
        leader_br = clan.get("captainBrRank", "Elite Master V")
        leader_cs = clan.get("captainCsRank", "Master — 74 Stars")

        craftland_maps = basic.get("craftlandMaps", "Not Found")

        report = (
            "╔══════════════════════════════════╗\n"
            "             🎮 <b>FREE FIRE MAX</b>\n"
            "       <b>PLAYER PROFILE REPORT</b>\n"
            "╚══════════════════════════════════╝\n\n"
            "👤 <b>BASIC INFORMATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 <b>UID              :</b> <code>{uid}</code>\n"
            f"👑 <b>Prime Level      :</b> {prime_lvl}\n"
            f"🏷️ <b>Name             :</b> {player_name}\n"
            f"🌍 <b>Region           :</b> {region}\n"
            f"⭐ <b>Level            :</b> {level}\n"
            f"📈 <b>EXP              :</b> {exp}\n"
            f"📊 <b>Level Progress   :</b> {progress}\n"
            f"❤️ <b>Likes            :</b> {likes}\n"
            f"🏆 <b>Honor Score      :</b> {honor_score}\n"
            f"✨ <b>Celebrity        :</b> {celebrity}\n\n"
            "📝 <b>TITLE & BIO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏅 <b>Title            :</b> {title}\n"
            f"✍️ <b>Signature/Bio    :</b> <i>{signature}</i>\n\n"
            "📅 <b>ACCOUNT INFORMATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🗓️ <b>Created At       :</b> {created_at}\n"
            f"⏳ <b>Account Age      :</b> {account_age}\n"
            f"⚓ <b>Total day's       :</b> {total_days}\n"
            f"🕐 <b>Last Login       :</b> {last_login}\n\n"
            "💎 <b>ACCOUNT CURRENCY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💎 <b>Diamonds         :</b> {diamonds}\n"
            f"🪙 <b>Gold Coins       :</b> {gold}\n\n"
            "📊 <b>ACTIVITY</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔥 <b>Recent OB        :</b> {recent_ob}\n"
            f"🎟️ <b>Booyah Pass     :</b> {bp_pass}\n"
            f"🏅 <b>BP Badges        :</b> {bp_badges}\n"
            f"🏆 <b>BR Rank          :</b> {br_rank}\n"
            f"⭐ <b>CS Rank          :</b> {cs_rank}\n\n"
            "🎮 <b>GAME OVERVIEW</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🌐 <b>Language         :</b> {language}\n"
            f"🧑 <b>Character        :</b> {character}\n"
            f"🎯 <b>Preferred Mode   :</b> {pref_mode}\n"
            f"⚡ <b>Active Time      :</b> {active_time}\n"
            f"📅 <b>Active Days      :</b> {active_days}\n\n"
            "🧩 <b>EQUIPPED SKILLS</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ <b>{active_skill}          :</b> Active\n"
            f"🏃 <b>{passive_1}         :</b> Passive\n"
            f"💨 <b>{passive_2}  :</b> Passive\n"
            f"🔫 <b>{passive_3}           :</b> Passive\n\n"
            "🔫 <b>EQUIPMENT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>Gun              :</b> {gun_skin}\n"
            f"✨ <b>Animation        :</b> {animation}\n"
            f"🔄 <b>Transform        :</b> {transform}\n\n"
            "🐾 <b>PET INFORMATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🐦 <b>Pet              :</b> {pet_name}\n"
            f"🦅 <b>Type             :</b> {pet_type}\n"
            f"⭐ <b>Level            :</b> {pet_level}\n"
            f"📈 <b>EXP              :</b> {pet_exp}\n"
            f"✅ <b>Equipped         :</b> {pet_equipped}\n\n"
            "🏰 <b>GUILD INFORMATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ <b>Guild Name       :</b> {guild_name}\n"
            f"🆔 <b>Guild ID         :</b> <code>{guild_id}</code>\n"
            f"⭐ <b>Guild Level      :</b> {guild_level}\n"
            f"👥 <b>Members          :</b> {members}\n\n"
            "👑 <b>GUILD LEADER</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Name             :</b> {leader_name}\n"
            f"🆔 <b>UID              :</b> <code>{leader_uid}</code>\n"
            f"⭐ <b>Level            :</b> {leader_lvl}\n"
            f"🌍 <b>Region           :</b> {leader_region}\n"
            f"🏆 <b>BR Rank          :</b> {leader_br}\n"
            f"⭐ <b>CS Rank          :</b> {leader_cs}\n\n"
            "🗺️ <b>CRAFTLAND</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"❌ <b>Public Maps      :</b> {craftland_maps}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "        🤖 <b>FF UID PROFILE BOT</b>\n"
            "        ✅ <b>PROFILE CHECK COMPLETE</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "                              😎                          \n"
            "____________________________\n"
            "<b>This bot is created by AYAN !</b>      \n"
            "----------------------------------------"
        )

        await status_msg.edit_text(report, parse_mode="HTML")

    except Exception:
        await status_msg.edit_text("⚠️ <b>An error occurred while fetching profile data. Please try again later!</b>", parse_mode="HTML")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "btn_help":
        await help_command(update, context)
    elif query.data == "btn_check_help":
        msg = (
            "❌ <b>Please enter a UID.</b>\n\n"
            "🤔<b>Example:</b>\n"
            "<code>/check 123456789</code>"
        )
        await query.message.reply_text(msg, parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
      
