from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import openpyxl

from .models import Student
from .serializers import StudentSerializer


# 📌 GET all students / POST new student
@api_view(['GET', 'POST'])
def student_list_create(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 📌 UPDATE or DELETE a student
@api_view(['PUT', 'DELETE'])
def student_update_delete(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 📥 EXPORT STUDENTS TO EXCEL
@api_view(['GET'])
def export_students_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Students"

    # Header row
    headers = ["ID", "Name", "Roll Number", "Email", "Department"]
    sheet.append(headers)

    # Student data
    students = Student.objects.all()
    for student in students:
        sheet.append([
            student.id,
            student.name,
            student.roll_number,
            student.email,
            student.department,
        ])

    # Create downloadable response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=students.xlsx"

    workbook.save(response)
    return response
