import sozluk
import shelve
from copy import deepcopy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty,ObjectProperty
from kivy.uix.screenmanager import ScreenManager,Screen, FadeTransition
from kivy.lang import Builder
from kivmob import KivMob, TestIds
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
import random
class giris_ekrani(Screen):
    def hakkinda(self):
        box=BoxLayout(orientation="vertical")
        box.add_widget(Image(source='nasil-oynanir-page-with-bg.png'))
        popup = Popup(title="{}Tabu Nasıl Oynanır?".format("    "*24), content=box, size_hint=(None, None),
                       size=(self.width,self.height*5/6), separator_color=[1, 1, 1, 0.9],auto_dismiss=False)
        box.add_widget(Button(text="Geri",size_hint=(0.30, 0.1),font_name="font2", pos_hint={"x": 0.325},background_normal="nasil-oynanir-ve-cikis-button.png",on_release=popup.dismiss))
        popup.open()
    def exit(self):
        App.get_running_app().stop()
        Window.close()
class oyun(Screen):
    oyuncu=StringProperty

    progress_bar = ObjectProperty()
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.olustur()
        LabelBase.register(name="font",fn_regular="Font1.ttf")
        LabelBase.register(name="font2",fn_regular="Font2.ttf")
        self.zaman_sesi=SoundLoader.load("zaman.wav")
        self.yanlis_sesi=SoundLoader.load("yanlis.wav")
        self.dogru_sesi=SoundLoader.load("dogru.wav")
        self.pas_sesi=SoundLoader.load("pas.wav")
        self.dogru_sesi.play()
        self.yanlis_sesi.play()
        self.pas_sesi.play()
        self.yanlis_sesi.stop()
        self.dogru_sesi.stop()
        self.pas_sesi.stop()
        self.button=self.ids['start-stop']
        self.kazanma=30
        self.oyuncu="A Takımı"
        self.progress_bar = ProgressBar()
        self.progress_bar.size_hint_x = 0.8
        self.progress_bar.size_hint_y= 0.8
        self.progress_bar.pos_hint= {'x': 0.1,"y":0.44}
        self.progress_bar.max=61
        self.random_sayı=0
        self.sure=61
        self.add_widget(self.progress_bar)
        self.increment_time(0)
        self.zaman_sesi.stop()
        self.giris_bos=True
        self.pas_hakkı=3
        self.sayacA=0
        self.sayacB=0
        self.izin=False

        self.label = Label(text=str("BAŞLAMAK İÇİN"), color=(1,1,1,1),font_name="font", font_size=(50),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.8})
        self.label2 = Label(text=str("BAŞLAT BUTONUNA"), color=(0,1,0,1),font_name="font2", font_size=(40),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.6})
        self.label3 = Label(text=str("BAS, 30 OLAN TAKIM"), color=(0,1,0,1),font_name="font2", font_size=(40),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.5})
        self.label4 = Label(text=str("KAZANIR,SÜRE 60SN"), color=(0,1,0,1),font_name="font2", font_size=(40),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.4})
        self.label5 = Label(text=str("3 PAS HAKKIN VAR"), color=(0,1,0,1),font_name="font2", font_size=(40),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.3})
        self.label6 = Label(text=str("İYİ EĞLENCELER"), color=(0,1,0,1),font_name="font2", font_size=(40),size_hint=(0.2,0.1), pos_hint={"center_x":0.5, "center_y":0.2})

        self.label_sayac=Label(text=str(self.sayacA), color=(1,1,1,1),font_name="font2", font_size=(50),size_hint=(0.3,0.1), pos_hint={"center_x":0.9, "center_y":0.9})
        self.label_oyuncu=Label(text=(self.oyuncu), color=(1,1,1,1),font_name="font", font_size=(50),size_hint=(0.3,0.1), pos_hint={"center_x":0.7, "center_y":0.9})
        self.add_widget(self.label)
        self.add_widget(self.label2)
        self.add_widget(self.label3)
        self.add_widget(self.label4)
        self.add_widget(self.label5)
        self.add_widget(self.label6)
        self.add_widget(self.label_sayac)
        self.add_widget(self.label_oyuncu)
    def olustur(self):
        with shelve.open('test_shelf.db') as s:
            if "control" not in s:
                s["quests"] = deepcopy(sozluk.sozluk)
                self.existing = s["quests"]
                s["control"] = 1
            else:
                self.existing=s["quests"]
    def delete(self):
        with shelve.open('test_shelf.db') as s:
            temp = deepcopy(s["quests"])
            del temp[str(self.random_sayı)]
            s["quests"] = temp
        del self.existing[str(self.random_sayı)]
    def control_database(self):
        with shelve.open('test_shelf.db') as s:
            if self.existing == {}:
                s["quests"] = sozluk.sozluk
                self.existing = s["quests"]

    def kontrol(self):
        if self.oyuncu== ("A Takımı"):
            self.oyuncu="B Takımı"
            self.label_oyuncu.text=self.oyuncu
            self.label_sayac.text=str(self.sayacB)
            self.pas_hakkı=3
            self.progress_bar.value=0
            self.popAc()
            self.soru_getir()
        else:
            self.oyuncu="A Takımı"
            self.label_oyuncu.text=self.oyuncu
            self.label_sayac.text=str(self.sayacA)
            self.progress_bar.value=0
            self.pas_hakkı=3
            self.popAc()
            self.soru_getir()

    def winner_pop(self):
        self.progress_bar.value=0
        self.stop()
        box=BoxLayout(orientation="vertical",spacing=10,padding=30)
        popup2 = Popup(title="{}   TEBRİKLER KAZANDINIZ.".format(self.oyuncu), content=box, size_hint=(None, None),
                       size=(self.width,self.height*5/8), separator_color=[1, 1, 1, 0.9],auto_dismiss=False)
        box.add_widget(Button(background_normal="tekrar-oyna-button-yazili.png", size_hint=(0.80, 1), pos_hint={"x": 0.120}, on_release=self.play_again,on_press=popup2.dismiss))
        box.add_widget(Button(background_normal="menuye-don-button-yazili.png", size_hint=(0.35, 0.75), pos_hint={"x": 0.325}, on_release=self.return_menu,on_press=popup2.dismiss))
        box.add_widget(Label(text="{} Puanınız: {}".format("A Takımı",self.sayacA),font_name="font", size=(self.width,self.height*5/20)))
        box.add_widget(Label(text="{} Puanınız: {}".format("B Takımı",self.sayacB),font_name="font", size=(self.width,self.height*5/20)))
        popup2.open()
    def play_again(self,instance):
        self.oyuncu="A Takımı"
        self.progress_bar.value=0
        self.label.text=str("BAŞLAMAK İÇİN")
        self.label2.text=str("BAŞLAT BUTONUNA")
        self.label3.text=str("BAS, 30 OLAN TAKIM")
        self.label4.text=str("KAZANIR,SÜRE 60SN")
        self.label5.text=str("3 PAS HAKKIN VAR")
        self.label6.text=str("İYİ EĞLENCELER")
        self.pas_hakkı=3
        self.sayacA=0
        self.sayacB=0
        self.giris_bos=True
        self.button.text="BAŞLAT"
        self.label_sayac.text=str(self.sayacA)
        self.izin=False
    def return_menu(self,instance):
        self.manager.current = "giris"
        self.oyuncu="A Takımı"
        self.progress_bar.value=0
        self.label.text=str("BAŞLAMAK İÇİN")
        self.label2.text=str("BAŞLAT BUTONUNA")
        self.label3.text=str("BAS, 30 OLAN TAKIM")
        self.label4.text=str("KAZANIR,SÜRE 60SN")
        self.label5.text=str("3 PAS HAKKIN VAR")
        self.label6.text=str("İYİ EĞLENCELER")
        self.pas_hakkı=3
        self.sayacA=0
        self.sayacB=0
        self.giris_bos=True
        self.button.text="BAŞLAT"
        self.label_sayac.text=str(self.sayacA)
        self.izin=False
    def popAc(self):
        self.button.text="DURDUR"
        box=BoxLayout(orientation="vertical",spacing=10,padding=30)
        popup = Popup(title="{}".format(self.oyuncu), content=box, size_hint=(None, None),
                       size=(self.width,self.height*5/8), separator_color=[1, 1, 1, 0.9],auto_dismiss=False)
        box.add_widget(Button(background_normal="start-button-yazili.png", size_hint=(0.80, 1), pos_hint={"x": 0.120}, on_release=self.progress_bar_start,on_press=popup.dismiss))
        box.add_widget(Button(background_normal="menuye-don-button-yazili.png", size_hint=(0.35, 0.75), pos_hint={"x": 0.325}, on_release=self.return_menu,on_press=popup.dismiss))
        box.add_widget(Label(text="{} Puanınız: {}".format("A Takımı",self.sayacA),font_name="font", size=(self.width,self.height*5/20)))
        box.add_widget(Label(text="{} Puanınız: {}".format("B Takımı",self.sayacB),font_name="font", size=(self.width,self.height*5/20)))
        popup.open()
    def progress_bar_start(self,interval):
        if self.giris_bos==True:
            self.soru_getir()
            self.giris_bos=False
        else:
            pass
        self.increment_time(0)
        self.izin=True
        self.zaman_sesi.stop()
        self.zaman_sesi.play()
        Clock.schedule_interval(self.increment_time, 1)
    def increment_time(self, interval):
        self.progress_bar.value += 1
        if self.progress_bar.value==self.sure:
            self.stop()
            self.kontrol()
    def stop(self):
        self.zaman_sesi.stop()
        self.yanlis_sesi.stop()
        self.dogru_sesi.stop()
        self.pas_sesi.stop()
        Clock.unschedule(self.increment_time)
    def soru_getir(self):
        self.control_database()
        self.random_sayı=random.choice(list(self.existing))
        self.label.text=str(self.existing[str(self.random_sayı)][0])
        self.label2.text=str(self.existing[str(self.random_sayı)][1])
        self.label3.text=str(self.existing[str(self.random_sayı)][2])
        self.label4.text=str(self.existing[str(self.random_sayı)][3])
        self.label5.text=str(self.existing[str(self.random_sayı)][4])
        self.label6.text=str(self.existing[str(self.random_sayı)][5])
        self.delete()
    def kim_kazandi(self):
        if self.sayacA==self.kazanma:
            self.winner_pop()
        elif self.sayacB==self.kazanma:
            self.winner_pop()
        else:
            pass
    def dogru(self):
        if self.izin ==True:
            self.dogru_sesi.stop()
            self.dogru_sesi.play()
            if self.oyuncu=="A Takımı":
                self.sayacA+=1
                self.label_sayac.text=str(self.sayacA)
            else:
                self.sayacB+=1
                self.label_sayac.text=str(self.sayacB)
            self.soru_getir()
            self.kim_kazandi()
        else:
            pass
    def yanlis(self):
        if self.izin ==True:
            self.yanlis_sesi.stop()
            self.yanlis_sesi.play()
            if self.oyuncu=="A Takımı":
                    self.sayacA-=1
                    self.label_sayac.text=str(self.sayacA)
            else:
                self.sayacB-=1
                self.label_sayac.text=str(self.sayacB)
            self.soru_getir()
    def pas(self):
        if self.izin ==True:
            if self.pas_hakkı==3 or self.pas_hakkı==2 or self.pas_hakkı==1:
                self.pas_sesi.stop()
                self.pas_sesi.play()
                self.soru_getir()
                self.pas_hakkı-=1


kv=Builder.load_file("tabusal.kv")
sm = ScreenManager()
sm.add_widget(giris_ekrani(name='giris'))
sm.add_widget(oyun(name='oyun'))
class Game(App):
    def build(self):
        self.ads = KivMob("admobid")
        self.ads.new_interstitial("ca-app-pub-admobid")
        self.ads.request_interstitial()
        return sm
    def show_interstitial(self):
        self.ads.request_interstitial()
        if self.ads.is_interstitial_loaded():
            self.ads.show_interstitial()
    def on_resume(self):
        self.ads.request_interstitial()
    def on_pre_enter(self):
        self.show_interstitial()

if __name__=="__main__":
    Game().run()
