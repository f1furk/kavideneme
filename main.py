from gtts import gTTS
import pygame
import os
import speech_recognition as sr
import webbrowser
import datetime
from bs4 import BeautifulSoup
from pytube import YouTube
import threading

pygame.init()

def speak(text):
    tts = gTTS(text=text, lang='tr')
    tts.save("output.mp3")
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    os.remove("output.mp3")

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def play_music(song):
    speak(f"{song} şarkısını çalıyorum.")
    try:
        query = f"{song} official audio"
        url = f"https://www.youtube.com/results?search_query={query}"
        soup = BeautifulSoup(webbrowser.get().open(url), "html.parser")
        video_link = soup.find("a", {"class": "yt-uix-tile-link"})["href"]
        
        video_url = f"https://www.youtube.com{video_link}"
        YouTube(video_url).streams.get_audio_only().download()
        
        speak("Şarkı çalınıyor. Keyifli dinlemeler!")
    except Exception as e:
        speak("Bir hata oluştu. Şarkı çalınırken bir problem oluştu.")
        print(e)

def read_news(category):
    speak(f"{category} haberlerini getiriyorum.")
    try:
        url = f"https://news.google.com.tr/rss/category/{category}"
        soup = BeautifulSoup(webbrowser.get().open(url), "html.parser")
        news_titles = [item.text for item in soup.find_all("title")[1:6]]
        
        speak("İşte en güncel haber başlıkları:")
        for title in news_titles:
            speak(title)
    except Exception as e:
        speak("Bir hata oluştu. Haber başlıkları getirilirken bir problem oluştu.")
        print(e)

def set_reminder(reminder_time):
    try:
        scheduled_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        current_time = datetime.datetime.now()
        time_difference = (scheduled_time - current_time).seconds

        if time_difference > 0:
            speak(f"{reminder_time} tarihinde hatırlatıcı kuruldu. İyi günler dilerim!")
            threading.Timer(time_difference, lambda: speak(f"Hatırlatıcı! {reminder_time} geldi!")).start()
        else:
            speak("Geçmiş bir tarihe hatırlatıcı ekleyemezsiniz. Lütfen geçerli bir tarih belirtin.")
    except ValueError:
        speak("Geçersiz tarih veya saat formatı. Lütfen doğru bir format kullanın (YYYY-MM-DD HH:mm).")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Sizi dinliyorum, lütfen konuşun.")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="tr-TR")
            print("Söylenen: {}".format(text))
            return text.lower()
        except sr.UnknownValueError:
            print("Anlayamadım.")
            return None
        except sr.RequestError as e:
            print("Ses tanıma servisine ulaşılamıyor; {0}".format(e))
            return None

def main():
    speak("Merhaba! Size nasıl yardımcı olabilirim?")

    while True:
        command = listen()

        if command:
            if "müzik çal" in command:
                speak("Hangi şarkıyı çalmamı istersiniz?")
                song = listen()
                play_music(song)
            elif "haberleri getir" in command:
                speak("Hangi kategorideki haberleri getirmemi istersiniz? Örneğin, 'spor' veya 'teknoloji'.")
                category = listen()
                read_news(category)
            elif "hatırlatıcı ekle" in command:
                speak("Hatırlatıcı eklemek için tarih ve saati belirtin. Örneğin, '2023-12-31 15:00'.")
                reminder_time = listen()
                set_reminder(reminder_time)
            elif "güle güle" in command:
                speak("Güle güle! İyi günler dilerim.")
                break
            else:
                speak("Anlayamadım. Lütfen tekrar edin.")

if __name__ == "__main__":
    main()
