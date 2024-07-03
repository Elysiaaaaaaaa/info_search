$currentDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git add .
git commit -m "Commit on $currentDate"
git push