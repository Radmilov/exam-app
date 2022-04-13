from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

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

class Course(HashModel):
    name: str
    professor: str
    value: int

    class Meta:
        database = redis


@app.get('/courses')
def all():
    return [format(pk) for pk in Course.all_pks()]

def format(pk: str):
    course = Course.get(pk)

    return {
        'id': course.pk,
        'name': course.name,
        'professor': course.professor,
        'value': course.value
    }


@app.post('/courses')
def create(obj: Course):
    return obj.save()


@app.get('/courses/{pk}')
def get(pk: str):
    return Course.get(pk)


@app.delete('/courses/{pk}')
def delete(pk: str):
    return Course.delete(pk)