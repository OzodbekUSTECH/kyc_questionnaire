from dishka import Provider, Scope, provide_all


class ServicesProvider(Provider):

    scope = Scope.REQUEST

    services = provide_all()