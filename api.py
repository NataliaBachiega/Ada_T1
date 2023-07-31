from fastapi import FastAPI, Request
app = FastAPI()

def melhor_opcao(montante, valor_aluguel, aumento_aluguel, valorizacao_imovel, juros_aplicacao):
  
  if aumento_aluguel > 1:
    aumento_aluguel /= 100
  
  if valorizacao_imovel > 1:
    valorizacao_imovel /= 100
  
  if juros_aplicacao > 1:
    juros_aplicacao /= 100

  

  #calculo do valor final da casa
  valorizacao_mensal = ((1 + valorizacao_imovel)**(1/12) -1)
  valores_da_casa = []
  for i in range(1, 20*12+1):
    valor_do_mes = montante * (1 + valorizacao_mensal)**i
    valores_da_casa.append(valor_do_mes)

  valor_final_da_casa = montante * (1 + valorizacao_imovel)**20
  print("\nValor final da casa: R$%.2f" %valor_final_da_casa)

  #calculo do valor final da aplicação
  juros_mensal = ((1 + juros_aplicacao)**(1/12) -1)
  valores_aplicacao = []
  for i in range(1,20*12+1):
    montante_do_mes = montante * (1 + juros_mensal)**i
    valores_aplicacao.append(montante_do_mes)

  valor_final_da_aplicacao = montante * (1 + juros_aplicacao)**20
  print("\nValor final da aplicação: R$%.2f" %valor_final_da_aplicacao)

  #lista para armazenar o valor dos aluguéis
  valores_aluguel = []

  for i in range(20):
    aluguel_no_ano_i =  valor_aluguel * (1 + aumento_aluguel)**i
    for j in range(12):
      valores_aluguel.append(aluguel_no_ano_i)

  #acumular valor do aluguel
  acumulado_aluguel = []
  acum = 0
  for i in range(20*12):
    acum += valores_aluguel[i]
    acumulado_aluguel.append(acum)

  valor_total_aluguel = sum(valores_aluguel)
  print("\nValor total gasto com aluguel: R$%.2f" %valor_total_aluguel)

  #opção1(alugar + aplicação): valor total considerando o valor final da aplicação descontando o gasto com aluguel
  opcao1 = valor_final_da_aplicacao - valor_total_aluguel

  #opção2(comprar): valor total da casa considerando a valorização do imóvel
  opcao2 = valor_final_da_casa

  print("\nValores da casa: ", valores_da_casa)
  print("Valores da aplicação: ", valores_aplicacao)
  print("Valores do aluguel acumulado: ", acumulado_aluguel)


  if opcao1 > opcao2:
    lista_resultado = []
    mes_virada = -1
    for i in range(20*12):
      resultado = (valores_aplicacao[i] - acumulado_aluguel[i]) - valores_da_casa[i]
      lista_resultado.append(resultado)
      if resultado > 0:
        if mes_virada == -1:
          mes_virada = i + 1

    print("Valores resultado mês a mês", lista_resultado)
    return ["alugar casa", opcao1, mes_virada]

  else:
    lista_resultado = []
    mes_virada = -1
    for i in range(20*12):
      resultado = valores_da_casa[i] - (valores_aplicacao[i] - acumulado_aluguel[i])
      lista_resultado.append(resultado)
      if resultado > 0:
        if mes_virada == -1:
          mes_virada = i + 1

    print("Valores resultado mês a mês", lista_resultado)
    return ["comprar casa", opcao2, mes_virada]


def mes_from_int(i: int):
  match i:
    case 1:
        return "Janeiro"
    case 2:
        return "Fevereiro"
    case 3:
        return "Março"
    case 4:
        return "Abril"
    case 5:
        return "Maio"
    case 6:
        return "Junho"
    case 7:
        return "Julho"
    case 8:
        return "Agosto"
    case 9:
        return "Setembro"
    case 10:
        return "Outubro"
    case 11:
        return "Novembro"
    case 12:
        return "Dezembro"


class Result:
    melhor_opcao: str
    valor_acumulado: float
    numero_mes: int


def consultor(montante: float, 
              valor_aluguel: float, 
              aumento_aluguel: float, 
              valorizacao_imovel: float, 
              juros_aplicacao: float) -> Result:
    pass

@app.get("/")
def home(montante: float, 
         valor_aluguel: float, 
         aumento_aluguel: float, 
         valorizacao_imovel: float, 
         juros_aplicacao: float):
    [melhor, valor_acumulado, numero_mes] = melhor_opcao(montante, valor_aluguel, aumento_aluguel, valorizacao_imovel, juros_aplicacao)

    # Obtém o nome do mês
    mes = numero_mes % 12
    mes_str = mes_from_int(mes)

    # Obtém o ano
    ano = numero_mes // 12

    res = {
        'melhor_opcao': melhor,
        'valor_acumulado': {
           'valor': f'{valor_acumulado:.2f}',
           'moeda': 'R$'
        },
        'mes_virada': {
            'mes': mes_str,
            'numero_mes': numero_mes,
            'apos_x_anos': ano
        }
    }

    return res