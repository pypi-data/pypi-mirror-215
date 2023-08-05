import json
import boto3
import ipywidgets as widgets
from IPython.display import display
from pyspark.sql import SparkSession


class Model:
    def __init__(self, user_name: str = '', password: str = '', end_point: str = '', max_new_tokens: int = 200):
        self.end_point = end_point
        self.prompt = None
        self.result = None
        self.cleaned_code = ''
        self.response = None
        self.max_new_tokens = max_new_tokens

        self.client = boto3.client(
            'sagemaker-runtime',
            aws_access_key_id=user_name,
            aws_secret_access_key=password,
            region_name='us-west-2'
        )

    def code(self):
        self.cleaned_code = self.response.replace(self.prompt, '').strip()
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
                    "stop": ["<|endoftext|>"]
                }
            }

            response = self.client.invoke_endpoint(
                EndpointName=self.end_point,
                ContentType='application/json',
                Body=json.dumps(payload)
            )

            self.response = json.loads(response['Body'].read())[0]['generated_text']
            print(self.response)

        if prompt:
            self.prompt = prompt
            submit_request(self.prompt)
        else:
            textarea_bg = widgets.Textarea(description='Provide any necessary background:', layout=widgets.Layout(width='80%', height='200px'),
                                           style={'description_width': 'initial'})
            input_text = widgets.Text(description='What SQL are you looking for:', layout=widgets.Layout(width='80%'), style={'description_width': 'initial'})
            button = widgets.Button(description='Submit')
            display(textarea_bg)
            display(input_text)
            display(button)

            # Define button click event
            def submit_button(b):
                prompt = f"Given this background:\n\"{textarea_bg.value}\"\n\nAnswer this question: \"{input_text.value}\""
                self.prompt = prompt
                submit_request(prompt)

            # Bind button click event to function
            button.on_click(submit_button)
