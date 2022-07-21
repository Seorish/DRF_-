from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.generics import get_object_or_404
# Create your views here.
from .models import Todo
from .serializers import TodoCreatedSerializer, TodoSimpleSerializer, TodoDetailSerializer


# GET 전송과 POST 전송 모두 동일한 url 사용하기 때문에 한번에 처리함
class TodosAPIView(APIView):
    # 전체 조회
    def get(self,request):
        # GET /todo/
        todos = Todo.objects.filter(complete=False)
        # DB에 저장된 Todo 모델로부터 데이터 받아옴
        # 필터 조건 : complete 되지 않은 항목
        serializer = TodoSimpleSerializer(todos, many=True)
        # serializer 에 전체 글 정보를 전달해 직렬화
        # many 옵션을 이용해 한번에 여러 데이터 전달
        return Response(serializer.data, status=status.HTTP_200_OK)
        # 직렬화된 JSON 에서 data 속성을 응답으로 전달하고 상태코드를 설정

    def post(self, request):
        # POST /todo/ 글 내용을 등록하는 요청
        serializer = TodoCreatedSerializer(data=request.data)
        # POST 요청으로 받은 데이터를 serializer에 전달
        if serializer.is_valid():
            # 전달받은 데이터 유효성 확인
            serializer.save()
            # modelserializer의 역직렬화를 통해 save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TodoAPIView(APIView):
    # 세부 조회
    def get(self, request, pk):
        # GET todo/<int:pk>/
        todo = get_object_or_404(Todo, id=pk)
        # 전송된 데이터의 유효성 검사
        # pk 이용해 해당 글 정보 가져옴
        # 객체가 존재하지 않을 시 get()을 사용해 Http404 에러 발생시킴
        # 모델 계층을 뷰 계층에 연결하는 방법
        serializer = TodoDetailSerializer(todo)
        # serializer에 todo 모델 전달해 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)
        # 직렬화된 내용 중 data와 상태코드를 응답으로 전달

    def put(self, request, pk):
        # PUT todo/<int:pk>/
        # 글 수정
        todo = get_object_or_404(Todo, id=pk)
        # 전송된 데이터의 유효성 검사
        # 객체가 없다면 404 오류 발생
        serializer = TodoCreatedSerializer(todo, data=request.data)
        if serializer.is_valid():
            # 전달받은 데이터 유효성 확인
            serializer.save()
            # modelserializer의 역직렬화를 통해 save
            return Response(serializer.data, status=status.HTTP_200_OK)
            # 직렬화된 내용 중 data와 상태코드를 응답으로 전달
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoneTodosAPIView(APIView):
    # 완료한 항목 보여주기
    def get(self,request):
        #GET done/
        dones = Todo.objects.filter(complete=True)
        # DB에 저장된 Todo 모델로부터 데이터 받아옴
        # 필터 조건 : 완료한 항목만 받아오기
        serializer = TodoSimpleSerializer(dones, many=True)
        # serializer에 dones 모델 전달해 직렬화
        # many 옵션 이용해 한 번에 많은 데이터 전달
        return Response(serializer.data, status=status.HTTP_200_OK)
        # 직렬화된 내용 중 data와 상태코드를 응답으로 전달

class DoneTodoAPIView(APIView):
    # 완료한 항목들 '완료'로 바꿔주기
    def get(self,request,pk):
        # GET done/<int:pk>/
        done = get_object_or_404(Todo, id =pk)
        # 전송된 데이터의 유효성 검사
        # 객체가 없다면 404 오류 발생
        done.complete = True
        # 완료한 항목이라면
        done.save()
        # modelserializer의 역직렬화를 통해 save
        serializer = TodoDetailSerializer(done)
        # serializer에 done 모델 전달해 직렬화
        return Response(status=status.HTTP_200_OK)
        # 직렬화된 내용 중 data와 상태코드를 응답으로 전달