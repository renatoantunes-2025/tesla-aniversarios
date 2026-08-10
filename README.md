# Aviso automatico de aniversarios - Tesla Brasil

## O que faz

Todo dia, o robo verifica a lista de funcionarios (`employees.csv`) e:

- **3 dias antes** do aniversario de alguem: envia um e-mail de aviso para `socios@tesla.com.br`.
- **No dia** do aniversario: envia um e-mail de parabens para o proprio funcionario (precisa do e-mail dele cadastrado).

Envia pela conta `renato.antunes@tesla.com.br`.

## Arquivos

- `employees.csv` - lista de funcionarios (Nome, Nascimento, Email). **Preencha a coluna Email** de cada funcionario antes de usar; sem isso, o e-mail de parabens nao pode ser enviado para essa pessoa.
- `birthday_check.py` - script que faz a checagem e envia os e-mails.
- `birthday-check.yml` - workflow do GitHub Actions que roda o script todo dia. **Deve ser movido** para o caminho `.github/workflows/birthday-check.yml` dentro do repositorio.

## Passo a passo para colocar no ar

1. **Crie um repositorio privado** no GitHub (ex: `tesla-aniversarios`).
2. Suba os 3 arquivos para o repositorio, colocando o `birthday-check.yml` dentro da pasta `.github/workflows/` (crie essas pastas).
3. **Gere uma senha de app do Gmail** na conta `renato.antunes@tesla.com.br`:
   - Ative a verificacao em duas etapas em https://myaccount.google.com/security (se ainda nao tiver).
   - Va em https://myaccount.google.com/apppasswords e gere uma senha de app para "Mail".
   - Guarde essa senha (16 caracteres) - ela sera usada no lugar da sua senha normal.
4. **Configure os secrets no repositorio**: Settings > Secrets and variables > Actions > New repository secret. Crie 3:
   - `GMAIL_USER` = `renato.antunes@tesla.com.br`
   - `GMAIL_APP_PASSWORD` = a senha de app gerada no passo 3
   - `HR_EMAIL` = `socios@tesla.com.br`
5. Pronto. O workflow roda automaticamente todo dia as 08h (horario de Brasilia). Para testar na hora, va na aba **Actions** do repositorio, escolha "Aviso de Aniversarios" e clique em **Run workflow**.

## Seguranca

- Mantenha o repositorio **privado** e com acesso restrito.
- A senha de app do Gmail so tem permissao de enviar e-mail (nao acessa a conta inteira).
- Os secrets do GitHub Actions sao criptografados e nao aparecem nos logs.
- Como a planilha tem nome e data de nascimento de funcionarios (dado pessoal, sob LGPD), evite dar acesso ao repositorio para quem nao precisa.
