# Claude Code comme centre de commande vidéo

Bilan au 3 novembre 2026 : Seedance, Google Flow/Veo et DaVinci Resolve.

## Ce qui a été vérifié

| Outil | Intégration retenue | État dans la session cloud |
|---|---|---|
| Seedance | Connecteur ElevenLabs (modèles Seedance 1 Pro → 2.5), plus le MCP AceDataCloud | Les outils répondent et sont authentifiés, mais la génération vidéo est refusée : **forfait ElevenLabs payant requis** |
| Google Flow | Pas d'API publique. Le modèle qui fait tourner Flow, **Veo 3.1**, est disponible via ElevenLabs | Même blocage : forfait payant requis |
| DaVinci Resolve | `samuelgursky/davinci-resolve-mcp` | Pas installable depuis le cloud : le serveur doit tourner sur le PC où Resolve est installé |

## Sources

- DaVinci Resolve MCP : https://github.com/samuelgursky/davinci-resolve-mcp (README et `docs/install.md`)
- Seedance MCP : https://github.com/AceDataCloud/SeedanceMCP (paquet PyPI `mcp-seedance`)
- Veo officiel Google (Vertex AI) : https://github.com/GoogleCloudPlatform/vertex-ai-creative-studio/tree/main/experiments/mcp-genmedia

## Installation sur le PC Windows

1. Installez Node.js 18+, Python 3.10+ et Claude Code (ffmpeg en plus, facultatif).
2. Ouvrez DaVinci Resolve. Sur la version Studio, réglez *Préférences > Général > External scripting using* sur **Local**.
3. Dans PowerShell, depuis ce dossier :
   ```
   powershell -ExecutionPolicy Bypass -File .\installer-mcp-video.ps1
   ```
4. Dans Claude Code, tapez `/mcp`, choisissez `seedance`, puis **Authenticate** (compte AceDataCloud).

## Tests à faire (un serveur ne compte comme opérationnel qu'après ces tests)

Demandez à Claude Code, dans l'ordre :

1. « Liste les outils MCP davinci-resolve disponibles. » Les outils doivent s'afficher.
2. « Avec DaVinci Resolve, donne-moi le nom du projet ouvert et la liste des timelines, sans rien modifier. » C'est un test en lecture seule.
3. « Crée un projet Resolve nommé TEST-MCP, importe un clip, puis supprime le projet. » Ce test n'écrit que dans un projet jetable.
4. « Liste les outils MCP seedance, puis génère une vidéo de 5 secondes. » Ce test est facturé.
5. Après passage au forfait ElevenLabs payant : « Génère 4 secondes avec Veo 3.1 Lite via ElevenLabs. »

## Limites connues

- **Google Flow** : aucun MCP ne pilote Flow par une API officielle. Les projets « google-flow-mcp » automatisent le navigateur ou réutilisent vos cookies de session Google. Ce ne sont pas de vrais MCP d'API, ils sont fragiles et peuvent contrevenir aux conditions de Google. Ils ne sont donc pas installés. On utilise Veo 3.1 (ElevenLabs, ou Vertex AI avec un projet Google Cloud facturé).
- **DaVinci Resolve gratuit** : le scripting externe est réservé à la version Studio. Le « pont » interne marche jusqu'à la 21.0.x. À partir de la 21.1 gratuite, il faut passer à Studio.
- **Coûts** : Seedance via AceDataCloud est débité sur ce compte, Veo et Seedance via ElevenLabs sur le forfait ElevenLabs.
