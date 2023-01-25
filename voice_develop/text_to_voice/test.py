import pyttsx3
 
engine = pyttsx3.init() #创建engine并初始化
engine.say('有志者，事竟成。') #开始朗读
engine.runAndWait() #等待语音播报完毕
