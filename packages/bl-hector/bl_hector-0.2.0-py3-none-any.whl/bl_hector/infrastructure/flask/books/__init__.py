# Hector --- A collection manager.
# Copyright © 2023 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from typing import Any

from flask import Blueprint, flash, get_flashed_messages, request

from bl_hector.application.use_cases import (
    add_book,
    display_book,
    look_up_book,
    search_books,
    update_book,
)
from bl_hector.infrastructure.flask import services
from bl_hector.infrastructure.flask.utils import htmx, presenter_to_response
from bl_hector.interfaces import from_dict as controllers
from bl_hector.interfaces.to_http import as_html as presenters

blueprint = Blueprint("books", __name__)


def notify(message: str, type: str) -> None:
    get_flashed_messages()  # FIXME… wtf?!
    flash(message, type)


@blueprint.get("")
@presenter_to_response
def search() -> Any:
    presenter = presenters.SearchBooks(
        request.args, htmx(request).target, user=services.get_user()
    )
    interactor = search_books.Interactor(presenter, services.get_books())
    controller = controllers.SearchBooks(request.args)
    controller.call(interactor)
    return presenter


@blueprint.post("@<string:attribute>")
@presenter_to_response
def validate(attribute: str) -> Any:
    return presenters.ValidateBook(
        attribute, request.form.get(attribute, ""), user=services.get_user()
    )


@blueprint.get("__new__")
@presenter_to_response
def add() -> Any:
    return presenters.AddBook(
        request.form, htmx(request).target, notify, user=services.get_user()
    )


@blueprint.post("__new__")
@presenter_to_response
def add_POST() -> Any:
    presenter = presenters.AddBook(
        request.form,
        htmx(request).target,
        notify,
        user=services.get_user(),
    )
    interactor = add_book.Interactor(
        presenter,
        services.get_books(),
        services.get_calendar(),
        services.get_permissions(),
    )
    controller = controllers.AddBook(request.form, str(services.get_user().id))
    controller.call(interactor)
    return presenter


@blueprint.post("__info__")
@presenter_to_response
def look_up() -> Any:
    presenter = presenters.LookUpBook(user=services.get_user())
    interactor = look_up_book.Interactor(
        presenter, services.get_book_info_provider(), services.get_cover_provider()
    )
    interactor.execute(look_up_book.Request(request.form.get("isbn", "")))
    return presenter


@blueprint.get("<string:isbn>")
@presenter_to_response
def display(isbn: str) -> Any:
    presenter = presenters.DisplayBook(notify, user=services.get_user())
    interactor = display_book.Interactor(presenter, services.get_books())
    interactor.execute(display_book.Request(isbn))
    return presenter


@blueprint.get("<string:isbn>/__update__")
@presenter_to_response
def update(isbn: str) -> Any:
    presenter = presenters.DisplayBookToUpdate(isbn, notify, user=services.get_user())
    interactor = display_book.Interactor(presenter, services.get_books())
    interactor.execute(display_book.Request(isbn))
    return presenter


@blueprint.post("<string:isbn>/__update__")
@presenter_to_response
def update_POST(isbn: str) -> Any:
    presenter = presenters.UpdateBook(
        isbn, request.form, htmx(request).target, notify, user=services.get_user()
    )
    interactor = update_book.Interactor(
        presenter,
        services.get_books(),
        services.get_calendar(),
        services.get_permissions(),
    )
    controller = controllers.UpdateBook(isbn, request.form, str(services.get_user().id))
    controller.call(interactor)
    return presenter
