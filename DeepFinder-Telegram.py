import requests
import time
import telebot
import urllib3
import threading
from datetime import datetime

## DeepFinder 서버의 SSL 인증서가 유효하지 않은 경우에도 요청을 처리하기 위해 아래 구문을 추가
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# DeepFinder 서버 정보를 가져오는 API URL

## 해당 구문은 예시 구문으로 아래와 같이 작성해주세요
#API_URL = "https://test.com" ## DeepFinder 서버 도메인 혹은 아이피 주소를 입력해주세요
#AUTH_KEY = "keykeykeykey" ## DeepFinder 서버의 AUTH_KEY를 입력해주세요
#TELEGRAM_BOT_TOKEN = "123123:ABCDEFGHIJKLMN" ## Telegram Bot Token을 입력
#ALLOWED_CHAT_IDS = [12345678] ## 텔레그램 채팅방 ID를 입력해주세요
#MUTE_FILE = "mute.txt" ## Mute IP 주소를 저장하는 파일명

API_URL = "" ## DeepFinder 서버 도메인 혹은 아이피 주소를 입력해주세요
AUTH_KEY = "" ## DeepFinder 서버의 AUTH_KEY를 입력해주세요
TELEGRAM_BOT_TOKEN = "" ## Telegram Bot Token을 입력
ALLOWED_CHAT_IDS = [] ## 텔레그램 채팅방 ID를 입력해주세요
MUTE_FILE = "mute.txt" ## Mute IP 주소를 저장하는 파일명


# 서버 정보를 가져오는 함수
# API_URL에 AUTH_KEY를 파라미터로 전달하여 요청
def get_server_config():
    try:
        params = {"key": AUTH_KEY}
        response = requests.get(API_URL, params={"key": AUTH_KEY}, verify=False)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to get server config. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error while calling the API: {e}")
        return None

 # 등록된 채팅방(Chat) ID 목록에 있는 경우에만 메시지를 전송
def send_telegram_message(message):
    for chat_id in ALLOWED_CHAT_IDS: 
        bot.send_message(chat_id, message)
    else:
        print("Unauthorized chat ID.")
        

 # IP 주소를 mute.txt 파일에 추가
def mute_ip(ip_address):
    with open("mute.txt", "a") as file:
        file.write(ip_address + "\n")

 # mute.txt 파일에서 IP 주소 목록을 가져옴
def get_muted_ips():
    with open("mute.txt", "r") as file:
        return [ip.strip() for ip in file.readlines()]

 # IP 주소를 mute.txt 파일에서 제거
def unmute_ip(ip_address):
    muted_ips = get_muted_ips()
    if ip_address in muted_ips:
        muted_ips.remove(ip_address)
        with open("mute.txt", "w") as file:
            for ip in muted_ips:
                file.write(ip + "\n")
        return True
    return False

 # 봇을 시작하고 메시지를 수신 대기
def start_bot_polling():
    bot.polling(none_stop=True)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# /mute 명령어를 처리하는 함수
@bot.message_handler(commands=['mute'])
def handle_mute_command(message):
    ip_address = message.text.replace("/mute", "").strip()
    if ip_address:
        mute_ip(ip_address)
        bot.reply_to(message, f"IP {ip_address} 알람 Mute 완료")
    else:
        bot.reply_to(message, f"/mute IP 주소를 입력해주세요 ex) /mute 115.68.1.1 ")

# /excute 명령어를 처리하는 함수
@bot.message_handler(commands=['excute'])
def handle_excute_command(message):
    ip_address = message.text.replace("/excute", "").strip()
    if ip_address:
        if unmute_ip(ip_address):
            bot.reply_to(message, f"IP {ip_address} 알람 Unmute 완료")
        else:
            bot.reply_to(message, f"IP {ip_address} mute 목록에 없습니다.")
    else:
        bot.reply_to(message, f"/excute IP 주소를 입력해주세요 ex) /excute 115.68.1.1")

# /list 명령어를 처리하는 함수
@bot.message_handler(commands=['list'])
def handle_list_command(message):
    muted_ips = get_muted_ips() 
    if len(muted_ips) > 0:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_message = f"ℹ️ [DeepFinder Monitoring] Muted IP 리스트 \n\n"
        response_message += " == Muted IP == \n"
        response_message += "\n".join(muted_ips)
    else:
        response_message = "등록된 Muted IP가 없습니다."
    
    bot.reply_to(message, response_message)


if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot_polling, daemon=True)
    bot_thread.start()


    # 주기적으로 서버 정보를 가져와서 문제가 있는지 확인
    # 문제가 있는 경우에는 텔레그램으로 메시지 전송
    # 문제가 없는 경우에는 5분 대기
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
                    sid = item['filter_yn2']
                    ip = item['ip']
                    if ip not in muted_ips:
                        message += f"{ip} \n"
                        unmuted_ips_count += 1

                if unmuted_ips_count > 0:
                    send_telegram_message(message)

        time.sleep(3000)