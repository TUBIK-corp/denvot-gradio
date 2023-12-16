import os
import edge_tts as tts
from edge_tts import VoicesManager
import asyncio, concurrent.futures
import gradio as gr
from rvc_infer import rvc_convert

import hashlib
from datetime import datetime

def date_to_short_hash():
    current_date = datetime.now()
    date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
    sha256_hash = hashlib.sha256(date_str.encode()).hexdigest()
    short_hash = sha256_hash[:8]
    return short_hash

model = "DenVot.pth"
can_speak = True

voice_instances = []
async def load_voices():
    voicesobj = await VoicesManager.create()
    global voice_instances
    voice_instances = [data["ShortName"] for data in voicesobj.voices]
async def speech(mess, pitch, voice):
    communicate = tts.Communicate(mess, voice)
    i = 0
    file_name = "test"

    await communicate.save("input\\" + file_name)
    output_path = rvc_convert(model_path=os.getcwd() + "\\models\\" + model,
                              input_path="E:\\pyProjects\\denvot-gr\\input\\" + file_name,
                              f0_up_key=pitch)
    os.rename("output\\out.wav", "output\\" + date_to_short_hash() + ".wav")
    os.remove("input\\" + file_name)
    print("DenVot: " + file_name)
    global can_speak
    can_speak = True



def get_last_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None  # No files in the directory

    # Get the most recently created file based on the creation time
    last_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))

    return os.path.join(directory, last_file)

pool = concurrent.futures.ThreadPoolExecutor()
pool.submit(asyncio.run, load_voices()).result()

def makeSpeech(request, pitch, voice):
    global can_speak
    if can_speak is False: return
    can_speak = False
    result = pool.submit(asyncio.run, speech(request, pitch, voice)).result()
    return get_last_file("output")

with gr.Blocks() as grad:
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            # Введите текст для озвучки
            DenVot с радостью озвучит его!
            """)
            print(voice_instances)
            combobox = gr.Dropdown(voice_instances, label="Голос", info="Список всех доступных голосов", value="ru-RU-DmitryNeural")
            request = gr.TextArea(placeholder="Задай свой текст денвотику!!")
            btn = gr.Button()
            btn.label = "Запуск"
            gr.Markdown("""
                Выберите питч для денвотика!
                """)
            slider = gr.Slider()
        with gr.Column():
            gr.Markdown("""
                        # Тут результат
                        DenVot же такой классный!!
                        """)
            out = gr.Audio()
            gr.ClearButton(out)
    request.label = "Текст"
    slider.maximum = 24
    slider.minimum = -24
    slider.value = 12
    slider.label = "Питч"
    btn.click(makeSpeech, inputs=[request, slider, combobox], outputs=out)
grad.launch()

class VoiceInfo:
    def __init__(self, name, short_name, gender, locale, suggested_codec, friendly_name, status, voice_tag, language):
        self.Name = name
        self.ShortName = short_name
        self.Gender = gender
        self.Locale = locale
        self.SuggestedCodec = suggested_codec
        self.FriendlyName = friendly_name
        self.Status = status
        self.VoiceTag = voice_tag
        self.Language = language