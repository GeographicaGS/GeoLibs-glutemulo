from environs import Env

env = Env()

with env.prefixed("GLUTEMULO_"):
    backend = env("BACKEND", default="carto")
    config = {"backend": backend, "debug": env.bool("DEBUG", False)}

    if backend == "carto":
        with env.prefixed("CARTO_"):
            config.update(
                {
                    "carto_user": env("USER"),
                    "carto_api_key": env("API_KEY"),
                    "carto_org": env("ORG"),
                }
            )
            api_url = env("API_URL", None)
            if not api_url:
                api_url = f"https://{env('USER')}.carto.com"
            config["carto_api_url"] = api_url
    elif backend == "postgres":
        with env.prefixed("PG_"):
            postgres_uri = env("URI", None)
            if not postgres_uri:
                config.update(
                    {
                        "pg_user": env("USER"),
                        "pg_password": env("PASSWORD"),
                        "pg_dbname": env("DBNAME"),
                        "pg_host": env("HOST"),
                        "pg_port": env("PORT"),
                    }
                )
                config[
                    "postgres_uri"
                ] = f'host={env("HOST")} port={env("PORT")} dbname={env("DBNAME")} user={env("USER")} password={env("PASSWORD")}'
