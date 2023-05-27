from django.http import JsonResponse
from .models import User
import json
import hashlib

def check_password(user, input_word): # 비밀번호 확인
    password = user.password

    if input_word == password:
        return True
    else:
        return False



def register_view(request):
    if request.method == "POST": # 회원가입
        body = json.loads(request.body)
        id = body.get("id")
        email = body.get("email")
        pw = body.get("pw")
        user = User(username=id, email=email, password=pw) # id, email, password
        if User.objects.filter(username=id).exists():
            response_data = {
            "message": "이미 존재하는 회원입니다.",
            "id" : id,
            "email" : email,
            "pw" : pw
        } # 이미 회원 정보가 존재하는 경우
        else:
            user.save()   
            response_data = {
            "message": "회원가입이 완료되었습니다.",
            "id" : id,
            "email" : email,
            "pw" : pw
        } # 새로 만든 경우
    
        
        return JsonResponse(response_data)
    
    else:
        id = request.GET.get('id')
        pw = request.GET.get('pw')
        user = User.objects.get(username=id)
        print()
        if user and check_password(user,pw): # db와 비교 나중에 손좀 봐야함
            # 로그인 성공
            hash_object = hashlib.md5(id.encode())
            hash_value = hash_object.hexdigest()
            
            response_data = {
            "message" : "로그인이 완료되었습니다.",
            "id" : id,
            "pw" : pw,
            "cookie" : hash_value,
        }
            return JsonResponse(response_data)
        else:
            # 로그인 실패
            response_data = {
            "message" : "로그인이 실패했습니다"
        }
            return JsonResponse(response_data)
    
  

