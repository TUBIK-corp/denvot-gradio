# Гайд по установке:
1) Установите [Python 3.10](https://www.python.org/downloads/)
2) Установите [git](https://git-scm.com/downloads)
3) Установите [ffmpeg](https://ffmpeg.org/download.html)
4) Скачиваем denvot-gradio репозиторий:
   ```
   git clone https://github.com/TUBIK-corp/gradio
   cd .\denvot-gradio\
   ```
5) Создаём venv:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```
   Если вы используете Windows и получаете ошибку

   ```"cannot be loaded because the execution of scripts is disabled on this system"```
   
   То откройте PowerShell от имени администратора и запустите следующее:
   ```
   Set-ExecutionPolicy RemoteSigned
   A
   ```
6) Скачайте файлы [hubert_base.pt](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt) и [rmvpe.pt](https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt), и поместите их в репозиторий
7) Установите все оставшиеся необходимые библиотеки:   
    ```
    pip install -r requirements.txt
    ```
8) Запустите своего денвотика для озвучки текста:
   ```
   python main.py
   ```
10)
