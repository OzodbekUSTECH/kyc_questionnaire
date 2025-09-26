from dishka import Provider, Scope, provide_all
from app.interactors.answers.create import CreateAnswerInteractor
from app.interactors.answers.update import UpdateAnswerPartiallyInteractor
from app.interactors.answers.get import GetAllAnswersInteractor, GetAnswerByIdInteractor
from app.interactors.answers.delete import DeleteAnswerInteractor


class AnswersInteractorProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(
        CreateAnswerInteractor,
        UpdateAnswerPartiallyInteractor,
        GetAllAnswersInteractor,
        GetAnswerByIdInteractor,
        DeleteAnswerInteractor,
    )
