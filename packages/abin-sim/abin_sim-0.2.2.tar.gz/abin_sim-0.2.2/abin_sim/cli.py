import pkg_resources
from rich.console import Console
from rich.table import Table
from typer import Option, Typer

from .config import settings
from .core.file_manager import make_return
from .core.functions import (
    convert_to_json,
    get_metadata,
    get_secret,
    make_conf,
    update_secret,
)

console = Console()
app = Typer()

@app.command('version')
def version():
    console.print(pkg_resources.get_distribution('abin-sim').version)

@app.command('make-conf')
def conf():
    configuration = make_conf()
    if configuration['Status']:
        console.print(configuration['Message'])
    else:
        console.print(configuration['Message'])

@app.command('get')
def get(
    app: str = Option(
        ...,
        help='Nome da aplicação que deseja recuperar os secrets.',
    ),
    env: str = Option(
        ...,
        help='Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main).'
    ),
    proj: str = Option(
        ...,
        help='Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua)'
    ),
    file: bool = Option(
        True,
        help='Cria um arquivo .env para armazenar os secrets.',
    ),
):
    vault_token = settings.params.vault_token
    vault_url = settings.params.vault_url
    metadata = get_metadata(app, env, proj, vault_token, vault_url)
    if not 'Erro' in metadata:
        if file == None or file == False:
            for conf in metadata:
                secret = get_secret(app, env, proj, conf, vault_token, vault_url)
                console.print(f'--- {conf} ---')
                console.print(secret)
                console.print('\n')
        else:
            for conf in metadata:
                secret = get_secret(app, env, proj, conf, vault_token, vault_url)
                if 'Erro' not in secret:
                    make_return(app, secret, settings.params.path, conf)
            console.print(f'{app} secrets salvos em {settings.params.path}')
    else:
        console.print(f'Erro ao buscar metadata -> {metadata}')

@app.command('update')
def update(
    app: str = Option(
        ...,
        help='Nome da aplicação que deseja recuperar os secrets.',
    ),
    env: str = Option(
        ...,
        help='Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main).'
    ),
    proj: str = Option(
        ...,
        help='Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua)'
    ),
    file: str = Option(
        ...,
        help='Arquivo com variárias de ambiente',
    ),
):
    vault_token = settings.params.vault_token
    vault_url = settings.params.vault_url
    payload = convert_to_json(file)
    ret = update_secret(app, env, proj, vault_token, vault_url, payload)
    console.print(ret)

@app.command('compare')
def compare(
    app: str = Option(
        ...,
        help='Nome da aplicação que deseja recuperar os secrets.',
    ),
    env: str = Option(
        ...,
        help='Ambiente da aplicação que deseja recuperar (Envs possíveis: dev, qa, main).'
    ),
    proj: str = Option(
        ...,
        help='Projeto que deseja conectar para recuperar os secrets (Projs possíveis: simlabs, charrua)'
    ),
):
    # envs = []
    envs_a = []
    envs_b = []
    envs = env.split(',')
    if len(envs) == 2:
        pass
    else:
        console.print('2 ambientes devem ser informados no parâmetro --env.')        
        exit()

    vault_token = settings.params.vault_token
    vault_url = settings.params.vault_url
    for environ in envs:
        if len(envs_a) == 0: 
            dados = get_secret(app, environ, proj, 'env', vault_token, vault_url)
            for item, value in dados.items():
                envs_a.append(item)
        else: 
            dados = get_secret(app, environ, proj, 'env', vault_token, vault_url)
            for item, value in dados.items():
                envs_b.append(item)
    envs_a.sort()
    envs_b.sort()
        
    tbl_envs = Table(title=f'Environments {envs[0]} x {envs[1]}', style="cyan", width=settings.console.table_width)
    for environment in envs:
        tbl_envs.add_column(environment.upper(), justify='left')
    counter = len(envs_a) if len(envs_a) > len(envs_b) else len(envs_b)
    for num in range(0, counter):
        if 0 <= num < len(envs_a): value_a = str(envs_a[num])
        else: value_a = ''
        if 0 <= num < len(envs_b): value_b = str(envs_b[num])
        else: value_b = ''
        tbl_envs.add_row(value_a, value_b, style='green')

    tbl_diferences = Table(title=f'Diferenças {envs[0]} x {envs[1]}', width=settings.console.table_width, style="red")
    for environment in envs:
        tbl_diferences.add_column(environment.upper(), justify='left')
    envs_a_diff = [x for x in envs_a if x not in envs_b]
    envs_b_diff = [x for x in envs_b if x not in envs_a]
    counter = len(envs_a_diff) if len(envs_a_diff) > len(envs_b_diff) else len(envs_b_diff)
    for num in range(0, counter):
        if 0 <= num < len(envs_a_diff): value_a = str(envs_a_diff[num])
        else: value_a = ''
        if 0 <= num < len(envs_b_diff): value_b = str(envs_b_diff[num])
        else: value_b = ''
        tbl_diferences.add_row(value_a, value_b, style='red')
    console.print(tbl_envs, tbl_diferences)