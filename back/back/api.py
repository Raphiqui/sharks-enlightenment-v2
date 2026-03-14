from ninja import NinjaAPI
from typing import Any, List
from home.models import QuizPage
from ninja import Schema
from pydantic import model_validator

api = NinjaAPI()


class ResponseSchema(Schema):
    response: str
    is_correct: bool


class QuestionSchema(Schema):
    question: str
    responses: List[ResponseSchema]
    explanation: str


class QuizSchema(Schema):
    questions: List[QuestionSchema]

    @model_validator(mode="before")
    @classmethod
    def extract_quiz_data(cls, data):
        if hasattr(data, "quiz"):
            questions = []
            for block in data.quiz:

                for question_struct in block.value:

                    responses = []

                    for resp_block in question_struct["responses"]:
                        responses.append(
                            {
                                "response": resp_block.value["response"],
                                "is_correct": resp_block.value["is_correct"],
                            }
                        )

                    questions.append(
                        {
                            "question": question_struct["question"],
                            "responses": responses,
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
