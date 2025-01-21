def process_content(content):
    if isinstance(content, str):
        offensive_words = [
            "badword1",
            "badword2",
            "offensive",
        ]
        for word in offensive_words:
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
        offensive_words = [
            "badword1",
            "badword2",
            "offensive",
        ]
        for word in content:
            if word in offensive_words:
                return {"type": "audio", "status": "flagged"}
        return {"type": "audio", "status": "approved"}

    else:
        return {"type": "unknown", "status": "error"}
