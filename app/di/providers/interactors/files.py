from dishka import Provider, Scope, provide_all

from app.interactors.files.save import SaveFileInteractor
from app.interactors.files.delete import DeleteFileInteractor


class FilesInteractorProvider(Provider):
    scope = Scope.REQUEST

    interactors = provide_all(
        SaveFileInteractor,
        DeleteFileInteractor,
    )
