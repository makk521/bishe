'''
https://github.com/openai/openai-python
pip install --upgrade openai  v0.27.0

tr-ist.prod.surfshark.com_udp.ovpn
us-stl.prod.surfshark.com_udp.ovpn
us-slc.prod.surfshark.com_udp.ovpn
us-slc.prod.surfshark.com_tcp.ovpn
'''
import openai
def ask_gpt(prompt):
    '''
    chatgpt的api调用。
    参数:问题
    返回:问题结果
    '''
    openai.api_key = "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"  
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

if __name__ == '__main__':
    print(ask_gpt('上海今天天气怎么样'))