# automacao-bioinformatica

Pipeline modular em Python para processamento de genomas procariontes e metagenomas, com foco em automação de laudos e reprodutibilidade via Docker.

## 📋 Descrição

Este projeto fornece uma pipeline bioinformática modular para:
- **Montagem de genomas** usando SPAdes
- **Visualização de dados** com Pandas e Matplotlib
- **Ambiente reproduzível** via Docker

## 🏗️ Estrutura do Projeto

```
automacao-bioinformatica/
├── main.py                 # Ponto de entrada CLI
├── src/                    # Módulos da aplicação
│   ├── __init__.py
│   ├── genome_assembly.py  # Módulo de montagem de genomas
│   └── data_visualization.py # Módulo de visualização
├── data/                   # Diretório para dados de entrada
├── tests/                  # Testes (futuro)
├── requirements.txt        # Dependências Python
├── Dockerfile             # Configuração Docker
└── README.md              # Este arquivo
```

## 🚀 Instalação

### Opção 1: Instalação Local

#### Requisitos
- Python 3.11+
- SPAdes (para montagem de genomas)

#### Passos

1. Clone o repositório:
```bash
git clone https://github.com/pietrob3elli/automacao-bioinformatica.git
cd automacao-bioinformatica
```

2. Instale as dependências Python:
```bash
pip install -r requirements.txt
```

3. Instale SPAdes:
```bash
# Ubuntu/Debian
wget http://cab.spbu.ru/files/release3.15.5/SPAdes-3.15.5-Linux.tar.gz
tar -xzf SPAdes-3.15.5-Linux.tar.gz
sudo mv SPAdes-3.15.5-Linux /opt/spades
sudo ln -s /opt/spades/bin/spades.py /usr/local/bin/spades.py
```

### Opção 2: Docker (Recomendado)

```bash
# Construir a imagem
docker build -t bioinformatics-pipeline .

# Executar o container
docker run --rm bioinformatics-pipeline
```

## 💻 Uso

### Interface de Linha de Comando

O pipeline oferece dois comandos principais: `assemble` e `visualize`.

#### Ver ajuda geral:
```bash
python main.py --help
```

#### 1. Montagem de Genomas

Montar genoma a partir de reads paired-end:

```bash
python main.py assemble \
    -1 data/reads_R1.fastq \
    -2 data/reads_R2.fastq \
    -o output/assembly \
    -t 4
```

**Opções:**
- `-1, --forward`: Arquivo FASTQ com reads forward (obrigatório)
- `-2, --reverse`: Arquivo FASTQ com reads reverse (obrigatório)
- `-o, --output`: Diretório de saída (obrigatório)
- `-t, --threads`: Número de threads (padrão: 4)
- `--careful`: Modo cuidadoso do SPAdes (reduz erros)

**Exemplo com Docker:**
```bash
docker run --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/output:/app/output \
    bioinformatics-pipeline \
    python main.py assemble \
    -1 /app/data/reads_R1.fastq \
    -2 /app/data/reads_R2.fastq \
    -o /app/output/assembly \
    -t 4
```

#### 2. Visualização de Dados

Gerar gráficos a partir de dados CSV:

```bash
python main.py visualize \
    -i data/assembly_stats.csv \
    -o output/plots \
    --plot-type all
```

**Opções:**
- `-i, --input`: Arquivo CSV com dados (obrigatório)
- `-o, --output`: Diretório de saída para gráficos (obrigatório)
- `--plot-type`: Tipo de gráfico (bar, line, histogram, all)

**Exemplo com Docker:**
```bash
docker run --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/output:/app/output \
    bioinformatics-pipeline \
    python main.py visualize \
    -i /app/data/stats.csv \
    -o /app/output/plots
```

## 📊 Exemplos de Dados

### Formato CSV para Visualização

Exemplo de arquivo CSV (`assembly_stats.csv`):

```csv
sample,contigs,total_length,n50,gc_content
sample1,45,4500000,125000,52.3
sample2,38,4200000,145000,51.8
sample3,52,4800000,110000,53.1
```

## 🔧 Desenvolvimento

### Estrutura Modular

O projeto segue princípios de design modular:

- **`main.py`**: Interface CLI usando argparse
- **`src/genome_assembly.py`**: Lógica de montagem com subprocess
- **`src/data_visualization.py`**: Visualização com Pandas/Matplotlib

### Adicionando Novos Módulos

1. Crie um novo arquivo em `src/`
2. Implemente a classe/funções
3. Adicione ao `src/__init__.py`
4. Atualize `main.py` com novo subcomando

## 🐳 Docker

### Construir Imagem

```bash
docker build -t bioinformatics-pipeline .
```

### Executar com Volumes

```bash
docker run --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/output:/app/output \
    bioinformatics-pipeline \
    python main.py --help
```

### Modo Interativo

```bash
docker run -it --rm \
    -v $(pwd)/data:/app/data \
    -v $(pwd)/output:/app/output \
    bioinformatics-pipeline \
    /bin/bash
```

## 📦 Dependências

- **pandas**: Manipulação e análise de dados
- **numpy**: Operações numéricas
- **matplotlib**: Criação de gráficos
- **seaborn**: Visualizações estatísticas
- **SPAdes**: Montador de genomas (externo)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👤 Autor

Pietro Belli

## 🔗 Links Úteis

- [SPAdes Documentation](http://cab.spbu.ru/software/spades/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Docker Documentation](https://docs.docker.com/)
