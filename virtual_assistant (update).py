import os
import playsound
import speech_recognition as sr
import time
import ctypes
import wikipedia
import datetime
import json
import webbrowser
import smtplib
import requests
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from gtts import gTTS
import tkinter as tk
from youtube_search import YoutubeSearch
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Định nghĩa biến toàn cục
text_widget = None


def set_text_widget(widget):
    global text_widget
    text_widget = widget


wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

# Hàm chuyển text sang giọng nói
def speak(text):
    try:
        if text_widget:
            text_widget.config(state=tk.NORMAL)  # Mở quyền ghi vào Text widget
            text_widget.insert(tk.END, f"Bot: {text}\n")
            text_widget.see(tk.END)
            text_widget.config(state=tk.DISABLED)  # Ngăn người dùng nhập liệu

        # Xóa tệp nếu nó đã tồn tại
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")

        # Tạo âm thanh từ văn bản
        tts = gTTS(text=text, lang='vi')
        tts.save("speech.mp3")

        # Phát âm thanh
        full_path = os.path.abspath("speech.mp3")
        playsound.playsound(full_path)

    except Exception as e:
        if text_widget:
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, f"Lỗi khi phát âm: {e}\n")
            text_widget.see(tk.END)
            text_widget.config(state=tk.DISABLED)

# Chuyển đổi âm thanh sang văn bản
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            return text
        except sr.UnknownValueError:
            speak("Bot không nghe rõ. Bạn nói lại được không!")
            return None
        except sr.RequestError as e:
            speak(f"Lỗi kết nối đến Google Speech Recognition service: {e}")
            return None


def stop():
    speak("Hẹn gặp lại bạn sau!")


def get_text():
    attempt_count = 3  # Số lần thử lắng nghe
    for i in range(attempt_count):
        text = get_audio()
        if text:
            if text_widget:
                text_widget.config(state=tk.NORMAL)
                text_widget.insert(tk.END, f"Bạn: {text}\n")
                text_widget.see(tk.END)
                text_widget.config(state=tk.DISABLED)
            return text.lower()
        elif i == attempt_count - 1:  # Chỉ nói thông báo khi hết lần thử cuối
            speak("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(2)
    stop()
    return 0



def hello():
    day_time = int(datetime.datetime.now().strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn. Chúc bạn một ngày tốt lành.")
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn. Bạn đã dự định gì cho chiều nay chưa.")
    else:
        speak("Chào buổi tối bạn. Bạn đã ăn tối chưa nhỉ.")


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")


def open_application(text):
    if "word" in text:
        speak("Mở Microsoft Word")
        os.startfile('C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE')
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile('C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE')
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")


def open_website(command):
    if "google" in command:
        speak("Đang mở Google")
        webbrowser.open("https://www.google.com")
    elif "youtube" in command:
        speak("Đang mở YouTube")
        webbrowser.open("https://www.youtube.com")
    else:
        speak("Xin lỗi, tôi không thể mở trang web đó.")


def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1].strip()
    if not search_for:
        speak("Xin lỗi, bạn chưa cung cấp từ khóa tìm kiếm.")
        return

    speak('Đang mở Google và tìm kiếm cho bạn...')
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("http://www.google.com")

        que = driver.find_element("name", "q")
        que.send_keys(search_for)
        que.send_keys(Keys.RETURN)

        speak("Tìm kiếm đã hoàn tất. Bạn có thể nói 'tắt Google' để tắt trình duyệt.")

        while True:
            command = get_text()
            if command and "tắt google" in command.lower():
                speak("Đang tắt Google...")
                driver.quit()
                break
            else:
                speak("Bạn có thể nói 'tắt Google' để đóng trình duyệt.")
    except Exception as e:
        speak(f"Đã xảy ra lỗi khi mở trình duyệt: {e}")


def send_email(text):
    speak('Bạn gửi email cho ai nhỉ')
    recipient = get_text()
    if 'nhiên' in recipient.lower():
        speak('Nội dung bạn muốn gửi là gì')
        content = get_text()
        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('your_email@gmail.com', 'your_password')
            mail.sendmail('your_email@gmail.com', '2254810197@vaa.edu.vn', content.encode('utf-8'))
            mail.close()
            speak('Email của bạn vùa được gửi.')
        except Exception as e:
            speak(f"Lỗi khi gửi email: {e}")
    else:
        speak('Bot không hiểu bạn muốn gửi email cho ai.')


def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute,
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        return f"{content}"
    else:
        speak("Không tìm thấy địa chỉ của bạn")
        return "Không tìm thấy địa chỉ của bạn"


def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    mysong = get_text()
    if not mysong:
        speak("Bot không nhận được tên bài hát.")
        return
    try:
        results = YoutubeSearch(mysong, max_results=10).to_dict()
        if not results:
            speak("Xin lỗi, không tìm thấy bài hát nào.")
            return
        video = results[0]
        url = f'https://www.youtube.com/watch?v={video["id"]}'
        webbrowser.open(url)
        speak(f"Đang mở bài hát {mysong} trên YouTube.")
    except Exception as e:
        speak(f"Đã xảy ra lỗi khi mở bài hát: {e}")


def change_wallpaper():
    try:
        api_key = 'your_api_key'
        url = f'https://api.unsplash.com/photos/random?client_id={api_key}'
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        photo = data['urls']['full']
        image_path = "C:/Users/nhiensadboizz/Downloads/a.png"
        urllib2.urlretrieve(photo, image_path)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        speak('Hình nền máy tính vừa được thay đổi')
    except Exception as e:
        speak(f"Lỗi khi thay đổi hình nền: {e}")


def read_news():
    speak("Bạn muốn đọc báo về gì")
    query = get_text()
    api_key = "your_api_key"
    params = {'apiKey': api_key, "q": query}
    api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
    articles = api_result.json().get('articles', [])
    for i, article in enumerate(articles[:3], start=1):
        speak(f"Tin {i}: {article['title']}.")
        webbrowser.open(article['url'])


def tell_me_about(text):
    try:
        search_term = text.split("định nghĩa", 1)[1].strip()
        if not search_term:
            speak("Xin lỗi, bạn chưa cung cấp từ khóa để định nghĩa.")
            return
        speak(f"Tìm kiếm định nghĩa cho {search_term} trên Wikipedia...")
        summary = wikipedia.summary(search_term, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("Có nhiều kết quả cho từ khóa của bạn. Bạn có thể cho tôi biết rõ hơn không?")
    except Exception as e:
        speak(f"Lỗi khi tìm kiếm định nghĩa: {e}")


def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng
    4. Tìm kiếm trên Google
    5. Gửi email
    6. Dự báo thời tiết
    7. Mở video nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Nói cho bạn biết định nghĩa mọi thứ.""")


def get_response(text):
    if not text:
        return
    if "dừng" in text or "tạm biệt" in text or "bye" in text:
        speak("Hẹn gặp lại bạn sau!")
        stop_assistant()  # Gọi hàm tắt giao diện ngay lập tức
        return "exit"  # Trả về tín hiệu để dừng vòng lặp
    elif "chào trợ lý ảo" in text:
        hello()
    elif "có thể làm gì" in text:
        help_me()
    elif "hiện tại" in text:
        get_time(text)
    elif "mở" in text:
        if 'mở google và tìm kiếm' in text:
            open_google_and_search(text)
        elif "trang" in text:
            open_website(text)
        else:
            open_application(text)
    elif "chơi nhạc" in text:
        play_song()
    elif "email" in text or "mail" in text or "gmail" in text:
        send_email(text)
    elif "thời tiết" in text:
        current_weather()
    elif "hình nền" in text:
        change_wallpaper()
    elif "đọc báo" in text:
        read_news()
    elif "định nghĩa" in text:
        tell_me_about(text)
    else:
        speak("Bot không thể trả lời câu hỏi này")


# Biến toàn cục để lưu cửa sổ chính
root_window = None

# Hàm để tắt giao diện và kết thúc ứng dụng
def stop_assistant():
    global root_window
    if root_window:
        root_window.quit()     # Thoát khỏi vòng lặp chính của Tkinter
        root_window.destroy()  # Phá hủy cửa sổ và kết thúc chương trình

def assistant():
    speak("Xin chào, bạn tên là gì nhỉ?")
    name = get_text()
    if name:
        speak(f"Chào bạn {name}")
        speak("Bạn cần Bot Alex có thể giúp gì ạ?")
        while True:
            text = get_text()  # Lắng nghe người dùng
            if not text:
                break
            response = get_response(text)
            if response == "exit":  # Nếu người dùng nói tạm biệt
                break



# Hàm main()
def main():
    assistant()  # Gọi hàm trợ lý ảo


if __name__ == "__main__":
    main()
