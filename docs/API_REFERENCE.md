# API Reference - Multiverse Character Generator

## Visão Geral

A biblioteca Multiverse Character Generator fornece uma API simples e poderosa para gerar personagens ficcionais usando modelos GPT-2. Esta referência documenta todas as classes, métodos e funções disponíveis.

## Módulos Principais

### `multiverse_character_generator.generator`

#### Classe `MultiverseCharacterGenerator`

Classe principal para geração de personagens ficcionais.

```python
class MultiverseCharacterGenerator:
    def __init__(
        self,
        model_name: str = "gpt2-medium",
        use_gpu: Optional[bool] = None,
        cache_dir: Optional[str] = None
    )
```

**Parâmetros:**
- `model_name`: Nome do modelo GPT-2 ("gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl")
- `use_gpu`: Usar GPU se disponível (None para auto-detecção)
- `cache_dir`: Diretório para cache de modelos

**Métodos:**

##### `generate_character()`

```python
def generate_character(
    self,
    universe: str,
    details: List[str],
    max_length: int = 350,
    temperature: float = 0.85,
    top_p: float = 0.92,
    repetition_penalty: float = 1.2,
    save_to_file: bool = False,
    output_dir: Optional[str] = None
) -> GeneratedCharacter
```

Gera um personagem com detalhes customizados.

**Parâmetros:**
- `universe`: Universo fictício
- `details`: Lista de detalhes do personagem
- `max_length`: Comprimento máximo (50-1000)
- `temperature`: Criatividade (0.0-1.0)
- `top_p`: Amostragem nucleus (0.0-1.0)
- `repetition_penalty`: Penalidade repetição (1.0-2.0)
- `save_to_file`: Salvar em arquivo
- `output_dir`: Diretório de saída

**Retorna:** `GeneratedCharacter`

**Exceções:**
- `InvalidUniverseError`: Universo não suportado
- `InvalidDetailsError`: Detalhes inválidos
- `GenerationError`: Falha na geração

### Universos Disponíveis

#### Fantasia ("fantasia")
**Campos:** Raça, Classe, Alinhamento, Reino de Origem

#### Ficção Científica ("sci-fi")
**Campos:** Espécie, Profissão, Afiliação, Planeta Natal

#### Terror ("terror")
**Campos:** Ocupação, Fobia, Relíquia Amaldiçoada, Local Assombrado

#### Cyberpunk ("cyberpunk")
**Campos:** Implantes Cibernéticos, Afiliação Corporativa/Gangue, Especialização Criminal, Distrito Urbano

#### Anime ("anime")
**Campos:** Tipo de Personagem, Habilidade Única, Backstory, Objetivo

#### Marvel ("marvel")
**Campos:** Origem do Poder, Afiliação, Arquétipo, Localização