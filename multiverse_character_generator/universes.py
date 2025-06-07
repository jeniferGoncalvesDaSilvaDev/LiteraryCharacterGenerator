"""
Universe definitions and prompt templates for character generation.
"""

from typing import Dict, List


def get_universes() -> Dict[str, Dict[str, List[str]]]:
    """
    Get all available universe configurations.
    
    Returns:
        Dictionary mapping universe names to their configuration
        (inputs and examples)
    """
    return {
        "fantasia": {
            "inputs": ["Raça", "Classe", "Alinhamento", "Reino de Origem"],
            "exemplos": ["Elfo", "Mago", "Neutro", "Floresta das Brumas"]
        },
        "sci-fi": {
            "inputs": ["Espécie", "Profissão", "Afiliação", "Planeta Natal"],
            "exemplos": ["Ciborgue", "Piloto de Nave", "Aliança Galáctica", "Proxima Centauri"]
        },
        "terror": {
            "inputs": ["Ocupação", "Fobia", "Relíquia Amaldiçoada", "Local Assombrado"],
            "exemplos": ["Jornalista", "Medo de Aranhas", "Diário Antigo", "Asilo Abandonado"]
        },
        "cyberpunk": {
            "inputs": ["Implantes Cibernéticos", "Afiliação Corporativa/Gangue",
                      "Especialização Criminal", "Distrito Urbano"],
            "exemplos": ["Braço Biônico MK-5", "Night City Mercenaries",
                        "Hacker de ICE", "Zona do Mercado Negro"]
        },
        "anime": {
            "inputs": ["Tipo de Personagem", "Habilidade Única", "Backstory", "Objetivo"],
            "exemplos": ["Shonen Protagonista", "Rasengan", "Órfão de Guerra", "Tornar-se Hokage"]
        },
        "marvel": {
            "inputs": ["Origem do Poder", "Afiliação", "Arquétipo", "Localização"],
            "exemplos": ["Radiação Cósmica", "Vingadores", "Anti-Herói", "Nova York"]
        }
    }


def get_universe_info(universe: str) -> Dict[str, List[str]]:
    """
    Get information about a specific universe.
    
    Args:
        universe: Name of the universe
        
    Returns:
        Dictionary with inputs and examples for the universe
        
    Raises:
        KeyError: If universe is not found
    """
    universes = get_universes()
    if universe not in universes:
        available = ", ".join(universes.keys())
        raise KeyError(f"Universe '{universe}' not found. Available: {available}")
    
    return universes[universe]


def create_prompt(universe: str, details: List[str]) -> str:
    """
    Create a detailed prompt for character generation based on universe and details.
    
    Args:
        universe: The fictional universe
        details: List of character details
        
    Returns:
        Formatted prompt string for text generation
        
    Raises:
        KeyError: If universe is not supported
        ValueError: If details list length doesn't match expected inputs
    """
    universes = get_universes()
    
    if universe not in universes:
        available = ", ".join(universes.keys())
        raise KeyError(f"Universe '{universe}' not supported. Available: {available}")
    
    expected_count = len(universes[universe]["inputs"])
    if len(details) != expected_count:
        raise ValueError(
            f"Expected {expected_count} details for universe '{universe}', "
            f"got {len(details)}"
        )
    
    templates = {
        "fantasia": (
            "Crie um personagem de fantasia detalhado com:\n"
            "- Raça: {0}\n- Classe: {1}\n- Alinhamento: {2}\n- Origem: {3}\n"
            "Inclua habilidades mágicas, equipamento e um segredo obscuro."
        ),
        "sci-fi": (
            "Desenvolva um personagem de ficção científica com:\n"
            "- Espécie: {0}\n- Profissão: {1}\n- Afiliação: {2}\n- Planeta: {3}\n"
            "Descreva tecnologia avançada, conflitos interestelares e motivações."
        ),
        "terror": (
            "Elabore um personagem de horror cósmico com:\n"
            "- Ocupação: {0}\n- Fobia: {1}\n- Relíquia: {2}\n- Local: {3}\n"
            "Inclua sintomas de insanidade, conexões com entidades e aparência deteriorada."
        ),
        "cyberpunk": (
            "Construa um personagem cyberpunk noir com:\n"
            "- Implantes: {0}\n- Afiliação: {1}\n- Especialização: {2}\n- Distrito: {3}\n"
            "Descreva:\n"
            "1. Modificações cibernéticas visíveis\n"
            "2. Um traço de personalidade distópico\n"
            "3. Um vício ou dependência tecnológica\n"
            "4. Conflito com megacorporações\n"
            "Use gírias cyberpunk como 'choomba', 'corpo' e 'netrunner'."
        ),
        "anime": (
            "Crie um personagem de anime detalhado com:\n"
            "1. Tipo: {0}\n2. Habilidade: {1}\n3. História: {2}\n4. Objetivo: {3}\n\n"
            "Inclua:\n"
            "- Um poder secreto ou transformação\n"
            "- Um lema característico\n"
            "- Design visual icônico (cabelo, roupas)\n"
            "- Uma fraqueza emocional\n\n"
            "Estilo: Use termos como 'nakama', 'power-up' e exclamações dramáticas!"
        ),
        "marvel": (
            "Desenvolva um personagem do universo Marvel com:\n"
            "1. Origem: {0}\n2. Afiliação: {1}\n3. Arquétipo: {2}\n4. Base: {3}\n\n"
            "Detalhe:\n"
            "- Uniforme/cosmético distintivo\n"
            "- Um conflito moral recorrente\n"
            "- Relacionamento icônico com outro herói/vilão\n"
            "- Frase de efeito característica\n\n"
            "Estilo: Misture ação grandiosa com dilemas humanos, no estilo MCU."
        )
    }
    
    template = templates.get(universe, templates["fantasia"])
    return template.format(*details)


def get_universe_templates() -> Dict[str, str]:
    """
    Get all universe prompt templates.
    
    Returns:
        Dictionary mapping universe names to their prompt templates
    """
    return {
        "fantasia": (
            "Crie um personagem de fantasia detalhado com:\n"
            "- Raça: {0}\n- Classe: {1}\n- Alinhamento: {2}\n- Origem: {3}\n"
            "Inclua habilidades mágicas, equipamento e um segredo obscuro."
        ),
        "sci-fi": (
            "Desenvolva um personagem de ficção científica com:\n"
            "- Espécie: {0}\n- Profissão: {1}\n- Afiliação: {2}\n- Planeta: {3}\n"
            "Descreva tecnologia avançada, conflitos interestelares e motivações."
        ),
        "terror": (
            "Elabore um personagem de horror cósmico com:\n"
            "- Ocupação: {0}\n- Fobia: {1}\n- Relíquia: {2}\n- Local: {3}\n"
            "Inclua sintomas de insanidade, conexões com entidades e aparência deteriorada."
        ),
        "cyberpunk": (
            "Construa um personagem cyberpunk noir com:\n"
            "- Implantes: {0}\n- Afiliação: {1}\n- Especialização: {2}\n- Distrito: {3}\n"
            "Descreva:\n"
            "1. Modificações cibernéticas visíveis\n"
            "2. Um traço de personalidade distópico\n"
            "3. Um vício ou dependência tecnológica\n"
            "4. Conflito com megacorporações\n"
            "Use gírias cyberpunk como 'choomba', 'corpo' e 'netrunner'."
        ),
        "anime": (
            "Crie um personagem de anime detalhado com:\n"
            "1. Tipo: {0}\n2. Habilidade: {1}\n3. História: {2}\n4. Objetivo: {3}\n\n"
            "Inclua:\n"
            "- Um poder secreto ou transformação\n"
            "- Um lema característico\n"
            "- Design visual icônico (cabelo, roupas)\n"
            "- Uma fraqueza emocional\n\n"
            "Estilo: Use termos como 'nakama', 'power-up' e exclamações dramáticas!"
        ),
        "marvel": (
            "Desenvolva um personagem do universo Marvel com:\n"
            "1. Origem: {0}\n2. Afiliação: {1}\n3. Arquétipo: {2}\n4. Base: {3}\n\n"
            "Detalhe:\n"
            "- Uniforme/cosmético distintivo\n"
            "- Um conflito moral recorrente\n"
            "- Relacionamento icônico com outro herói/vilão\n"
            "- Frase de efeito característica\n\n"
            "Estilo: Misture ação grandiosa com dilemas humanos, no estilo MCU."
        )
    }
