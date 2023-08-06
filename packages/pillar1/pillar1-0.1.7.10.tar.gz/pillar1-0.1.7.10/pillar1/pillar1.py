import json
import boto3
import ipywidgets as widgets
from IPython.display import display
from pyspark.sql import SparkSession
import pillar1.constants as cn

MODELS_META = {
    'pillar1-f40b-instruct': {
        'context': '',
        'stop_token': '<|endoftext|>'
    },
    'starcoder-beta': {
        'context': cn.STARCODER_BETA,
        'prepend': '<|user|>',
        'append': '(only return DataBricks-compatible SQL code)<|end|>',
        'stop_token': '<|end|>',
        'replaces': {'': '', }
    }
}


class Model:
    def __init__(self, user_name: str = '', password: str = '', end_point: str = '', max_new_tokens: int = 100, verbose: bool = False):
        self.end_point = end_point
        self.prompt = None
        self.result = None
        self.cleaned_code = ''
        self.response = None
        self.max_new_tokens = max_new_tokens
        self.verbose = verbose

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

        self.cleaned_code = self.cleaned_code.split('<|assistant|>')[1].split('<|end|>')[0].strip().replace(' claims;', ' uc_beesbridge.abacus.claims;').replace(' claims ',
                                                                                                                                                                 ' uc_beesbridge.abacus.claims ').replace(
            ' claims\n', ' uc_beesbridge.abacus.claims\n')
        self.cleaned_code = self.cleaned_code.strip()
        print(self.cleaned_code)

    def execute(self):
        spark = SparkSession.builder.getOrCreate()
        self.result = spark.sql(self.cleaned_code)
        self.result.show()

    def query(self, prompt: str = ''):
        def submit_request(prompt):
            payload = {
                'inputs': prompt,
                "parameters": {
                    "do_sample": True,
                    "top_p": 0.7,
                    "temperature": 0.7,
                    "top_k": 50,
                    "max_new_tokens": self.max_new_tokens,
                    "repetition_penalty": 1.03,
                    "stop": [MODELS_META[self.end_point].get('stop_token')]
                }
            }

            if self.verbose:
                print(f"Submit payload: {payload}")

            response = self.client.invoke_endpoint(
                EndpointName=self.end_point,
                ContentType='application/json',
                Body=json.dumps(payload)
            )

            self.response = json.loads(response['Body'].read())[0]['generated_text']
            self.code()

        if prompt:
            self.prompt = prompt
            submit_request(self.prompt)
        else:
            # textarea_bg = widgets.Textarea(description='Provide any necessary background:', layout=widgets.Layout(width='80%', height='200px'),
            #                                style={'description_width': 'initial'})

            question = input('What SQL are you looking for: ')
            prompt = f"{MODELS_META[self.end_point].get('prepend', '')}Given this background:" \
                     f"\n\"{MODELS_META[self.end_point].get('context', '')}\"\n\nAnswer this question: " \
                     f"\"{question}\" {MODELS_META[self.end_point].get('append', '')}"
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
