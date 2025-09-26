from app.di.providers.interactors.answers import AnswersInteractorProvider
from app.di.providers.interactors.surveys import SurveysInteractorProvider
from app.di.providers.interactors.files import FilesInteractorProvider

all_interactors = [
    AnswersInteractorProvider(),
    SurveysInteractorProvider(),
    FilesInteractorProvider(),
]
