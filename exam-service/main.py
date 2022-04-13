from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, Migrator, Field
from starlette.requests import Request

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


class Exam(HashModel):
    date: str
    student_id: str = Field(index=True)
    course_id: str = Field(index=True)
    grade: int
    passed: int
    sentry: str

    class Meta:
        database = redis


@app.get('/exams')
def all():
    return [format(pk) for pk in Exam.all_pks()]

def format(pk: str):
    exam = Exam.get(pk)

    return {
        'id': exam.pk,
        'date': exam.date,
        'student_id': exam.student_id,
        'course_id': exam.course_id,
        'grade': exam.grade,
        'passed': exam.passed,
        'sentry': exam.sentry
    }


@app.post('/exams')
async def create(request: Request):  # id, quantity
    body = await request.json()

    exam = Exam(
        date=body['date'],
        student_id=body['student_id'],
        course_id=body['course_id'],
        grade=int((int(body['points']) + 9) / 10),
        passed=1 if int(body['points']) > 50 else 0,
        sentry=body['sentry']
    )
    exam.save()


    return exam


@app.get('/exams/{pk}')
def get(pk: str):
    return Exam.get(pk)

@app.get('/getExamsByStudentId/{student_pk}')
def getExamsByStudent(student_pk: str):
    Migrator().run()
    return Exam.find(Exam.student_id == student_pk).all()


@app.delete('/exams/{pk}')
def delete(pk: str):
    return Exam.delete(pk)
