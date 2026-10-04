from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from pydantic import model_validator
from wagtail.models import Locale

from home.models import QuizPage

api = NinjaAPI()


class OptionSchema(Schema):
    option: str
    is_correct: bool


class QuestionSchema(Schema):
    id: int
    question: str
    options: list[OptionSchema]
    explanation: str


class QuizSchema(Schema):
    questions: list[QuestionSchema]

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
def get_quiz(request, lang: str | None = None):
    # The API lives outside i18n_patterns, so the frontend passes the page language
    # explicitly. Fall back to the default locale when there's no translation yet.
    quizzes = QuizPage.objects.live()
    quiz = None
    if lang:
        quiz = quizzes.filter(locale__language_code=lang).first()
    if not quiz:
        quiz = quizzes.filter(locale=Locale.get_default()).first()

    if not quiz:
        raise HttpError(404, "No Quiz page found")

    return quiz
