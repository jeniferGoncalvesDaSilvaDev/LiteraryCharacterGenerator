# Documentação - Multiverse Character Generator

## Índice da Documentação

### Documentos Principais

1. **[Guia de Início Rápido](QUICK_START.md)** - Como começar a usar a biblioteca
2. **[Referência da API](API_REFERENCE.md)** - Documentação completa de todas as classes e métodos
3. **[Exemplos de Uso](EXAMPLES.md)** - Exemplos práticos e casos de uso avançados

### Documentação do Projeto

- **[README Principal](../README.md)** - Visão geral completa da biblioteca
- **[Arquivo de Setup](../setup.py)** - Configuração de instalação e dependências

## Estrutura da Biblioteca

```
multiverse_character_generator/
├── __init__.py          # Ponto de entrada principal
├── generator.py         # Classe principal de geração
├── models.py           # Modelos Pydantic para validação
├── universes.py        # Configurações dos universos
├── exceptions.py       # Exceções customizadas
└── utils.py            # Funções utilitárias

examples/
├── basic_usage.py      # Exemplos básicos
├── async_usage.py      # Uso assíncrono
└── custom_parameters.py # Parâmetros customizados

tests/
├── test_generator.py   # Testes do gerador
└── test_universes.py   # Testes dos universos

docs/
├── README.md           # Este arquivo
├── QUICK_START.md      # Início rápido
├── API_REFERENCE.md    # Referência da API
└── EXAMPLES.md         # Exemplos avançados
```

## Fluxo de Aprendizado Recomendado

### Para Iniciantes

1. Leia o [README principal](../README.md) para entender o conceito
2. Siga o [Guia de Início Rápido](QUICK_START.md) para primeiros passos
3. Execute os exemplos em `examples/basic_usage.py`
4. Explore diferentes universos com `examples/custom_parameters.py`

### Para Desenvolvedores

1. Revise a [Referência da API](API_REFERENCE.md) para entender todas as funcionalidades
2. Estude os [Exemplos Avançados](EXAMPLES.md) para casos de uso complexos
3. Execute os testes: `pytest tests/`
4. Explore o código fonte para customizações

### Para Integração

1. Veja exemplos de integração com frameworks web em [EXAMPLES.md](EXAMPLES.md)
2. Estude padrões de tratamento de erro na [Referência da API](API_REFERENCE.md)
3. Implemente cache e otimizações conforme necessário

## Recursos Principais

### Universos Suportados

| Universo | Descrição | Campos Obrigatórios |
|----------|-----------|-------------------|
| **fantasia** | Fantasia medieval clássica | Raça, Classe, Alinhamento, Origem |
| **sci-fi** | Ficção científica | Espécie, Profissão, Afiliação, Planeta |
| **terror** | Horror cósmico | Ocupação, Fobia, Relíquia, Local |
| **cyberpunk** | Futuro distópico tecnológico | Implantes, Afiliação, Especialização, Distrito |
| **anime** | Estilo anime/mangá | Tipo, Habilidade, História, Objetivo |
| **marvel** | Universo Marvel | Origem Poder, Afiliação, Arquétipo, Local |

### Características Técnicas

- **Modelos GPT-2**: Suporte para gpt2, gpt2-medium, gpt2-large, gpt2-xl
- **Geração Assíncrona**: Processamento concorrente para múltiplos personagens
- **Validação de Dados**: Modelos Pydantic para entrada e saída
- **Tratamento de Erros**: Exceções específicas para diferentes falhas
- **Cache de Modelos**: Otimização de carregamento
- **Suporte a GPU**: Detecção automática e uso quando disponível

## Casos de Uso Comuns

### Jogos e RPG
- Geração de NPCs para jogos
- Criação de grupos de aventureiros
- Desenvolvimento de campanhas

### Escrita Criativa
- Desenvolvimento de personagens para histórias
- Criação de antagonistas e protagonistas
- Geração de personagens secundários

### Aplicações Web
- APIs de geração de personagens
- Ferramentas interativas
- Sistemas de moderação de conteúdo

### Educação
- Ensino de narrativa
- Exercícios de criação literária
- Ferramentas pedagógicas

## Suporte e Contribuição

### Obtendo Ajuda

1. Consulte esta documentação primeiro
2. Verifique os exemplos em `examples/`
3. Execute os testes para validar instalação
4. Abra issues no GitHub para bugs

### Contribuindo

1. Fork o repositório
2. Crie branch para sua feature
3. Implemente testes para novas funcionalidades
4. Envie pull request com descrição detalhada

### Reportando Problemas

Inclua sempre:
- Versão da biblioteca
- Versão do Python
- Sistema operacional
- Código que reproduz o problema
- Mensagem de erro completa

## Licença e Créditos

Este projeto é licenciado sob a Licença MIT. Veja o arquivo LICENSE para detalhes.

### Dependências Principais

- **PyTorch**: Framework de machine learning
- **Transformers**: Biblioteca da Hugging Face para modelos de linguagem
- **Pydantic**: Validação de dados e settings
- **NLTK**: Processamento de linguagem natural

### Agradecimentos

- Comunidade Hugging Face pelos modelos GPT-2
- OpenAI pela pesquisa original do GPT-2
- Contribuidores da biblioteca Transformers