from dishka import Provider, Scope, provide_all

from app.interactors.surveys.create import CreateSurveyInteractor
from app.interactors.surveys.get import GetAllSurveysInteractor, GetSurveyByIdInteractor
from app.interactors.surveys.update import UpdateSurveyPartiallyInteractor
from app.interactors.surveys.delete import DeleteSurveyInteractor


class SurveysInteractorProvider(Provider):
    scope = Scope.REQUEST
        
    interactors = provide_all(
        CreateSurveyInteractor,
        GetAllSurveysInteractor,
        GetSurveyByIdInteractor,
        UpdateSurveyPartiallyInteractor,
        DeleteSurveyInteractor,
    )
