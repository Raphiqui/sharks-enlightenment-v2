from ninja import NinjaAPI
from typing import List
from home.models import QuizPage
from ninja import Schema
from pydantic import model_validator

api = NinjaAPI()


class OptionSchema(Schema):
    option: str
    is_correct: bool


class QuestionSchema(Schema):
    id: int
    question: str
    options: List[OptionSchema]
    explanation: str


class QuizSchema(Schema):
    questions: List[QuestionSchema]

    @model_validator(mode="before")
    @classmethod
    def extract_quiz_data(cls, data):
        if hasattr(data, "quiz"):
            questions = []
            for index, block in enumerate(data.quiz):

                for question_struct in block.value:

                    options = []

                    for opt_block in question_struct["options"]:
                        options.append(
                            {
                                "option": opt_block.value["option"],
                                "is_correct": opt_block.value["is_correct"],
                            }
                        )

                    questions.append(
                        {
                            "id": index,
                            "question": question_struct["question"],
                            "options": options,
                            "explanation": question_struct["answer"],
                        }
                    )

            return {
                "questions": questions,
            }
        return data


@api.get("/quiz", response=QuizSchema)
def get_quiz(request):
    quiz = QuizPage.objects.first()
    return quiz
