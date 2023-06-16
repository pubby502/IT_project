import speech
import serial
import os
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

def ConnectRelay(PORT="COM3"):
 try:
  master = modbus_rtu.RtuMaster(serial.Serial(port=PORT, baudrate=9600, bytesize=8, parity='E', stopbits=1))
  master.set_timeout(5.0)
  master.set_verbose(True)
# 读输入寄存器
# c2s03 设备默认 slave=2, 起始地址=0, 输入寄存器个数 2
  master.execute(2, cst.READ_INPUT_REGISTERS, 0, 2)
# 读保持寄存器
# c2s03 设备默认 slave=2, 起始地址=0, 保持寄存器个数 1
  master.execute(2, cst.READ_HOLDING_REGISTERS, 0, 1)
# 这里可以修改
#需要读取的功能码
# 没有报错，返回 1
  response_code = 1
 except Exception as exc:
  print(str(exc))
# 报错，返回<0 并输出错误
  response_code = -1
  master = None

 return  response_code, master


def Switch(master, ACTION):
 """
 此函数为控制继电器开合函数，如果 ACTION=ON 则闭合，如果如果 ACTION=OFF 则断开。
 :param master: 485 主机对象，由 ConnectRelay 产生
 :param ACTION: ON 继电器闭合，开启风扇；OFF 继电器断开，关闭风扇。
 :return: >0 操作成功，<0 操作失败
    # 写单个线圈，状态常量为 0xFF00，请求线圈接通
     # c2s03 设备默认 slave=2, 线圈地址=0, 请求线圈接通即 output_value 不22 等于 0
      # 写单个线圈，状态常量为 0x0000，请求线圈断开
 # c2s03 设备默认 slave=2, 线圈地址=0, 请求线圈断开即 output_value 等
于 0
 # 没有报错，返回 1
  # 报错，返回<0 并输出错误
 """
 try:
     if "on" in ACTION.lower():
         master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=1)
     else:
         master.execute(2, cst.WRITE_SINGLE_COIL, 0, output_value=0)
         response_code = 1
 except Exception as exc:
         print(str(exc))
 response_code = -1
 return response_code


import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import webbrowser

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'

base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "1Rx8Vr0YDiZmANl05PPfGMrl"  # 填写自己的APIKey
SecretKey = "d77fI2h04j6A3EITtGD3Pu3ztyqtGpY9"  # 填写自己的SecretKey

HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # count = 0
    t = time.time()
    print('正在录音...')

    while time.time() < t + 4:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)
    print('录音结束.')
    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    # r=requests.post(url,data=json.dumps(data),headers=headers)
    print('正在识别...')
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


def openbrowser(text):
    maps = {
        '开': ['开。', '想开风扇。','开开开。','快开吧你。','热死了。'],
        '关': ['不。', '关掉。','好冷。'],
    }
    if text in maps['开']:
        print(1111111)
        # speech.say("现在为您开风扇")

        start = time.time()
        os.system('y.mp3')
        i = 0
        while time.time() < start + 5:
            i = i + 1
        Switch(master, "on")

    elif text in maps['关']:
        os.system( 'n.mp3')
        # speech.say("现在为您关风扇")
        start = time.time()
        os.system('n.mp3')
        i = 0
        while time.time() < start + 5:
            i = i + 1
        Switch(master, "off")
    else:
        print(222222)
        start = time.time()
        os.system('o.mp3')
        i = 0
        while time.time() < start + 5:
            i = i + 1

if __name__ == '__main__':
    flag = 'y'
    code, master = ConnectRelay("COM3")
    while flag.lower() == 'y':
        # speech.say(string)
        # time(3000)
        start = time.time()
        os.system('q.mp3')
        i=0
        while time.time()<start+3:
             i=i+1

        my_record()
        TOKEN = getToken(HOST)
        speech = get_audio(FILEPATH)
        result = speech2text(speech, TOKEN, int(1537))
        print(result)
        if type(result) == str:
            openbrowser(result.strip('，'))
        flag = input('Continue?(y/n):')