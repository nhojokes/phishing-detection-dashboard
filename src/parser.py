import email
from email.policy import default
from typing import Dict, Any

class EmailParser:
    """Parses raw text and uploaded .eml files into structured components."""
    
    @staticmethod
    def parse_raw(sender: str, subject: str, body: str) -> Dict[str, Any]:
        return {
            "sender": sender.strip(),
            "subject": subject.strip(),
            "body": body.strip(),
            "headers": {}
        }
    
    @staticmethod
    def parse_eml_file(file_bytes: bytes) -> Dict[str, Any]:
        msg = email.message_from_bytes(file_bytes, policy=default)
        sender = msg.get("From", "")
        subject = msg.get("Subject", "")
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")
            
        headers = {k: v for k, v in msg.items()}
        return {
            "sender": sender,
            "subject": subject,
            "body": body,
            "headers": headers
        }