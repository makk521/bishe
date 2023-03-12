# encoding:utf-8
import requests
import json
import urllib
import urllib.request
import time
import struct
import pyaudio
import pvporcupine
import wave
# import speech_recognition as sr
from aip import AipSpeech



APP_ID = '24690625'
API_KEY = '4wvprFyDikit7dGDmr3qMVW1'
SECRET_KEY = 'xGZ3AyezrZpncTYnTaXdoONVWfvKB3op'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
url = 'https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token=24.3666976f79d1b2fa4394975b9220df55.2592000.1680009411.282335-29476996' # token id
headers = {'content-type': 'application/x-www-form-urlencoded'}
access_key = "c7E0vdPeiP6qg4pXo/AdHrMq9a6UFx6qczLYex7g0qKwmFkJm0UEmQ==" #porcupine
porcupine = pvporcupine.create( access_key=access_key,keywords=['porcupine', 'ok google', "picovoice", "blueberry"])
framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=5

def save_wave_file(filename,data):
    '''save the data to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()
# 直接调本函数即可录制时长为TIME的音频output.wav
def my_record():
    pa=pyaudio.PyAudio()
    stream=pa.open(format = pyaudio.paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while count<TIME*8:   # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count+=1
        print('.',end="")
    save_wave_file('output.wav',my_buf)
    stream.close()

# 直接调取麦克风权限录音5秒，返回识别结果
# def voice_to_speech_google():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio_data = r.record(source, duration=5)
#         print("Recognizing...")
#         question = r.recognize_google(audio_data,language="zh-cn")
#     return question
#     print(question)

# 输出音频识别结果(字符串)
def voice_to_text_baidu_sdk(filePath):
    with open(filePath, 'rb') as fp:
    # 识别本地文件
        result = client.asr(fp.read(), 'pcm', 16000, {
            'dev_pid': 1537,
        })
        end = time.time()
        # print(result.get('result')[0])
        try:
            return result.get('result')[0]
        except TypeError:
            return ' '
        
# 输入为字符串，输出为问题答案
def chat_unit(QUESTION):   
    post_data = "{\"version\":\"3.0\",\"service_id\":\"S80122\",\"session_id\":\"\",\"log_id\":\"1114749\",\"request\":{\"terminal_id\":\"88888\",\"query\":\"" + QUESTION +"\"}} "
    response = requests.post(url, data=post_data.encode('utf-8'), headers=headers)
    answer = json.loads(response.text)
    return answer
    # print(answer['result']['responses'][0]['actions'][0]['say'])

def chat_own_think(Question):
    temp = requests.get('https://api.ownthink.com/bot?spoken=' + Question)
    answer = temp.text
    answer = json.loads(answer)
    return answer['data']['info']['text']


# porcupine = pvporcupine.create(keyword_paths=['samel__en_windows_2021-10-26-utc_v1_9_0.ppn'])
pa = pyaudio.PyAudio()
audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)


while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        print("收到,请讲话：")
        my_record()
        question = voice_to_text_baidu_sdk('output.wav')
        
        print(question)
        
        try:
            print(chat_unit(question)['result']['responses'][0]['actions'][0]['say'])
        except KeyError:
            print("请提问！")
        except TypeError:
            print("请提问！")

        
        
# try:
#   print(chat_unit(' ')['result']['responses'][0]['actions'][0]['say'])
# except KeyError:
#   print("请提问！")
# except TypeError:
#   print("请提问！")
  
