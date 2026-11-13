import csv
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

taxas = {}

with open("data/taxas_cambio.csv", encoding="utf-8", newline="") as arquivo:
  leitor = csv.DictReader(arquivo)
  for linha in leitor:
    moeda = linha["currency"]
    taxa = linha["rate_to_brl"]
    taxas[moeda] = Decimal(taxa)



total_confirmadas = 0
valor_br_total = Decimal("0")
noites = 0  

with open("data/reservas_hoteis.csv", encoding="utf-8", newline="") as arquivo:
  leitor = csv.DictReader(arquivo)
  for linha in leitor:
    if linha["status"] == "CONFIRMED":
      moeda = linha["currency"]
      valor_brl = Decimal(linha["amount"]) * taxas[moeda]
      total_confirmadas += 1
      valor_br_total += (valor_brl)
      checkin = date.fromisoformat(linha["checkin_date"])
      checkout = date.fromisoformat(linha["checkout_date"])
      noites += (checkout - checkin).days * int(linha["rooms"])

  total_arredondado = valor_br_total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
  print(total_confirmadas, total_arredondado, noites)



