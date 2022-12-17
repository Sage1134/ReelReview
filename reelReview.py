import math, winsound, pyglet, customtkinter
from mongo import *
from tensorModel import loadModel
from PIL import Image

pyglet.font.add_file('poppins-reg.otf')

model = loadModel()
model.predict(["Test Line. Do Not Remove"])

def getMovieInfo(value, movieName):
    if value >= 0:
        dif = math.dist([1], [value])
        if dif > 0.1:
            dif = 0.1
        dif = 0.1 - dif
        dif = 0.1 + dif
        asyncio.run(updateMovieInfo(movieName, "Good", 0))
        return ["good! You should watch it.", round(dif * 500)]
    else:
        dif = math.dist([-1], [value])
        if dif > 0.05:
            dif = 0.05
        asyncio.run(updateMovieInfo(movieName, "Bad", 0))
        return ["bad! Do not watch it.", round(dif * 1000)]

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title = ("Reel Review")
        self.fg_color = "#0a0a0a"
        self.geometry("1000x800")
        self.minsize(400, 300)
        self.page = True
        self.pgONE()

    def pgONE(self):
        self.clear(self)
        self.frame = customtkinter.CTkFrame(master=self,fg_color="#1f2130",bg_color="#1f2130")
        self._set_appearance_mode("dark")
        self.icon = customtkinter.CTkImage(dark_image=Image.open("Logo.png"), size=(100, 100))
        self.invisLabel = customtkinter.CTkLabel(master=self.frame, image=self.icon, text="")
        self.label = customtkinter.CTkLabel(master=self.frame, text="Reel Review", font=("poppins-reg", 40),text_color="#d2ecff")
        self.label2 = customtkinter.CTkLabel(master=self.frame, text="Enter A Movie Review Below",font=("poppins-reg", 20), text_color="#d2ecff")
        self.textbox = customtkinter.CTkTextbox(master=self.frame, width=500, height=200, font=("poppins-reg", 15),text_color="#d2ecff",fg_color="#313345")
        self.textbox.insert("0.0", "I really enjoyed this movie! The scenes were so exciting and filled with action.")
        self.label3 = customtkinter.CTkLabel(master=self.frame, text="Enter The Movie Name Below",font=("poppins-reg", 20), text_color="#d2ecff")
        self.textbox2 = customtkinter.CTkTextbox(master=self.frame, width=400, height=25, font=("poppins-reg", 15),text_color="#d2ecff", fg_color="#313345")
        self.textbox2.insert("0.0", "Avengers: End Game")
        self.button = customtkinter.CTkButton(master=self.frame, text="Read Review", font=("poppins-reg", 20),text_color="#181124", fg_color="#3cadff", corner_radius=75,command=self.readReview)
        self.cycle = customtkinter.CTkButton(master=self.frame, text=">>", font=("poppins-reg", 20), text_color="#181124",fg_color="#3cadff", corner_radius=75,command=self.toggle)
        self.outcome = customtkinter.CTkLabel(master=self.frame, text="", font=("poppins-reg", 18),text_color="#a1ffd6")  # a1ffd6 good, ffb7b7 bad

        self.cycle.pack(pady=10,padx=10,anchor="ne")
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.invisLabel.pack(pady=10)
        self.label.pack(pady=10, padx=10)
        self.label2.pack()
        self.textbox.pack(pady=10, padx=10)
        self.label3.pack(pady=30,padx=10)
        self.textbox2.pack(pady=10, padx=10)
        self.button.pack(pady=10, padx=10)
        self.outcome.pack()

    def pgTWO(self):
        self.clear(self)

        self.frame = customtkinter.CTkFrame(master=self, fg_color="#1f2130",bg_color="#1f2130")
        self._set_appearance_mode("dark")
        self.icon = customtkinter.CTkImage(dark_image=Image.open("Logo.png"), size=(100, 100))
        self.invisLabel = customtkinter.CTkLabel(master=self.frame, image=self.icon, text="")
        self.label = customtkinter.CTkLabel(master=self.frame, text="Reel Review: Movie Lookup", font=("poppins-reg", 40),text_color="#d2ecff")
        self.label2 = customtkinter.CTkLabel(master=self.frame,text="Enter A Movie Name Below",font=("poppins-reg", 20), text_color="#d2ecff")
        self.textbox = customtkinter.CTkTextbox(master=self.frame, width=500, height=100, font=("poppins-reg", 15),text_color="#d2ecff",fg_color="#313345")
        self.textbox.insert("0.0", "Avengers: End Game")
        self.button = customtkinter.CTkButton(master=self.frame, text="Search Database", font=("poppins-reg", 20),text_color="#181124", fg_color="#3cadff", corner_radius=75,command=self.lookupMovie)
        self.cycle = customtkinter.CTkButton(master=self.frame, text="<<", font=("poppins-reg", 20),text_color="#181124", fg_color="#3cadff", corner_radius=75,command=self.toggle)
        self.outcome = customtkinter.CTkLabel(master=self.frame, text="", font=("poppins-reg", 18),text_color="#a1ffd6")  # a1ffd6 good, ffb7b7 bad

        self.cycle.pack(pady=10, padx=10, anchor="nw")
        self.frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.invisLabel.pack(pady=20)
        self.label.pack(pady=20, padx=20)
        self.label2.pack()
        self.textbox.pack(pady=50, padx=10)
        self.button.pack(pady=10, padx=10)
        self.outcome.pack()

    def readReview(self):
        winsound.Beep(300, 15)
        text = self.textbox.get("0.0", "end").replace("\n", "")
        if text.isspace() or not text:
            self.outcome.configure(text="Please Enter A Movie Review!")
            self.outcome.configure(text_color="#d2ecff")
            return
        text2 = self.textbox2.get("0.0", "end").replace("\n", "")
        if text2.isspace() or not text:
            self.outcome.configure(text="Please Enter A Movie Name!")
            self.outcome.configure(text_color="#d2ecff")
            return
        self.outcome.configure(text="")
        self.outcome.configure(text_color="#a1ffd6")

        def load():
            self.outcome.configure(text=". . .")

        def done():
            prediction = model.predict([text])[0][0]
            info = getMovieInfo(prediction, text2)
            if "bad" in info[0]:
                self.outcome.configure(text_color="#ffb7b7")
            elif "good" in info[0]:
                self.outcome.configure(text_color="#a1ffd6")
            self.outcome.configure(text=f'The movie was {info[0]} Soggy Tomatoes Rating: {info[1]} / 100.')

        self.after(10, load)
        self.after(20, done)

    def lookupMovie(self):
        winsound.Beep(300, 15)
        text = self.textbox.get("0.0", "end").replace("\n", "")
        if text.isspace() or not text:
            self.outcome.configure(text="Please Enter A Movie Name!")
            self.outcome.configure(text_color="#d2ecff")
            return
        self.outcome.configure(text="")
        self.outcome.configure(text_color="#a1ffd6")

        def load():
            self.outcome.configure(text=". . .")

        def done():
            info = searchDatabase(text, 0)
            total = info[0] + info[1]
            self.outcome.configure(text=f'{text} Has {info[0]} Good Reviews And {info[1]} Bad Reviews. This Is A {round((info[0] / total) * 100)}% Positive Feedback Rate!')

        self.after(10, load)
        self.after(20, done)

    def clear(self, target):
        for widget in target.winfo_children():
            widget.destroy()

    def toggle(self):
        self.page = not self.page
        if self.page:
            self.pgONE()
        else:
            self.pgTWO()

app = App()
app.mainloop()