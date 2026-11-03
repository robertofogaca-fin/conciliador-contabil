# Conciliador Contábil

Script em Python para cruzar o extrato bancário com o razão contábil e apontar
as diferenças: o que bateu, o que está só no banco e o que está só na contabilidade.

> Todos os dados deste repositório são fictícios.

## Problema

A conciliação manual é lenta e sujeita a erro. Itens sem lançamento (tarifas),
lançamentos sem movimento (provisões), datas diferentes e erros de digitação
(transposição de dígitos) exigem revisão linha a linha.

## Como funciona

1. Lê os dois arquivos CSV (extrato e razão).
2. Converte os valores para centavos (inteiros), evitando erros de arredondamento.
3. Concilia por valor exato e data dentro de uma tolerância de dias (padrão: 2).
4. Quando há mais de um candidato, escolhe o de data mais próxima.
5. Gera três listas: conciliados, só no extrato e só no razão.

A diferença entre o saldo do extrato e o do razão é explicada pela soma
dos itens não conciliados.

## Como rodar

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
pytest
```

## Exemplo de resultado

=== CONCILIADOS ===
data_extrato      descricao_extrato data_razao        historico_razao   valor
  2026-10-01 TED RECEBIDA CLIENTE A 2026-10-01  Recebimento cliente A 15000.0
  2026-10-02     PAGTO FORNECEDOR X 2026-10-02 Pagamento fornecedor X -4200.5
  2026-10-05 PIX RECEBIDO CLIENTE B 2026-10-04  Recebimento cliente B  7300.0

=== SÓ NO EXTRATO (falta lançar na contabilidade) ===
      data              descricao   valor
2026-10-03        TARIFA BANCARIA   -85.0
2026-10-06     PAGTO FORNECEDOR Y -1999.9
2026-10-08 TED RECEBIDA CLIENTE C  3200.0

=== SÓ NO RAZÃO (sem movimento no banco) ===
      data              historico   valor
2026-10-06 Pagamento fornecedor Y -1990.9
2026-10-09       Provisao despesa  -500.0

Diferença total extrato - razão: R$ 3,606.00

## Limitações e próximos passos

- Conciliação 1 para N (um depósito que agrupa vários lançamentos)
- Detecção de transposição de dígitos (ex.: 1.999,90 contra 1.990,90)
- Similaridade de texto entre descrição e histórico
- Relatório em Excel e interface com Streamlit