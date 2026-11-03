from pathlib import Path

from conciliador import carregar, conciliar

extrato = carregar("dados/extrato_exemplo.csv")
razao = carregar("dados/razao_exemplo.csv")
resultado = conciliar(extrato, razao, tolerancia_dias=2)

print("\n=== CONCILIADOS ===")
print(resultado["conciliados"].to_string(index=False))
print("\n=== SÓ NO EXTRATO (falta lançar na contabilidade) ===")
print(resultado["so_extrato"][["data", "descricao", "valor"]].to_string(index=False))
print("\n=== SÓ NO RAZÃO (sem movimento no banco) ===")
print(resultado["so_razao"][["data", "historico", "valor"]].to_string(index=False))

diferenca = extrato["valor"].sum() - razao["valor"].sum()
print(f"\nDiferença total extrato - razão: R$ {diferenca:,.2f}")

# Salva o relatório em CSV
Path("saida").mkdir(exist_ok=True)
for nome, df in resultado.items():
    df.to_csv(f"saida/{nome}.csv", index=False)