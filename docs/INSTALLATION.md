# Installation

Trois méthodes. La première est la plus simple.

---

## Méthode 1 — Plugin Claude Code

```
/plugin marketplace add NathanFenina/claude-seo
/plugin install claude-code-seo-decupler@decupler
```

Skills, agents, commandes et déclarations MCP sont branchés en une fois.
Redémarrez Claude Code, puis :

```
/seo doctor
```

---

## Méthode 2 — Script d'installation

**macOS / Linux**
```bash
curl -fsSL https://raw.githubusercontent.com/NathanFenina/claude-seo/main/install.sh | bash
```

**Windows (PowerShell)**
```powershell
irm https://raw.githubusercontent.com/NathanFenina/claude-seo/main/install.ps1 | iex
```

Le script installe les skills dans `~/.claude/skills/`, les agents dans
`~/.claude/agents/`, les commandes dans `~/.claude/commands/`, et les
dépendances Python dans un environnement virtuel dédié.

---

## Méthode 3 — Manuelle

```bash
git clone https://github.com/NathanFenina/claude-seo.git
cd claude-seo
./install.sh
```

Ou en copiant à la main :
```bash
cp -r skills/*   ~/.claude/skills/
cp -r agents/*   ~/.claude/agents/
cp -r commands/* ~/.claude/commands/
pip install -r requirements.txt
```

---

## Configuration

### 1 · Les clés

```bash
cp config/.env.example .env
```

Remplissez **uniquement ce dont vous avez besoin**. Chaque outil est
optionnel. Voir [MCP.md](MCP.md) pour obtenir chaque clé.

`.env` et `secrets/` sont dans `.gitignore`. Ne les commitez jamais.

### 2 · Le projet

Ouvrez `config/decupler-seo.config.yml`, section `projet` :

```yaml
projet:
  nom: "Mon entreprise"
  domaine: "https://exemple.com"
  secteur: "Plomberie"
  proposition_valeur: "Dépannage plomberie en 2 h à Lyon, 24/7"
  concurrents:
    - "concurrent-a.fr"
    - "concurrent-b.fr"
  pages_prioritaires:
    - "/devis"
    - "/services/plomberie"
  ton: "expert, direct, sans jargon"
  vouvoiement: true
```

Cinq minutes ici vous font gagner cinq minutes à chaque session ensuite.

### 3 · Le mode

```yaml
mode: autonomous     # safe | assisted | autonomous
```

`autonomous` par défaut : Claude écrit et publie tout seul, dans les limites
des garde-fous. Voir [SECURITE.md](SECURITE.md).

---

## Vérifier

```
/seo doctor
```

Attendu : les prérequis en vert, la liste des outils branchés, et une
proposition de première action.

---

## Prérequis

| Élément | Requis pour |
|---------|-------------|
| Claude Code | tout |
| Node | les MCP en npx |
| Python 3.8+ | les scripts d'analyse |
| Chrome | les Core Web Vitals réels (optionnel) |

```bash
pip install -r requirements.txt
```

---

## Désinstaller

```bash
./uninstall.sh
```

Ou, dans Claude Code : `/plugin uninstall claude-code-seo-decupler`.
