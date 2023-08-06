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

from abc import ABC, abstractmethod
from http import HTTPStatus as HTTP
from typing import Any


class HttpPresenter(ABC):
    @abstractmethod
    def status_code(self) -> int:
        ...

    @abstractmethod
    def headers(self) -> dict[str, str]:
        ...

    @abstractmethod
    def data(self) -> str:
        ...


class HttpMeta:
    def __init__(
        self,
        content_type: str,
        /,
        *,
        status: int = HTTP.OK,
        is_logged_in: bool = False,
        is_htmx: bool = False,
    ) -> None:
        self.__status_code: int = status
        self.__headers: dict[str, Any] = {"Content-Type": content_type}
        self.__is_logged_in = is_logged_in
        self.__is_htmx = is_htmx

    def see_other(self, target: str, /, *, permanent: bool = False) -> None:
        self.__status_code = HTTP.MOVED_PERMANENTLY if permanent else HTTP.SEE_OTHER

        if "Content-Type" in self.__headers:
            del self.__headers["Content-Type"]

        if self.__is_htmx:
            self.__headers["HX-Location"] = target
        else:
            self.__headers["Location"] = target

    def bad_request(self) -> None:
        self.__status_code = HTTP.BAD_REQUEST

    def not_authorized(self) -> None:
        if self.__is_logged_in:
            self.__status_code = HTTP.FORBIDDEN
        else:
            self.__status_code = HTTP.UNAUTHORIZED

    def status_code(self) -> int:
        # TODO set status only if not htmx, for it only handles 2xx and 3xx
        return self.__status_code

    def headers(self) -> dict[str, Any]:
        # Disable cache for htmx requests
        if self.__is_htmx:
            self.__headers["Cache-Control"] = "no-store, max-age=0"
        return self.__headers


class Redirection(HttpPresenter):
    def __init__(self, cible: str, code_statut: HTTP = HTTP.SEE_OTHER) -> None:
        self.__cible = cible
        self.__code_statut = code_statut

    def status_code(self) -> int:
        return self.__code_statut

    def headers(self) -> dict[str, str]:
        return {"Location": self.__cible}

    def data(self) -> str:
        return ""
