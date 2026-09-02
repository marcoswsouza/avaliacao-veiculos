"""
Sistema de Avaliação de Veículos
Autor: Marcos Souza

Programa que cadastra veículos com dados técnicos (ano, quilometragem
e estado de conservação) e calcula uma nota de avaliação (score de 0
a 100) para cada um.
"""

import json
import os
from datetime import datetime

ARQUIVO_VEICULOS = "veiculos.json"
ANO_ATUAL = datetime.now().year


def carregar_veiculos():
    if not os.path.exists(ARQUIVO_VEICULOS):
        return []
    with open(ARQUIVO_VEICULOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_veiculos(veiculos):
    with open(ARQUIVO_VEICULOS, "w", encoding="utf-8") as arquivo:
        json.dump(veiculos, arquivo, ensure_ascii=False, indent=2)


def calcular_score(ano, km, estado_conservacao, teve_acidente):
    """
    Calcula uma nota de 0 a 100 para o veículo.

    Regras (critérios simples, só para fins didáticos):
    - Começa com 100 pontos
    - Perde 1 ponto a cada 3 anos completos de idade do veículo
    - Perde 1 ponto a cada 15.000 km completos rodados
    - Perde 10 pontos se já teve algum acidente
    - O estado de conservação (1 a 5) funciona como um multiplicador
      direto (nota / 5)
    """
    idade = ANO_ATUAL - ano
    score = 100
    score -= idade // 3
    score -= km // 15000
    if teve_acidente:
        score -= 10

    multiplicador = estado_conservacao / 5
    score = score * multiplicador

    score = max(0, min(100, score))
    return round(score, 1)


def classificar_score(score):
    if score >= 80:
        return "Excelente"
    elif score >= 60:
        return "Bom"
    elif score >= 40:
        return "Regular"
    else:
        return "Ruim"


def cadastrar_veiculo(veiculos):
    print("\n--- CADASTRO DE VEÍCULO ---")
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()

    try:
        ano = int(input("Ano de fabricação: "))
        km_texto = input("Quilometragem atual: ").strip().replace(".", "")
        km = float(km_texto)
    except ValueError:
        print("\nValor inválido. Cadastro cancelado.")
        return

    try:
        estado_conservacao = int(input("Estado de conservação (1 a 5): "))
    except ValueError:
        print("\nValor inválido. Cadastro cancelado.")
        return

    if estado_conservacao < 1 or estado_conservacao > 5:
        print("\nEstado de conservação deve ser entre 1 e 5. Cadastro cancelado.")
        return

    resposta_acidente = input("Já teve algum acidente? (s/n): ").strip().lower()
    teve_acidente = resposta_acidente == "s"

    score = calcular_score(ano, km, estado_conservacao, teve_acidente)
    classificacao = classificar_score(score)

    veiculo = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "km": km,
        "estado_conservacao": estado_conservacao,
        "teve_acidente": teve_acidente,
        "score": score,
        "classificacao": classificacao,
        "avaliado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }

    veiculos.append(veiculo)
    salvar_veiculos(veiculos)

    print(f"\nVeículo cadastrado! Score de avaliação: {score}/100 ({classificacao})")


def listar_veiculos(veiculos):
    if not veiculos:
        print("\nNenhum veículo cadastrado ainda.")
        return

    print("\n--- VEÍCULOS AVALIADOS ---")
    for indice, veiculo in enumerate(veiculos, start=1):
        print(
            f"{indice}. {veiculo['marca']} {veiculo['modelo']} ({veiculo['ano']}) "
            f"- {veiculo['km']} km - Score: {veiculo['score']}/100 ({veiculo['classificacao']})"
        )


def exibir_menu():
    print("\n===== AVALIAÇÃO DE VEÍCULOS =====")
    print("1. Cadastrar e avaliar veículo")
    print("2. Listar veículos avaliados")
    print("3. Sair")


def main():
    veiculos = carregar_veiculos()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_veiculo(veiculos)
        elif opcao == "2":
            listar_veiculos(veiculos)
        elif opcao == "3":
            print("\nAté mais!")
            break
        else:
            print("\nOpção inválida, tente novamente.")


if __name__ == "__main__":
    main()
