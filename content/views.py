from django.core.exceptions import ValidationError
from rest_framework.views import APIView, Request, Response, status
from django.forms.models import model_to_dict

from .models import Content

# Create your views here.

class ContentsRoutes(APIView):
    def get(self, request: Request) -> Response:
        courses = Content.objects.all()

        courses_list = []

        for course in courses:
            courses_dict = model_to_dict(course)
            courses_list.append(courses_dict)
        return Response(courses_list)
    
    def post(self, request: Request) -> Response:
        course = Content(**request.data)

        try:
            course.full_clean()
            
        except ValidationError as err:
            print(request.data)

            cd = model_to_dict(course)

            response_object1 = {
                "title": "missing key",
                "module": "missing key",
                "description": "missing key",
                "students": "missing key",
                "is_active": "missing key"
            }

            if not request.data:
                return Response(response_object1, status.HTTP_400_BAD_REQUEST)

            title = type(request.data['title']) == str
            module = type(request.data['module']) == str
            description = type(request.data['description']) == str
            students = type(request.data['students']) == int
            is_active = type(request.data['is_active']) == bool

                  

            response_object2 = {
                "title": "must be a str",
                "module": "must be a str",
                "description": "must be a str",
                "students": "must be a int",
                "is_active": "must be a bool"
            }

            if not title or not module or not description or not students or not is_active:
                return Response(response_object2, status.HTTP_400_BAD_REQUEST)
        
        course.save()
        courses_dict = model_to_dict(course)
        return Response(courses_dict, status.HTTP_201_CREATED)

class ContentsById(APIView):
    def get(self, request: Request, course_id: int) -> Response:
        try:
            course = Content.objects.get(id = course_id)
        
        except Content.DoesNotExist:
            return Response({"message": "Content not found."}, status.HTTP_404_NOT_FOUND)
        
        courses_dict = model_to_dict(course)

        return Response(courses_dict)

    def patch(self, request: Request, course_id: int) -> Response:
        try:
            course = Content.objects.get(id = course_id)
        
        except Content.DoesNotExist:
            return Response({"message": "Content not found."}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(course, key, value)

        course.save()
        courses_dict = model_to_dict(course)

        return Response(courses_dict)
    
    def delete(self, request: Request, course_id: int) -> Response:
        try:
            course = Content.objects.get(id = course_id)
        
        except Content.DoesNotExist:
            return Response({"message": "Content not found."}, status.HTTP_404_NOT_FOUND)

        course.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

class ContentsFilter(APIView):
    def get(self, request: Request) -> Response:
        title = request.query_params.get('title', None)

        print(title)

        filtered_courses = Content.objects.filter(title__contains=title)
        
        courses_list = [model_to_dict(course) for course in filtered_courses]
        return Response(courses_list)