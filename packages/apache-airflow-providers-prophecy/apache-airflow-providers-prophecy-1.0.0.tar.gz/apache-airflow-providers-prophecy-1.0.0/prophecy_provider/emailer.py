import smtplib
import logging
from typing import Iterable, Any

from airflow.utils.email import build_mime_message
from airflow.configuration import conf
from airflow.hooks.base import BaseHook

log = logging.getLogger(__name__)


def send_email(
        to: list[str] | Iterable[str],
        subject: str,
        html_content: str,
        files: list[str] | None = None,
        dryrun: bool = False,
        cc: str | Iterable[str] | None = None,
        bcc: str | Iterable[str] | None = None,
        mime_subtype: str = 'mixed',
        mime_charset: str = 'utf-8',
        conn_id: str | None = None,
        custom_headers: dict[str, Any] | None = None,
        **kwargs,
):
    backend_conn_id = conn_id or conf.get("email", "email_conn_id", fallback=None)
    from_email = conf.get('email', 'from_email', fallback=None)

    if backend_conn_id is None:
        raise Exception(
            "Please set email.email_conn_id Airflow configuration"
        )
    if from_email is None:
        raise Exception(
            "Please set email.from_email Airflow configuration"
        )

    msg, recipients = build_mime_message(
        mail_from=from_email,
        to=to,
        subject=subject,
        html_content=html_content,
        files=files,
        cc=cc,
        bcc=bcc,
        mime_subtype=mime_subtype,
        mime_charset=mime_charset,
        custom_headers=custom_headers,
    )

    airflow_conn = BaseHook.get_connection(backend_conn_id)
    smtp_host = airflow_conn.host
    smtp_port = airflow_conn.port
    smtp_user = airflow_conn.login
    smtp_password = airflow_conn.password
    server = smtplib.SMTP(smtp_host, smtp_port, source_address=("0.0.0.0", 0))
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, recipients, msg.as_string())
    server.quit()
