from dishka import Provider, Scope, provide_all

from app.repositories.uow import UnitOfWork
from app.repositories.surveys import SurveysRepository
from app.repositories.answers import AnswersRepository




class RepositoriesProvider(Provider):

    scope = Scope.REQUEST

    repositories = provide_all(
        UnitOfWork,
        SurveysRepository,
        AnswersRepository,
    )
