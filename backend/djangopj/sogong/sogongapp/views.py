from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def main(request):
    """id = request.GET.get('id')
    print(id)
    email = request.GET.get('email')
    print(email)
    pw = request.GET.get('pw')
    print(pw)
    delid = request.GET.get('delid')
    print(delid)"""
    print(request.method)
    if request.method == "POST":
        id = request.POST.get('id')
        email = request.POST.get('email')
        pw = request.POST.get('pw')
        delid = request.POST.get('delid')

        users = User.objects.all()
        for user in users:
            print(user)
        if id is not None and email is not None and pw is not None:
            # User 모델 인스턴스 생성
            user = User(username=id, email=email, password=pw)
            if User.objects.filter(username=id).exists():
                print('username이 이미 데이터베이스에 있습니다.')
                return HttpResponse("Fail" + id)
            else:
                print('username이 데이터베이스에 없습니다.')
                # 데이터베이스에 저장
                user.save()
                # 저장된 정보를 출력
                print(user)
                return HttpResponse("Success" + id)
        elif delid is not None:
            # User 모델 테이블 삭제
            User.objects.all().delete()
            print('User 테이블을 초기화했습니다.')
            users = User.objects.all()
            for user in users:
                print(user)
            return HttpResponse("User 테이블을 초기화했습니다.")
        else:
            return HttpResponse("Totally Fail")
    else:
        return HttpResponse("Failed")
