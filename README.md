# API BaaS DynamoDB

## Descrição do Projeto

A API BaaS DynamoDB implementa um sistema bancário simples com funcionalidades como criar contas de usuário, excluir contas de usuário, consultar contas de usuário e realizar operações de saldo como depósito, transferência e saque. O projeto foi feito para ser implementado em uma lambda, contendo os arquivos de configuração "samconfig.toml" e "template.yaml"


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

### Deletar pessoa

- **Endpoint**: `/delete-person`
- **Método**: DELETE
- **Entrada**: JSON contendo o email da pessoa a ser deletada
- **Exemplo**: {
    "email": "joao@gmail.com",
}

### Encontrar pessoa por email

- **Endpoint**: `/get-person`
- **Método**: PUT
- **Entrada**:  JSON contendo email da pessoa a ser buscada
- **Exemplo**: {
    "name": "joao@gmail.com",
}

### Depositar saldo

- **Endpoint**: `/deposit-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo email da pessoa que vai receber o depósito e amount com a quantia do valor
- **Exemplo**: {
    "email": "joao@gmail.com",
    "amount": 100 (int)
}

### Transferir saldo entre contas

- **Endpoint**: `/transferir-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo source_email, target_email, e amount com a quantia do valor.
- **Exemplo**: {
    "source_email": "joao@gmail.com",
    "target_email": "vitor@gmail.com"
    "amount": 100 (int)
}

### Sacar saldo

- **Endpoint**: `/withdraw-saldo`
- **Método**: POST
- **Entrada**:  JSON contendo email da conta e amount com a quantia do valor
- **Exemplo**: {
    "email": "joao@gmail.com",
    "amount": 100 (int)
}

## Informações técnicas:
- Para garantir a validação dos campos na requisição, utilizei a biblioteca Cerberus para facilitar esse processo, onde as configurações dela se encontram na pasta `validators` como schema desejado, onde a mesma é chamada nas views dos processos depois.
- Foram implementadas interfaces para garantir a conformidade das classes com os contratos especificados, as quais se encontram na pasta `interface` dos módulos do projeto.
- O projeto inclui o design pattern adapter para conectar diferentes partes do sistema, como adaptadores de solicitação, o qual se encontra na pasta `main/adapter`, que utiliza os http_types na pasta `views`.
- O projeto também possui o design pattern `composer` que são responsáveis por construir lógicas complexas, a partir de partes menores, o qual se encontra na pasta `main/composers` e são chamados no routes.py.
  
