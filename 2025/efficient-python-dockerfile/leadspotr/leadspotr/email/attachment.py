from abc import ABC, abstractmethod

from sendgrid.helpers.mail import Attachment as SendgridAttachment


class Attachment(ABC):
    """
    Abstract class for email attachment
    """

    @abstractmethod
    def get_content(self) -> str | None: ...

    @abstractmethod
    def get_filename(self) -> str | None: ...

    @abstractmethod
    def get_file_type(self) -> str | None: ...

    @abstractmethod
    def get_disposition(self) -> str | None: ...


class SendGridAttachmentWrapper(Attachment):
    """
    Wrapper class for SendGrid attachment
    """

    def __init__(
        self,
        file_content: str | None,
        file_name: str | None,
        file_type: str | None,
        disposition: str | None,
    ):
        self.attachment = SendgridAttachment(
            file_content=file_content,
            file_name=file_name,
            file_type=file_type,
            disposition=disposition,
        )

    def get_content(self) -> str | None:
        content = self.attachment.file_content

        if content is not None:
            return content.get()  # type: ignore

        return None

    def get_filename(self) -> str | None:
        file_name = self.attachment.file_name

        if file_name is not None:
            return file_name.get()  # type: ignore

        return None

    def get_file_type(self) -> str | None:
        file_type = self.attachment.file_type

        if file_type is not None:
            return file_type.get()  # type: ignore

        return None

    def get_disposition(self) -> str | None:
        disposition = self.attachment.disposition

        if disposition is not None:
            return disposition.get()  # type: ignore

        return None
