# Job Finder Junior - Java Backend

![CI](https://github.com/Ivictors/openx-job-finder/workflows/CI/badge.svg)

Automatizador de busca de vagas para desenvolvedores Java Backend Junior com foco em vagas remotas ou presenciais em Sao Paulo.

## Funcionalidades

- Busca automatica em multiplos sites de emprego
- Filtra vagas por nivel (Junior, Estagiario, Trainee, Pleno)
- Filtra por tecnologia (Java, Spring Boot, Backend)
- Filtra por localizacao (Remoto ou Sao Paulo - Capital)
- Filtra por periodo (ultimas 2 semanas)
- Remove duplicatas automaticamente
- Salva resultado em JSON

## Sites Pesquisados

- LinkedIn
- ProgramaThor
- Workana
- GeekHunter

## Tecnologias Utilizadas

- **Python 3.14+** - Linguagem principal
- **Playwright** - Automacao de navegador para web scraping
- **asyncio** - Operacoes assincronas
- **JSON** - Formato de saida dos dados

## Pre-requisitos

```bash
# Python 3.14 ou superior
python --version

# Instalar dependencias
pip install playwright

# Instalar navegador para Playwright
python -m playwright install chromium
```

## Como Usar

### Executar busca

```bash
python busca_vagas_junior.py
```

### Resultado

O script gera um arquivo JSON em `output/vagas_junior_java.json`:

```json
{
  "search_metadata": {
    "search_date": "2026-04-10 17:00:00",
    "filter_date_from": "2026-03-27",
    "location_filter": "Remoto ou Sao Paulo (Capital)",
    "total_jobs": 5,
    "recent_jobs": 3
  },
  "jobs": [
    {
      "title": "Junior Java Developer",
      "company": "Empresa XYZ",
      "location": "Sao Paulo, SP",
      "link": "https://...",
      "source": "LinkedIn",
      "posted_date": "2026-04-08"
    }
  ]
}
```

## Filtros Aplicados

### Nivel
- Junior
- Estagiario
- Trainee
- Pleno (aceitavel)
- Entry Level
- Intern

### Tecnologias
- Java
- Spring Boot
- Backend / Back-end
- Software Developer
- Programador
- Desenvolvedor

### Exclusoes
- Senior / Sênior
- Lead / Tech Lead
- Arquiteto
- Gerente / Manager
- Frontend
- Mobile
- PHP
- Node.js
- React / Angular / Vue

### Localizacao
- Remoto
- Sao Paulo (Capital)
- Brasil (aceitavel)

### Periodo
- Ultimas 2 semanas

## Estrutura do Projeto

```
openx-job-finder/
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # Pipeline de CI
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md       # Template de bug
│   │   └── feature_request.md  # Template de feature
│   └── pull_request_template.md # Template de PR
├── .gitignore
├── busca_vagas_junior.py       # Script principal
├── README.md                   # Documentacao
└── output/                     # Resultados (gerado automaticamente)
    └── vagas_junior_java.json
```

## Personalizacao

### Adicionar novos termos de busca

Edite a lista `SEARCH_TERMS` no arquivo `busca_vagas_junior.py`:

```python
SEARCH_TERMS = [
    "Java Junior",
    "Java Estagiario",
    "Backend Junior",
    "Spring Boot",
    # Adicione novos termos aqui
]
```

### Ajustar periodo de busca

Modifique a funcao `is_within_two_weeks()`:

```python
def is_within_two_weeks(date_str):
    # Altere 14 para o numero de dias desejado
    two_weeks_ago = datetime.now() - timedelta(days=14)
    ...
```

### Adicionar novo site de vagas

Crie uma nova funcao de scraping seguindo o padrao:

```python
def scrape_novo_site(page):
    jobs = []
    # Implementar logica de scraping
    return jobs
```

## Limitacoes

- Alguns sites podem bloquear requisicoes automatizadas
- O scraping depende da estrutura HTML dos sites (pode quebrar se mudarem)
- LinkedIn limita resultados sem login

## Contribuindo

Contribuicoes sao bem-vindas! Siga os passos:

1. Faca um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudancas usando conventional commits:
   - `feat:` para novas funcionalidades
   - `fix:` para correcoes de bugs
   - `docs:` para documentacao
   - `refactor:` para refatoracoes
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Templates Disponiveis

- **Bug Report**: Use o template em `.github/ISSUE_TEMPLATE/bug_report.md`
- **Feature Request**: Use o template em `.github/ISSUE_TEMPLATE/feature_request.md`
- **Pull Request**: Siga o template em `.github/pull_request_template.md`

### CI/CD

O projeto utiliza GitHub Actions para validacao continua:

- **Lint**: Verificacao de sintaxe com flake8
- **Syntax Check**: Validacao de codigo Python
- **Pylint**: Analise estatica (informativo)

O CI roda automaticamente em cada push para `main` e em Pull Requests.

## Autor

Victor Marques de Oliveira

- GitHub: [Ivictors](https://github.com/Ivictors)
- LinkedIn: [vi-marques](https://linkedin.com/in/vi-marques)
