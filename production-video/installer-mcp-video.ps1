<#
  Kit d'installation MCP video pour Claude Code (Windows)
  - DaVinci Resolve : samuelgursky/davinci-resolve-mcp (serveur local, API de scripting officielle)
  - Seedance        : AceDataCloud/SeedanceMCP (serveur heberge, connexion OAuth, aucune cle a coller)
  - Google Veo      : deja disponible via le connecteur ElevenLabs de claude.ai (forfait payant requis)

  Le script n'efface et ne remplace aucune configuration : un serveur deja
  enregistre sous le meme nom est laisse tel quel.

  Lancement (PowerShell, dans ce dossier) :
    powershell -ExecutionPolicy Bypass -File .\installer-mcp-video.ps1
#>

$ErrorActionPreference = "Stop"

function Etape($texte) { Write-Host "`n=== $texte" -ForegroundColor Cyan }
function Ok($texte)    { Write-Host "  [OK] $texte" -ForegroundColor Green }
function Ko($texte)    { Write-Host "  [!!] $texte" -ForegroundColor Yellow }

function Test-Commande($nom) { return [bool](Get-Command $nom -ErrorAction SilentlyContinue) }

function Test-ServeurMcp($nom) {
  & claude mcp get $nom *> $null
  return ($LASTEXITCODE -eq 0)
}

# ---------------------------------------------------------------- 1. Prerequis
Etape "1. Verification des prerequis"
$manque = @()
if (Test-Commande "claude") { Ok "Claude Code : $(claude --version)" } else { $manque += "Claude Code (https://code.claude.com)" }
if (Test-Commande "node")   { Ok "Node.js : $(node --version)" }      else { $manque += "Node.js 18+ (https://nodejs.org)" }
if (Test-Commande "npx")    { Ok "npx present" }                        else { $manque += "npx (fourni avec Node.js)" }
$python = $null
foreach ($c in @("py", "python")) { if (Test-Commande $c) { $python = $c; break } }
if ($python) { Ok "Python : $(& $python --version)" } else { $manque += "Python 3.10+ (https://www.python.org, cocher 'Add to PATH')" }
if (Test-Commande "ffmpeg") { Ok "ffmpeg present (analyse audio DaVinci)" } else { Ko "ffmpeg absent : facultatif, utile pour l'analyse audio (winget install Gyan.FFmpeg)" }

if ($manque.Count -gt 0) {
  Ko "Logiciels manquants :"
  $manque | ForEach-Object { Write-Host "     - $_" }
  throw "Installez les elements ci-dessus puis relancez le script."
}

# ---------------------------------------------------------------- 2. DaVinci Resolve
Etape "2. DaVinci Resolve"
$resolveExe = "C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
$scriptApi  = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
if (Test-Path $resolveExe) {
  $v = (Get-Item $resolveExe).VersionInfo.ProductVersion
  Ok "DaVinci Resolve detecte, version $v"
} else {
  Ko "Resolve.exe introuvable a l'emplacement standard. Le programme d'installation du MCP cherchera ailleurs."
}
if (Test-Path $scriptApi) { Ok "API de scripting presente : $scriptApi" } else { Ko "Dossier de l'API de scripting introuvable : $scriptApi" }

Write-Host @"

  AVANT DE CONTINUER, dans DaVinci Resolve :
   - Edition Studio : Preferences > General > 'External scripting using' = Local
   - Edition gratuite : le scripting externe est reserve a Studio. Le MCP propose un
     'pont' interne (scripts/install_resolve_bridge.py) qui fonctionne jusqu'a Resolve 21.0.x ;
     a partir de Resolve 21.1 gratuit, le scripting Python est reserve a Studio.
"@
Read-Host "  Appuyez sur Entree quand Resolve est ouvert et configure"

if (Test-ServeurMcp "davinci-resolve") {
  Ok "Un serveur 'davinci-resolve' est deja enregistre dans Claude Code : laisse tel quel."
} else {
  Write-Host "  Lancement de l'installateur officiel (interactif). Choisissez 'Claude Code' quand il le demande."
  & npx -y davinci-resolve-mcp setup
  & npx -y davinci-resolve-mcp doctor
}

# ---------------------------------------------------------------- 3. Seedance
Etape "3. Seedance (AceDataCloud, serveur heberge)"
if (Test-ServeurMcp "seedance") {
  Ok "Un serveur 'seedance' est deja enregistre : laisse tel quel."
} else {
  & claude mcp add --transport http --scope user seedance https://seedance.mcp.acedata.cloud/mcp
  Ok "Serveur 'seedance' enregistre (portee utilisateur)."
}
Write-Host @"
  Connexion : ouvrez Claude Code, tapez /mcp, choisissez 'seedance' puis 'Authenticate'.
  Il faut un compte AceDataCloud (https://platform.acedata.cloud) avec du solde :
  chaque generation est facturee sur ce compte.
"@

# ---------------------------------------------------------------- 4. Bilan
Etape "4. Bilan des serveurs MCP enregistres"
& claude mcp list

Write-Host @"

  Etape suivante : ouvrez Claude Code et lancez les tests du fichier GUIDE.md
  (section 'Tests a faire'). Un serveur n'est operationnel que si ces tests passent.
"@
