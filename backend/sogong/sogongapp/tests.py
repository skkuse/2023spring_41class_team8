from django.test import TestCase
import openai
import gpt_prompts
from API_KEY import OPENAI_API_KEY  
import sqlite3

openai.api_key = OPENAI_API_KEY
# Create your tests here.
def gpt_inference( method,problem_content=None,  testcases=None, answer=None):
    messages = []
    if method == 'feedback':
        prompt = getattr(gpt_prompts, 'GPT_CODE_FEEDBACK')
        prompt = '문제: \n' + problem_content + '\n' + '답변 CODE: \n'+ answer + '\n' + prompt
        messages.append({'role': 'user', 'content': prompt})
    elif method == 'testcase':
        prompt = 'Code: \n' + answer
        tmp_message= ''
        for i in range(4):
            try:
                tmp_message = f'case_input{i+1}: \n' + getattr(testcases, f'case_input{i+1}') + '\n' 
                tmp_message += f'case_output{i+1} : \n' + getattr(testcases, f'case_output{i+1}') +'\n'
            except:
                print(f'{i+1}번째 input case는 존재하지 않습니다.')
        prompt += tmp_message
        prompt += getattr(gpt_prompts, 'GPT_CODE_CHECK')
        messages.append({'role': 'user', 'content': prompt})
    wait = 1
    while True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                temperature=1.0,
                messages=messages
            )
            content = [response['choices'][i]['message']['content'] for i in range(1)]
            return content
        except openai.error.RateLimitError:
            print('openai.error.RateLimitError')
            import time
            time.sleep(min(wait, 60))
        except openai.error.ServiceUnavailableError:
            print('openai.error.ServiceUnavailableError')
            import time
            time.sleep(min(wait, 60))
        except openai.error.InvalidRequestError:
            print('openai.error.InvalidRequestError')
            import time
            time.sleep(min(wait, 60))
        except openai.error.APIError:
            print('openai.error.APIError')
            import time
            time.sleep(min(wait, 60))
        except openai.error.APIConnectionError:
            print('openai.error.APIConnectionError')
            import time
            time.sleep(min(wait, 60))    

def get_feedback(problem_content, user_submission):
    #!---피드백을 지피티로부터 받아서 피드백을 리턴---!
    response = gpt_inference('feedback',problem_content, answer= user_submission)
    return response