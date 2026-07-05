import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.environ.get("TOKEN")

logging.basicConfig(level=logging.INFO)

# -----------------------
# 敏感詞庫（之後可以升級成 DB）
# -----------------------
bad_words = set([
    "操你妈",
    "鸡巴",
    "阴茎"
    "阴道"
    "台湾是中国的"
    "台独必亡"
    "小日子"
    "社会主义"
    "资本主义"
])

# -----------------------
# 歡迎訊息
# -----------------------
WELCOME_TEXT = """
欢迎 {name} 加入本群！本群为遵纪手法文明用的b站频道交流群，（中国人请进）
这是群规则，请务必遵守
1. 友好交流，礼貌相待
2. 禁止发送色情暴力有关的影片，图像和内容
3. 禁止在群中发表有关政治立场有关的言论

违反以上规则，可能会被管理员踢出群聊
主包在各大社交媒体的账号：
国内平台：
bilibili:https://b23.tv/6WtfDsb
快手：https://v.kuaishou.com/J5mfHFS2
国外平台：
YouTube：https://youtube.com/channel/UCF2c15DJ-EcqdcCFTA46f5g?si=_VD83CZ97lR62TvQ
facebook:https://www.facebook.com/share/14h2VZAjaiV/?mibextid=wwXIfr
instagram:https://www.instagram.com/zunjishoufawenmingyongw?igsh=ejFyemJmcHZudzNq&utm_source=qr
tiktok:https://www.tiktok.com/@zunjishoufawmy?_r=1&_d=f31c0l94d872b7&sec_uid=MS4wLjABAAAAC5wjGsbN2XNTuIX3uV5zwsD-0tBGBqEMlIbktD0K4BvfzWSfsaj9FjEB1TTqSDRi&share_author_id=7627744596160119825&sharer_language=en&source=h5_t&u_code=f31c2mbmabl8h8&item_author_type=1&utm_source=copy&tt_from=copy&enable_checksum=1&utm_medium=ios&share_link_id=2F84D75E-3BF3-49CD-A9BC-8A5062B7091F&user_id=7627744596160119825&sec_user_id=MS4wLjABAAAAC5wjGsbN2XNTuIX3uV5zwsD-0tBGBqEMlIbktD0K4BvfzWSfsaj9FjEB1TTqSDRi&social_share_type=4&ug_btm=b8727,b0&utm_campaign=client_share&share_app_id=1180
tiwwter:https://x.com/zwenmingyong?s=11"
"""
# -----------------------
# 新人歡迎
# -----------------------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:
        await update.message.reply_text(
            WELCOME_TEXT.format(name=user.full_name)
        )

# -----------------------
# 敏感詞檢測核心
# -----------------------
async def filter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()
    user = update.message.from_user

    for word in bad_words:
        if word in text:
            try:
                await update.message.delete()

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"⚠️ {user.full_name} 的訊息包含違規內容，已被刪除"
                )
            except Exception as e:
                logging.warning(e)

            return

# -----------------------
# 管理指令：新增敏感詞
# -----------------------
async def add_badword(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if not user:
        return

    if len(context.args) == 0:
        await update.message.reply_text("用法：/addbadword xxx")
        return

    word = context.args[0].lower()
    bad_words.add(word)

    await update.message.reply_text(f"已新增敏感詞：{word}")

# -----------------------
# 管理指令：查看敏感詞
# -----------------------
async def list_badwords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "目前敏感詞：\n" + "\n".join(bad_words)
    )

# -----------------------
# main
# -----------------------
def main():
    app = Application.builder().token(TOKEN).build()

    # 歡迎
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # 訊息過濾（核心）
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_message))

    # 管理指令
    app.add_handler(CommandHandler("addbadword", add_badword))
    app.add_handler(CommandHandler("badwords", list_badwords))

    print("Bot running...")
    app.run_polling()

if name == "__main__":
    main()
