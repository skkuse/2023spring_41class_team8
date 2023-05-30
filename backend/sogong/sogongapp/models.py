from django.db import models


# 윤리 문제 테이블
class EthicsProblem(models.Model):
    title = models.CharField(max_length=100, unique=True) # 윤리 문제의 제목
    content = models.CharField(max_length=200) # 윤리 문제의 내용
    optionA = models.CharField(max_length=100) # 윤리 문제의 옵션 A
    optionB = models.CharField(max_length=100) # 윤리 문제의 옵션 B
    submissionA = models.CharField(max_length=300) # Option A를 선택한 경우의 답변, GPT생성 or 미리 저장
    submissionB = models.CharField(max_length=300) # Option B를 선택한 경우의 답변, GPT생성 or 미리 저장


# 코딩 문제 테이블
class CodingProblem(models.Model):
    title = models.CharField(max_length=100, unique=True) # 코딩 문제의 제목
    level = models.IntegerField() # 코딩 문제의 레빌
    content_problem = models.CharField(max_length=200) # 코딩 문제의 문제글
    content_input = models.CharField(max_length=200) # 코딩 문제의 입력 포맷 설명
    content_output = models.CharField(max_length=200) # 코딩 문제의 출력 포맷 설명
    answer = models.CharField(max_length=3000)

# 사용자 테이블
class User(models.Model):
    username = models.CharField(max_length=100, unique=True) # 사용자 이름
    email = models.EmailField() # 사용자 이메일
    password = models.CharField(max_length=128) # 사용자 패스워드
# (기술적인 문제로 사용자 테이블에서 분리)
class SolvedCoding(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE) # 해결 한 사람
    problem = models.ForeignKey(CodingProblem, to_field='title', on_delete=models.CASCADE) # 해결 한 코딩 문제
# (기술적인 문제로 사용자 테이블에서 분리)
class SolvedEthics(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE) # 해결 한 사람
    problem = models.ForeignKey(EthicsProblem, to_field='title', on_delete=models.CASCADE) # 해결 한 윤리 문제
   
# 윤리 문제 제출 
class EthicsSubmission(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE) # 제출 한 사람
    problem = models.ForeignKey(EthicsProblem, to_field='title', on_delete=models.CASCADE)
    user_submission = models.CharField(max_length=100) # 유저가 제출한 옵션내용

# 코드 문제 제출 및 정답 확인
class CodingSubmission(models.Model):
    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE) # 제출 한 사람
    problem = models.ForeignKey(CodingProblem, to_field='title', on_delete=models.CASCADE) # 제출 한 문제
    gpt_answer= models.CharField(max_length=200) # 제출한 문제의 GPT의 답
    user_submission = models.CharField(max_length=200) # 사용자 제출 내용
    gpt_feedback= models.CharField(max_length=200) # 제출한 문제의 답변에 대한 피드백

# 문제에 대한 테스트 케이스
class CodingTestCase(models.Model):
    problem = models.ForeignKey(CodingProblem, to_field='title', on_delete=models.CASCADE) # 문제 제목
    case_input1 = models.CharField(max_length=100) # 테스트 케이스 Input
    case_input2 = models.CharField(max_length=100)
    case_input3 = models.CharField(max_length=100)
    case_input4 = models.CharField(max_length=100)
    case_output1 = models.CharField(max_length=100) # 테스트 케이스 Output
    case_output2 = models.CharField(max_length=100)
    case_output3 = models.CharField(max_length=100)
    case_output4 = models.CharField(max_length=100)