import time
import os
import telebot
import threading
import urllib3
from datetime import datetime
from server_config import get_server_config
from ip_mute import mute_ip, get_muted_ips, unmute_ip
from datetime import datetime
from dotenv import load_dotenv
from telegram_bot import send_telegram_message

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TELEBOT = os.getenv("TELEGRAM_BOT_TOKEN")
TELECHAT = [int(chat_id) for chat_id in os.getenv("TELEGRAM_CHAT_ID").split(",")]

bot = telebot.TeleBot(TELEBOT)

def send_telegram_message(bot, message):
    for chat_id in TELECHAT:  # 등록된 채팅방(Chat) ID 목록에 있는 경우에만 메시지를 전송합니다.
        bot.send_message(chat_id, message)

def start_bot_polling(bot):
    bot.polling(none_stop=True)
    
def automatic_server_status_check():
    while True:
        server_data = get_server_config()
        if server_data:
            filtered_data = [item for item in server_data.get('data', []) if (int(item.get('sid')) == 0 or int(item.get('filter_yn2')) == -1) and int(item.get('filter_yn2')) != 1]
            if filtered_data:
                message = "⚠️ [DeepFinder Monitoring] Agent 문제발생 \n\n"
                message += f"알람명 : Agent 체크 불가 \n"
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message += f"발생 시기 :{current_time} \n"
                message += f" === IP 목록 === \n"
                muted_ips = get_muted_ips()

                unmuted_ips_count = 0
                for item in filtered_data:
                    sid = item['sid']
                    filter_yn2 = item['filter_yn2']
                    ip = item['ip']
                    if ip not in muted_ips:
                        message += f"{ip} \n"
                        unmuted_ips_count += 1

                if unmuted_ips_count > 0:
                    send_telegram_message(bot, message)  # 변경된 코드
        time.sleep(10 * 60)  # 10분마다 서버 상태를 확인합니다.

# IP 주소를 차단하는 함수를 정의합니다.
@bot.message_handler(commands=['mute'])
def mute(message):
    ip_address = message.text.split(' ')[1]
    mute_ip(ip_address)
    bot.reply_to(message, f"{ip_address} 차단되었습니다.")

# IP 차단을 해제하는 함수를 정의합니다.
@bot.message_handler(commands=['unmute'])
def unmute(message):
    ip_address = message.text.split(' ')[1]
    if unmute_ip(ip_address):
        bot.reply_to(message, f"{ip_address} 차단이 해제되었습니다.")
    else:
        bot.reply_to(message, f"{ip_address} 차단 목록에 없습니다.")

# 차단된 IP 목록을 출력하는 함수를 정의합니다.
@bot.message_handler(commands=['muteip'])
def blocked_ips(message):
    ips = get_muted_ips()
    if len(ips) > 0:    
        ips_text = "\n".join(ips)
        bot.send_message(message.chat.id, f"차단된 IP 목록:\n{ips_text}")
    else:
        bot.send_message(message.chat.id, "차단된 IP가 없습니다.")



if __name__ == "__main__":
    threading.Thread(target=start_bot_polling, args=(bot,)).start()
    threading.Thread(target=automatic_server_status_check).start()
