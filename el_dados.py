
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import argparse
import sys
import os

# Configure Faker for Brazilian Portuguese
fake = Faker('pt_BR')

def generate_cpf() -> str:
    """Generate a unique CPF number"""
    return fake.cpf()

# Maximum number of rows for dimension tables, and number of rows for fact tables
NUM_ROWS_DIM = 40
NUM_ROWS_FACT = 10000

###############################
# Utility Functions
###############################

def gerar_categoria_e_estabelecimento() -> Tuple[str, str]:
    """Generate a category and establishment pair"""
    categorias_estabelecimentos = {
        'Alimentação': [
            'Restaurante Gourmet', 'Fast Food', 'Padaria Premium', 
            'Cafeteria Especializada', 'Mercado Orgânico'
        ],
        'Transporte': [
            'Aplicativo de Mobilidade', 'Posto de Combustível', 
            'Estacionamento', 'Pedágio', 'Locadora de Veículos'
        ],
        'Entretenimento': [
            'Cinema Premium', 'Teatro Municipal', 'Streaming', 
            'Casa de Shows', 'Parque Temático'
        ],
        'Saúde': [
            'Farmácia', 'Academia Premium', 'Clínica Especializada', 
            'Laboratório', 'Plano de Saúde'
        ],
        'Educação': [
            'Livraria', 'Curso Online', 'Material Escolar', 
            'Mensalidade', 'Plataforma Educacional'
        ],
        'Vestuário': [
            'Loja de Departamento', 'Boutique de Luxo', 
            'Fast Fashion', 'Outlet Premium', 'E-commerce'
        ],
        'Serviços': [
            'Assinatura Digital', 'Serviço de Streaming', 
            'Aplicativo Premium', 'Seguro', 'Manutenção'
        ],
        'Viagem': [
            'Companhia Aérea', 'Hotel de Luxo', 'Agência de Viagens', 
            'Cruzeiro', 'Aluguel por Temporada'
        ]
    }
    
    categoria = random.choice(list(categorias_estabelecimentos.keys()))
    estabelecimento = random.choice(categorias_estabelecimentos[categoria])
    
    return categoria, estabelecimento

###############################
# Fast Food Data Generator
###############################

class FastFoodDataGenerator:
    """Generates sample data for fast food business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with employee data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Data_Nascimento': [fake.date_of_birth(minimum_age=18, maximum_age=65) 
                              for _ in range(num_rows)],
            'Endereço': [fake.street_address() for _ in range(num_rows)],
            'Cidade': [fake.city() for _ in range(num_rows)],
            'Estado': [fake.estado_sigla() for _ in range(num_rows)],
            'CEP': [fake.postcode() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Cargo': [random.choice([
                'Atendente', 'Cozinheiro', 'Gerente', 
                'Caixa', 'Auxiliar', 'Supervisor'
            ]) for _ in range(num_rows)],
            'Turno': [random.choice([
                'Manhã', 'Tarde', 'Noite', 'Madrugada'
            ]) for _ in range(num_rows)],
            'Data_Admissao': [fake.date_between(start_date='-5y', end_date='today') 
                            for _ in range(num_rows)],
            'Salario': [round(random.uniform(1320, 5000), 2) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Afastado', 'Treinamento'
            ]) for _ in range(num_rows)],
            'Setor': [random.choice([
                'Cozinha', 'Atendimento', 'Caixa', 'Limpeza', 'Delivery'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with transaction data"""
        cpfs = dim_df['CPF'].tolist()
        
        # Enhanced transaction data for better insights
        data = {
            'CPF': [random.choice(cpfs) for _ in range(num_rows)],
            'Transacao_ID': [fake.uuid4() for _ in range(num_rows)],
            'Data_Transacao': [fake.date_time_between(
                start_date='-1y', end_date='now'
            ) for _ in range(num_rows)],
            'Valor_Total': [round(random.uniform(10, 300), 2) for _ in range(num_rows)],
            'Quantidade_Itens': [random.randint(1, 10) for _ in range(num_rows)],
            'Item_Principal': [random.choice([
                'Hambúrguer Simples', 'Hambúrguer Duplo',
                'Pizza Grande', 'Pizza Média',
                'Combo Família', 'Combo Individual',
                'Salada Premium', 'Sobremesa Especial'
            ]) for _ in range(num_rows)],
            'Acompanhamentos': [random.choice([
                'Batata Frita Grande', 'Batata Frita Média',
                'Onion Rings', 'Salada Caesar',
                'Sem Acompanhamento'
            ]) for _ in range(num_rows)],
            'Bebida': [random.choice([
                'Refrigerante 500ml', 'Refrigerante 700ml',
                'Suco Natural', 'Água Mineral',
                'Milk Shake Premium', 'Sem Bebida'
            ]) for _ in range(num_rows)],
            'Tipo_Pedido': [random.choice([
                'Delivery Express', 'Balcão Rápido',
                'Drive-thru', 'Mesa VIP',
                'Take Away Premium'
            ]) for _ in range(num_rows)],
            'Tempo_Preparo_Min': [random.randint(5, 45) for _ in range(num_rows)],
            'Desconto_Aplicado': [round(random.uniform(0, 30), 2) for _ in range(num_rows)],
            'Forma_Pagamento': [random.choice([
                'Dinheiro', 'Cartão Débito',
                'Cartão Crédito', 'Pix',
                'Vale Refeição', 'App Próprio'
            ]) for _ in range(num_rows)],
            'Avaliacao_Cliente': [random.randint(1, 5) for _ in range(num_rows)],
            'Status_Pedido': [random.choice([
                'Concluído', 'Em Preparo',
                'Cancelado', 'Em Entrega',
                'Aguardando Retirada'
            ]) for _ in range(num_rows)],
            'Canal_Venda': [random.choice([
                'App Próprio Premium', 'iFood Plus',
                'Uber Eats Select', 'Rappi Prime',
                'Presencial VIP'
            ]) for _ in range(num_rows)],
            'Custo_Operacional': [round(random.uniform(5, 100), 2) for _ in range(num_rows)],
            'Margem_Lucro': [round(random.uniform(0.1, 0.6), 2) for _ in range(num_rows)],
            'Tempo_Entrega_Min': [random.randint(10, 90) for _ in range(num_rows)],
            'Satisfacao_Entrega': [random.randint(1, 5) for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Marketing Data Generator
###############################

class MarketingDataGenerator:
    """Generates sample data for marketing business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with marketing professionals data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Departamento': [random.choice([
                'Marketing Digital', 'Branding', 'Mídia Social', 
                'Conteúdo', 'SEO', 'Eventos', 'Relações Públicas'
            ]) for _ in range(num_rows)],
            'Cargo': [random.choice([
                'Analista Jr', 'Analista Pleno', 'Analista Sênior', 
                'Coordenador', 'Gerente', 'Diretor', 'CMO'
            ]) for _ in range(num_rows)],
            'Data_Admissao': [fake.date_between(start_date='-5y', end_date='today') 
                            for _ in range(num_rows)],
            'Especialidade': [random.choice([
                'Google Ads', 'Facebook Ads', 'Email Marketing', 
                'Inbound Marketing', 'Growth Hacking', 'Copywriting', 'Analytics'
            ]) for _ in range(num_rows)],
            'Nivel_Experiencia': [random.choice([
                'Iniciante', 'Intermediário', 'Avançado', 'Especialista'
            ]) for _ in range(num_rows)],
            'Certificacoes': [random.choice([
                'Google Analytics', 'HubSpot', 'Facebook Blueprint', 
                'Google Ads', 'Nenhuma', 'Múltiplas'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with marketing campaign data"""
        cpfs = dim_df['CPF'].tolist()
        
        data = {
            'CPF': [random.choice(cpfs) for _ in range(num_rows)],
            'Campanha_ID': [fake.uuid4() for _ in range(num_rows)],
            'Nome_Campanha': [f"Campanha {fake.word().capitalize()} {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])}" 
                             for _ in range(num_rows)],
            'Data_Inicio': [fake.date_between(start_date='-1y', end_date='today') 
                           for _ in range(num_rows)],
            'Data_Fim': [fake.date_between(start_date='today', end_date='+6m') 
                        for _ in range(num_rows)],
            'Canal': [random.choice([
                'Email', 'Social Media', 'Google Ads', 'Facebook Ads', 
                'Instagram', 'LinkedIn', 'TikTok', 'YouTube'
            ]) for _ in range(num_rows)],
            'Orcamento': [round(random.uniform(1000, 50000), 2) for _ in range(num_rows)],
            'Gasto_Real': [round(random.uniform(800, 60000), 2) for _ in range(num_rows)],
            'Impressoes': [random.randint(1000, 1000000) for _ in range(num_rows)],
            'Cliques': [random.randint(100, 50000) for _ in range(num_rows)],
            'Conversoes': [random.randint(1, 1000) for _ in range(num_rows)],
            'CTR': [round(random.uniform(0.01, 0.15), 4) for _ in range(num_rows)],
            'CPC': [round(random.uniform(0.5, 10), 2) for _ in range(num_rows)],
            'CPA': [round(random.uniform(5, 200), 2) for _ in range(num_rows)],
            'ROI': [round(random.uniform(-0.5, 10), 2) for _ in range(num_rows)],
            'Publico_Alvo': [random.choice([
                'Jovens 18-24', 'Adultos 25-34', 'Adultos 35-44', 
                'Sênior 45-65', 'Empresas B2B', 'Pais e Mães', 'Estudantes'
            ]) for _ in range(num_rows)],
            'Objetivo': [random.choice([
                'Awareness', 'Consideração', 'Conversão', 
                'Retenção', 'Fidelização', 'Engajamento'
            ]) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativa', 'Pausada', 'Concluída', 'Planejada', 'Cancelada'
            ]) for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Banking Data Generator
###############################

class BankingDataGenerator:
    """Generates sample data for banking business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with banking customers data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Data_Nascimento': [fake.date_of_birth(minimum_age=18, maximum_age=80) 
                              for _ in range(num_rows)],
                      'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Endereco': [fake.street_address() for _ in range(num_rows)],
            'Cidade': [fake.city() for _ in range(num_rows)],
            'Estado': [fake.estado_sigla() for _ in range(num_rows)],
            'CEP': [fake.postcode() for _ in range(num_rows)],
            'Renda_Mensal': [round(random.uniform(1500, 30000), 2) for _ in range(num_rows)],
            'Score_Credito': [random.randint(100, 1000) for _ in range(num_rows)],
            'Tipo_Conta': [random.choice([
                'Corrente', 'Poupança', 'Salário', 'Digital', 'Premium', 'Universitária'
            ]) for _ in range(num_rows)],
            'Data_Abertura_Conta': [fake.date_between(start_date='-10y', end_date='today') 
                                  for _ in range(num_rows)],
            'Saldo_Atual': [round(random.uniform(-1000, 50000), 2) for _ in range(num_rows)],
            'Limite_Credito': [round(random.uniform(500, 25000), 2) for _ in range(num_rows)],
            'Tipo_Cartao': [random.choice([
                'Básico', 'Gold', 'Platinum', 'Black', 'Infinite', 'Corporate', 'Empresarial', 'Sem Cartão'
            ]) for _ in range(num_rows)],
            'Programa_Fidelidade': [random.choice([
                'Pontos Básico', 'Milhas Premium', 'Cashback', 'Rewards Plus', 'Nenhum'
            ]) for _ in range(num_rows)],
            'Segmento': [random.choice([
                'Varejo', 'Alta Renda', 'Private', 'Corporate', 'Empresarial', 'Universitário'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with banking transaction data"""
        transacoes = []
        pessoas = dim_df.to_dict('records')
        
        for _ in range(num_rows):
            pessoa = random.choice(pessoas)
            cpf = pessoa['CPF']
            
            # Gerar data da transação
            data_transacao = fake.date_time_between(start_date='-1y', end_date='now')
            
            # Gerar data de vencimento (para transações de crédito)
            data_vencimento = data_transacao + timedelta(days=random.choice([10, 15, 30]))
            
            # Gerar data de pagamento (pode ser antes ou depois do vencimento)
            offset = random.randint(-5, 15)  # Dias antes ou depois do vencimento
            data_pagamento = data_vencimento + timedelta(days=offset)
            
            # Gerar valor da transação baseado no tipo de cartão
            tipo_cartao = pessoa['Tipo_Cartao']
            if tipo_cartao in ['Black', 'Infinite', 'Corporate']:
                valor = round(random.uniform(100, 5000), 2)
            elif tipo_cartao in ['Gold', 'Platinum', 'Empresarial']:
                valor = round(random.uniform(50, 1000), 2)
            else:
                valor = round(random.uniform(10, 500), 2)
            
            # Gerar categoria e estabelecimento
            categoria, estabelecimento = gerar_categoria_e_estabelecimento()
            
            # Adicionar à lista de transações
            transacoes.append({
                'CPF': cpf,
                'Transacao_ID': fake.uuid4(),
                'Data_Transacao': data_transacao,
                'Valor_Transacao': valor,
                'Categoria_Compra': categoria,
                'Estabelecimento': estabelecimento,
                'Cidade_Transacao': fake.city(),
                'Estado_Transacao': fake.estado_sigla(),
                'Pais_Transacao': 'Brasil' if random.random() < 0.9 else fake.country(),
                'Moeda': 'BRL' if random.random() < 0.9 else random.choice(['USD', 'EUR', 'GBP']),
                'Metodo_Pagamento': random.choice([
                    'Crédito à Vista', 'Crédito Parcelado', 'Débito',
                    'Contactless', 'Mobile Payment', 'QR Code'
                ]),
                'Numero_Parcelas': random.randint(1, 12) if random.random() < 0.3 else 1,
                'Canal_Transacao': random.choice([
                    'Loja Física', 'E-commerce', 'Aplicativo', 'Telefone',
                    'Recorrente', 'Internacional'
                ]),
                'Status_Transacao': random.choice([
                    'Aprovada', 'Negada', 'Em análise', 'Cancelada',
                    'Estornada', 'Contestada'
                ]),
                'Data_Vencimento': data_vencimento,
                'Data_Pagamento': data_pagamento if random.random() < 0.95 else None,
                'Valor_Juros': round(valor * 0.15 * (offset/30), 2) if offset > 0 else 0,
                'Valor_IOF': round(valor * 0.0638, 2) if random.random() < 0.1 else 0,
                'Pontos_Acumulados': int(valor * random.uniform(0.5, 2.0)) if pessoa['Programa_Fidelidade'] != 'Nenhum' else 0,
                'Taxa_Cambio': round(random.uniform(4.5, 5.5), 2) if random.random() < 0.1 else None
            })
        
        return pd.DataFrame(transacoes)

###############################
# Healthcare Data Generator
###############################

class HealthcareDataGenerator:
    """Generates sample data for healthcare business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with healthcare professionals data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'CRM': [f"{random.randint(10000, 99999)}-{fake.estado_sigla()}" for _ in range(num_rows)],
            'Especialidade': [random.choice([
                'Clínica Geral', 'Cardiologia', 'Pediatria', 'Ortopedia',
                'Ginecologia', 'Neurologia', 'Dermatologia', 'Psiquiatria',
                'Oftalmologia', 'Endocrinologia', 'Oncologia', 'Urologia'
            ]) for _ in range(num_rows)],
            'Departamento': [random.choice([
                'Emergência', 'Ambulatório', 'Centro Cirúrgico', 'UTI',
                'Enfermaria', 'Maternidade', 'Pediatria', 'Oncologia'
            ]) for _ in range(num_rows)],
            'Hospital': [f"Hospital {fake.last_name()} {random.choice(['Central', 'Regional', 'Especializado', 'Universitário'])}" 
                       for _ in range(num_rows)],
            'Data_Contratacao': [fake.date_between(start_date='-15y', end_date='today') 
                               for _ in range(num_rows)],
            'Carga_Horaria': [random.choice([20, 30, 40, 60]) for _ in range(num_rows)],
            'Salario': [round(random.uniform(5000, 30000), 2) for _ in range(num_rows)],
            'Plantoes_Mensais': [random.randint(0, 10) for _ in range(num_rows)],
            'Nivel': [random.choice([
                'Residente', 'Especialista', 'Sênior', 'Chefe de Equipe', 'Diretor Clínico'
            ]) for _ in range(num_rows)],
            'Titulacao': [random.choice([
                'Graduação', 'Especialização', 'Mestrado', 'Doutorado', 'Pós-Doutorado'
            ]) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Licença', 'Afastado', 'Treinamento'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with healthcare attendance data"""
        cpfs = dim_df['CPF'].tolist()
        
        data = {
            'CPF_Medico': [random.choice(cpfs) for _ in range(num_rows)],
            'Atendimento_ID': [fake.uuid4() for _ in range(num_rows)],
            'CPF_Paciente': [generate_cpf() for _ in range(num_rows)],
            'Data_Atendimento': [fake.date_time_between(start_date='-1y', end_date='now') 
                               for _ in range(num_rows)],
            'Tipo_Atendimento': [random.choice([
                'Consulta', 'Emergência', 'Cirurgia', 'Exame', 
                'Retorno', 'Telemedicina', 'Procedimento'
            ]) for _ in range(num_rows)],
            'Diagnostico_Principal': [random.choice([
                'Hipertensão', 'Diabetes', 'Infecção Respiratória', 'Trauma',
                'Cardiopatia', 'Transtorno Psiquiátrico', 'Câncer', 'Gestação',
                'Doença Autoimune', 'Obesidade', 'Fratura', 'Check-up'
            ]) for _ in range(num_rows)],
            'Gravidade': [random.choice(['Baixa', 'Média', 'Alta', 'Crítica']) 
                        for _ in range(num_rows)],
            'Tempo_Atendimento_Min': [random.randint(10, 180) for _ in range(num_rows)],
            'Medicamentos_Prescritos': [random.randint(0, 8) for _ in range(num_rows)],
            'Exames_Solicitados': [random.randint(0, 5) for _ in range(num_rows)],
            'Valor_Procedimento': [round(random.uniform(50, 10000), 2) for _ in range(num_rows)],
            'Convenio': [random.choice([
                'SUS', 'Unimed', 'Bradesco Saúde', 'Amil', 'SulAmérica',
                'Particular', 'Golden Cross', 'Notredame Intermédica'
            ]) for _ in range(num_rows)],
            'Retorno_Agendado': [random.choice([True, False]) for _ in range(num_rows)],
            'Internacao': [random.choice([True, False]) for _ in range(num_rows)],
            'Dias_Internacao': [random.randint(1, 30) if random.random() < 0.3 else 0 
                              for _ in range(num_rows)],
            'Satisfacao_Paciente': [random.randint(1, 5) for _ in range(num_rows)],
            'Complicacoes': [random.choice([True, False]) for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# E-commerce Data Generator
###############################

class EcommerceDataGenerator:
    """Generates sample data for e-commerce business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with e-commerce customers data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Data_Nascimento': [fake.date_of_birth(minimum_age=18, maximum_age=80) 
                              for _ in range(num_rows)],
            'Endereco_Entrega': [fake.street_address() for _ in range(num_rows)],
            'Cidade': [fake.city() for _ in range(num_rows)],
            'Estado': [fake.estado_sigla() for _ in range(num_rows)],
            'CEP': [fake.postcode() for _ in range(num_rows)],
            'Data_Cadastro': [fake.date_between(start_date='-5y', end_date='today') 
                            for _ in range(num_rows)],
            'Ultima_Compra': [fake.date_between(start_date='-1y', end_date='today') 
                            for _ in range(num_rows)],
            'Total_Compras': [random.randint(1, 50) for _ in range(num_rows)],
            'Valor_Total_Gasto': [round(random.uniform(100, 10000), 2) for _ in range(num_rows)],
            'Categoria_Preferida': [random.choice([
                'Eletrônicos', 'Moda', 'Casa e Decoração', 'Esportes',
                'Beleza e Saúde', 'Livros', 'Alimentos', 'Brinquedos'
            ]) for _ in range(num_rows)],
            'Dispositivo_Preferido': [random.choice([
                'Desktop', 'Mobile', 'Tablet', 'App'
            ]) for _ in range(num_rows)],
            'Programa_Fidelidade': [random.choice([
                'Bronze', 'Prata', 'Ouro', 'Diamante', 'Não Participante'
            ]) for _ in range(num_rows)],
            'Newsletter': [random.choice([True, False]) for _ in range(num_rows)],
            'Cupom_Ativo': [random.choice([True, False]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
            """Generate fact table with e-commerce transaction data"""
            cpfs = dim_df['CPF'].tolist()
            
            data = {
                'CPF': [random.choice(cpfs) for _ in range(num_rows)],
                'Pedido_ID': [fake.uuid4() for _ in range(num_rows)],
                'Data_Pedido': [fake.date_time_between(start_date='-1y', end_date='now') 
                            for _ in range(num_rows)],
                'Valor_Total': [round(random.uniform(20, 2000), 2) for _ in range(num_rows)],
                'Quantidade_Itens': [random.randint(1, 15) for _ in range(num_rows)],
                'Categoria_Principal': [random.choice([
                    'Eletrônicos', 'Moda', 'Casa e Decoração', 'Esportes',
                    'Beleza e Saúde', 'Livros', 'Alimentos', 'Brinquedos'
                ]) for _ in range(num_rows)],
                'Produto_Principal': [f"{random.choice(['Smartphone', 'Notebook', 'TV', 'Tênis', 'Camiseta', 'Livro', 'Perfume', 'Relógio'])} {fake.word().capitalize()}" 
                                    for _ in range(num_rows)],
                'Valor_Frete': [round(random.uniform(0, 50), 2) for _ in range(num_rows)],
                'Cupom_Desconto': [round(random.uniform(0, 100), 2) if random.random() < 0.3 else 0 
                                for _ in range(num_rows)],
                'Metodo_Pagamento': [random.choice([
                    'Cartão de Crédito', 'Boleto', 'Pix', 'PayPal',
                    'Cartão de Débito', 'Vale-Presente', 'Transferência Bancária'
                ]) for _ in range(num_rows)],
                'Parcelas': [random.randint(1, 12) if random.random() < 0.6 else 1 
                        for _ in range(num_rows)],
                'Status_Pedido': [random.choice([
                    'Aguardando Pagamento', 'Pagamento Aprovado', 'Em Separação',
                    'Em Transporte', 'Entregue', 'Cancelado', 'Devolvido'
                ]) for _ in range(num_rows)],
                'Data_Entrega': [fake.date_between(start_date='today', end_date='+30d') 
                            if random.random() < 0.8 else None for _ in range(num_rows)],
                'Tempo_Entrega_Dias': [random.randint(1, 30) for _ in range(num_rows)],
                'Avaliacao_Produto': [random.randint(1, 5) if random.random() < 0.7 else None 
                                    for _ in range(num_rows)],
                'Comentario': [fake.text(max_nb_chars=100) if random.random() < 0.3 else None 
                            for _ in range(num_rows)],
                'Dispositivo_Compra': [random.choice([
                    'Desktop', 'Mobile Android', 'Mobile iOS', 'Tablet', 'App'
                ]) for _ in range(num_rows)],
                'Canal_Aquisicao': [random.choice([
                    'Busca Orgânica', 'Google Ads', 'Facebook Ads', 'Email Marketing',
                    'Indicação', 'Instagram', 'Comparador de Preços', 'Link Direto'
                ]) for _ in range(num_rows)],
                'Devolucao': [random.choice([True, False]) for _ in range(num_rows)],
                'Motivo_Devolucao': [random.choice([
                    'Produto Danificado', 'Tamanho Incorreto', 'Cor Diferente',
                    'Arrependimento', 'Produto Errado', None
                ]) for _ in range(num_rows)]
            }
            
            return pd.DataFrame(data)

###############################
# Call Center Data Generator
###############################

class CallCenterDataGenerator:
    """Generates sample data for call center business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with call center agents data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Data_Nascimento': [fake.date_of_birth(minimum_age=18, maximum_age=60) 
                              for _ in range(num_rows)],
            'Data_Contratacao': [fake.date_between(start_date='-5y', end_date='today') 
                               for _ in range(num_rows)],
            'Nivel': [random.choice([
                'Júnior', 'Pleno', 'Sênior', 'Especialista', 'Supervisor'
            ]) for _ in range(num_rows)],
            'Equipe': [random.choice([
                'Suporte Técnico', 'Vendas', 'SAC', 'Retenção',
                'Cobrança', 'Ouvidoria', 'Backoffice'
            ]) for _ in range(num_rows)],
            'Turno': [random.choice([
                'Manhã', 'Tarde', 'Noite', 'Madrugada', 'Integral'
            ]) for _ in range(num_rows)],
            'Idiomas': [random.choice([
                'Português', 'Português/Inglês', 'Português/Espanhol',
                'Português/Inglês/Espanhol', 'Português/Francês'
            ]) for _ in range(num_rows)],
            'Habilidades': [random.choice([
                'Técnico', 'Vendas', 'Negociação', 'Resolução de Problemas',
                'Atendimento Premium', 'Multiskill', 'Especialista'
            ]) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Afastado', 'Treinamento', 'Desligado'
            ]) for _ in range(num_rows)],
            'Salario': [round(random.uniform(1500, 5000), 2) for _ in range(num_rows)],
            'Meta_Mensal': [random.randint(100, 500) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with call center attendance data"""
        cpfs = dim_df['CPF'].tolist()
        equipes = dim_df['Equipe'].tolist()
        
        data = {
            'CPF_Atendente': [random.choice(cpfs) for _ in range(num_rows)],
            'Chamada_ID': [fake.uuid4() for _ in range(num_rows)],
            'Data_Hora_Inicio': [fake.date_time_between(start_date='-1y', end_date='now') 
                               for _ in range(num_rows)],
            'Duracao_Segundos': [random.randint(30, 3600) for _ in range(num_rows)],
            'Tipo_Chamada': [random.choice([
                'Receptiva', 'Ativa', 'Transferida', 'Retorno'
            ]) for _ in range(num_rows)],
            'Assunto': [random.choice([
                'Dúvida Técnica', 'Reclamação', 'Cancelamento', 'Compra',
                'Informação', 'Suporte', 'Cobrança', 'Elogio'
            ]) for _ in range(num_rows)],
            'Equipe': [random.choice(equipes) for _ in range(num_rows)],
            'Prioridade': [random.choice(['Baixa', 'Média', 'Alta', 'Crítica']) 
                         for _ in range(num_rows)],
            'Tempo_Espera_Segundos': [random.randint(0, 900) for _ in range(num_rows)],
            'Transferencias': [random.randint(0, 5) for _ in range(num_rows)],
            'Resolucao_Primeiro_Contato': [random.choice([True, False]) 
                                         for _ in range(num_rows)],
            'Satisfacao_Cliente': [random.randint(1, 5) if random.random() < 0.7 else None 
                                 for _ in range(num_rows)],
            'Protocolo': [f"{fake.random_number(digits=10)}" for _ in range(num_rows)],
            'Canal': [random.choice([
                'Telefone', 'Chat', 'Email', 'WhatsApp', 'Redes Sociais', 'App'
            ]) for _ in range(num_rows)],
            'Status_Final': [random.choice([
                'Resolvido', 'Pendente', 'Escalado', 'Abandonado', 'Transferido'
            ]) for _ in range(num_rows)],
            'Feedback': [fake.text(max_nb_chars=100) if random.random() < 0.3 else None 
                       for _ in range(num_rows)],
            'Custo_Chamada': [round(random.uniform(1, 50), 2) for _ in range(num_rows)],
            'Venda_Realizada': [random.choice([True, False]) for _ in range(num_rows)],
            'Valor_Venda': [round(random.uniform(50, 1000), 2) if random.random() < 0.3 else 0 
                          for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Education Data Generator
###############################

class EducationDataGenerator:
    """Generates sample data for education business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with education professionals data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Data_Nascimento': [fake.date_of_birth(minimum_age=25, maximum_age=70) 
                              for _ in range(num_rows)],
            'Formacao': [random.choice([
                'Licenciatura', 'Bacharelado', 'Especialização', 
                'Mestrado', 'Doutorado', 'Pós-Doutorado'
            ]) for _ in range(num_rows)],
            'Area_Conhecimento': [random.choice([
                'Exatas', 'Humanas', 'Biológicas', 'Linguagens', 
                'Tecnologia', 'Artes', 'Saúde', 'Negócios'
            ]) for _ in range(num_rows)],
            'Disciplina': [random.choice([
                'Matemática', 'Português', 'História', 'Geografia', 
                'Física', 'Química', 'Biologia', 'Inglês', 
                'Educação Física', 'Artes', 'Filosofia', 'Sociologia'
            ]) for _ in range(num_rows)],
            'Instituicao': [f"Escola {fake.last_name()} {random.choice(['Municipal', 'Estadual', 'Federal', 'Particular'])}" 
                          for _ in range(num_rows)],
            'Cargo': [random.choice([
                'Professor', 'Coordenador', 'Diretor', 'Orientador', 
                'Pedagogo', 'Tutor', 'Monitor', 'Pesquisador'
            ]) for _ in range(num_rows)],
            'Tempo_Experiencia_Anos': [random.randint(1, 40) for _ in range(num_rows)],
            'Carga_Horaria_Semanal': [random.choice([20, 30, 40, 60]) for _ in range(num_rows)],
            'Salario': [round(random.uniform(2000, 15000), 2) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Licença', 'Afastado', 'Aposentado'
            ]) for _ in range(num_rows)],
            'Nivel_Ensino': [random.choice([
                'Infantil', 'Fundamental I', 'Fundamental II', 
                'Médio', 'Superior', 'Pós-Graduação', 'EJA'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with education class data"""
        cpfs = dim_df['CPF'].tolist()
        disciplinas = dim_df['Disciplina'].tolist()
        
        data = {
            'CPF_Professor': [random.choice(cpfs) for _ in range(num_rows)],
            'Aula_ID': [fake.uuid4() for _ in range(num_rows)],
            'Data_Aula': [fake.date_time_between(start_date='-1y', end_date='now') 
                        for _ in range(num_rows)],
            'Disciplina': [random.choice(disciplinas) for _ in range(num_rows)],
            'Turma': [f"{random.choice(['1º', '2º', '3º', '4º', '5º', '6º', '7º', '8º', '9º'])} {random.choice(['A', 'B', 'C', 'D', 'E'])}" 
                    for _ in range(num_rows)],
            'Quantidade_Alunos': [random.randint(15, 50) for _ in range(num_rows)],
            'Presenca_Percentual': [round(random.uniform(0.5, 1.0), 2) for _ in range(num_rows)],
                        'Duracao_Minutos': [random.choice([50, 100, 150]) for _ in range(num_rows)],
            'Conteudo': [f"Módulo {random.randint(1, 10)}: {fake.sentence(nb_words=5)}" 
                       for _ in range(num_rows)],
            'Metodologia': [random.choice([
                'Expositiva', 'Prática', 'Projeto', 'Debate', 
                'Seminário', 'Laboratório', 'Híbrida', 'EAD'
            ]) for _ in range(num_rows)],
            'Recursos_Utilizados': [random.choice([
                'Lousa', 'Projetor', 'Computadores', 'Livros', 
                'Apostilas', 'Experimentos', 'Plataforma Digital'
            ]) for _ in range(num_rows)],
            'Avaliacao_Aplicada': [random.choice([True, False]) for _ in range(num_rows)],
            'Media_Notas': [round(random.uniform(0, 10), 1) if random.random() < 0.7 else None 
                          for _ in range(num_rows)],
            'Participacao_Alunos': [random.choice([
                'Baixa', 'Média', 'Alta', 'Excelente'
            ]) for _ in range(num_rows)],
            'Dificuldades_Encontradas': [random.choice([
                'Nenhuma', 'Comportamento', 'Aprendizado', 'Infraestrutura', 
                'Material Didático', 'Tempo Insuficiente', 'Heterogeneidade'
            ]) for _ in range(num_rows)],
            'Atividade_Extraclasse': [random.choice([True, False]) for _ in range(num_rows)],
            'Observacoes': [fake.text(max_nb_chars=100) if random.random() < 0.3 else None 
                          for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Real Estate Data Generator
###############################

class RealEstateDataGenerator:
    """Generates sample data for real estate business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with real estate agents data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'CRECI': [f"{random.randint(10000, 99999)}-{fake.estado_sigla()}" 
                    for _ in range(num_rows)],
            'Data_Admissao': [fake.date_between(start_date='-10y', end_date='today') 
                            for _ in range(num_rows)],
            'Regiao_Atuacao': [random.choice([
                'Zona Sul', 'Zona Norte', 'Zona Leste', 'Zona Oeste', 
                'Centro', 'Região Metropolitana', 'Litoral', 'Interior'
            ]) for _ in range(num_rows)],
            'Especialidade': [random.choice([
                'Residencial', 'Comercial', 'Industrial', 'Rural', 
                'Lançamentos', 'Alto Padrão', 'Econômico', 'Investimentos'
            ]) for _ in range(num_rows)],
            'Nivel': [random.choice([
                'Júnior', 'Pleno', 'Sênior', 'Master', 'Diretor'
            ]) for _ in range(num_rows)],
            'Certificacoes': [random.choice([
                'Nenhuma', 'Avaliador', 'Consultor', 'Perito', 'Múltiplas'
            ]) for _ in range(num_rows)],
            'Modelo_Trabalho': [random.choice([
                'CLT', 'Autônomo', 'PJ', 'Associado', 'Franqueado'
            ]) for _ in range(num_rows)],
            'Comissao_Percentual': [round(random.uniform(1.5, 6.0), 2) for _ in range(num_rows)],
            'Meta_Mensal': [round(random.uniform(50000, 500000), 2) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Afastado', 'Treinamento', 'Desligado'
            ]) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with real estate transaction data"""
        cpfs = dim_df['CPF'].tolist()
        
        data = {
            'CPF_Corretor': [random.choice(cpfs) for _ in range(num_rows)],
            'Transacao_ID': [fake.uuid4() for _ in range(num_rows)],
            'Data_Transacao': [fake.date_time_between(start_date='-1y', end_date='now') 
                             for _ in range(num_rows)],
            'Tipo_Imovel': [random.choice([
                'Apartamento', 'Casa', 'Sobrado', 'Terreno', 'Sala Comercial', 
                'Galpão', 'Loja', 'Cobertura', 'Flat', 'Sítio', 'Fazenda'
            ]) for _ in range(num_rows)],
            'Endereco': [fake.street_address() for _ in range(num_rows)],
            'Bairro': [fake.bairro() for _ in range(num_rows)],
            'Cidade': [fake.city() for _ in range(num_rows)],
            'Estado': [fake.estado_sigla() for _ in range(num_rows)],
            'CEP': [fake.postcode() for _ in range(num_rows)],
            'Area_M2': [random.randint(30, 1000) for _ in range(num_rows)],
            'Quartos': [random.randint(0, 6) for _ in range(num_rows)],
            'Banheiros': [random.randint(1, 6) for _ in range(num_rows)],
            'Vagas_Garagem': [random.randint(0, 6) for _ in range(num_rows)],
            'Valor_Anunciado': [round(random.uniform(100000, 5000000), 2) 
                              for _ in range(num_rows)],
            'Valor_Transacao': [round(random.uniform(90000, 4800000), 2) 
                              for _ in range(num_rows)],
            'Tipo_Transacao': [random.choice([
                'Venda', 'Aluguel', 'Temporada', 'Permuta', 'Arrendamento'
            ]) for _ in range(num_rows)],
            'Tempo_Anuncio_Dias': [random.randint(1, 365) for _ in range(num_rows)],
            'Visitas_Realizadas': [random.randint(0, 50) for _ in range(num_rows)],
            'Propostas_Recebidas': [random.randint(0, 10) for _ in range(num_rows)],
            'Comissao_Valor': [round(random.uniform(3000, 150000), 2) 
                             for _ in range(num_rows)],
            'Financiamento': [random.choice([True, False]) for _ in range(num_rows)],
            'Banco_Financiador': [random.choice([
                'Caixa', 'Banco do Brasil', 'Itaú', 'Bradesco', 
                'Santander', 'Não Aplicável', None
            ]) for _ in range(num_rows)],
            'Captacao_Origem': [random.choice([
                'Site Próprio', 'Portal Imobiliário', 'Indicação', 
                'Anúncio', 'Redes Sociais', 'Prospecção Ativa', 'Vitrine'
            ]) for _ in range(num_rows)],
            'Status_Final': [random.choice([
                'Concluída', 'Cancelada', 'Desistência', 'Pendência Documental'
            ]) for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Supply Chain Data Generator
###############################

class SupplyChainDataGenerator:
    """Generates sample data for supply chain business analytics"""
    
    @staticmethod
    def generate_dimension(num_rows: int = NUM_ROWS_DIM) -> pd.DataFrame:
        """Generate dimension table with supply chain professionals data"""
        data = {
            'CPF': [generate_cpf() for _ in range(num_rows)],
            'Nome': [fake.name() for _ in range(num_rows)],
            'Email': [fake.email() for _ in range(num_rows)],
            'Telefone': [fake.phone_number() for _ in range(num_rows)],
            'Departamento': [random.choice([
                'Compras', 'Logística', 'Armazenagem', 'Distribuição', 
                'Planejamento', 'Importação', 'Qualidade', 'Produção'
            ]) for _ in range(num_rows)],
            'Cargo': [random.choice([
                'Analista Jr', 'Analista Pleno', 'Analista Sênior', 
                'Coordenador', 'Gerente', 'Diretor', 'Operador'
            ]) for _ in range(num_rows)],
            'Data_Admissao': [fake.date_between(start_date='-8y', end_date='today') 
                            for _ in range(num_rows)],
            'Centro_Distribuicao': [f"CD {random.choice(['Norte', 'Sul', 'Leste', 'Oeste', 'Central'])}" 
                                  for _ in range(num_rows)],
            'Nivel_Acesso': [random.choice([
                'Básico', 'Intermediário', 'Avançado', 'Administrativo', 'Total'
            ]) for _ in range(num_rows)],
            'Certificacoes': [random.choice([
                'Nenhuma', 'CPIM', 'CSCP', 'CLTD', 'Six Sigma', 'ISO', 'Múltiplas'
            ]) for _ in range(num_rows)],
            'Status': [random.choice([
                'Ativo', 'Férias', 'Afastado', 'Treinamento', 'Desligado'
            ]) for _ in range(num_rows)],
            'Salario': [round(random.uniform(2000, 20000), 2) for _ in range(num_rows)]
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def generate_facts(dim_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """Generate fact table with supply chain operation data"""
        cpfs = dim_df['CPF'].tolist()
        
        data = {
            'CPF_Responsavel': [random.choice(cpfs) for _ in range(num_rows)],
            'Operacao_ID': [fake.uuid4() for _ in range(num_rows)],
            'Data_Operacao': [fake.date_time_between(start_date='-1y', end_date='now') 
                            for _ in range(num_rows)],
            'Tipo_Operacao': [random.choice([
                'Recebimento', 'Expedição', 'Transferência', 'Inventário', 
                'Devolução', 'Descarte', 'Produção', 'Importação'
            ]) for _ in range(num_rows)],
            'Produto_Categoria': [random.choice([
                'Eletrônicos', 'Alimentos', 'Vestuário', 'Farmacêuticos', 
                'Automotivos', 'Construção', 'Higiene', 'Bebidas'
            ]) for _ in range(num_rows)],
            'Produto_ID': [f"SKU-{fake.random_number(digits=6)}" for _ in range(num_rows)],
            'Quantidade': [random.randint(1, 10000) for _ in range(num_rows)],
            'Unidade_Medida': [random.choice([
                'Unidade', 'Caixa', 'Pallet', 'Kg', 'Litro', 'Metro', 'Lote'
            ]) for _ in range(num_rows)],
            'Valor_Unitario': [round(random.uniform(0.5, 5000), 2) for _ in range(num_rows)],
            'Valor_Total': [round(random.uniform(100, 500000), 2) for _ in range(num_rows)],
            'Fornecedor': [f"{fake.company()} {random.choice(['Ltda', 'S.A.', 'ME', 'EPP', 'EIRELI'])}" 
                         for _ in range(num_rows)],
            'Origem': [random.choice([
                'Nacional', 'Importado China', 'Importado EUA', 'Importado Europa', 
                'Importado Mercosul', 'Produção Própria'
            ]) for _ in range(num_rows)],
            'Destino': [random.choice([
                'CD Norte', 'CD Sul', 'CD Leste', 'CD Oeste', 'CD Central', 
                'Loja', 'Cliente Final', 'Exportação'
            ]) for _ in range(num_rows)],
            'Meio_Transporte': [random.choice([
                'Rodoviário', 'Marítimo', 'Aéreo', 'Ferroviário', 
                'Multimodal', 'Próprio', 'Terceirizado'
            ]) for _ in range(num_rows)],
            'Custo_Frete': [round(random.uniform(10, 10000), 2) for _ in range(num_rows)],
            'Prazo_Entrega_Dias': [random.randint(1, 90) for _ in range(num_rows)],
            'Lead_Time_Dias': [random.randint(1, 120) for _ in range(num_rows)],
                        'Status_Operacao': [random.choice([
                'Concluída', 'Em Andamento', 'Atrasada', 'Cancelada', 
                'Pendente Documentação', 'Aguardando Aprovação'
            ]) for _ in range(num_rows)],
            'Problemas_Encontrados': [random.choice([
                'Nenhum', 'Avaria', 'Falta', 'Atraso', 'Qualidade',
                'Documentação', 'Transporte', None
            ]) for _ in range(num_rows)],
            'Nivel_Servico': [round(random.uniform(0.7, 1.0), 2) for _ in range(num_rows)]
        }
        
        return pd.DataFrame(data)

###############################
# Main Function
###############################

def generate_data(business_case: str, num_dim_rows: int = NUM_ROWS_DIM, num_fact_rows: int = NUM_ROWS_FACT) -> tuple:
    """
    Generate dimension and fact tables for a specific business case
    
    Parameters:
    -----------
    business_case : str
        The business case to generate data for
    num_dim_rows : int
        Number of rows to generate for dimension table
    num_fact_rows : int
        Number of rows to generate for fact table
        
    Returns:
    --------
    tuple
        (dimension_df, fact_df)
    """
    generators = {
        'restaurant': FastFoodDataGenerator,
        'marketing': MarketingDataGenerator,
        'banking': BankingDataGenerator,
        'healthcare': HealthcareDataGenerator,
        'ecommerce': EcommerceDataGenerator,
        'callcenter': CallCenterDataGenerator,
        'education': EducationDataGenerator,
        'realestate': RealEstateDataGenerator,
        'supplychain': SupplyChainDataGenerator
    }
    
    if business_case.lower() not in generators:
        raise ValueError(f"Business case '{business_case}' not supported. Available options: {', '.join(generators.keys())}")
    
    generator = generators[business_case.lower()]
    
    print(f"Generating {num_dim_rows} dimension rows for {business_case}...")
    dim_df = generator.generate_dimension(num_dim_rows)
    
    print(f"Generating {num_fact_rows} fact rows for {business_case}...")
    fact_df = generator.generate_facts(dim_df, num_fact_rows)
    
    return dim_df, fact_df

def save_data(dim_df: pd.DataFrame, fact_df: pd.DataFrame, business_case: str, output_dir: str = '.') -> None:
    """
    Save dimension and fact tables to CSV files
    
    Parameters:
    -----------
    dim_df : pd.DataFrame
        Dimension table
    fact_df : pd.DataFrame
        Fact table
    business_case : str
        The business case name
    output_dir : str
        Directory to save the files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save dimension table
    dim_path = os.path.join(output_dir, f"{business_case}_dimension.csv")
    dim_df.to_csv(dim_path, index=False)
    print(f"Dimension table saved to {dim_path}")
    
    # Save fact table
    fact_path = os.path.join(output_dir, f"{business_case}_facts.csv")
    fact_df.to_csv(fact_path, index=False)
    print(f"Fact table saved to {fact_path}")

def gerar_categoria_e_estabelecimento():
    """Generate a random purchase category and establishment"""
    categorias = {
        'Alimentação': ['Supermercado Pão de Açúcar', 'Restaurante Outback', 'McDonald\'s', 'Padaria São Paulo', 'iFood'],
        'Transporte': ['Uber', '99 Táxi', 'Posto Ipiranga', 'Estacionamento Shopping', 'Metrô SP'],
        'Saúde': ['Drogaria São Paulo', 'Farmácia Raia', 'Academia SmartFit', 'Clínica Einstein', 'Ultrafarma'],
        'Educação': ['Livraria Cultura', 'Curso Alura', 'Udemy', 'Faculdade Anhembi', 'Escola de Idiomas'],
        'Lazer': ['Cinema Cinemark', 'Netflix', 'Spotify', 'Teatro Municipal', 'Parque Hopi Hari'],
        'Vestuário': ['Renner', 'C&A', 'Zara', 'Nike Store', 'Adidas'],
        'Casa': ['Casas Bahia', 'Magazine Luiza', 'Leroy Merlin', 'Tok&Stok', 'Cobasi'],
        'Tecnologia': ['Amazon', 'Apple Store', 'Samsung Store', 'Fast Shop', 'Kabum'],
        'Serviços': ['Salão de Beleza', 'Lavanderia 5àSec', 'Conserto Celular', 'Advocacia', 'Seguro Auto'],
        'Viagem': ['Decolar.com', 'Booking.com', 'Hotel Ibis', 'Gol Linhas Aéreas', 'Airbnb']
    }
    
    categoria = random.choice(list(categorias.keys()))
    estabelecimento = random.choice(categorias[categoria])
    
    return categoria, estabelecimento

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Generate synthetic business data for analytics')
    parser.add_argument('business_case', type=str, help='Business case to generate data for')
    parser.add_argument('--dim-rows', type=int, default=NUM_ROWS_DIM, 
                        help=f'Number of dimension rows (default: {NUM_ROWS_DIM})')
    parser.add_argument('--fact-rows', type=int, default=NUM_ROWS_FACT, 
                        help=f'Number of fact rows (default: {NUM_ROWS_FACT})')
    parser.add_argument('--output-dir', type=str, default='data', 
                        help='Directory to save output files (default: data)')
    
    args = parser.parse_args()
    
    # Generate and save data
    try:
        dim_df, fact_df = generate_data(args.business_case, args.dim_rows, args.fact_rows)
        save_data(dim_df, fact_df, args.business_case, args.output_dir)
        print(f"Successfully generated data for {args.business_case} business case!")
    except Exception as e:
        print(f"Error generating data: {e}")
        sys.exit(1)



