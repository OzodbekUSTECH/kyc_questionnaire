from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from app.di.providers.db import DBProvider
from app.di.providers.repositories import RepositoriesProvider
from app.di.providers.services import ServicesProvider
from app.di.providers.interactors import all_interactors

providers = [
    FastapiProvider(),
    DBProvider(),
    RepositoriesProvider(),
    ServicesProvider(),
    *all_interactors,
]


app_container = make_async_container(*providers)

