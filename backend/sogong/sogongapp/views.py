import logging
import sys
import contextlib
import io
import os
from django.http import JsonResponse, HttpResponse
import sqlite3
from .models import User
from .models import EthicsProblem
from .models import CodingProblem
from .models import SolvedEthics
from .models import SolvedCoding
from .models import CodingTestCase
import json
import openai
import time
import sogongapp.gpt_prompts as gpt_prompts
from .API_KEY import OPENAI_API_KEY  

openai.api_key = OPENAI_API_KEY

# gpt로부터 response를 얻어오는 코드
def gpt_inference( method,problem_content=None,  testcases=None, answer=None):
    messages = []
    # feedback 얻어올시 문제, 입력형식, 출력형식과 함께 사용자가 입력한 코드 전송
    if method == 'feedback':
        prompt = getattr(gpt_prompts, 'GPT_CODE_FEEDBACK')
        prompt = problem_content + '\n' + '답변 CODE: \n'+ answer + '\n' + prompt
        messages.append({'role': 'user', 'content': prompt})
    # 문제에 대한 gpt의 answer를 불러올 시 문제와 python code 요청
    elif method == 'getanswer':
        prompt = getattr(gpt_prompts, 'GPT_GETANSWER')
        messages.append({'role':'user', 'content':problem_content+prompt})
    wait = 1
    while True:
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                temperature=0.8,
                messages=messages
            )
            # message의 content 부분이 gpt response 
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

def check_password(user, input_word): # 비밀번호 확인
    password = user.password

    if input_word == password:
        return True 
    else:
        return False
  
#GPT로 부터 답변을 얻어오는 함수
def get_gpt_answer(problem_text, problem_input, problem_output):
    #!---GPT에게 넘겨주어야 할 것은 문제 텍스트, 문제의 입력값 예시, 문제의 출력값 예시---!
    problem = '문제: \n' + problem_text + '\n입력: \n' + problem_input + '\n출력: \n' + problem_output
    
    answer = gpt_inference('getanswer', problem_content=problem)
    #!---GPT로 부터 받아온 코드를 answer에 넣고 answer를 반환
    return answer

#답이 유효한지 확인하는 함수
def answer_validation(answer, testcases):
    #!---GPT에게 넘겨주어야 코드와, 일련의 테스트 케이스 집합---!
    case_inputs = []
    case_outputs = []
    for i in range(4):
        input1 = getattr(testcases, f'case_input{i+1}')
        output1 = getattr(testcases, f'case_output{i+1}')
        if input1 == None:
            break
        case_inputs.append(input1)
        case_outputs.append(output1)
    output = open('./temp/output.txt', 'w+')
    for i in range(len(case_inputs)):
        
        testinput = open('./temp/testinput.txt', 'w+')
        testinput.write(case_inputs[i])
        testinput.close()
        # sys.stdout 재지정
        try:
            testcode = open('./temp/testcode.py', 'w+')
            testcode.write(answer)
            testcode.close()
            terminal_command =  "python ./temp/testcode.py < ./temp/testinput.txt > ./temp/output.txt"
            os.system(terminal_command)
            f = open('./temp/output.txt', 'r') 
            output_data = f.read()
            f.close()
            output.close()
            if case_outputs[i] not in output_data:
                return False
        except:
            print('execution error')
            return False
    print('success')
    return True
    

    #!---정상적으로 통과했으면 True를, 통과하지 못했으면 False를 반환

#사용자의 답의 피드백을 받는 함수
def get_feedback(problem_content, user_submission):
    #!---피드백을 지피티로부터 받아서 피드백을 리턴---!
    feedback = gpt_inference('feedback',problem_content, answer= user_submission)
    return feedback


# 로그인  : 1번
def login_view(request):
    
    print(os.getcwd())
    email = request.GET.get('email')
    password = request.GET.get('password')
    
    try:
        user = User.objects.get(username=email)
        print(email, password)
        if user and check_password(user,password): # db와 비교 
            # 로그인 성공      
            solvedEthicsProblems = []
            solvedCodingProblems = []
            get_scored = 0        
            total_score = 0
            percentage_score = 0
            ethicsProblems = EthicsProblem.objects.all() #전체 윤리 문제를 불러와서 저장
            solvedEthics = SolvedEthics.objects.filter(user=email).all() #해결한 윤리 문제를 불러와서 저장
            for ethicsProblem in ethicsProblems: #전체 문제 리스트 순회
                solved_ethics = solvedEthics.filter(problem=ethicsProblem.title).first() #지금 선택한 문제 제목이 solvedEthics에 존재 하는지 확인
                if solved_ethics is not None:
                    solvedEthicsProblems.append(ethicsProblem.id)

            codingsProblems = CodingProblem.objects.all() #전체 코딩 문제를 불러와서 저장
            solvedCodings = SolvedCoding.objects.filter(user=email).all() #해결한 코딩 문제를 불러와서 저장
            for codingproblem in codingsProblems: #전체 문제 리스트 순회
                total_score += int(codingproblem.level)
                solved_coding = solvedCodings.filter(problem=codingproblem.title).first() #지금 선택한 문제 제목이 solvedCodings에 존재하는 지 확인
                if solved_coding is not None:
                    get_scored += int(codingproblem.level)
                    solvedCodingProblems.append(codingproblem.id)

            percentage_score = get_scored / total_score * 100
            
            response_data = {
                "email" : email,
                "score" : percentage_score,
                "solvedCodingProblems" : solvedCodingProblems,
                "solvedEthicsProblems" : solvedEthicsProblems,
            }
        else:
            response_data = {
                "email" : '',
                "score" : 0,
                "solvedCodingProblems" : solvedCodingProblems,
                "solvedEthicsProblems" : solvedEthicsProblems,
            }
        return JsonResponse(response_data)
    except:
        response_data={}
        return JsonResponse(response_data, status=501)

# email 중복검사 : 1.1번
def user_idcheck(request):
    if request.method == "GET":
        id = request.GET.get('email')
        try:
            user = User.objects.get(username=id)
            response_data = {
                "status": 501
            }
        except User.DoesNotExist:
            response_data = {
                "status": 200
            }
        return JsonResponse(response_data)
    
def register_view(request):
    if request.method =="POST":
        body = json.loads(request.body)
        id = body.get('email')
        pw = body.get('password')
        try:
            user = User.objects.get(username=id)
            response_data={
                'status':501
            }
            return JsonResponse(response_data)
        except User.DoesNotExist:
            response_data ={
                'status':200
            }
            user = User(username=id, password = pw)
            user.save()
            return JsonResponse(response_data)
"""
#유저가 얼마나 문제 풀었나 확인하는 함수 : 3번 
def userinfo_view(request):
    username = request.GET.get('token')
    solvedEthics_count = SolvedEthics.objects.filter(username=username).count() #해결 한 윤리 문제의 수
    solvedCoding_count = SolvedCoding.objects.filter(username=username).count() #해결 한 코딩 문제의 수
    ethicsProblem_count = EthicsProblem.objects.all().count() #전체 윤리 문제의 수
    codingProblem_count = CodingProblem.objects.all().count() #전체 코딩 문제의 수
    ethics_progress_rate = solvedEthics_count / ethicsProblem_count * 100 #윤리 문제 진행도 계산
    coding_progress_rate = solvedCoding_count / codingProblem_count * 100 #코딩 문제 진행도 계산
    response_data = {
        "message" : "사용자의 진척도 입니다.",
        "ethics_progress_rate" : ethics_progress_rate,
        "coding_progress_rate" : coding_progress_rate,
    }
    return JsonResponse(response_data)


#유저가 얼마나 문제 풀었나 확인하는 함수 : 3번 수정
def userinfo_view(request):
    username = request.GET.get('token')
    solved_ethics_list = []
    solved_coding_list = []
    ethicsProblems = EthicsProblem.objects.all() #전체 윤리 문제를 불러와서 저장
    solvedEthics = SolvedEthics.objects.filter(username=username).all() #해결한 윤리 문제를 불러와서 저장
    for ethicsProblem in ethicsProblems: #전체 문제 리스트 순회
        solved_ethics = solvedEthics.filter(problem=ethicsProblem.title).first() #지금 선택한 문제 제목이 solvedEthics에 존재 하는지 확인
        if solved_ethics is not None:
            solved_ethics_list.append(ethicsProblem.id) #존재시 해결한 문제 번호를 저장

        codingsProblems = CodingProblem.objects.all() #전체 코딩 문제를 불러와서 저장
    solvedCodings = SolvedCoding.objects.filter(username=username).all() #해결한 코딩 문제를 불러와서 저장
    for codingproblem in codingsProblems: #전체 문제 리스트 순회
        solved_coding = solvedCodings.filter(problem=codingproblem.title).first() #지금 선택한 문제 제목이 solvedCodings에 존재하는 지 확인
        if solved_coding is not None:
            solved_coding_list.append(codingproblem.id) #존재시 해결한 문제 번호를 저장
    
    response_data = {
        "solvedCodingProblems" : solved_coding_list,
        "solvedEthicsProblems" : solved_ethics_list,
    }
    return JsonResponse(response_data)


#사용자 정보 업데이트 : 4번 
def user_newinfo(request):
    data = json.loads(request.body)
    username = data.get('token')
    solvedEthics_count = SolvedEthics.objects.filter(username=username).count() #해결 한 윤리 문제의 수
    solvedCoding_count = SolvedCoding.objects.filter(username=username).count() #해결 한 코딩 문제의 수
    ethicsProblem_count = EthicsProblem.objects.all().count() #전체 윤리 문제의 수
    codingProblem_count = CodingProblem.objects.all().count() #전체 코딩 문제의 수
    ethics_progress_rate = solvedEthics_count / ethicsProblem_count * 100 #윤리 문제 진행도 계산
    coding_progress_rate = solvedCoding_count / codingProblem_count * 100 #코딩 문제 진행도 계산


    response_data = {
        "message" : "사용자의 진척도 입니다.",
        "ethics_progress_rate" : ethics_progress_rate,
        "coding_progress_rate" : coding_progress_rate,
    }

    ethicsProblems = EthicsProblem.objects.all() #전체 윤리 문제를 불러와서 저장
    solvedEthics = SolvedEthics.objects.filter(username=username).all() #해결한 윤리 문제를 불러와서 저장
    for ethicsProblem in ethicsProblems: #전체 문제 리스트 순회
        solved_ethics = solvedEthics.filter(problem=ethicsProblem.title).first() #지금 선택한 문제 제목이 solvedEthics에 존재 하는지 확인
        if solved_ethics is not None:
            response_data.append({
                "title": ethicsProblem.title,
                "solved": True,
            }) #존재시 해결한 문제임을 전송
        else:
            response_data.append({
                "title": ethicsProblem.title,
                "solved": False,
            }) #부재시 해결한 적 없는 문제임을 전송
    #전체 업데이트된 윤리문제 풀었는지 여부전송

    codingsProblems = CodingProblem.objects.all() #전체 코딩 문제를 불러와서 저장
    solvedCodings = SolvedCoding.objects.filter(username=username).all() #해결한 코딩 문제를 불러와서 저장
    for codingproblem in codingsProblems: #전체 문제 리스트 순회
        solved_coding = solvedCodings.filter(problem=codingproblem.title).first() #지금 선택한 문제 제목이 solvedCodings에 존재하는 지 확인
        if solved_coding is not None:
            response_data.append({
                "title": codingproblem.title,
                "solved": True,
            }) #존재시 해결한 문제임을 전송
        else:
            response_data.append({
                "title": codingproblem.title,
                "solved": False,
            }) #부재시 해결한 적 없는 문제임을 전송
       #전체 업데이트된 코딩문제 풀었는지 여부 전송

    return JsonResponse(response_data)
"""

#윤리문제 전체 전송 : 3번 
def ethics_view(request):
    username = request.GET.get('email')
    ethicsProblems = EthicsProblem.objects.all() #전체 윤리 문제를 불러와서 저장
    ethicsProblem = []
    if username is not None:
        for problem in ethicsProblems:
            ethicsProblem.append({
                "pid": problem.id,
                "title": problem.title,
                "content":problem.content,
                "optionA": problem.optionA,
                "optionB": problem.optionB,
                "submissionA": problem.submissionA,
                "submissionB": problem.submissionB
            })
    
    response_data = {
        "ethicsProblem":ethicsProblem
    }

    return JsonResponse(response_data)

#윤리문제 선택 시 그것에 대한 피드백 전송 : 4번 
def ethics_submission(request):
    body = json.loads(request.body)
    pid = body.get("pid")
    username = body.get("email")

    if username is not None: #토큰값 있는 경우
        ethicsproblem = EthicsProblem.objects.get(id = pid)
        user = User.objects.get(username=username) 
        submissionA = ethicsproblem.submissionA
        submissionB = ethicsproblem.submissionB # 각각의 선택에 대한 결과
        
        results = []
        results.append(submissionA)
        results.append(submissionB)

        response_data = {
            "results":results,
        }  
        print(results)
        solvedEthics = SolvedEthics(user = user, problem = ethicsproblem)
        solvedEthics.save()
    #피드백 보내기
        return JsonResponse(response_data)
    
    else: # 토큰값 없는 경우
        results =[]
        response_data = {
            "results":results,
        }

        return JsonResponse(response_data)


    

# 코딩문제 전체 전송 : 5번 
def codings_view(request):
    username = request.GET.get('email')
    codingsProblems = CodingProblem.objects.all() #전체 코딩 문제를 불러와서 저장

    if username is not None:
        codingproblem = []

        for problem in codingsProblems:
            codingproblem.append({
                "pid": problem.id,
                "title": problem.title,
                "level": problem.level,
                "content": problem.content_problem,
                "input": problem.content_input,
                "output": problem.content_output,
            })
    else:
        codingproblem =[]
    
    response_data = {
        "codingproblem":codingproblem
    }

    return JsonResponse(response_data)

# 코딩시 GPT답 전송 : 8번 
def coding_answer(request):
    pid = request.GET.get('pid')
    username = request.GET.get('email')
    if username is not None:
        problem_info = CodingProblem.objects.get(id=pid) #pid를 통해 전체 문제를 불러온다
        problem_title = problem_info.title
        problem_text = problem_info.content_problem
        problem_input = problem_info.content_input
        problem_output = problem_info.content_output

        #이미 해결한 적 있는 경우 저장되어 있을 것이므로 CodingSubmission을 찾아서 gpt_answer를 반환
        # if problem_info.gpt_answer is not None:
        #     gpt_answer = problem_info.gpt_answer
        # #해결한 적 없는 경우 GPT에게 요청
        # else:
        
        gpt_answer = get_gpt_answer(problem_text, problem_input, problem_output) #GPT답을 받아오는 함수(구현요망)
        while gpt_answer is None:
            time.sleep(1)
        testcases = CodingTestCase.objects.get(problem = problem_title) #해당 문제의 테스트 케이스를 가져옴

        # 테스트 케이스를 통과하지 못하면 GPT의 답변에 문제가 있는것으로 판단, 재생성
        if answer_validation(gpt_answer, testcases) is False:
            print("GPT 답변에 문제가 있습니다.")
            gpt_answer = problem_info.gpt_answer
        response_data = {
            "answer" : gpt_answer,
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            "answer" : "",
        }
        return JsonResponse(response_data)
# 유저 답 확인 : 7번 
def useranswer_view(request):
    if request.method == "POST": 
        body = json.loads(request.body)
        username = body.get("email")
        user = User.objects.get(username=username) 
        pid = body.get("pid")
        user_submission = body.get("answer")
        is_timeout  = body.get("isTimeout")
        if username is not None:
            problem_info = CodingProblem.objects.get(id=pid) #pid를 통해 전체 문제를 불러온다
            problem_content = '문제: \n' +problem_info.content_problem + '\n입력 : ' + problem_info.content_input + '\n 출력: ' + problem_info.content_output
            testcases = CodingTestCase.objects.get(problem = problem_info.title) #해당 문제의 테스트 케이스를 가져옴
        
            #사용자의 답변이 정확한지 확인
            if is_timeout:
                if answer_validation(user_submission, testcases):
                    gpt_feedback = get_feedback(problem_content, user_submission)
                    response_data = {
                        "result" : "pass",
                        "feedback" : gpt_feedback,
                    }
                    solvedCoding = SolvedCoding(user = user, problem = problem_info)
                    solvedCoding.save()
                else:
                    gpt_feedback = get_feedback(problem_content, user_submission)
                    response_data = {
                        "result" : "fail",
                        "feedback" : gpt_feedback,
                    }
            elif answer_validation(user_submission, testcases):
                gpt_feedback = get_feedback(problem_content, user_submission)
                response_data = {
                    "result" : "pass",
                    "feedback" : gpt_feedback,
                }
                
                solvedCoding = SolvedCoding(user = user, problem = problem_info)
                solvedCoding.save()
            else:
                gpt_feedback = get_feedback(problem_content, user_submission)
                response_data = {
                    "result" : "fail",
                    "feedback" : gpt_feedback,
                }  #
            return JsonResponse(response_data)
        else:
            response_data = {
                "result" : "",
                "feedback" : "",
            }  #
            return JsonResponse(response_data)
    
"""
codingProblem = CodingProblem.objects.all()
codingProblem_count = CodingProblem.objects.all().count()
print(codingProblem_count)


database = "db.sqlite3"
conn = sqlite3.connect(database)
cursor = conn.cursor()

cursor.execute("SELECT * FROM sogongapp_codingproblem")
coding_problems = cursor.fetchall()

for problem in coding_problems:
    print("Title:", problem[1])
    print("Level:", problem[2])
    print("Problem Text:", problem[3])
    print("Input Format:", problem[4])
    print("Output Format:", problem[5])
    print("Answer:", problem[6])
    print("----------------------")

cursor.close()
conn.close()

conn = sqlite3.connect(database)
cursor = conn.cursor()

cursor.execute("SELECT * FROM sogongapp_CodingTestCase")
coding_problems = cursor.fetchall()

for problem in coding_problems:
    print("Title:", problem[0])
    print("Input1:", problem[1])
    print("Input2:", problem[2])
    print("Input3:", problem[3])
    print("Input4:", problem[4])
    print("Output1:", problem[5])
    print("Output2:", problem[6])
    print("Output3:", problem[7])
    print("Output4:", problem[8])
    print("----------------------")

cursor.close()
conn.close()
"""