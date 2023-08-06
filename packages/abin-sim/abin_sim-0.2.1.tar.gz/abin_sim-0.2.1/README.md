## Instalação

```
sudo apt install pipx
pipx install abin_sim
```
A versão da aplicação no README será atualizada sempre que um novo build rodar.

## Configuração

Após realizar a instalação do App, criar um diretório no seu $HOME chamado 'abin_sim' e, neste diretório, um arquivo chamado 'settings.toml'
O conteúdo do arquivo deverá ser o seguinte:

```
name = "ABIN"

[params]
vault_token = "{token}"
vault_url = "https://aspirina.simtech.solutions"
path = "./"

[console]
table_width = 40
```
{token} -> Seu token de autenticação no Vault
path    -> Caminho que deseja salvar os dados provenientes do Vault (default: ./)

Para conseguir seu token basta autenticar no Web UI do Vault.
Acesse no seu navegador o endereço https://aspirina.simtech.solutions
Na tela de login:
    * Mude **Method** para ***Username***
    * Entre com o seu usuário em **Username**
    * Entre com a sua senha em **Password**
    * Clique em **More Options**
    * Em **Mount Path** digite ***simtech***
    * Clique em **Sign in**
Após o login clique no boneco localizao no canto superior direito e, após, clique em **Copy Token**

**Importante:** O Token é válido por 30 dias, portanto lembre de renová-lo.

## Funções
    
### GET
    Usage: abin get [OPTIONS]                                                                                                                            
                                                                                                                                                      
    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *  --app                  TEXT  Nome da aplicação que deseja recuperar os secrets. [default: None] [required]                                        │
    │ *  --env                  TEXT  Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main). [default: None] [required]               │
    │ *  --proj                 TEXT  Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua) [default: None] [required] │
    │    --file    --no-file          Cria um arquivo para cada path cadastrada no secrets. [default: file]                                                │
    │    --help                       Show this message and exit.                                                                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

    For example:
    * Imprime os dados no StdOut (Tela)
        abin get --app=api-auth --env=dev --proj=simlabs --no-file
    * Imprime os dados em arquivo (Com base no arquivo $HOME/abin_sim/settings.toml)
        abin get --app=api-auth --env=dev --proj=simlabs

### UPDATE
    Usage: abin update [OPTIONS] 
                                               
    ╭─ Options─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *  --app         TEXT  Nome da aplicação que deseja recuperar os secrets. [default: None]  [required]                                        │
    │ *  --env         TEXT  Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main). [default: None] [required]                │
    │ *  --proj        TEXT  Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua) [default: None] [required]  │
    │ *  --file        TEXT  Arquivo com variárias de ambiente [default: None] [required]                                                          │
    │    --help              Show this message and exit.                                                                                           │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

    For example:
        abin update --app=api-auth --env=dev --proj=simlabs --file=.env

### COMPARE
    Usage: abin compare [OPTIONS]

    ╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
    │ *  --app                  TEXT  Nome da aplicação que deseja recuperar os secrets. [default: None] [required]                                            │
    │ *  --env                  TEXT  Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main). [default: None] [required]                   │
    │ *  --proj                 TEXT  Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua) [default: None] [required]     │
    │    --help                       Show this message and exit.                                                                                              │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

    For example:
        abin compare --app=api-auth --env=qa,dev --proj=simlabs