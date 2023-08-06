import json
import boto3
from pyspark.sql import SparkSession
import pillar1.constants as cn
import requests


class MODELS:
    STARCODERPLUS = 'starcoderplus'
    STARCHAT_BETA = 'starchat-beta'
    FALCON_40B_INSTRUCT = 'f40b-instruct'


MODELS_META = {
    'f40b-instruct': {
        'stop_token': '<|endoftext|>'
    },
    'starcoderplus': {
        'free': {
            'prepend': 'Given this `claims` table description:',
            'append': '',
            'stop_token': '<|end|>',
            'API_URL': 'https://api-inference.huggingface.co/models/bigcode/starcoderplus',
            'replaces': {'': '', }
        }
    },
    'starchat-beta': {
        'free': {
            'prepend': '<|user|>Given this `claims` table description:',
            'append': '<|end|>',
            'stop_token': '<|end|>',
            'API_URL': 'https://api-inference.huggingface.co/models/HuggingFaceH4/starchat-beta',
            'replaces': {'': '', }
        }
    }
}


class Model:
    def __init__(self, user_name: str = '', password: str = '', end_point: str = '', max_new_tokens: int = 100, verbose: bool = False, api_type: str = 'free',
                 huggingface_token='', background: str = '', temperature: float = .1, do_sample: bool = True):
        self.do_sample = do_sample
        self.temperature = temperature
        self.end_point = end_point
        self.prompt = None
        self.result = None
        self.huggingface_token = huggingface_token
        self.cleaned_code = ''
        self.response = None
        self.max_new_tokens = max_new_tokens
        self.verbose = verbose
        self.curr_model = MODELS_META[end_point][api_type]
        self.api_type = api_type
        if not background:
            self.background = cn.STARCODER_BETA
        else:
            self.background = background

        if self.api_type == 'hosted':
            self.client = boto3.client(
                'sagemaker-runtime',
                aws_access_key_id=user_name,
                aws_secret_access_key=password,
                region_name='us-west-2'
            )

    def code(self):
        self.cleaned_code = self.response.replace(self.prompt, '').strip()
        ELS_TO_REMOVE = ['<pre>', '<code>', '</code>', '</pre>']
        for curr_el_to_remove in ELS_TO_REMOVE:
            self.cleaned_code = self.cleaned_code.replace(curr_el_to_remove, '')

        # self.cleaned_code = self.cleaned_code.split('<|assistant|>')[1].split('<|end|>')[0].strip().replace(' claim_item;', ' uc_beesbridge.abacus.claim_item;').replace(
        #    ' claim_item ',
        #    ' uc_beesbridge.abacus.claim_item ').replace(
        #    ' claim_item\n', ' uc_beesbridge.abacus.claim_item\n')

        self.cleaned_code = self.cleaned_code.strip()
        print(self.cleaned_code)

    def execute(self):
        spark = SparkSession.builder.getOrCreate()
        self.result = spark.sql(self.cleaned_code)
        return self.result

    def query(self, prompt: str = ''):
        def submit_request(prompt):
            payload = {
                'inputs': prompt,
                "parameters": {
                    "do_sample": self.do_sample,
                    "top_p": 0.7,
                    "temperature": self.temperature,
                    "top_k": 50,
                    "max_new_tokens": self.max_new_tokens,
                    "repetition_penalty": 1.03,
                    "stop": [self.curr_model['stop_token']]
                }
            }

            if self.verbose:
                print(f"Submit payload: {payload}")

            if self.api_type == "hosted":
                response = self.client.invoke_endpoint(
                    EndpointName=self.end_point,
                    ContentType='application/json',
                    Body=json.dumps(payload)
                )
                self.response = json.loads(response['Body'].read())[0]['generated_text']
                self.code()

            if self.api_type == 'free':
                response = requests.post(self.curr_model['API_URL'], headers={"Authorization": f"Bearer {self.huggingface_token}"}, json=payload)
                self.response = response.json()[0]['generated_text']
                return self.response

        if prompt:
            prompt = f"{self.curr_model['prepend']}{self.background}{prompt}{self.curr_model['append']}"
            self.prompt = prompt
            submit_request(self.prompt)

        else:
            question = input('What SQL are you looking for: ')
            prompt = f"{self.curr_model['prepend']}:\n\"{self.background}\"\n\nAnswer this question: {question}\" {self.curr_model['append']}"
            self.prompt = prompt
            submit_request(self.prompt)

            # input_text = widgets.Text(description='What SQL are you looking for:', layout=widgets.Layout(width='80%'), style={'description_width': 'initial'})
            # button = widgets.Button(description='Submit')
            # # display(textarea_bg)
            # display(input_text)
            # display(button)
            #
            # # Define button click event
            # def submit_button(b):
            #     prompt = f"{MODELS_META[self.end_point].get('prepend', '')}Given this background:\n\"{MODELS_META[self.end_point].get('context', '')}\"\n\nAnswer this
            #             #     question: " \
            #             #              f"\"{input_text.value}\" {MODELS_META[self.end_point].get('append', '')}"
            #     submit_request(prompt)
            #
            # # Bind button click event to function
            # button.on_click(submit_button)
