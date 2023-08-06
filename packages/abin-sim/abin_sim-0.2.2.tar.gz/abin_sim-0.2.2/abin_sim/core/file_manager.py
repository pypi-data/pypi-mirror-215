from pathlib3x import Path


def make_return(app: str, secret: dict, filepath: str, file: str) -> bool:
    try:
        # path = Path(filepath) / app

        path = Path(filepath)
        # path.rmtree(ignore_errors=True)
        # path.mkdir()
        if file == 'env':
            arqenv = open(f'{path}/.env', 'w')
        # elif file == 'env.js':
        #     arqenv = open(f'{path}/src/assets/env.js', 'w')
        else:
            arqenv = open(f'{path}/{file}', 'w')
    except Exception as e:
        print(e)
        retorno = False
    else:
        if file == 'env':
            for k, v in secret.items():
                arqenv.write(f'{k}={v}' + '\n')
        else: 
            arqenv.write(secret)
        arqenv.close()
        retorno = True
    return retorno
