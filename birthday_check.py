"""
Verifica aniversarios de funcionarios e envia e-mails via Gmail:
  - 3 dias antes, 2 dias antes e no dia do aniversario: aviso para o RH/socios (HR_EMAIL)
  - No dia do aniversario: e-mail de parabens para o proprio funcionario

Le os dados de employees.csv (colunas: Nome, Nascimento [DD/MM/AAAA], Email).

Variaveis de ambiente necessarias:
  GMAIL_USER          - conta Gmail que envia os e-mails
  GMAIL_APP_PASSWORD  - senha de app gerada na conta acima
  HR_EMAIL             - e-mail que recebe o aviso antecipado (default: socios@tesla.com.br)
"""

import csv
import os
import smtplib
import ssl
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
HR_EMAIL = os.environ.get("HR_EMAIL", "socios@tesla.com.br")
CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.csv")


def send_email(to_addr, subject, body):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls(context=context)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, to_addr, msg.as_string())
    print(f"E-mail enviado para {to_addr}: {subject}")


def load_employees():
    employees = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row["Nome"].strip()
            nascimento = row["Nascimento"].strip()  # DD/MM/AAAA
            email = (row.get("Email") or "").strip()
            dia, mes, ano = nascimento.split("/")
            employees.append(
                {
                    "nome": nome,
                    "dia": int(dia),
                    "mes": int(mes),
                    "ano": int(ano),
                    "email": email,
                }
            )
    return employees


def main():
    today = date.today()

    employees = load_employees()
    avisos_enviados = 0
    parabens_enviados = 0

    # Avisos ao RH: 3 dias antes, 2 dias antes e no dia
    for offset in (3, 2, 0):
        alvo = today + timedelta(days=offset)
        for emp in employees:
            if emp["dia"] == alvo.day and emp["mes"] == alvo.month:
                idade = alvo.year - emp["ano"]
                if offset == 0:
                    quando = "hoje"
                elif offset == 1:
                    quando = "amanha"
                else:
                    quando = f"em {offset} dias"
                assunto = f"Aviso: aniversario de {emp['nome']} {quando} ({alvo.strftime('%d/%m')})"
                corpo = (
                    f"Ola,\n\n"
                    f"O funcionario {emp['nome']} faz aniversario {quando}, no dia "
                    f"{alvo.strftime('%d/%m/%Y')} (completa {idade} anos).\n\n"
                    f"Este e um aviso automatico."
                )
                send_email(HR_EMAIL, assunto, corpo)
                avisos_enviados += 1

    for emp in employees:
        # No dia -> parabens para o proprio funcionario
        if emp["dia"] == today.day and emp["mes"] == today.month:
            if emp["email"]:
                primeiro_nome = emp["nome"].split()[0].title()
                assunto = f"Feliz aniversario, {primeiro_nome}!"
                corpo = (
                    f"Ola {primeiro_nome},\n\n"
                    f"Hoje e um dia especial e nao poderiamos deixa-lo passar em branco!\n\n"
                    f"Toda a equipe da Tesla Brasil se une para desejar a voce um feliz "
                    f"aniversario. Obrigado por fazer parte da nossa jornada e contribuir, "
                    f"todos os dias, com seu talento e dedicacao.\n\n"
                    f"Que este novo ciclo seja repleto de conquistas, saude e momentos "
                    f"inesqueciveis, dentro e fora do trabalho.\n\n"
                    f"Aproveite o seu dia!\n\n"
                    f"Com carinho,\n"
                    f"Diretoria - Tesla Brasil"
                )
                send_email(emp["email"], assunto, corpo)
                parabens_enviados += 1
            else:
                print(
                    f"Aviso: {emp['nome']} faz aniversario hoje mas nao tem "
                    f"e-mail cadastrado em employees.csv."
                )

    print(
        f"Concluido. Avisos ao RH enviados: {avisos_enviados}. "
        f"Parabens enviados: {parabens_enviados}."
    )


if __name__ == "__main__":
    main()
