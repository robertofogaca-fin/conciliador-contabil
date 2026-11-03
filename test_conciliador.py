import pandas as pd

from conciliador import conciliar


def _df(linhas, col_texto):
    df = pd.DataFrame(linhas, columns=["data", col_texto, "valor"])
    df["data"] = pd.to_datetime(df["data"])
    df["centavos"] = (df["valor"] * 100).round().astype(int)
    return df


def test_concilia_valor_igual_e_data_proxima():
    extrato = _df([("2026-10-05", "PIX", 7300.00)], "descricao")
    razao = _df([("2026-10-04", "Recebimento", 7300.00)], "historico")
    r = conciliar(extrato, razao, tolerancia_dias=2)
    assert len(r["conciliados"]) == 1
    assert r["so_extrato"].empty and r["so_razao"].empty


def test_nao_concilia_valor_diferente():
    extrato = _df([("2026-10-06", "PAGTO", -1999.90)], "descricao")
    razao = _df([("2026-10-06", "Pagamento", -1990.90)], "historico")
    r = conciliar(extrato, razao)
    assert r["conciliados"].empty
    assert len(r["so_extrato"]) == 1 and len(r["so_razao"]) == 1


def test_nao_concilia_fora_da_tolerancia():
    extrato = _df([("2026-10-01", "TED", 100.00)], "descricao")
    razao = _df([("2026-10-10", "Receb", 100.00)], "historico")
    r = conciliar(extrato, razao, tolerancia_dias=2)
    assert r["conciliados"].empty