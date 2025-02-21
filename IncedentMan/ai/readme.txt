wanna build image ?? here's the steps
docker build -t your-image-name .
docker stop your-container-name  # if it's running
docker rm your-container-name    # if it exists
docker run -d --name your-container-name -p 5000:5000 your-image-name


for test : 
$body = @{
    description = "Cannot connect to the database server"
} | ConvertTo-Json

step2:
Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method Post -ContentType "application/json" -Body $body