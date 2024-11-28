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
from time import strftime
from gtts import gTTS
import os
import tkinter as tk
import webbrowser
import os
from youtube_search import YoutubeSearch
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from openai import OpenAI
import threading
import cohere

# Định nghĩa biến toàn cục
text_widget = None

def set_text_widget(widget):
    global text_widget
    text_widget = widget


wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

print("Vui lòng chạy file app.py")
# Hàm chuyển text sang giọng nói
def speak(text):
    try:
        # Xóa tệp nếu nó đã tồn tại
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")
        print(f"Bot: {text}")   
        tts = gTTS(text=text, lang='vi')
        tts.save("speech.mp3")
        playsound.playsound("speech.mp3")
    except Exception as e:
        print(f"Lỗi khi phát âm: {e}")
# Chuyển đổi âm anh sang văn bản
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(f"{text}")  # In giá trị ghi nhận
            return text
        except sr.UnknownValueError:
            print("... Không nghe rõ.")
            return None
        except sr.RequestError as e:
            print(f"Lỗi kết nối đến Google Speech Recognition service: {e}")
            return None
def stop():
    speak("Hẹn gặp lại bạn sau!")
# Cố gắng thử chuyển đổi 3 lần từ âm thanh sang văn bản
def get_text(): 
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(2)
    stop()
    return 0 
def hello():
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.")
        return "Ch��o buổi sáng bạn {}. Chúc bạn một ngày tốt lành."
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.")
        return "Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa."
    else:
        speak("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.")
        return "Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ."
def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
        return 'Bây giờ là %d giờ %d phút' % (now.hour, now.minute)
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year))
        return "Hôm nay là ngày %d tháng %d năm %d" % (now.day, now.month, now.year)
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")
def open_application(text):
    if "word" in text:
        speak("Mở Microsoft Word")
        os.startfile('C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE')
        return "Mở phần mềm Word"
    elif "excel" in text:
        speak("Mở Microsoft Excel")
        os.startfile('C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE')
        return "Mở phần mềm Excel"
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")
        return "Ứng dụng chưa được cài đặt. Bạn hãy thử lại!"
        
def open_website(command):
    if "google" in command:
        speak("Đang mở Google")
        webbrowser.open("https://www.google.com")
        return "Đang mở trình duyệt Google"
    elif "youtube" in command:
        speak("Đang mở YouTube")
        webbrowser.open("https://www.youtube.com")
        return "Đang mở trang youtube.com"
    else:
        speak("Xin lỗi, tôi không thể mở trang web đó.")
        return "Xin lỗi, tôi không thể mở trang web đó."

def open_google_and_search(text):
    # Tìm kiếm phần sau từ "kiếm"
    search_for = text.split("kiếm", 1)[1].strip()  # loại bỏ khoảng trắng
    if not search_for:  # Kiểm tra nếu không có từ khóa tìm kiếm
        speak("Xin lỗi, bạn chưa cung cấp từ khóa tìm kiếm.")
        return "Xin lỗi, bạn chưa cung cấp từ khóa tìm kiếm."
    
    speak('Đang mở Google và tìm kiếm cho bạn...')

    # Khởi tạo Options cho Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Khởi tạo driver
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("http://www.google.com")
        
        # Tìm kiếm
        que = driver.find_element("name", "q")
        que.send_keys(search_for)
        que.send_keys(Keys.RETURN)
        
        speak("Tìm kiếm đã hoàn tất. Bạn có thể nói 'tắt Google' để tắt trình duyệt.")
        
        # Vòng lặp chờ người dùng yêu cầu tắt Google
        while True:
            command = get_text()  # Hàm này lắng nghe giọng nói của người dùng
            if command and "tắt google" in command.lower():
                speak("Đang tắt Google...")
                driver.quit()  # Đóng trình duyệt
                break
            else:
                speak("Bot đang chờ lệnh tắt Google. Bạn có thể nói 'tắt Google' để đóng trình duyệt.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi mở trình duyệt: {e}")
        speak("Xin lỗi, đã xảy ra lỗi khi mở trình duyệt.")



def send_email(text):
    speak('Bạn gửi email cho ai nhỉ')
    recipient = get_text()
    if 'tuấn' in recipient.lower():
        speak('Nội dung bạn muốn gửi là gì')
        content = get_text()
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('kingofpro1410@gmail.com', 'ypvc gccd fysu cqyp') #Vào trang này mà tạo nhé https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4OCULUaL9Mu5coD8hG6luRej3zx6WWfUsH8pZbZbQv9vBzJ1En1nVOaxRjLy7S6mKXLPRO7djjB2LVooYn9jH9PzkcDOyZgxf3VAMUg-anRWlr9SZ8
        mail.sendmail('kingofpro1410@gmail.com',
                      '2254810197@vaa.edu.vn', content.encode('utf-8'))
        mail.close()
        speak('Email của bạn vùa được gửi. Bạn check lại email nhé hihi.')
        return f"Email người nhận: 2254810197@vaa.edu.vn, nội dung: {content}"
    else:
        speak('Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?')
        return 'Bot không hiểu bạn muốn gửi email cho ai. Bạn nói lại được không?'
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
import webbrowser




def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    mysong = get_text()
    
    if not mysong:
        speak("Bot không nhận được tên bài hát.")
        return "Bot không nhận được tên bài hát."
    
    try:
        results = YoutubeSearch(mysong, max_results=10).to_dict()
        if not results:
            speak("Xin lỗi, không tìm thấy bài hát nào.")
            return "Xin lỗi, không tìm thấy bài hát nào."
        
        video = results[0]
        video_id = video.get('id')
        if not video_id:
            speak("Không tìm thấy video hợp lệ.")
            return "Không tìm thấy video hợp lệ."
        
        url = f'https://www.youtube.com/watch?v={video_id}'
        print(f"URL được tạo: {url}")  # In ra URL để kiểm tra
        
        # Mở URL trên trình duyệt mặc định
        webbrowser.open(url)
        
        speak(f"Đang mở bài hát {mysong} trên YouTube.")
        return f"Đang mở bài hát {mysong} trên YouTube."
    except Exception as e:
        print(f"Đã xảy ra lỗi khi mở bài hát: {e}")
        speak("Xin lỗi, đã xảy ra lỗi khi mở bài hát.")
        return f"Đã xảy ra lỗi khi mở bài hát: {e}"



def change_wallpaper():
    api_key = 'RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw'
    url = 'https://api.unsplash.com/photos/random?client_id=' + \
        api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url)
    json_string = f.read()
    f.close()
    parsed_json = json.loads(json_string)
    photo = parsed_json['urls']['full']
    # Location where we download the image to.
    urllib2.urlretrieve(photo, "C:/Users/nhiensadboizz/Downloads/a.png")
    image=os.path.join("C:/Users/nhiensadboizz/Downloads/a.png")
    ctypes.windll.user32.SystemParametersInfoW(20,0,image,3)
    speak('Hình nền máy tính vừa được thay đổi')
    return 'Hình nền my tính vừa được thay đổi'
def read_news():
    speak("Bạn muốn đọc báo về gì")
    
    queue = get_text()
    params = {
        'apiKey': '30d02d187f7140faacf9ccd27a1441ad',
        "q": queue,
    }
    api_result = requests.get('http://newsapi.org/v2/top-headlines?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"""Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}
    """)
        if number <= 3:
            webbrowser.open(result['url'])
def tell_me_about(text):
    try:
        # Tách từ khóa từ lệnh "định nghĩa"
        search_term = text.split("định nghĩa", 1)[1].strip()
        if not search_term:
            speak("Xin lỗi, bạn chưa cung cấp từ khóa để định nghĩa.")
            return "Xin lỗi, bạn chưa cung cấp từ khóa để định nghĩa."
        
        speak(f"Tìm kiếm định nghĩa cho {search_term} trên Wikipedia...")
        
        
        # Tìm kiếm trên Wikipedia
        contents = wikipedia.summary(search_term).split('\n')
        
        if contents:
            speak(contents[0])  # Đọc nội dung đầu tiên
            return f"{contents[0]}"
        else:
            speak("Xin lỗi, không tìm thấy thông tin.")
        
        time.sleep(10)  # Dừng một chút trước khi hỏi lại

        # Hỏi xem có muốn nghe thêm không
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không?")
            ans = get_text()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(10)

        speak('Cảm ơn bạn đã lắng nghe!!!')
        
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Có nhiều kết quả cho từ khóa của bạn. Bạn có thể cho tôi biết rõ hơn không?")
    except Exception as e:
        speak("Xin lỗi, đã xảy ra lỗi khi truy cập Wikipedia.")
        print(e)  # In lỗi ra console để kiểm tra



def help_me():
    speak("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Gửi email
    6. Dự báo thời tiết
    7. Mở video nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Nói cho bạn biết định nghĩa mọi thứ """)
    return """Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Gửi email
    6. Dự báo thời tiết
    7. Mở video nhạc
    8. Thay đổi hình nền máy tính
    9. Đọc báo hôm nay
    10. Nói cho bạn biết định nghĩa mọi thứ """
    
    
# Khởi tạo OpenAI client cho Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


# Thêm biến toàn cục để lưu lịch sử hội thoại
conversation_history = []

# Initialize Cohere client
co = cohere.Client('ZOQFdWG6N06aCiWwqqtsIcImDlOAv8eBOihK9vdf')  # Replace with your actual API key

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

def ask_gemma(question):
    try:
        global conversation_history
        conversation_history.append({"role": "user", "content": question})
        
        response_stream = client.chat.completions.create(
            model="gemma2:9b",  # hoặc model khác từ Ollama
            messages=conversation_history,
            temperature=0.7,
            max_tokens=2048,
            stream=True
        )

        full_response = ""
        for chunk in response_stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                
                # Hiển thị từng ký tự trong text widget
                if text_widget:
                    text_widget.insert(tk.END, content)
                    text_widget.see(tk.END)
                    text_widget.update()

        # Thêm xuống dòng sau khi hoàn thành
        if text_widget:
            text_widget.insert(tk.END, "\n")
            text_widget.see(tk.END)
            text_widget.update()

        conversation_history.append({"role": "assistant", "content": full_response})
        
        # Giới hạn lịch sử
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]

        # Tạo thread mới để xử lý speech
        threading.Thread(target=speak, args=(full_response,), daemon=True).start()
        
        return full_response
        
    except Exception as e:
        print(f"Error using Ollama: {e}")
        return "Xin lỗi, tôi không thể xử lý câu hỏi này."

# Thêm hàm để xóa lịch sử khi cần
def clear_conversation_history():
    global conversation_history
    conversation_history = []

def get_response(text):
    command_handled = False
    response = None

    if not text:
        return
    elif "dừng" in text or "tạm biệt" in text or "chào tạm biệt" in text or "ngủ thôi" in text:
        stop()
        command_handled = True
    elif "chào trợ lý ảo" in text:
        response = hello()
        command_handled = True
    elif "có thể làm gì" in text:
        response = help_me()
        command_handled = True
    elif "hiện tại" in text:
        response = get_time(text)
        command_handled = True
    elif "mở" in text:
        if 'mở google và tìm kiếm' in text:
            response = open_google_and_search(text)
        elif "trang" in text:
            response = open_website(text)
        else:
            response = open_application(text)
        command_handled = True
    elif "chơi nhạc" in text:
        response = play_song()
        command_handled = True
    elif "email" in text or "mail" in text or "gmail" in text:
        response = send_email(text)
        command_handled = True
    elif "thời tiết" in text:
        response = current_weather()
        command_handled = True
    elif "định nghĩa" in text:
        response = tell_me_about(text)
        command_handled = True
    elif "thay đổi hình nền" in text:
        response = change_wallpaper()   
        command_handled = True

    # If no command was handled, use Cohere
    if not command_handled:
        response = ask_gemma(text)
        return response
            
    return response
    
