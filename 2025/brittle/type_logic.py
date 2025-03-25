OFFENSIVE_WORDS = [
    "badword1",
    "badword2",
    "offensive",
]


def process_content(content):
    if isinstance(content, str):
        for word in OFFENSIVE_WORDS:
            if word in content:
                return {"type": "text", "status": "flagged"}
        return {"type": "text", "status": "approved"}

    elif isinstance(content, dict):
        if "image_url" in content:
            if content.get("is_inappropriate", False):
                return {"type": "image", "status": "flagged"}
            return {"type": "image", "status": "approved"}
        elif "user_report" in content:
            severity = content.get("severity", "low")

            if severity == "high":
                return {"type": "report", "action": "ban user"}
            elif severity == "medium":
                return {"type": "report", "action": "flag content"}
            return {"type": "report", "action": "review"}

    elif isinstance(content, list):
        for word in content:
            if word in OFFENSIVE_WORDS:
                return {"type": "audio", "status": "flagged"}
        return {"type": "audio", "status": "approved"}

    else:
        return {"type": "unknown", "status": "error"}


def main() -> None:
    # Text content
    text_content = "This is a badword1 example"
    result = process_content(text_content)
    print(result)

    # Image content
    image_content = {
        "image_url": "https://example.com/image.jpg",
        "is_inappropriate": True,
    }
    result = process_content(image_content)
    print(result)

    # Report content
    report_content = {"user_report": "Spam", "severity": "high"}
    result = process_content(report_content)
    print(result)

    # Audio content
    audio_content = ["good", "badword2", "nice"]
    result = process_content(audio_content)
    print(result)

    # Unknown content
    unknown_content = 123
    result = process_content(unknown_content)
    print(result)


if __name__ == "__main__":
    main()
