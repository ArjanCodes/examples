import rustimport.import_hook
from pyo3_rust_simple import Attachment, AttachmentType, Email


def main():
    attachment = Attachment("attachment.txt", AttachmentType.File)
    print(attachment)
    email = Email("This is the subject", "This is the body", [attachment])
    print(email)
    email.send("Example@ArjanCodes.com")


if __name__ == "__main__":
    main()
