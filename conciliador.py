import pandas as pd


def carregar(caminho: str) -> pd.DataFrame:
    """Lê um CSV com colunas data, descrição e valor."""
    df = pd.read_csv(caminho, sep=None, engine="python", encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    df["data"] = pd.to_datetime(df["data"])
    # Trabalhar em centavos (inteiros) evita erros de arredondamento
    df["centavos"] = (df["valor"] * 100).round().astype(int)
    return df.reset_index(drop=True)


def conciliar(extrato: pd.DataFrame, razao: pd.DataFrame, tolerancia_dias: int = 2) -> dict:
    """Cruza extrato e razão por valor exato e data dentro da tolerância."""
    extrato = extrato.copy()
    razao = razao.copy()
    extrato["conciliado"] = False
    razao["conciliado"] = False
    pares = []

    for i, linha in extrato.iterrows():
        candidatos = razao[
            (~razao["conciliado"])
            & (razao["centavos"] == linha["centavos"])
            & ((razao["data"] - linha["data"]).abs() <= pd.Timedelta(days=tolerancia_dias))
        ]
        if candidatos.empty:
            continue

        # Escolhe o candidato com a data mais próxima
        j = (candidatos["data"] - linha["data"]).abs().idxmin()
        extrato.at[i, "conciliado"] = True
        razao.at[j, "conciliado"] = True
        pares.append(
            {
                "data_extrato": linha["data"].date(),
                "descricao_extrato": linha["descricao"],
                "data_razao": razao.at[j, "data"].date(),
                "historico_razao": razao.at[j, "historico"],
                "valor": linha["valor"],
            }
        )

    return {
        "conciliados": pd.DataFrame(pares),
        "so_extrato": extrato[~extrato["conciliado"]].drop(columns=["conciliado"]),
        "so_razao": razao[~razao["conciliado"]].drop(columns=["conciliado"]),
    }