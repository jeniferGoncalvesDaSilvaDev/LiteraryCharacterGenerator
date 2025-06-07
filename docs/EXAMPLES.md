# Exemplos de Uso - Multiverse Character Generator

## Exemplos Básicos

### Geração Simples por Universo

```python
from multiverse_character_generator import MultiverseCharacterGenerator

generator = MultiverseCharacterGenerator()

# Fantasia Medieval
personagem_fantasia = generator.generate_character(
    universe="fantasia",
    details=["Anão", "Clérigo", "Lawful Good", "Montanha Sagrada"]
)

# Ficção Científica
personagem_scifi = generator.generate_character(
    universe="sci-fi",
    details=["Ciborgue", "Mercenário", "Independente", "Colônia Mineira"]
)

# Terror Cósmico
personagem_terror = generator.generate_character(
    universe="terror",
    details=["Arqueólogo", "Megalofobia", "Estatueta Antiga", "Ruínas Submarinas"]
)
```

### Configurações Personalizadas

```python
# Personagem detalhado e criativo
personagem_detalhado = generator.generate_character(
    universe="cyberpunk",
    details=["Próteses Neurais", "Netrunner Solo", "Espionagem Corporativa", "Setor 7"],
    max_length=500,          # Descrição longa
    temperature=0.9,         # Muito criativo
    top_p=0.95,             # Vocabulário diverso
    repetition_penalty=1.3,  # Evitar repetições
    save_to_file=True,
    output_dir="./characters/cyberpunk"
)

# Personagem focado e conciso
personagem_conciso = generator.generate_character(
    universe="anime",
    details=["Samurai Moderno", "Técnica do Vento", "Honra Perdida", "Restaurar Nome"],
    max_length=200,         # Descrição curta
    temperature=0.6,        # Mais focado
    top_p=0.8              # Vocabulário controlado
)
```

## Exemplos Assíncronos

### Geração Concorrente

```python
import asyncio
from multiverse_character_generator import MultiverseCharacterGenerator

async def gerar_grupo_aventureiros():
    generator = MultiverseCharacterGenerator()
    
    # Definir membros do grupo
    membros = [
        ("fantasia", ["Humano", "Paladino", "Lawful Good", "Reino do Sol"]),
        ("fantasia", ["Elfo", "Ranger", "Chaotic Good", "Floresta Ancestral"]),
        ("fantasia", ["Halfling", "Ladino", "Chaotic Neutral", "Cidade dos Ladrões"]),
        ("fantasia", ["Anão", "Guerreiro", "Lawful Neutral", "Fortaleza de Ferro"])
    ]
    
    # Gerar todos concorrentemente
    tasks = [
        generator.generate_character_async(universe, detalhes, max_length=300)
        for universe, detalhes in membros
    ]
    
    grupo = await asyncio.gather(*tasks)
    
    # Salvar grupo completo
    for i, personagem in enumerate(grupo):
        print(f"\n=== MEMBRO {i+1} ===")
        print(personagem.character)
    
    return grupo

# Executar
grupo_aventureiros = asyncio.run(gerar_grupo_aventureiros())
```

### Processamento em Lote com Controle de Taxa

```python
async def processar_lote_personagens(requests, taxa_por_segundo=2):
    generator = MultiverseCharacterGenerator()
    resultados = []
    
    intervalo = 1.0 / taxa_por_segundo
    
    for i, (universe, details) in enumerate(requests):
        print(f"Processando {i+1}/{len(requests)}: {universe}")
        
        try:
            personagem = await generator.generate_character_async(
                universe=universe,
                details=details,
                max_length=250
            )
            resultados.append(personagem)
            
        except Exception as e:
            print(f"Erro em {universe}: {e}")
            resultados.append(None)
        
        # Controle de taxa
        if i < len(requests) - 1:
            await asyncio.sleep(intervalo)
    
    return resultados

# Lote de requisições
lote_requests = [
    ("marvel", ["Radiação Gama", "Vingadores", "Herói", "Laboratório"]),
    ("anime", ["Espadachim", "Corte Dimensional", "Mestre Morto", "Vingança"]),
    ("terror", ["Médico", "Hemofobia", "Bisturi Ritual", "Hospital Abandonado"]),
    ("cyberpunk", ["Olhos Artificiais", "Yakuza Digital", "Assassinato", "Neo-Tóquio"])
]

resultados = asyncio.run(processar_lote_personagens(lote_requests))
```

## Integração com Frameworks Web

### Flask API

```python
from flask import Flask, request, jsonify, render_template
from multiverse_character_generator import MultiverseCharacterGenerator
from multiverse_character_generator.exceptions import MultiverseGeneratorError

app = Flask(__name__)
generator = MultiverseCharacterGenerator(model_name="gpt2")

@app.route('/')
def index():
    universos = generator.list_universes()
    return render_template('generator.html', universos=universos)

@app.route('/api/universes')
def listar_universos():
    return jsonify(generator.list_universes())

@app.route('/api/universe/<universe>/info')
def info_universo(universe):
    try:
        info = generator.get_universe_info(universe)
        return jsonify(info)
    except Exception as e:
        return jsonify({'erro': str(e)}), 404

@app.route('/api/generate', methods=['POST'])
def gerar_personagem():
    dados = request.json
    
    try:
        personagem = generator.generate_character(
            universe=dados['universe'],
            details=dados['details'],
            max_length=dados.get('max_length', 350),
            temperature=dados.get('temperature', 0.85)
        )
        
        return jsonify({
            'sucesso': True,
            'personagem': personagem.character,
            'universo': dados['universe']
        })
        
    except MultiverseGeneratorError as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e),
            'tipo': type(e).__name__
        }), 400

@app.route('/api/quick-generate/<universe>')
def geracao_rapida(universe):
    try:
        personagem = generator.quick_generate(universe)
        return jsonify({
            'sucesso': True,
            'personagem': personagem.character,
            'universo': universe
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Assíncrono

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from multiverse_character_generator import MultiverseCharacterGenerator

app = FastAPI(title="Multiverse Character Generator API")
generator = MultiverseCharacterGenerator()

class RequestPersonagem(BaseModel):
    universe: str
    details: List[str]
    max_length: Optional[int] = 350
    temperature: Optional[float] = 0.85
    save_to_file: Optional[bool] = False

class ResponsePersonagem(BaseModel):
    character: str
    universe: str
    filename: Optional[str] = None

@app.get("/universes")
async def listar_universos():
    return generator.list_universes()

@app.get("/universe/{universe}/info")
async def info_universo(universe: str):
    try:
        return generator.get_universe_info(universe)
    except KeyError:
        raise HTTPException(status_code=404, detail="Universo não encontrado")

@app.post("/generate", response_model=ResponsePersonagem)
async def gerar_personagem(request: RequestPersonagem):
    try:
        personagem = await generator.generate_character_async(
            universe=request.universe,
            details=request.details,
            max_length=request.max_length,
            temperature=request.temperature,
            save_to_file=request.save_to_file
        )
        
        return ResponsePersonagem(
            character=personagem.character,
            universe=request.universe,
            filename=personagem.filename
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/quick-generate/{universe}")
async def geracao_rapida(universe: str):
    try:
        personagem = await generator.quick_generate_async(universe)
        return ResponsePersonagem(
            character=personagem.character,
            universe=universe
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint para geração em lote
@app.post("/batch-generate")
async def geracao_lote(requests: List[RequestPersonagem]):
    tasks = [
        generator.generate_character_async(
            universe=req.universe,
            details=req.details,
            max_length=req.max_length,
            temperature=req.temperature
        )
        for req in requests
    ]
    
    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    personagens = []
    erros = []
    
    for i, resultado in enumerate(resultados):
        if isinstance(resultado, Exception):
            erros.append({
                "index": i,
                "erro": str(resultado),
                "request": requests[i].dict()
            })
        else:
            personagens.append(ResponsePersonagem(
                character=resultado.character,
                universe=requests[i].universe,
                filename=resultado.filename
            ))
    
    return {
        "personagens": personagens,
        "erros": erros,
        "total_sucesso": len(personagens),
        "total_erro": len(erros)
    }
```

## Aplicações Específicas

### Gerador para Jogos de RPG

```python
class GeradorRPG:
    def __init__(self):
        self.generator = MultiverseCharacterGenerator()
        self.templates_nivel = {
            "iniciante": {"max_length": 150, "temperature": 0.7},
            "intermediario": {"max_length": 250, "temperature": 0.8},
            "avancado": {"max_length": 400, "temperature": 0.85},
            "lendario": {"max_length": 600, "temperature": 0.9}
        }
    
    def gerar_npc(self, universo, nivel_importancia="intermediario"):
        """Gera NPC baseado no nível de importância"""
        config = self.templates_nivel[nivel_importancia]
        
        return self.generator.quick_generate(
            universe=universo,
            **config
        )
    
    def gerar_grupo_inimigos(self, universo, quantidade=3):
        """Gera grupo de inimigos para encontro"""
        return [
            self.generator.quick_generate(universo, max_length=200)
            for _ in range(quantidade)
        ]
    
    async def gerar_campanha_completa(self, universo, config_campanha):
        """Gera personagens para campanha inteira"""
        tasks = []
        
        # NPCs principais
        for npc_config in config_campanha.get("npcs_principais", []):
            tasks.append(
                self.generator.generate_character_async(
                    universe=universo,
                    details=npc_config["details"],
                    max_length=400,
                    save_to_file=True,
                    output_dir=f"./campanhas/{universo}/npcs"
                )
            )
        
        # Inimigos
        for inimigo_config in config_campanha.get("inimigos", []):
            tasks.append(
                self.generator.generate_character_async(
                    universe=universo,
                    details=inimigo_config["details"],
                    max_length=250,
                    save_to_file=True,
                    output_dir=f"./campanhas/{universo}/inimigos"
                )
            )
        
        return await asyncio.gather(*tasks)

# Uso do gerador RPG
gerador_rpg = GeradorRPG()

# Configuração de campanha
config_campanha = {
    "npcs_principais": [
        {"details": ["Elfo Ancião", "Arquimago", "Neutro", "Torre dos Ventos"]},
        {"details": ["Anão Ferreiro", "Artesão", "Lawful Good", "Forja Ancestral"]}
    ],
    "inimigos": [
        {"details": ["Orc Chefe", "Bárbaro", "Chaotic Evil", "Cavernas Negras"]},
        {"details": ["Necromante", "Feiticeiro", "Neutral Evil", "Cemitério Antigo"]}
    ]
}

# Gerar campanha
campanha = asyncio.run(
    gerador_rpg.gerar_campanha_completa("fantasia", config_campanha)
)
```

### Ferramenta para Escritores

```python
class AssistenteEscrita:
    def __init__(self):
        self.generator = MultiverseCharacterGenerator()
        self.personagens_historia = []
    
    def criar_protagonista(self, universo, traits_principais):
        """Cria protagonista principal da história"""
        protagonista = self.generator.generate_character(
            universe=universo,
            details=traits_principais,
            temperature=0.8,
            max_length=500
        )
        
        self.personagens_historia.append({
            "tipo": "protagonista",
            "personagem": protagonista,
            "universo": universo
        })
        
        return protagonista
    
    def criar_antagonista(self, universo, caracteristicas):
        """Cria antagonista principal"""
        antagonista = self.generator.generate_character(
            universe=universo,
            details=caracteristicas,
            temperature=0.85,
            max_length=450
        )
        
        self.personagens_historia.append({
            "tipo": "antagonista", 
            "personagem": antagonista,
            "universo": universo
        })
        
        return antagonista
    
    def criar_personagens_secundarios(self, universo, quantidade=3):
        """Cria múltiplos personagens secundários"""
        secundarios = []
        
        for i in range(quantidade):
            personagem = self.generator.quick_generate(
                universe=universo,
                max_length=200,
                temperature=0.9  # Mais diversidade
            )
            
            secundarios.append(personagem)
            self.personagens_historia.append({
                "tipo": "secundario",
                "personagem": personagem,
                "universo": universo
            })
        
        return secundarios
    
    def gerar_desenvolvimento_personagem(self, personagem_base, nova_situacao):
        """Desenvolve personagem existente para nova situação"""
        # Extrair características do personagem base
        prompt_desenvolvimento = f"""
        Baseado neste personagem: {personagem_base.character[:200]}...
        
        Desenvolva como ele reagiria e evoluiria na seguinte situação: {nova_situacao}
        """
        
        # Usar geração customizada
        return self.generator._generate_text(
            prompt=prompt_desenvolvimento,
            max_length=300,
            temperature=0.75,
            top_p=0.9,
            repetition_penalty=1.2
        )
    
    def exportar_biblia_personagens(self, arquivo_saida):
        """Exporta todos os personagens para arquivo"""
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("# Bíblia de Personagens\n\n")
            
            for categoria in ["protagonista", "antagonista", "secundario"]:
                personagens_categoria = [
                    p for p in self.personagens_historia 
                    if p["tipo"] == categoria
                ]
                
                if personagens_categoria:
                    f.write(f"## {categoria.title()}s\n\n")
                    
                    for i, entrada in enumerate(personagens_categoria):
                        f.write(f"### {categoria.title()} {i+1}\n")
                        f.write(f"**Universo:** {entrada['universo']}\n\n")
                        f.write(f"{entrada['personagem'].character}\n\n")
                        f.write("---\n\n")

# Uso para escrita criativa
assistente = AssistenteEscrita()

# Criar personagens principais
protagonista = assistente.criar_protagonista(
    "cyberpunk",
    ["Hacker Renegado", "Interface Neural Ilegal", "Corporação Traiu", "Derrubar Sistema"]
)

antagonista = assistente.criar_antagonista(
    "cyberpunk", 
    ["CEO Megacorp", "Controle Mental Tecnológico", "Dominação Global", "Torre Corporativa"]
)

# Personagens secundários
secundarios = assistente.criar_personagens_secundarios("cyberpunk", 3)

# Exportar bíblia
assistente.exportar_biblia_personagens("biblia_personagens_cyberpunk.md")
```

### Sistema de Moderação e Filtros

```python
class GeradorModerado:
    def __init__(self):
        self.generator = MultiverseCharacterGenerator()
        self.filtros_conteudo = [
            "violência extrema", "conteúdo adulto", "linguagem ofensiva"
        ]
    
    def gerar_personagem_familiar(self, universo, detalhes):
        """Gera personagem adequado para público geral"""
        personagem = self.generator.generate_character(
            universe=universo,
            details=detalhes,
            temperature=0.7,  # Menos criativo = mais seguro
            max_length=300
        )
        
        # Verificar conteúdo
        if self._verificar_conteudo_adequado(personagem.character):
            return personagem
        else:
            # Tentar novamente com parâmetros mais conservadores
            return self.generator.generate_character(
                universe=universo,
                details=detalhes,
                temperature=0.5,
                max_length=250
            )
    
    def _verificar_conteudo_adequado(self, texto):
        """Verifica se o conteúdo é adequado"""
        texto_lower = texto.lower()
        
        palavras_problematicas = [
            "violento", "sangue", "matar", "morte", "arma"
        ]
        
        for palavra in palavras_problematicas:
            if palavra in texto_lower:
                return False
        
        return True
    
    async def gerar_lote_educacional(self, requests_educacionais):
        """Gera lote de personagens para uso educacional"""
        personagens_aprovados = []
        
        for req in requests_educacionais:
            tentativas = 0
            max_tentativas = 3
            
            while tentativas < max_tentativas:
                personagem = await self.generator.generate_character_async(
                    universe=req["universe"],
                    details=req["details"],
                    temperature=0.6 - (tentativas * 0.1),  # Mais conservador a cada tentativa
                    max_length=250
                )
                
                if self._verificar_conteudo_adequado(personagem.character):
                    personagens_aprovados.append(personagem)
                    break
                
                tentativas += 1
            
            if tentativas == max_tentativas:
                print(f"Não foi possível gerar personagem adequado para {req}")
        
        return personagens_aprovados

# Uso educacional
gerador_moderado = GeradorModerado()

requests_escola = [
    {"universe": "fantasia", "details": ["Elfo Jovem", "Estudante Magia", "Curioso", "Academia Arcana"]},
    {"universe": "sci-fi", "details": ["Robô Amigável", "Professor", "Pacífico", "Escola Espacial"]},
    {"universe": "anime", "details": ["Estudante", "Poderes Curativos", "Ajudar Outros", "Escola Especial"]}
]

personagens_educacionais = asyncio.run(
    gerador_moderado.gerar_lote_educacional(requests_escola)
)
```

## Otimização e Performance

### Cache de Resultados

```python
import json
import hashlib
from pathlib import Path

class GeradorComCache:
    def __init__(self, cache_dir="./cache"):
        self.generator = MultiverseCharacterGenerator()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _gerar_hash_requisicao(self, universe, details, config):
        """Gera hash único para requisição"""
        requisicao = {
            "universe": universe,
            "details": sorted(details),  # Ordenar para consistência
            "config": config
        }
        
        requisicao_str = json.dumps(requisicao, sort_keys=True)
        return hashlib.md5(requisicao_str.encode()).hexdigest()
    
    def generate_character_cached(self, universe, details, **config):
        """Gera personagem com cache"""
        hash_req = self._gerar_hash_requisicao(universe, details, config)
        cache_file = self.cache_dir / f"{hash_req}.json"
        
        # Verificar cache
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
                print(f"Cache hit para {universe}")
                return cached_data
        
        # Gerar novo
        personagem = self.generator.generate_character(
            universe=universe,
            details=details,
            **config
        )
        
        # Salvar no cache
        cache_data = {
            "character": personagem.character,
            "universe": universe,
            "details": details,
            "config": config
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print(f"Cache miss para {universe} - resultado salvo")
        return cache_data

# Uso com cache
gerador_cache = GeradorComCache()

# Primeira chamada - gera e salva no cache
resultado1 = gerador_cache.generate_character_cached(
    "fantasia", 
    ["Elfo", "Mago", "Neutro", "Torre"],
    max_length=300
)

# Segunda chamada - usa cache
resultado2 = gerador_cache.generate_character_cached(
    "fantasia",
    ["Elfo", "Mago", "Neutro", "Torre"], 
    max_length=300
)
```

### Geração com Pool de Workers

```python
import concurrent.futures
from multiprocessing import Pool
import functools

def gerar_personagem_worker(args):
    """Worker function para multiprocessing"""
    universe, details, config = args
    generator = MultiverseCharacterGenerator(model_name="gpt2")  # Modelo menor para workers
    
    return generator.generate_character(
        universe=universe,
        details=details,
        **config
    )

class GeradorParalelo:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
    
    def gerar_lote_paralelo(self, requests, config_padrao=None):
        """Gera lote de personagens em paralelo"""
        if config_padrao is None:
            config_padrao = {"max_length": 250, "temperature": 0.8}
        
        # Preparar argumentos para workers
        worker_args = [
            (req["universe"], req["details"], {**config_padrao, **req.get("config", {})})
            for req in requests
        ]
        
        # Executar em paralelo
        with Pool(processes=self.max_workers) as pool:
            resultados = pool.map(gerar_personagem_worker, worker_args)
        
        return resultados

# Uso paralelo
gerador_paralelo = GeradorParalelo(max_workers=2)

requests_paralelo = [
    {"universe": "fantasia", "details": ["Orc", "Xamã", "Neutro", "Pântano"]},
    {"universe": "sci-fi", "details": ["Alien", "Cientista", "Pesquisador", "Laboratório"]},
    {"universe": "terror", "details": ["Detetive", "Aracnofobia", "Lupa Amaldiçoada", "Mansão"]},
    {"universe": "cyberpunk", "details": ["Soldado", "Implantes Militares", "Desertor", "Zona de Guerra"]}
]

resultados_paralelos = gerador_paralelo.gerar_lote_paralelo(requests_paralelo)
```