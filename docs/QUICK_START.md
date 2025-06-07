# Guia de Início Rápido - Multiverse Character Generator

## Instalação

```bash
# Instalar dependências necessárias
pip install torch transformers pydantic nltk numpy tokenizers

# Opcional: Para desenvolvimento
pip install pytest pytest-asyncio
```

## Primeiro Uso

### 1. Importar e Inicializar

```python
from multiverse_character_generator import MultiverseCharacterGenerator

# Inicializar o gerador
generator = MultiverseCharacterGenerator()
```

### 2. Gerar Personagem Básico

```python
# Gerar um personagem de fantasia
character = generator.generate_character(
    universe="fantasia",
    details=["Elfo", "Mago", "Neutro", "Torre Arcana"]
)

print(character.character)
```

### 3. Geração Rápida

```python
# Usar exemplos pré-definidos
character = generator.quick_generate("cyberpunk")
print(character.character)
```

### 4. Salvar em Arquivo

```python
# Gerar e salvar automaticamente
character = generator.generate_character(
    universe="sci-fi",
    details=["Androide", "Piloto", "Rebeldes", "Estação Orbital"],
    save_to_file=True,
    output_dir="./personagens"
)

print(f"Salvo em: {character.filename}")
```

## Universos Disponíveis

| Universo | Campos Obrigatórios |
|----------|-------------------|
| fantasia | Raça, Classe, Alinhamento, Origem |
| sci-fi | Espécie, Profissão, Afiliação, Planeta |
| terror | Ocupação, Fobia, Relíquia, Local |
| cyberpunk | Implantes, Afiliação, Especialização, Distrito |
| anime | Tipo, Habilidade, História, Objetivo |
| marvel | Origem Poder, Afiliação, Arquétipo, Local |

## Exemplos por Universo

### Fantasia
```python
character = generator.generate_character(
    "fantasia",
    ["Halfling", "Ladino", "Chaotic Neutral", "Cidade Portuária"]
)
```

### Ficção Científica
```python
character = generator.generate_character(
    "sci-fi", 
    ["Humano Modificado", "Engenheiro", "Federação", "Nave Colonial"]
)
```

### Terror
```python
character = generator.generate_character(
    "terror",
    ["Professor", "Agorafobia", "Livro Maldito", "Universidade Antiga"]
)
```

### Cyberpunk
```python
character = generator.generate_character(
    "cyberpunk",
    ["Interface Neural", "Hacker Freelance", "Roubo de Dados", "Submundo Digital"]
)
```

### Anime
```python
character = generator.generate_character(
    "anime",
    ["Estudante Ninja", "Controle Elemental", "Clã Destruído", "Vingança"]
)
```

### Marvel
```python
character = generator.generate_character(
    "marvel",
    ["Mutação Genética", "X-Men", "Herói Reluctante", "Nova Iorque"]
)
```

## Geração Assíncrona

```python
import asyncio

async def gerar_multiplos():
    tasks = [
        generator.generate_character_async("fantasia", ["Orc", "Guerreiro", "Evil", "Cavernas"]),
        generator.generate_character_async("sci-fi", ["Alien", "Comerciante", "Neutro", "Estação"]),
        generator.quick_generate_async("anime")
    ]
    
    personagens = await asyncio.gather(*tasks)
    return personagens

# Executar
personagens = asyncio.run(gerar_multiplos())
```

## Configurações Personalizadas

### Controlar Criatividade
```python
# Mais conservador
character = generator.generate_character(
    "fantasia", ["Elfo", "Ranger", "Good", "Floresta"],
    temperature=0.3  # Menos criativo
)

# Mais criativo
character = generator.generate_character(
    "fantasia", ["Elfo", "Ranger", "Good", "Floresta"], 
    temperature=0.9  # Mais criativo
)
```

### Controlar Tamanho
```python
# Descrição curta
character = generator.generate_character(
    "cyberpunk", ["Implante Ótico", "Corpo", "Infiltração", "Megacidade"],
    max_length=150
)

# Descrição detalhada
character = generator.generate_character(
    "cyberpunk", ["Implante Ótico", "Corpo", "Infiltração", "Megacidade"],
    max_length=500
)
```

## Tratamento de Erros

```python
from multiverse_character_generator.exceptions import InvalidUniverseError, InvalidDetailsError

try:
    character = generator.generate_character("universo_inexistente", ["detalhe"])
except InvalidUniverseError:
    print("Universo não encontrado!")
    print("Disponíveis:", generator.list_universes())
except InvalidDetailsError as e:
    print(f"Erro nos detalhes: {e}")
```

## Utilitários

### Listar Universos
```python
universos = generator.list_universes()
print("Universos disponíveis:", universos)
```

### Informações do Universo
```python
info = generator.get_universe_info("fantasia")
print("Campos obrigatórios:", info["inputs"])
print("Exemplos:", info["exemplos"])
```

### Informações do Modelo
```python
model_info = generator.get_model_info()
print(f"Modelo: {model_info['model_name']}")
print(f"GPU: {model_info['using_gpu']}")
```

## Próximos Passos

- Explore os exemplos em `examples/`
- Leia a documentação completa no `README.md`
- Veja a referência da API em `docs/API_REFERENCE.md`
- Execute os testes com `pytest`