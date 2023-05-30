
GPT_CODE_CHECK = '''
위에 제공된 모든 testcase input을, 제공된 code에서 실행했을 때 올바른 output을 낼 수 있을까?
True 또는 False로 대답해줘. 끝에 '.'은 붙이지 말아줘.
'''.strip()

GPT_CODE_FEEDBACK = '''
문제에 대한 code를 다음과 같이 작성했어 혹시 time complexity나 code의 효율성 혹은 가독성 측면에서 수정해야 할 부분이 있으면 수정하여 코드로 작성해줘
'''.strip()

GPT_GETANSWER='''
다음과 같이 문제와 조건이 주어져 있을 때 이를 해결할 수 있는 python code를 작성해줘
다른 부연설명없이 python code만 작성해줘
'''