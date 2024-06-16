import gradio as gr
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel

# download internlm2 to the base_path directory using git tool
base_path = './final_model'
os.system(f'git clone https://code.openxlab.org.cn/bob12/MedicalAssistant_internlm-7B.git {base_path}')
embedding_path = './bce-embedding-base_v1'
os.system(f'git clone https://www.modelscope.cn/maple77/bce-embedding-base_v1.git {embedding_path}')
reranker_path = './bce-reranker-base_v1'
os.system(f'git clone https://www.modelscope.cn/maple77/bce-reranker-base_v1.git {reranker_path}')
os.system(f'cd {base_path} && git lfs pull')
os.system(f'cd {embedding_path} && git lfs pull')
os.system(f'cd {reranker_path} && git lfs pull')


import argparse
import json
import time
from multiprocessing import Process, Value

import gradio as gr
import pytoml
from loguru import logger

from huixiangdou.service import ErrorCode, Worker, llm_serve, start_llm_server


def parse_args():
    """Parse args."""
    parser = argparse.ArgumentParser(description='Worker.')
    parser.add_argument('--work_dir',
                        type=str,
                        default='workdir',
                        help='Working directory.')
    parser.add_argument(
        '--config_path',
        default='config.ini',
        type=str,
        help='Worker configuration path. Default value is config.ini')
    parser.add_argument('--standalone',
                        action='store_true',
                        default=True,
                        help='Auto deploy required Hybrid LLM Service.')
    args = parser.parse_args()
    return args


args = parse_args()


def get_reply(query):
    assistant = Worker(work_dir=args.work_dir, config_path=args.config_path)
    code, reply, references = assistant.generate(query=query,
                                                 history=[],
                                                 groupname='')
    ret = dict()
    ret['text'] = str(reply)
    ret['code'] = int(code)
    ret['references'] = references

    return json.dumps(ret, indent=2, ensure_ascii=False)


# start service
if args.standalone is True:
    # hybrid llm serve
    start_llm_server(config_path=args.config_path)

# with gr.Blocks() as demo:
#     with gr.Row():
#         input_question = gr.Textbox(label='输入你的提问')
#         with gr.Column():
#             result = gr.Textbox(label='生成结果')
#             run_button = gr.Button()
#     run_button.click(fn=get_reply, inputs=input_question, outputs=result)





# tokenizer = AutoTokenizer.from_pretrained(base_path,trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(base_path,trust_remote_code=True, torch_dtype=torch.float16).cuda()

assistant = Worker(work_dir=args.work_dir, config_path=args.config_path)
# code, reply, references = assistant.generate(query=query,
#                                                 history=[],
#                                                 groupname='')

def chat(message,history=[]):
    code, reply, references = assistant.generate(query=message,
                                                history=history,
                                                groupname='')
    return reply

gr.ChatInterface(chat,
                 title="MedicalAssistant_internlm",
                description="""
MedicalAssistant_internlm is super Assistant.  
                 """,
                 ).queue(1).launch()