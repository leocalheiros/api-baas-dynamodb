# API BaaS DynamoDB

## Descrição do Projeto

A API BaaS DynamoDB implementa um sistema bancário simples com autenticação JWT e funcionalidades como criar contas de usuário, excluir contas de usuário, consultar contas de usuário, realizar operações de saldo como depósito, transferência e saque, , também gerar códigos pix copia e cola, vincular cartões de crédito ao email do usuário, criar pagamentos fictícios, e deletar o cartão de crédito vinculado. O projeto foi feito para ser implementado em uma lambda, contendo os arquivos de configuração "samconfig.toml" e "template.yaml"


## Configuração do Ambiente

Antes de executar o projeto, certifique-se de ter as seguintes dependências instaladas:

```bash
pip install -r requirements.txt
```

Como o projeto foi feito para rodar em uma lambda, não temos um arquivo de inicialização, porém fique a vontade para criar e testar localmente.
Caso implemente no lambda, crie a pasta package e instale os requirements nela com:
```bash
pip install --target ./package nomedapackage
```

## Autenticação JWT (token_verify)
- **Headers**:
- **Bearer token gerado no login**
- **Email do login**

## Endpoints da API
### Criar pessoa

- **Endpoint**: `/create-person`
- **Método**: POST
- **Entrada**: JSON contendo email, senha, saldo (opcional)
- **Exemplo**: {
    "email": "joao@gmail.com",
    "senha": "123
    "saldo": 100 (int)
}

### Login (token jwt é gerado aqui)
- **Endpoint**: `/login`
- **Método**: POST
- **Entrada**: JSON contendo email e senha
- **Exemplo**: {
    "email": "joao@gmail.com",
    "senha": "123
}

### Deletar pessoa (rota protegida com o token_verify)

- **Endpoint**: `/delete-person`
- **Método**: DELETE
- **Entrada**: JSON contendo o email da pessoa a ser deletada, Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
}

### Encontrar pessoa por email (rota protegida com o token_verify)

- **Endpoint**: `/get-person`
- **Método**: POST
- **Entrada**:  JSON contendo email da pessoa a ser buscada, Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com"
}

### Depositar saldo (rota protegida com o token_verify)

- **Endpoint**: `/deposit-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo email da pessoa que vai receber o depósito e amount com a quantia do valor, Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
    "amount": 100 (int)
}

### Transferir saldo entre contas (rota protegida com o token_verify)

- **Endpoint**: `/transfer-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo source_email, target_email, amount com a quantia do valor, Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "source_email": "joao@gmail.com",
    "target_email": "vitor@gmail.com"
    "amount": 100 (int)
}

### Sacar saldo (rota protegida com o token_verify)

- **Endpoint**: `/withdraw-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo email da conta e amount com a quantia do valor, Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
    "amount": 100 (int)
}

### Gerar código pix copia e cola
- **Endpoint**: `/gerar-pix`
- **Método**: POST
- **Entrada**:  JSON contendo nome da pessoa que está enviando, chave pix do mesmo, valor do pix a ser gerado e cidade de quem está enviando e opcionalmente o txtId com a mensagem do pix.
- **Exemplo**: {
  "nome": "Joao Silva",
  "chavepix": "+5544993694529",
  "valor": "10.00",
  "cidade": "Maringá",
  "txtId": "LOJA01" (opcional)
}

### Registrar cartão de crédito vinculado ao email no banco de dados (rota protegida com o token_verify)
- **Endpoint**: `/register-credit-card`
- **Método**: POST
- **Entrada**:  JSON contendo email do usuário (string), card_number (string), expiration_month (int), expiration_year (int), security_code (string), holder_name (string), Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
    "card_number": "5502902593408544",
    "expiration_month": 12,
    "expiration_year": 2027,
    "security_code": "123",
    "holder_name": "Julio Alvarenga"
}
- **Obs**: O card_number é salvo em encode base64 no banco de dados, onde temos que decodar esse base64 pra realizar outras operações com ele, visando simular uma "tokenização de cartão" somente a fins de demonstração.

### Criar pagamento fictício (rota protegida com o token_verify)
- **Endpoint**: `/create-payment`
- **Método**: POST
- **Entrada**:  JSON contendo "email" (string) e "amount" (int), Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
    "amount": 100
  }
- **Obs**: É feito o decode do base64 pra retornar o número válido do cartão nessa rota, e realizar a operação desejada.

### Deletar cartão de crédito (rota protegida com o token_verify)
- **Endpoint**: `/delete-card`
- **Método**: POST
- **Entrada**:  JSON contendo "email" (string), Bearer token authorization com o token jwt gerado no login, e email que foi gerado o token nos headers.
- **Exemplo**: {
    "email": "joao@gmail.com",
  }
- **Obs**: É feito o decode do base64 pra retornar o número válido do cartão nessa rota, e contextualizar o usuário de qual cartão foi removido.

## Informações técnicas:
- Há a presença de testes unitários em todos os controllers, validators e views, totalizando 88 testes em estado "passed"
- Para garantir a segurança das rotas, foi implementado a lógica de autenticação JWT, onde criamos o token no momento do login e exigimos ele nas outras rotas através de uma função decorator token_verify, onde o token é atrelado ao email do login (que é requerido nos headers juntos com o token para liberar a rota).
- Para garantir a validação dos campos na requisição, utilizei a biblioteca Cerberus para facilitar esse processo, onde as configurações dela se encontram na pasta `validators` como schema desejado, onde a mesma é chamada nas views dos processos depois.
- Implementei um tratamento de erros personalizados, retornando esses erros em situações específicas do código, você pode encontrar os mesmos em `/src/errors/`, onde temos a pasta types com os tipos de erros, e o error_handler que será chamado na view para mostrar esses erros personalizados.
- Foram implementadas interfaces para garantir a conformidade das classes com os contratos especificados, as quais se encontram na pasta `interface` dos módulos do projeto.
- O projeto inclui o design pattern adapter para conectar diferentes partes do sistema, como adaptadores de solicitação, o qual se encontra na pasta `main/adapter`, que utiliza os http_types na pasta `views`.
- O projeto também possui o design pattern `composer` que são responsáveis por construir lógicas complexas, a partir de partes menores, o qual se encontra na pasta `main/composers` e são chamados no routes.py.
  
