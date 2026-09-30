"""Download INBOX without changing read flags; credentials come from environment."""

import argparse
import imaplib
import json
import os
from email import policy
from email.parser import BytesParser
from pathlib import Path


def message_text(message):
    body = message.get_body(preferencelist=("plain", "html"))
    return body.get_content() if body else ""


def download(output):
    host = os.environ["IMAP_HOST"]
    port = int(os.environ.get("IMAP_PORT", "993"))
    user = os.environ["IMAP_USER"]
    password = os.environ["IMAP_PASSWORD"]
    connection = imaplib.IMAP4 if os.environ.get("IMAP_TLS", "1") == "0" else imaplib.IMAP4_SSL
    output.mkdir(parents=True, exist_ok=True)
    with connection(host, port, timeout=30) as client:
        client.login(user, password)
        status, _ = client.select("INBOX", readonly=True)
        if status != "OK":
            raise RuntimeError("Cannot select INBOX")
        status, data = client.uid("search", None, "ALL")
        if status != "OK":
            raise RuntimeError("Cannot search INBOX")
        messages = []
        for uid in data[0].split():
            status, parts = client.uid("fetch", uid, "(BODY.PEEK[])")
            if status != "OK":
                raise RuntimeError(f"Cannot fetch UID {uid!r}")
            raw = next((part[1] for part in parts if isinstance(part, tuple)), None)
            if raw is None:
                raise RuntimeError(f"Missing message for UID {uid!r}")
            identifier = uid.decode("ascii")
            (output / f"{identifier}.eml").write_bytes(raw)
            message = BytesParser(policy=policy.default).parsebytes(raw)
            messages.append({
                "uid": identifier,
                "subject": str(message.get("Subject", "")),
                "from": str(message.get("From", "")),
                "date": str(message.get("Date", "")),
                "body": message_text(message),
            })
        (output / "messages.json").write_text(
            json.dumps(messages, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return messages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("inbox"))
    args = parser.parse_args()
    try:
        result = download(args.output)
    except (KeyError, ValueError, OSError, imaplib.IMAP4.error, RuntimeError) as error:
        parser.exit(1, f"Download failed: {error}\n")
    print(f"Downloaded {len(result)} messages to {args.output}")
