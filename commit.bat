$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git add .
git commit -m $currentDate
git push