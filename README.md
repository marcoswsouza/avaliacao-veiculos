# Sistema de Avaliação de Veículos

Programa em Python de linha de comando que cadastra veículos e calcula
uma nota de avaliação (score de 0 a 100) para cada um, seguindo
critérios simples, parecido com o que é feito em uma vistoria real.

## Dados cadastrados por veículo

- Marca
- Modelo
- Ano de fabricação
- Quilometragem atual
- Estado de conservação (1 a 5)
- Histórico de acidentes (0 a 3)

## Como funciona o cálculo do score

O score começa em 100 pontos e sofre descontos:

| Fator                          | Desconto |
|--------------------------------|----------|
| Idade do veículo               | 1 ponto a cada 3 anos completos |
| Quilometragem                  | 1 ponto a cada 15.000 km completos rodados |
| Histórico de acidentes         | 0 (nenhum) / 5 (leve) / 15 (moderado) / 30 (grave) |

Depois desses descontos, o **estado de conservação** (1 a 5) entra
como um multiplicador sobre o score:

| Nota | Multiplicador | Desconto |
|------|----------------|----------
| 5 - Excelente | 1.0 | 0% |
| 4 - Bom       | 0.9 | 10% |
| 3 - Regular   | 0.8 | 20% |
| 2 - Ruim      | 0.7 | 30% |
| 1 - Péssimo   | 0.6 | 40% |

O score final fica sempre entre 0 e 100.

## Classificação final

 Score      | Classificação 
----------------------------
 80 - 100    Excelente      
 60 - 79     Bom            
 40 - 59     Regular        
 0 - 39      Ruim           

## Como rodar

```bash
python avaliacao_veiculos.py
```

O programa mostra um menu com três opções:

1. Cadastrar e avaliar veículo
2. Listar veículos avaliados
3. Sair

Os dados ficam salvos em `veiculos.json`, na mesma pasta, e
persistem entre execuções.

## Decisões de projeto

- **Estado de conservação como desconto percentual, não proporção
  direta.** A primeira versão multiplicava o score direto pela nota
  de conservação (nota/5), o que penalizava demais notas
  intermediárias — nota 3 já cortava 40% do score, mesmo com o resto
  do carro em bom estado. A versão atual usa um desconto fixo de 10%
  por nota abaixo da máxima (nota 5 = sem desconto, nota 1 = 40% de
  desconto), o que é mais justo pra carros com desgaste natural.
- **Histórico de acidentes em níveis de gravidade, não sim/não.** Um
  acidente leve (arranhão) e um acidente grave (dano estrutural) têm
  impactos muito diferentes no valor real do carro, então o programa
  pede o nível (0 a 3) em vez de só perguntar se houve acidente.
- **Marca e modelo como campos separados.** Facilita tanto a
  listagem quanto uma futura busca/filtro por marca.
- **Formatação da quilometragem na listagem.** A quilometragem é
  digitada como texto e convertida pra número, então internamente
  fica armazenada como float (ex: `145000.0`). Isso fazia a listagem
  mostrar o `.0` desnecessário; o programa agora formata a
  quilometragem como número inteiro com ponto separando milhares
  (ex: `145.000 km`) só na hora de exibir, sem alterar o dado salvo.
