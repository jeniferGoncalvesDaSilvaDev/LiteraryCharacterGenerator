# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2024-12-07

### Adicionado
- Implementação inicial da biblioteca Multiverse Character Generator
- Suporte para 6 universos ficcionais: fantasia, sci-fi, terror, cyberpunk, anime, marvel
- Classe principal `MultiverseCharacterGenerator` com métodos síncronos e assíncronos
- Sistema de validação de dados com Pydantic
- Tratamento abrangente de erros com exceções customizadas
- Utilitários para manipulação de arquivos e limpeza de texto
- Configurações otimizadas por universo
- Suporte a GPU com detecção automática
- Sistema de cache para modelos
- Exemplos básicos, assíncronos e com parâmetros customizados
- Suite completa de testes com pytest
- Documentação abrangente incluindo README, guias e referência da API
- Configuração profissional com setup.py

### Características Técnicas
- Integração com modelos GPT-2 via Transformers
- Lazy loading de dependências para melhor performance
- Prompts inteligentes específicos por universo
- Parâmetros configuráveis (temperature, top_p, repetition_penalty)
- Salvamento automático de personagens em arquivos
- Validação de entrada e saída
- Suporte a processamento em lote

### Universos Suportados
- **Fantasia**: Raça, Classe, Alinhamento, Reino de Origem
- **Ficção Científica**: Espécie, Profissão, Afiliação, Planeta Natal  
- **Terror**: Ocupação, Fobia, Relíquia Amaldiçoada, Local Assombrado
- **Cyberpunk**: Implantes Cibernéticos, Afiliação Corporativa/Gangue, Especialização Criminal, Distrito Urbano
- **Anime**: Tipo de Personagem, Habilidade Única, Backstory, Objetivo
- **Marvel**: Origem do Poder, Afiliação, Arquétipo, Localização

### Documentação
- README completo com exemplos e instruções
- Guia de início rápido
- Referência completa da API
- Exemplos avançados de uso e integração
- Documentação de arquitetura e casos de uso

### Dependências
- torch>=1.9.0
- transformers>=4.20.0
- pydantic>=1.8.0
- nltk>=3.6
- numpy>=1.21.0
- tokenizers>=0.12.0