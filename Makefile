ecr-login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 724819293261.dkr.ecr.us-east-1.amazonaws.com

img-pull:
	docker pull 724819293261.dkr.ecr.us-east-1.amazonaws.com/mwcore-cpu

build:
	docker build --platform linux/amd64 . -t img_name:latest

clean:
	docker system prune -a

streamlit:
	docker-compose up streamlit

streamlit-local:
	docker-compose up streamlit-local

shell:
	docker-compose run shell

shell-local:
	docker-compose run shell-local
