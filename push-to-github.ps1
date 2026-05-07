# VisionTouch - Git Push Script
# Executez ce script PowerShell pour initialiser et pousser le projet sur GitHub

# Variables
$projectPath = "C:\Users\USER\Desktop\VisionTouch"
$repoUrl = "https://github.com/ahmed-hamda/VisionTouch.git"
$branchName = "develop"  # Nouvelle branche au lieu de main

# Etape 1 : Verifier que le dossier existe
Write-Host "[*] Verification du dossier du projet..." -ForegroundColor Cyan
if (Test-Path $projectPath) {
    Write-Host "[OK] Dossier trouve: $projectPath" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Dossier non trouve: $projectPath" -ForegroundColor Red
    exit 1
}

# Etape 2 : Naviguer vers le dossier du projet
Write-Host "`n[*] Navigation vers le dossier du projet..." -ForegroundColor Cyan
cd $projectPath

# Etape 3 : Initialiser le repository git (s'il ne l'est pas deja)
Write-Host "`n[*] Initialisation du repository git..." -ForegroundColor Cyan
if (Test-Path .git) {
    Write-Host "[!] Repository git deja initialise" -ForegroundColor Yellow
} else {
    git init
    Write-Host "[OK] Repository git initialise" -ForegroundColor Green
}

# Etape 4 : Ajouter la remote GitHub (s'il ne l'est pas deja)
Write-Host "`n[*] Configuration de la remote GitHub..." -ForegroundColor Cyan
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "[!] Remote origin deja configuree" -ForegroundColor Yellow
} else {
    git remote add origin $repoUrl
    Write-Host "[OK] Remote origin configuree: $repoUrl" -ForegroundColor Green
}

# Etape 5 : Ajouter tous les fichiers
Write-Host "`n[*] Ajout de tous les fichiers..." -ForegroundColor Cyan
git add .
Write-Host "[OK] Fichiers ajoutes" -ForegroundColor Green

# Etape 6 : Commit initial
Write-Host "`n[*] Creation du commit initial..." -ForegroundColor Cyan
git commit -m "Initial commit: VisionTouch - Object Detection App

- Backend Flask + YOLOv8
- Frontend Flutter
- Architecture complete
- Documentation README
- Configuration git"

Write-Host "[OK] Commit cree" -ForegroundColor Green

# Etape 7 : Creer une nouvelle branche (pas main)
Write-Host "`n[*] Creation de la branche $branchName..." -ForegroundColor Cyan
git checkout -b $branchName
Write-Host "[OK] Branche $branchName creee et activee" -ForegroundColor Green

# Etape 8 : Pousser sur GitHub
Write-Host "`n[*] Poussage du code sur GitHub..." -ForegroundColor Cyan
Write-Host "   Branche: $branchName" -ForegroundColor Yellow
git push -u origin $branchName
Write-Host "[OK] Code pousse avec succes!" -ForegroundColor Green

# Etape 9 : Afficher les informations finales
Write-Host "`n" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "     VisionTouch pret pour GitHub!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "`n[INFO] Informations:" -ForegroundColor Cyan
Write-Host "   Repo: $repoUrl" -ForegroundColor White
Write-Host "   Branche: $branchName" -ForegroundColor White
Write-Host "   Chemin local: $projectPath" -ForegroundColor White

Write-Host "`n[*] Statut du projet:" -ForegroundColor Cyan
git log --oneline -1
git branch -a

Write-Host "`n[SUCCESS] Succes! Vous pouvez maintenant:" -ForegroundColor Green
Write-Host "   1. Verifier votre repository sur GitHub" -ForegroundColor White
Write-Host "   2. Creer une Pull Request vers main" -ForegroundColor White
Write-Host "   3. Commencer a developper de nouvelles features!" -ForegroundColor White

Write-Host "`n"
