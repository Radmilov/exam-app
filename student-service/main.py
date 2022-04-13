from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, Field, Migrator
from starlette.requests import Request
import requests
from starlette.responses import StreamingResponse

from graphics import produceGraphForStudentAndExams

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-18710.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port=18710,
    password="wSwPm59ziVM5z53sKwC8WmcIqF9JkAm2",
    decode_responses=True
)

Migrator().run()


class Student(HashModel):
    name: str = Field(index=True, full_text_search=True)
    index: int = Field(index=True)
    address: str
    programme: str

    class Meta:
        database = redis


@app.get('/students')
def all():
    return [format(pk) for pk in Student.all_pks()]

def format(pk: str):
    student = Student.get(pk)

    return {
        'id': student.pk,
        'index': student.index,
        'name': student.name,
        'address': student.address,
        'programme': student.programme
    }


@app.post('/students')
def create(obj: Student):
    return obj.save()


@app.get('/students/{pk}')
def get(pk: str):
    return Student.get(pk)


@app.delete('/students/{pk}')
def delete(pk: str):
    return Student.delete(pk)

@app.post('/students/graph')
async def get_graph_by_student_name(req: Request):
    body = await req.json()
    print(body['index'])
    student = Student.find(Student.index == body['index']).first()
    req = requests.get("http://localhost:8001/getExamsByStudentId/%s" % student.pk)
    exams = req.json()
    exams_dict = {}
    print(exams)
    for exam in exams:
        req = requests.get("http://localhost:8002/courses/%s" % exam['course_id'])
        req = req.json()
        exam['course'] = req['name']
        exams_dict[exam['course']] = exam['grade']
    print(exams_dict)
    buf = produceGraphForStudentAndExams(exams_dict)
    return StreamingResponse(buf, media_type="image/png")



