from django.http import JsonResponse
import sqlite3
from .models import User
from .models import EthicsProblem
from .models import CodingProblem
from .models import SolvedEthics
from .models import SolvedCoding
from .models import CodingSubmission
from .models import CodingTestCase
from .models import EthicsSubmission
import json
import hashlib
import openai
import sogongapp.gpt_prompts as gpt_prompts
from .API_KEY import OPENAI_API_KEY  

openai.api_key = OPENAI_API_KEY

# gpt로부터 response를 얻어오는 코드
def gpt_inference( method,problem_content=None,  testcases=None, answer=None):
    messages = []
    # feedback 얻어올시 문제, 입력형식, 출력형식과 함께 사용자가 입력한 코드 전송
    if method == 'feedback':
        prompt = getattr(gpt_prompts, 'GPT_CODE_FEEDBACK')
        prompt = '문제: \n' + problem_content + '\n' + '답변 CODE: \n'+ answer + '\n' + prompt
        messages.append({'role': 'user', 'content': prompt})
    # testcase확인시 사용자가 입력한 코드와 testcase 전송
    elif method == 'testcase':
        prompt = 'Code: \n' + answer
        try:
            # testcase 최대 4개, 4개보다 적을 경우, 존재하는 testcase만 포함
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
    # 문제에 대한 gpt의 answer를 불러올 시 문제와 python code 요청
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
    response = gpt_inference('testcase', testcases=testcases, answer = answer)
    if 'True' in response:
        return True
    else: return False
    #!---정상적으로 통과했으면 True를, 통과하지 못했으면 False를 반환

#사용자의 답의 피드백을 받는 함수
def get_feedback(problem_content, user_submission):
    #!---피드백을 지피티로부터 받아서 피드백을 리턴---!
    feedback = gpt_inference('feedback',problem_content, answer= user_submission)
    return feedback

# 로그인 및 회원가입 : 1번, 2번 
def register_view(request):
    if request.method == "POST": # 회원가입
        body = json.loads(request.body)
        id = body.get("email")
        pw = body.get("password")
        user = User(username=id, password=pw) #  email, password
        if User.objects.filter(username=id).exists():
            response_data = {
            "message": "이미 존재하는 회원입니다.",
            "id" : id,
            "pw" : pw
        } # 이미 회원 정보가 존재하는 경우
        else:
            
            print(id, pw)
            user.save()   
            response_data = {
            "message": "회원가입이 완료되었습니다.",
            "id" : id,
            "pw" : pw
        } # 새로 만든 경우
    
        
        return JsonResponse(response_data)
    
    else:
        id = request.GET.get('email')
        pw = request.GET.get('password')
        user = User.objects.get(username=id)
        print()
        if user and check_password(user,pw): # db와 비교 
            # 로그인 성공
            #hash_object = hashlib.md5(id.encode())
            #hash_value = hash_object.hexdigest()
            
            response_data = {
            "message" : "로그인이 완료되었습니다.",
            "id" : id,
            "pw" : pw,
            "cookie" : id,
        }
            return JsonResponse(response_data)
        else:
            # 로그인 실패
            response_data = {
            "message" : "로그인이 실패했습니다"
        }
            return JsonResponse(response_data)

def user_idcheck(request):
    if request.method == "GET":
    
        id = request.GET.get('email')
        try:
            user = User.objects.get(username=id)
            response_data = {
                "status": 200
            }
        except:
            response_data = {
                "status": 501
            }
        return JsonResponse(response_data)

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


#윤리문제 전체 전송 : 5번 
def ethics_view(request):
    username = request.GET.get('token')
    ethicsProblems = EthicsProblem.objects.all() #전체 윤리 문제를 불러와서 저장
    solvedEthics = SolvedEthics.objects.filter(username=username).all() #해결한 윤리 문제를 불러와서 저장
    response_data = []
    for ethicsProblem in ethicsProblems: #전체 문제 리스트 순회
        solved_ethics = solvedEthics.filter(problem=ethicsProblem.title).first() #지금 선택한 문제 제목이 solvedEthics에 존재 하는지 확인
        if solved_ethics is not None:
            response_data.append({
                "title": ethicsProblem.title,
                "content": ethicsProblem.content,
                "optionA": ethicsProblem.optionA,
                "optionB": ethicsProblem.optionB,
                "submissionA": ethicsProblem.submissionA,
                "submissionB": ethicsProblem.submissionB,
                "solved": True,
            }) #존재시 해결한 문제임을 전송
        else:
            response_data.append({
                "title": ethicsProblem.title,
                "content": ethicsProblem.content,
                "optionA": ethicsProblem.optionA,
                "optionB": ethicsProblem.optionB,
                "submissionA": ethicsProblem.submissionA,
                "submissionB": ethicsProblem.submissionB,
                "solved": False,
            }) #부재시 해결한 적 없는 문제임을 전송
    
    return JsonResponse(response_data)

#윤리문제 선택 시 그것에 대한 피드백 전송 : 6번 
def ethics_submission(request):
    body = json.loads(request.body)
    username = body.get("token")
    pid = body.get("pid")
    option = body.get("option") # 입력 데이터 받기 


    ethicssubmission = EthicsSubmission.objects.get_or_create(user=username,problem=pid)
    ethicssubmission.user_submission = option
    ethicssubmission.save()#유저의 답변값 EthicsSubmission DB저장
    
    ethicsproblem = EthicsProblem.objects.get(title = pid)
    optionA = ethicsproblem.optionA
    optionB = ethicsproblem.optionB
    submissionA = ethicsproblem.submissionA
    submissionB = ethicsproblem.submissionB # 각각의 선택에 대한 결과

    response_data = {
        "optionA": optionA,
        "optionB": optionB,
        "submissionA": submissionA,
        "submissionB": submissionB,
    }
    #피드백 보내기
    return JsonResponse(response_data)


    

# 코딩문제 전체 전송 : 7번 
def codings_view(request):
    username = request.GET.get('token')
    codingsProblems = CodingProblem.objects.all() #전체 코딩 문제를 불러와서 저장
    solvedCodings = SolvedCoding.objects.filter(username=username).all() #해결한 코딩 문제를 불러와서 저장
    response_data = []
    for codingproblem in codingsProblems: #전체 문제 리스트 순회
        solved_coding = solvedCodings.filter(problem=codingproblem.title).first() #지금 선택한 문제 제목이 solvedCodings에 존재하는 지 확인
        if solved_coding is not None:
            response_data.append({
                "title": codingproblem.title,
                "level": codingproblem.level,
                "content": codingproblem.content_problem,
                "input": codingproblem.content_input,
                "output": codingproblem.content_output,
                "solved": True,
            }) #존재시 해결한 문제임을 전송
        else:
            response_data.append({
                "title": codingproblem.title,
                "level": codingproblem.level,
                "content": codingproblem.content_problem,
                "input": codingproblem.content_input,
                "output": codingproblem.content_output,
                "solved": False,
            }) #부재시 해결한 적 없는 문제임을 전송
    
    return JsonResponse(response_data)

# 코딩시 GPT답 전송 : 8번 
def coding_answer(request):
    username = request.GET.get('token')
    pid = request.GET.get('pid')
    problem_info = CodingProblem.objects.get(id=pid) #pid를 통해 전체 문제를 불러온다
    problem_title = problem_info.title
    problem_text = problem_info.content_problem
    problem_input = problem_info.content_input
    problem_output = problem_info.content_output
    gpt_answer = ''  #gpt 답안을 받을 변수 선언

    #이미 해결한 적 있는 경우 저장되어 있을 것이므로 CodingSubmission을 찾아서 gpt_answer를 반환
    try:  
        codingSubmission = CodingSubmission.objects.get(user=username, problem=problem_title)
        gpt_answer = codingSubmission.gpt_answer
    #해결한 적 없는 경우 GPT에게 요청
    except CodingSubmission.DoesNotExist:
        gpt_answer = get_gpt_answer(problem_text, problem_input, problem_output) #GPT답을 받아오는 함수(구현요망)
        testcases = CodingTestCase.objects.get(problem = problem_title) #해당 문제의 테스트 케이스를 가져옴

        # 테스트 케이스를 통과하지 못하면 GPT의 답변에 문제가 있는것으로 판단, 재생성
        while answer_validation(gpt_answer, testcases) is False:
            print("GPT 답변에 문제가 있습니다.")
            gpt_answer = problem_info.answer

        codingSubmission = CodingSubmission(user=username, problem=problem_title, gpt_answer=gpt_answer, user_submission=None, gpt_feedback=None)
        codingSubmission.save() # 정상적 생성 이후 codingSubmission에 저장

    response_data = {
        "message" : "GPT의 답변입니다",
        "answer" : gpt_answer,
    }
    return JsonResponse(response_data)

# 유저 답 확인 : 9번 
def useranswer_view(request):
    if request.method == "POST": 
        body = json.loads(request.body)
        username = body.get("token")
        pid = body.get("pid")
        user_submission = body.get("answer")
        problem_info = CodingProblem.objects.get(id=pid) #pid를 통해 전체 문제를 불러온다
        problem_title = problem_info.title
        problem_content = '문제: \n' +problem_info.content_problem + '\n입력 : ' + problem_info.content_input + '\n 출력: ' + problem_info.content_output

        testcases = CodingTestCase.objects.get(problem = problem_title) #해당 문제의 테스트 케이스를 가져옴
    
        #사용자의 답변이 정확한지 확인
        if answer_validation(user_submission, testcases):
            gpt_feedback = get_feedback(problem_content, user_submission)
            codingSubmission = CodingSubmission.objects.get(user=username, problem=problem_title)
            codingSubmission.user_submission = user_submission
            codingSubmission.gpt_feedback = gpt_feedback
            codingSubmission.save() #답변이 정답일 시 사용자의 답변과 피드백을 저장

            response_data = {
                "message": "정답입니다!",
                "isPass" : True,
                "feedback" : gpt_feedback,
            }
        else:
            response_data = {
                "message": "틀렸습니다!",
                "isPass" : False,
                "feedback" : None,
            }  #정답이 아닐 시 저장하지 않음
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