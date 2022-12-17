import customtkinter, pyglet, tensorflow as tf, os, tensorflow_hub as hub, tensorflow_datasets as tfds, math, PIL, winsound, asyncio
from tensorflow.keras import layers

def get_database():
    import pymongo
    Cluster = pymongo.MongoClient("mongodb+srv://ReelReview12345:ReelReview12345@reelreview.im8higz.mongodb.net/?retryWrites=true&w=majority")
    Collection = Cluster["ReelReview"]
    return Collection['Movies']

def updateDatabase(MovieName, field, value):
    db = get_database()
    if db.find_one({'_id':MovieName}) is not None:
        movieData = db.find_one({'_id':MovieName})
        movieData['_id'] = MovieName
        movieData[field] = value
        db.find_one_and_replace({'_id':MovieName}, movieData)
    else:
        movieData = {}
        movieData['_id'] = MovieName
        movieData[field] = value
        print(1)
        db.insert_one(movieData)
        return

def databaseGet(MovieName, field, defaultVal):
    db = get_database()
    if db.find_one({'_id':MovieName}) is not None:
        movieData = db.find_one({'_id':MovieName})
        if not field in movieData.keys():
            movieData['_id'] = MovieName
            movieData[field] = defaultVal
            db.find_one_and_replace({'_id':MovieName}, movieData)
    else:
        movieData = {}
        movieData['_id'] = MovieName
        movieData[field] = defaultVal
        db.insert_one(movieData)
    return movieData[field]

pyglet.font.add_file('poppins-reg.otf')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

physical_devices = tf.config.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(physical_devices[0], True)

xTrain, yTrain = tfds.load(
    name="imdb_reviews",
    split=('train[:60%]', 'train[60%:]'),
    as_supervised=True)

embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)


model = tf.keras.Sequential()
model.add(hub_layer)
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='tanh'))

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005), loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

model = tf.keras.models.load_model('MovieModel/')

# model.fit(xTrain.shuffle(10000).batch(250), epochs=8, validation_data=yTrain.batch(250), verbose=1)

# model.save('MovieModel/')


def getMovieInfo(value):
    if value >= 0:
        dif = math.dist([1], [value])
        if dif > 0.1:
            dif = 0.1
        dif = 0.1 - dif
        dif = 0.1 + dif
        textInput = textbox2.get('0.0', 'end').replace('\n', '')
        current = databaseGet(textInput, "Good", 0)
        updateDatabase(textInput, "Good", current + 1)
        return ["good! You should watch it.", round(dif * 500)]
    else:
        dif = math.dist([-1], [value])
        if dif > 0.05:
            dif = 0.05
        textInput = textbox2.get('0.0', 'end').replace('\n', '')
        current = databaseGet(textInput, "Bad", 0)
        updateDatabase(textInput, "Bad", current + 1)
        return ["bad! Do not watch it.", round(dif * 1000)]


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk(fg_color="#0a0a0a")
app.geometry("800x600")
app.title("MovieAI")

model.predict(["Sample Text"])

def button_callback():
    winsound.Beep(300, 15)
    text = textbox.get("0.0", "end").replace("\n","")
    if text.isspace() or not text:
        outcome.configure(text="Please Enter A Movie Review!")
        outcome.configure(text_color="#d2ecff")
        return
    text2 = textbox.get('0.0', 'end').replace('\n','')
    if text2.isspace() or not text:
        outcome.configure(text="Please Enter A Movie Name!")
        outcome.configure(text_color="#d2ecff")
        return
    textInput = textbox.get('0.0', 'end').replace('\n', '')
    prediction = model.predict([textInput])[0][0]
    info = getMovieInfo(prediction)
    if "bad" in info[0]:
        outcome.configure(text_color="#ffb7b7")
    elif "good" in info[0]:
        outcome.configure(text_color="#a1ffd6")
    def load():
        outcome.configure(text=". . .")
    def done():
        outcome.configure(text=f'The movie was {info[0]} Soggy Tomatoes Rating: {info[1]} / 100.')

    app.after(100, load)
    app.after(250, done)


frame = customtkinter.CTkFrame(master=app,fg_color="#101010")
frame.pack(pady=0,padx=50,fill="both",expand=True)

icon = customtkinter.CTkImage(dark_image=PIL.Image.open("Screenshot 2022-12-14 192900.png"),size=(200,150))
invisLabel = customtkinter.CTkLabel(master=frame,image=icon,text="")
invisLabel.pack(pady=10)

label = customtkinter.CTkLabel(master=frame,text="Should I Watch This Movie?",font=("poppins-reg",40),text_color="#d2ecff")
label.pack(pady=10,padx=10)

label = customtkinter.CTkLabel(master=frame,text="Enter your movie review into the textbox below.",font=("poppins-reg",20),text_color="#d2ecff")
label.pack()

textbox = customtkinter.CTkTextbox(master=frame,width=500,height=200,font=("poppins-reg",15),text_color="#d2ecff")
textbox.pack(pady=30, padx=5)
defaultText = "I loved this movie! The scenes were action packed and enjoyable. One of the best movies I have watched."
textbox.insert("0.0",defaultText)

textbox2 = customtkinter.CTkTextbox(master=frame,width=400,height=20,font=("poppins-reg",15),text_color="#d2ecff")
textbox2.pack(pady=5, padx=1)
defaultText2 = "Avengers: End Game"
textbox.insert("0.0",defaultText)

button = customtkinter.CTkButton(master=frame,text="Read Review",font=("poppins-reg",20),text_color="#d2ecff",fg_color="#181124",corner_radius=75,command=button_callback)
button.pack(pady=10, padx=10)

outcome = customtkinter.CTkLabel(master=frame, text="", font=("poppins-reg", 18),text_color="#d2ecff")
outcome.pack()

app.mainloop()
