from services.excel_reader import read_contacts
from services.template_engine import render_template
from services.logger import log_result

from senders.gmail_sender import send_email
from senders.whatsapp_sender import send_whatsapp
from senders.instagram_sender import send_instagram_dm


contacts = read_contacts("data/contacts.xlsx")

for contact in contacts:
    if contact.get("status") == "sent":
        continue

    channel = contact["channel"]

    try:
        if channel == "email":
            message = render_template("templates/email_template.txt", contact)
            send_email(
                to=contact["email"],
                subject=f"Quick reach out to {contact['company_name']}",
                body=message
            )

        elif channel == "whatsapp":
            message = render_template("templates/whatsapp_template.txt", contact)
            send_whatsapp(
                phone=contact["whatsapp"],
                message=message
            )

        elif channel == "instagram":
            message = render_template("templates/instagram_template.txt", contact)
            send_instagram_dm(
                instagram_id=contact["instagram_id"],
                message=message
            )

        log_result(contact, "sent", "")

    except Exception as e:
        log_result(contact, "failed", str(e))