'''
执行脚本将输出导入变量
'''
import subprocess

# 所要识别的目标文件已经写进shell脚本中
def voice_to_text_sherpnn():
    result = subprocess.check_output('/home/pi/Desktop/bishe/voice_recongnize_local/recongnize_file.sh',shell=True)
    return result.decode('utf-8').split('\n')[-4]

if __name__ == '__main__':
    print(voice_to_text_sherpnn())