# ANA SDK

O projeto ANA SDK visa fornecer uma interface para interagir com os serviços
relacionados ao ambiente de automação de negócios, dados e clientes da ANA.
Permite realizar login, executar comandos e definir tenant, cliente
e empresa atuais para ter acesso automático ao ANA Data.

## Instalação

Use o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar a ANA SDK.

```bash
pip install ana-sdk
```

## Exemplo de utilização

Todos os métodos públicos estão documentados, com seus parâmetros, retornos e exceções mapeadas. Os atributos das classes também estão documentados.

```py
from ana_sdk import ANA


ana = ANA(rpa_api_base_url, dashboard_api_base_url, oauth_token_full_url)
ana.login("email@nasajon.com.br", "senha")

clientes = ana.api.get_clientes()
print(clientes)
ana.set_cliente(cliente[0]["id"])
lotacoes = ana.data.get_lotacoes(empresa=UUID_da_empresa)
lotacoes = ","join(lotacao["id"] for lotacao in lotacoes)

ana.execute("668.279", {"mes": "02", "ano": "2023", "lotacoes": lotacoes})
```

Além disso, você pode usar os clients para saber mais sobre os métodos disponíveis em cada um:

```py
rom ana_sdk import ANA


ana = ANA(rpa_api_base_url, dashboard_api_base_url, oauth_token_full_url)
ana.login("email@nasajon.com.br", "senha")

ana.api. # Te mostrará tudo que precisa saber sobre a RPA API, por exemplo
ana.rpa.
ana.data. # Só estará disponível caso uma empresa, cliente ou tenant já tenha sido selecionado
```

## Contribuição

Contribuições são bem-vindas! Para contribuir com o projeto, siga as orientações abaixo:

- Faça o fork do projeto
- Crie uma nova branch com o nome da sua contribuição: ```git checkout -b minha-contribuicao```
- Faça as modificações desejadas e adicione os arquivos alterados: ```git add .```
- Faça o commit das suas alterações: ```git commit -m "Descrição da minha contribuição"```
- Faça o push para a branch remota: ```git push origin minha-contribuicao```
- Abra um pull request descrevendo suas alterações
