 # How to use bot with AWS :
 ###### Based on [Shilleh tutorial](https://towardsdev.com/easily-use-selenium-with-aws-lambda-2cc49ca43b93)

---

#### This bot is a personal project for web scraping; I am not responsible for its use or results. Using bots for task automation is against Microsoft Reward rules and may lead to account bans. 

---
Before start deploying the image on Docker then AWS, take your AWS accound id (AMAZON ID) and define the wanted server region (REGION). Then replace values in following command lines.

1. Build the Docker Image :
    ```sh
    docker build -t selenium-chrome-driver .
    ```
2. Tag the Docker Image :
    ```sh
    docker tag selenium-chrome-driver (AMAZON ID).dkr.ecr.(REGION).amazonaws.com/docker-images:v1.0.0
    ```
3. Push the Docker Image to AWS ECR
    ```sh
    aws ecr get-login-password --region (REGION) | docker login --username AWS --password-stdin (AMAZON ID).dkr.ecr.(REGION).amazonaws.com/docker-images
    ```
    ```sh
    docker push (AMAZON ID).dkr.ecr.(REGION).amazonaws.com/docker-images:v1.0.0
    ```


*Bot Selenium to complete ms reward daily quests by Paul SALAÜN*
