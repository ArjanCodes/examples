from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

DEFAULT_EMAIL = "support@arjancodes.com"
LOGIN = "test"
PASSWORD = "my_password"


class EmailClient:
    def __init__(
        self,
        smtp_server: str,
        credentials: tuple[str, str] = (LOGIN, PASSWORD),
        name: str = "",
        to_address: str = DEFAULT_EMAIL,
    ):
        self._server = SMTP()
        self._server._host = smtp_server  # type: ignore
        self._host, _port = smtp_server.split(":")
        self._port = int(_port)
        self._login, self._password = credentials
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
        to_address: str | None = None,
        subject: str = "No subject",
        message: str = "",
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = from_address
        msg["To"] = to_address or self.to_address
        msg["Subject"] = subject
        mime = MIMEText(
            message,
            "html" if message.lower().startswith("<!doctype html>") else "plain",
        )
        msg.attach(mime)

        self._connect()
        self._server.sendmail(msg["From"], msg["To"], msg.as_string())
        self._quit()
