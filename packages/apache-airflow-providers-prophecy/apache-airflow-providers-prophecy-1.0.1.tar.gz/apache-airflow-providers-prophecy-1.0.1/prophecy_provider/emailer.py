import smtplib
from typing import Any, Dict, Iterable, List, Union

from airflow.utils.email import build_mime_message
from airflow.configuration import conf
from airflow.hooks.base import BaseHook


def send_email(
    to: Union[List[str], Iterable[str]],
    subject: str,
    html_content: str,
    files: Union[List[str], None] = None,
    dryrun: bool = False,
    cc: Union[str, Iterable[str], None] = None,
    bcc: Union[str, Iterable[str], None] = None,
    mime_subtype: str = 'mixed',
    mime_charset: str = 'utf-8',
    conn_id: Union[str, None] = None,
    custom_headers: Union[Dict[str, Any], None] = None,
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
