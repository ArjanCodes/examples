from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Protocol

DEFAULT_EMAIL = "support@arjancodes.com"
LOGIN = "admin"
PASSWORD = "admin"


class EmailServer(Protocol):
    @property
    def _host(self) -> str:
        ...

    def connect(self, host: str, port: int) -> None:
        ...

    def starttls(self) -> None:
        ...

    def login(self, login: str, password: str) -> None:
        ...

    def quit(self) -> None:
        ...

    def sendmail(self, from_address: str, to_address: str, message: str) -> None:
        ...


class EmailClient:
    def __init__(
        self,
        smtp_server: EmailServer,
        login: str | None = None,
        password: str | None = None,
        name: str | None = None,
        to_address: str = DEFAULT_EMAIL,
    ):
        self._server = smtp_server
        host, port = str(smtp_server._host).split(":")  # type: ignore
        self._host: str = host
        self._port = int(port)
        if not login or not password:
            self._login, self._password = LOGIN, PASSWORD
        else:
            self._login, self._password = login, password
        self.name = name
        self.to_address = to_address

    def _connect(self) -> None:
        self._server.connect(self._host, self._port)
        self._server.starttls()
        self._server.login(self._login, self._password)

    def _quit(self) -> None:
        self._server.quit()

    def send_message(
        self,
        from_address: str,
        to_address: str,
        subject: str = "No subject",
        message: str = "",
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = from_address
        if not to_address:
            to_address = self.to_address
        msg["To"] = to_address
        msg["Subject"] = subject
        mime = MIMEText(
            message,
            "html" if message.lower().startswith("<!doctype html>") else "plain",
        )
        msg.attach(mime)

        self._connect()
        self._server.sendmail(from_address, to_address, msg.as_string())
        self._quit()
