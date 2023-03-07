'''
https://github.com/openai/openai-python
pip install --upgrade openai  v0.27.0

tr-ist.prod.surfshark.com_udp.ovpn
us-stl.prod.surfshark.com_udp.ovpn
us-slc.prod.surfshark.com_udp.ovpn
us-slc.prod.surfshark.com_tcp.ovpn
'''
import openai
openai.api_key = "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"  # supply your API key however you choose1

completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "为什么天空是蓝色的!"}])
print(completion.choices[0].message.content)