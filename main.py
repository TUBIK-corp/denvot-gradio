import os
import edge_tts as tts
from edge_tts import VoicesManager
import asyncio, concurrent.futures
import gradio as gr
from rvc_infer import rvc_convert
import config
import hashlib
from datetime import datetime
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage

def date_to_short_hash():
    current_date = datetime.now()
    date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
    sha256_hash = hashlib.sha256(date_str.encode()).hexdigest()
    short_hash = sha256_hash[:8]
    return short_hash

model = "DenVot.pth"
can_speak = True
voice_instances = []
chat = GigaChat(credentials=config.API_AUTH, verify_ssl_certs=False, model="GigaChat-Pro")

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
                              input_path=os.getcwd() + "\\input\\" + file_name,
                              f0_up_key=pitch)
    os.rename("output\\out.wav", "output\\" + date_to_short_hash() + ".wav")
    os.remove("input\\" + file_name)
    print("DenVot: " + file_name)
    global can_speak
    can_speak = True


messages = list()
messages.append(SystemMessage(content="Ты милый мальчик по имени Денвот, ты любишь отвечать на вопросы! Не перепутай свою роль!"))

def GigaMessage(request):
    global messages
    messages.append(HumanMessage(content=request))
    response = chat(messages)
    messages.pop(1)
    return response

def get_last_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

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

def makeSpeechViaAnswer(question, pitch, voice):
    global can_speak
    if can_speak is False: return
    can_speak = False
    requested = GigaMessage(question).content
    print(requested)
    result = pool.submit(asyncio.run, speech(requested, pitch, voice)).result()
    return get_last_file("output")



with gr.Blocks() as grad:
    with gr.Tab("Озвучка текста"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                # Введите текст для озвучки
                DenVot с радостью озвучит его!
                """)
                print(voice_instances)
                combobox = gr.Dropdown(voice_instances, label="Голос", info="Список всех доступных голосов", value="ru-RU-DmitryNeural")
                request = gr.TextArea(placeholder="Напиши текст для озвучки денвотика!!")
                btn = gr.Button()
                btn.label = "Запуск"
                btn.value = "Запуск"
                gr.Markdown("""
                    Выберите питч для денвотика!
                    """)
                slider = gr.Slider()
            with gr.Column():
                gr.Markdown("""
                            # Тут результат
                            DenVot же такой классный!!
                            """)
                out1 = gr.Audio()
                clear = gr.ClearButton(out1)
                clear.label = "Очистить"
                clear.value = "Очистить"
    with gr.Tab("Вопросы"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("""
                            ### Или же задайте вопрос денвотику
                            DenVot с радостью ответит на него!
                            """)
                question = gr.TextArea(placeholder="Задай свой вопрос денвотику!!")
                quiz = gr.Button()
                quiz.label = "Задать вопрос"
                quiz.value = "Задать вопрос"
                gr.Markdown("""
                            Выберите питч для денвотика!
                            """)
                slider2 = gr.Slider()
            with gr.Column():
                gr.Markdown("""
                            # Тут результат
                            DenVot же такой классный!!
                            """)
                out2 = gr.Audio()
                clear2 = gr.ClearButton(out2)
                clear2.label = "Очистить"
                clear2.value = "Очистить"
    request.label = "Текст"
    slider.maximum = 24
    slider.minimum = -24
    slider.value = 6
    slider.label = "Питч"
    question.label = "Вопрос"
    btn.click(makeSpeech, inputs=[request, slider, combobox], outputs=out1)
    quiz.click(makeSpeechViaAnswer, inputs=[question, slider, combobox], outputs=out2)
grad.title = "Голосовой DenVot"
grad.launch()
