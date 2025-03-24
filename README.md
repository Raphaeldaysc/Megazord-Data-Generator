# Megazord Data Generator

Este repositório contém uma poderosa ferramenta de geração de dados para criar dados sintéticos de negócios para análises e testes. A ferramenta suporta múltiplos domínios de negócios e pode gerar tabelas de dimensão e fatos com dados realistas.

## Funcionalidades

- Gera dados sintéticos para múltiplos domínios de negócios:
    - Restaurante/Fast Food
    - Marketing
    - Bancário
    - Saúde
    - E-commerce
    - Call Center
    - Educação
    - Imobiliário
    - Cadeia de Suprimentos
- Cria tabelas de dimensão e fatos com relacionamentos realistas
- Número personalizável de linhas para ambos os tipos de tabela
- Localização em português brasileiro para dados realistas
- Exporta dados para arquivos CSV

## Instalação

1. Clone este repositório:

```bash
git clone <https://github.com/seuusuario/megazord-data-generator.git>
cd megazord-data-generator

```

1. Instale as dependências necessárias:

```bash
pip install -r requirements.txt

```

## Uso

### Interface de Linha de Comando

O script pode ser executado a partir da linha de comando com várias opções:

```bash
python el_dados.py caso_negocio [--dim-rows LINHAS_DIM] [--fact-rows LINHAS_FATO] [--output-dir DIR_SAIDA]

```

Argumentos:

- `caso_negocio`: O domínio de negócio para gerar dados (obrigatório)
- `-dim-rows`: Número de linhas para tabela de dimensão (padrão: 40)
- `-fact-rows`: Número de linhas para tabela de fatos (padrão: 10000)
- `-output-dir`: Diretório para salvar os arquivos de saída (padrão: 'data')

### Exemplos

Gerar dados de restaurante com configurações padrão:

```bash
python el_dados.py restaurant

```

Gerar dados bancários com contagens de linhas personalizadas:

```bash
python el_dados.py banking --dim-rows 100 --fact-rows 50000

```

Gerar dados de e-commerce e salvar em um diretório específico:

```bash
python el_dados.py ecommerce --output-dir meus_dados

```

### Usando como um Módulo

Você também pode importar e usar os geradores em seu próprio código Python:

```python
from el_dados import BankingDataGenerator, generate_data, save_data

# Opção 1: Use a função generate_data
dim_df, fact_df = generate_data('banking', num_dim_rows=50, num_fact_rows=5000)

# Opção 2: Use um gerador específico diretamente
banking_gen = BankingDataGenerator()
dim_df = banking_gen.generate_dimension(num_rows=50)
fact_df = banking_gen.generate_facts(dim_df, num_rows=5000)

# Salve os dados gerados
save_data(dim_df, fact_df, 'banking', output_dir='meus_dados')

```

## Domínios de Negócios Disponíveis

- `restaurant`: Dados de restaurante fast food
- `marketing`: Dados de campanha de marketing
- `banking`: Dados de transações bancárias
- `healthcare`: Dados de atendimento de saúde
- `ecommerce`: Dados de pedidos de e-commerce
- `callcenter`: Dados de atendimento de call center
- `education`: Dados de aulas educacionais
- `realestate`: Dados de transações imobiliárias
- `supplychain`: Dados de operações de cadeia de suprimentos

## Esquema de Dados

Cada domínio de negócio gera duas tabelas:

1. **Tabela de Dimensão**: Contém informações sobre entidades (pessoas, funcionários, agentes, etc.)
2. **Tabela de Fatos**: Contém dados transacionais relacionados às entidades na tabela de dimensão

As tabelas são vinculadas por um identificador comum (geralmente CPF).

## Licença

Este projeto está licenciado sob a Licença MIT com Atribuição - veja o arquivo [LICENSE](https://www.notion.so/LICENSE) para detalhes.

## Atribuição

Se você usar este código em seu projeto, deve incluir a seguinte atribuição:

```
Este projeto usa código do Megazord Data Generator por [Seu Nome].
GitHub: <https://github.com/seuusuario/megazord-data-generator>

```

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

1. Faça um fork do repositório
2. Crie sua branch de recurso (`git checkout -b feature/recurso-incrivel`)
3. Faça commit de suas alterações (`git commit -m 'Adicionar algum recurso incrível'`)
4. Envie para a branch (`git push origin feature/recurso-incrivel`)
5. Abra um Pull Request

## Agradecimentos

- Biblioteca [Faker](https://faker.readthedocs.io/) para gerar dados falsos realistas
- [Pandas](https://pandas.pydata.org/) para manipulação de dados

## Requirements.txt

Aqui está o conteúdo para o arquivo requirements.txt:

```
Faker==37.0.2
numpy==2.2.4
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2025.1
six==1.17.0
tzdata==2025.1

```
