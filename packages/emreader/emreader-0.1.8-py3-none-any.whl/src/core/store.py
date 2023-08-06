import os
from filestorage.handlers import LocalFileHandler
from filestorage import StorageContainer

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_store():
    handler = LocalFileHandler(os.path.join(base_dir, "db"))
    my_store = StorageContainer()
    my_store.handler = handler
    return my_store


def emails_folder():
    storage = get_store()
    folder = storage / "emails"
    return folder


def pdf_folder():
    storage = get_store()
    folder = storage / "pdf"
    return folder


store = get_store()
pdfs = pdf_folder()
emails = emails_folder()
