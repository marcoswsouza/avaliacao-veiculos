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


DESCONTO_POR_GRAVIDADE = {
    0: 0,   # Nenhum acidente
    1: 5,   # Leve
    2: 15,  # Moderado
    3: 30,  # Grave
}


def calcular_score(ano, km, estado_conservacao, gravidade_acidente):
    """
    Calcula uma nota de 0 a 100 para o veículo.

    Regras (critérios simples, só para fins didáticos):
    - Começa com 100 pontos
    - Perde 1 ponto a cada 3 anos completos de idade do veículo
    - Perde 1 ponto a cada 15.000 km completos rodados
    - O estado de conservação (1 a 5) funciona como um multiplicador
    - Perde pontos conforme a gravidade do acidente (0, 5, 15 ou 30 pontos)
    """
    idade = ANO_ATUAL - ano
    score = 100
    score -= idade // 3
    score -= km // 15000
    score -= DESCONTO_POR_GRAVIDADE[gravidade_acidente]

    # Estado de conservação 1 (ruim) a 5 (excelente) atua como multiplicador.
    # Cada nota abaixo da máxima desconta 10% do score (nota 5 = 100%, nota 1 = 60%),
    # em vez de uma proporção direta (que penalizava demais notas intermediárias).
    multiplicador = 0.6 + (estado_conservacao - 1) * 0.1
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

    print("\nEstado de conservação:")
    print("1 - Péssimo (pintura/lataria danificada, estofados rasgados, ruídos mecânicos, pneus carecas)")
    print("2 - Ruim (desgaste visível na pintura ou lataria, estofados manchados/gastos, manutenção atrasada)")
    print("3 - Regular (riscos e desgaste natural do uso, mecânica ok mas precisa de atenção em breve)")
    print("4 - Bom (pintura e lataria conservadas, interior limpo e sem danos, mecânica e revisões em dia)")
    print("5 - Excelente (sem avarias visíveis, pintura original, interior impecável, revisões todas em dia)")

    try:
        estado_conservacao = int(input("Escolha o estado de conservação (1 a 5): "))
    except ValueError:
        print("\nValor inválido. Cadastro cancelado.")
        return

    if estado_conservacao < 1 or estado_conservacao > 5:
        print("\nEstado de conservação deve ser entre 1 e 5. Cadastro cancelado.")
        return

    print("\nHistórico de acidentes:")
    print("0 - Nenhum acidente")
    print("1 - Leve (arranhões, pequenos amassados, sem troca de peça estrutural)")
    print("2 - Moderado (colisão com troca de peças, sem dano estrutural)")
    print("3 - Grave (dano estrutural, air bag acionado, perda total registrada)")

    try:
        gravidade_acidente = int(input("Escolha o nível (0 a 3): "))
    except ValueError:
        print("\nValor inválido. Cadastro cancelado.")
        return

    if gravidade_acidente not in DESCONTO_POR_GRAVIDADE:
        print("\nNível de acidente deve ser entre 0 e 3. Cadastro cancelado.")
        return

    score = calcular_score(ano, km, estado_conservacao, gravidade_acidente)
    classificacao = classificar_score(score)

    veiculo = {
        "marca": marca,
        "modelo": modelo,
        "ano": ano,
        "km": km,
        "estado_conservacao": estado_conservacao,
        "gravidade_acidente": gravidade_acidente,
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
