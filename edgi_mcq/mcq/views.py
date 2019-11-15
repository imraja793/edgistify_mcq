import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from numpy import random
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from mcq.decorators import user_is_admin
from mcq.models import UserProfile, AddQuestion, ApplicantMCQTest
from mcq.serializers import AddQuestionSerializer, ApplicantMCQTestSerializer

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class UserProfileList(APIView):
    """
    For registration of applicant and admin
    """
    def post(self, request):

        user = User()
        user.username = request.POST.get("username")
        user.set_password(request.POST.get("password"))
        user.first_name = request.POST.get("first_name")
        user.save()
        obj = UserProfile()
        obj.user = user
        obj.qualification = request.POST.get("qualification")

        obj.applicant = request.POST.get("applicant")  # if true applicant, else Admin
        obj.save()
        return Response("created")

    @user_is_admin
    def get(self,request):
        if User.objects.filter(username=request.GET.get("username")).exists():
            return Response("username already exist")

        return Response("valid username")


class AddQuestionApi(generics.ListCreateAPIView):
    queryset = AddQuestion.objects.all()
    serializer_class = AddQuestionSerializer


class Login(APIView):
    """
    Login api through DRFJWT
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        :param request: username, password
        :return: Jwt token along with role and user_id
        """
        if User.objects.filter(username=request.data['username']).exists():
            try:
                username = request.data['username']
                password = request.data['password']
                user = authenticate(username=username, password=password)
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                if user:

                    if user.user_profile.applicant == False:
                        context = {"token": token, "response": "success", "role": "Admin",
                                   "user_id": user.id}
                        return Response(context)

                    if user.userprofile.applicant == True:
                        context = {"token": token, "response": "success", "role": "Applicant",
                                   "user_id": user.id, "user_profile_id": user.userprofile.id}
                        return Response(context)
            except:
                context = {'response': "Password is not correct"}
                return Response(context)
        context = {'response': "Email is invalid"}
        return Response(context)


class ApplicantResponse(APIView):

    def post(self, request):
        try:
            save_data = ApplicantMCQTest
            save_data.applicant_id = request.user.id
            question_response = json.loads(request.data["response"])
            save_data.response = question_response
            assessment_score = 0
            for question, answer in question_response.items():
                if answer['answer'] is None:
                    pass
                else:
                    if answer['correct_ans'] == answer['answer']:
                        assessment_score += 1
            save_data.mark_scored = assessment_score
            save_data.save()
            return Response("Successfully Saved", status=status.HTTP_200_OK)
        except:
            return Response("Please contact administrator")


class ApplicantMCQTestApi(generics.ListAPIView):
    queryset = ApplicantMCQTest.objects.all()
    serializer_class = ApplicantMCQTestSerializer


class GetQuestion(APIView):
    def post(self, request):
        object = AddQuestion.objects.all()
        question_id_list = list(object.values_list("id", flat=True))
        try:
            random_ids = random.sample(question_id_list, 10)
            querryset = object.filter(id__in=random_ids)
            serializer = AddQuestionSerializer(querryset, many=True)
            return Response(serializer.data)
        except:
            return Response("required number of questions are not present"
                            " in the db kindly add the data first")

