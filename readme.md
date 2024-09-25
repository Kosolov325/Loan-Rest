# Loan-Rest 🏦💳

**Loan-Rest** é um sistema simples e leve para gerenciar empréstimos, pagamentos e usuários, com funcionalidades que incluem a criação e validação de empréstimos e pagamentos e autenticação de usuários. O projeto é desenvolvido com o framework Django, adotando algumas práticas não ortodoxas que facilitam a flexibilidade e legibilidade no código.

## Funcionalidades Principais ✨
- **Gerenciamento de Usuários:** Autenticação e autorização de usuários.
- **Criação e Validação de Empréstimos:** Controle completo sobre tipos de empréstimos e regras de negócios.
- **Gerenciamento de Pagamentos:** Controle sobre a criação e validação de pagamentos.
- **Prevenção de Fraudes:** Utilização de ferramentas administrativas para proteger contra inserções manuais de dados.

---

## Configuração do Projeto ⚙️

### Utilização de `settings.json` ao invés de `.env`

Este projeto optou por uma abordagem não convencional para a configuração de variáveis de ambiente, adotando um arquivo `settings.json` ao invés de um `.env` tradicional. Essa escolha se deve à flexibilidade que o formato JSON oferece ao lidar diretamente com dicionários, listas e valores mais complexos que refletem melhor a sintaxe do Django. O parsing do JSON também permite a manipulação fácil dos tipos de dados respectivos, o que é mais complicado de alcançar com arquivos `.env`.

O arquivo `settings.json` deve estar localizado na raiz do projeto (ao lado de `manage.py`), ou em um caminho personalizado especificado pela variável de ambiente `LOANREST_SETTINGS_PATH`.

### Exemplo de `settings.json`
```json
{
    "SECRET_KEY":"django-insecure-(fy#^wfu5dznpotomx-p35jkr1*d-(tj!)ev)fur7jcpy#ymt@",
    "DEBUG":true,
    "ALLOWED_HOSTS":["*"],
    "CORS_ALLOW_ALL_ORIGINS":true,
    "APPEND_SLASH":true,
    "DATABASES":{
            "default":{
                "ENGINE":"django.db.backends.mysql",
                "NAME": "matera",
                "USER": "root",
                "PASSWORD":"root",
                "HOST": "localhost", 
                "PORT": "3306"
            }
    },
    "LANGUAGE_CODE":"pt-BR",
    "TIME_ZONE":"America/Sao_Paulo",
    "USE_I18N":true,
    "USE_TZ":true,
    "STATIC_URL":"static/",
    "STATIC_ROOT":"static"
}
```

---

## Instalação 📦

### Requisitos

- Python 3.x
- Django
- Docker (opcional)

### Instalação Convencional

1. Clone o repositório:
    ```bash
    git clone https://github.com/Kosolov325/Loan-Rest.git
    cd loan-rest
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Crie o arquivo `settings.json` na raiz do projeto ou defina a variável `LOANREST_SETTINGS_PATH` apontando para seu caminho personalizado.

5. Execute as migrações e inicie o servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

### Instalação com Docker 🐳

1. Clone o repositório:
    ```bash
    git clone https://github.com/Kosolov325/Loan-Rest
    cd loan-rest
    ```

2. Crie o arquivo `settings.json` e insira os valores necessários.

3. Construa a imagem Docker::
    ```bash
    docker build -t loan-rest .
    ```
4. Execute o container:
    ```
    docker run -d -p 8000:8000 --name loan-rest loan-rest
    ```
---

## Modelos de Dados 🗂️

### **LoanType (Tipo de Empréstimo)**
Define os tipos de empréstimos disponíveis no sistema. Cada tipo de emprestimo pode conter juros especificos.

* **Juros Não Negativos**: O fator de juros associado a cada tipo de empréstimo não pode ser menor que zero. Isso garante que todos os tipos de empréstimos ofereçam, no mínimo, uma taxa de juros neutra, evitando condições prejudiciais aos usuários.

### **Loan (Empréstimo)**
Representa um empréstimo individual, que está vinculado a um tipo de empréstimo (`LoanType`) e a um usuário. Contém informações como valor do empréstimo, débito e outros.


* **Valor do Empréstimo**: O valor de um empréstimo não pode ser negativo ou igual a zero. Essa regra assegura que todos os empréstimos sejam válidos e que os usuários não possam solicitar valores que não sejam economicamente viáveis.

* **Cálculo do Débito**: O débito do usuário é calculado proporcionalmente aos dias e ao percentual de juros compostos do tipo de empréstimo escolhido. Isso significa que os juros são acumulados ao longo do tempo, refletindo um sistema mais justo e preciso de cobrança de juros. 

Durante a migração inicial da aplicação, foram criados os seguintes tipos de empréstimos padrão, cada um com um fator de juros específico. Esses tipos oferecem opções variadas para atender às diferentes necessidades financeiras dos usuários:

**Empréstimo Avulso**:

* **Fator de Juros**: 0.0
* **Descrição**: Um empréstimo sem incidência fiscal, ideal para quem precisa de um valor temporário sem custos adicionais de juros.

**Empréstimo Pessoal**:

* **Fator de Juros**: 0.0005 (0.05% ao dia, aproximadamente 1.5% ao mês)
* **Descrição**: Empréstimo destinado a despesas pessoais, com juros acessíveis, adequado para situações emergenciais ou financeiras.

**Empréstimo Consignado**:

* Fator de Juros: 0.0002 (0.02% ao dia, aproximadamente 0.6% ao mês)
* Descrição: Empréstimo com pagamento descontado diretamente da folha de pagamento, oferecendo taxas de juros mais baixas devido à menor chance de inadimplência.

**Financiamento Imobiliário**:

* **Fator de Juros**: 0.00015 (0.015% ao dia, aproximadamente 0.45% ao mês)
* **Descrição**: Destinado à compra de imóveis, com juros baixos para facilitar a aquisição de bens de valor significativo.

**Financiamento de Veículos**:

* **Fator de Juros**: 0.0003 (0.03% ao dia, aproximadamente 0.9% ao mês)
* **Descrição**: Empréstimo específico para a compra de veículos, oferecendo condições acessíveis para aquisição de automóveis.

**Empréstimo com Garantia de Imóvel**:

* **Fator de Juros**: 0.00025 (0.025% ao dia, aproximadamente 0.75% ao mês)
* **Descrição**: Empréstimo com a garantia de um imóvel, permitindo valores maiores e taxas de juros competitivas devido à segurança adicional.

### **Payment (Pagamento)**
Modelo que representa um pagamento realizado por um usuário em relação a um empréstimo. Ele é validado conforme as regras de negócios.

* **Limites de Pagamento**: O valor de um pagamento não pode exceder o valor do débito associado ao empréstimo. Essa regra evita que os usuários possam realizar pagamentos que não correspondem ao valor devido.

* **Valores Negativos**: Pagamentos com valores negativos não são aceitos. Isso garante a integridade dos dados financeiros e protege o sistema contra tentativas de inserções fraudulentas.

---

## Testes Unitários 🧪

A cobertura de testes é uma parte fundamental do Loan-Rest, garantindo a integridade e a confiabilidade das funcionalidades principais dos endpoints. Todos os testes foram cuidadosamente elaborados para cobrir os cenários mais críticos e estão organizados por seções para cada modelo.

Os testes são parametrizáveis por meio de arquivos JSON localizados na pasta raiz do projeto, permitindo a cobertura de uma variedade de cenários conforme necessário.

### LoanType
- **Uso**: `python manage.py test api.tests.loantype`
- **GET**: 
    * Valida se os tipos de empréstimos são retornados corretamente.
- **POST**: 
    * Verifica a criação de novos tipos de empréstimos, assegurando que o fator não seja irregular. 
    * Garante que usuários convencionais não tenham permissão para criar novos tipos de empréstimos.
- **PATCH**: 
    * Valida alterações nos valores dos tipos de empréstimos. 
    * Assegura que usuários convencionais não possam editar os tipos de empréstimos.
- **DELETE**: 
    * Verifica a possibilidade de exclusão dos tipos de empréstimos. 
    * Confirma que usuários convencionais não possam deletar os tipos de empréstimos.

### Loan
- **Uso**: `python manage.py test api.tests.loan`
- **GET**: 
    * Verifica o retorno de empréstimos associados ao usuário autenticado. 
    * Garante que usuários não possam visualizar empréstimos de outros usuários.
- **POST**: 
    * Valida a criação de novos empréstimos.
    * Assegura que empréstimos com valores negativos ou zerados não sejam permitidos.
- **PATCH**: 
    * Verifica que, uma vez criado, usuários não possam editar seus próprios empréstimos.
    * Confirma que usuários não possam editar empréstimos de outros usuários.
- **DELETE**: 
    * Garante que usuários não possam deletar empréstimos que criaram.
    * Assegura que usuários não possam deletar empréstimos de outros usuários.

### Payment
- **Uso**: `python manage.py test api.tests.payment`
- **GET**: 
    * Testa a visualização de um pagamento, garantindo que o usuário possa acessar os detalhes do pagamento que ele realizou.
    * Garante que um usuário não possa visualizar pagamentos associados a empréstimos de outros usuários, reforçando a privacidade.
- **POST**: 
    * Valida a criação de um pagamento, assegurando que ele seja registrado corretamente no banco de dados.
    * Verifica se o status da resposta está de acordo com o esperado e se o valor do pagamento corresponde ao especificado no contexto.
    * Garante que um usuário não possa criar um pagamento para um empréstimo que não pertence a ele, assegurando a proteção dos dados dos usuários.
    * Verifica que pagamentos que excedem a dívida total do empréstimo não são permitidos, evitando erros financeiros.
    * Assegura que pagamentos com valores negativos não sejam aceitos, mantendo a integridade dos dados financeiros.
- **PATCH**:
    * Verifica q8e um pagamento pode ser editado.
    * Assegura que um usuário não possa editar pagamentos de empréstimos de outros usuários, protegendo a integridade dos dados.
- **DELETE**:
    * Testa a exclusão de um pagamento, garantindo que o endpoint não remova o pagamento do banco de dados conforme esperado.
    * Garante que um usuário não possa deletar pagamentos relacionados a empréstimos de outros usuários, preservando a integridade dos dados.

### Autenticação
- **Uso**: `python manage.py test api.tests.auth`
    * Verifica se o endpoint para obtenção do token retorna o status esperado e inclui os tokens de acesso e de refresh na resposta.
    * Valida a resposta do endpoint ao tentar autenticar um usuário com credenciais inválidas.
    * Garante que a renovação do token de acesso funcione corretamente, retornando um novo token ao usuário.
    * Testa a resposta do endpoint quando uma solicitação de renovação de token é feita com dados inválidos.
    * Verifica se o endpoint nega o acesso a endpoints críticos quando o usuário não está autenticado.


---

## Ferramentas de `management` 🛠️

O Loan-Rest inclui diversos comandos personalizados do Django (`management commands`) para combater fraudes e inserções manuais de dados. Esses comandos garantem que os dados no banco de dados estão consistentes com as regras de negócio definidas, detectando e sinalizando possíveis anomalias.

- **check_loantypes**:
    * **Uso**: `python manage.py check_loantypes -o /home/sammy/check_loantypes.csv`
    * **Descrição**: Gera um CSV contendo tipos de empréstimos irregulares. (fatores negativos)
    * **Parâmetros**: 
        * `-o` Caminho para saída do arquivo
- **check_loans**:
    * **Uso**: `python manage.py check_loans -o /home/sammy/check_loans.csv`
    * **Descrição**: Gera um CSV contendo empréstimos irregulares (empréstimos com datas futuras ou debitos negativos)
    * **Parâmetros**: 
        * `-o` Caminho para saída do arquivo
- **check_payments**:
    * **Uso**: `python manage.py check_payments -o /home/sammy/check_payments.csv`
    * **Descrição**: Gera um CSV contendo empréstimos irregulares (pagamentos com valores negativos ou maiores que o próprio débito)
    * **Parâmetros**: 
        * `-o` Caminho para saída do arquivo
- **gen_loantype**:
    * **Uso**: `python manage.py gen_loantype -n "Empréstimo de Teste" -f 0.00033`
    * **Descrição**: Gera tipos de empréstimos rapidamente
    * **Parâmetros**: 
        * `-n` Nome do Tipo de Empréstimo
        * `-f` Fator de juros do tipo de empréstimo
- **gen_loan**:
    * **Uso**: `python manage.py gen_loan -u 1 -a 100 -t 1`
    * **Descrição**: Gera empréstimos rapidamente
    * **Parâmetros**: 
        * `-u` ID do cliente
        * `-a` Valor do empréstimo
        * `-t` ID do tipo de empréstimo
- **gen_payment**:
    * **Uso**: `python manage.py gen_payment -l 78f7094b-2a51-4bdb-a99b-8b318dcb17a2 -a 100.00`
    * **Descrição**: Gera pagamentos rapidamente
    * **Parâmetros**: 
        * `-l` UUID do empréstimo
        * `-a` Valor do pagamento
- **gen_user**:
    * **Uso**: `python manage.py gen_user -u Kosolov -p sekret`
    * **Descrição**: Gera usuários rapidamente
    * **Parâmetros**: 
        * `-u` Nome do usuário
        * `-p` Senha do usuário
---

## Licença 📝

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.