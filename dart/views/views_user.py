from ..models import User
from ..serializers import RegisterSerializer, UserSerializer

from rest_framework import generics
from rest_framework.response import Response

# 회원가입
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# # jwt token 결과 커스텀 
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
#     # response 커스텀 
#     default_error_messages = {
#         'no_active_account': {'message':'username or password is incorrect!',
#                               'success': False,
#                               'status' : 401}
#     }
#     # 유효성 검사
#     def validate(self, attrs):
#         data = super().validate(attrs)
        
#         refresh = self.get_token(self.user)
        
#          # response에 추가하고 싶은 key값들 추가
#         data['username'] = self.user.username
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['success'] = True
        
#         return data


# class MyTokenObtainPairView(TokenObtainPairView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer