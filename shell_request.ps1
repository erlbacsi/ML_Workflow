$jsonData = @{
    text = "The best Italian dish is Lasagne!!"
    sentiment = "positive"
} | ConvertTo-Json

$answer = Invoke-WebRequest -Uri "http://127.0.0.1:5000/sentiment" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body $jsonData

$responseData = $answer.Content | ConvertFrom-Json
$responseData | Format-List

