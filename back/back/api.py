from ninja import NinjaAPI
from home.models import QuizPage
from ninja import Schema

api = NinjaAPI()

class QuizShema(Schema):
    id: int
    title: str

@api.get("/quiz", response=QuizShema)
def get_quiz(request):
    quiz = QuizPage.objects.first()
    return quiz
