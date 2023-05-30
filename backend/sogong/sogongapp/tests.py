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
        try:
            tmp_message= ''
            for i in range(4):
                if getattr(testcases, f'case_input{i+1}') == 'None': break
                tmp_message += f'case_input{i+1}: \n' + getattr(testcases, f'case_input{i+1}') + '\n' 
                tmp_message += f'case_output{i+1} : \n' + getattr(testcases, f'case_output{i+1}') +'\n'
        except:
            print(f'\ntestcase 개수 부족: \n {i+1}번째 input case는 존재하지 않습니다.\n')
        prompt += tmp_message
        prompt += getattr(gpt_prompts, 'GPT_CODE_CHECK')
        messages.append({'role': 'user', 'content': prompt})
    elif method == 'getanswer':
        prompt = getattr(gpt_prompts, 'GPT_GETANSWER')
        messages.append({'role':'user', 'content':problem_content+prompt})

    wait = 1
    while True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                temperature=1.0,
                messages=messages
            )
            print(response)
            content = response['choices'][0]['message']['content']
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
def get_gpt_answer(problem_text, problem_input, problem_output):
    #!---GPT에게 넘겨주어야 할 것은 문제 텍스트, 문제의 입력값 예시, 문제의 출력값 예시---!
    problem = '문제: \n' + problem_text + '\n입력: \n' + problem_input + '\n출력: \n' + problem_output
    answer = gpt_inference('getanswer', problem_content=problem)
    #!---GPT로 부터 받아온 코드를 answer에 넣고 answer를 반환
    return answer
def answer_validation(answer, testcases):
    #!---GPT에게 넘겨주어야 코드와, 일련의 테스트 케이스 집합---!
    response = gpt_inference('testcase', testcases=testcases, answer = answer)
    if 'True' in response:
        return True
    else: return False

# SQLite DB 연결
conn = sqlite3.connect("../db.sqlite3")
 
# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# SQL 쿼리 실행
cur.execute("select * from sogongapp_codingproblem where title='주사위 게임'")
row = cur.fetchone()
problem_text = row[2]
problem_input = row[3]
problem_output = row[4]
answer = row[5]
problem_content = '문제: \n'+ problem_text + '\n입력 : ' + problem_input + '\n 출력: ' + problem_output
cur.execute("select * from sogongapp_codingtestcase where problem='주사위 게임'")
row1 = cur.fetchone()
print('title :' +row[0] +'\n'+'problem :'+ row[2])
print(row1)
class testcase:
    def __init__(self, row1):
        self.case_input1 = row1[1]
        self.case_input2 = row1[2]
        self.case_input3 = row1[3]
        self.case_input4 = row1[4]
        self.case_output1 = row1[5]
        self.case_output2 = row1[6]
        self.case_output3 = row1[7]
        self.case_output4 = row1[8]
testcases = testcase(row1) 
gpt_answer = get_gpt_answer(problem_text, problem_input, problem_output)
print('gpt가 푼 답: \n'+ gpt_answer)

answer_validation_response = answer_validation(gpt_answer, testcases)
print('정답 validation: ' + str(answer_validation_response))

gpt_feedback = get_feedback(problem_content , gpt_answer)
print('gpt feedback:' + gpt_feedback)