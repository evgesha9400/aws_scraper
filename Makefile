BASE_PATH=./src

download-chrome-and-chromedriver:
	CHROME_URL=$$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url') && \
	CHROMEDRIVER_URL=$$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url') && \
	curl -sL $$CHROME_URL -o chrome-linux64.zip && \
	curl -sL $$CHROMEDRIVER_URL -o chromedriver-linux64.zip && \
	unzip -o chromedriver-linux64.zip -d $(BASE_PATH)
	unzip -o chrome-linux64.zip -d $(BASE_PATH)
	rm -f chrome-linux64.zip chromedriver-linux64.zip

export_requirements:
	poetry export -f requirements.txt --without-hashes > src/requirements.txt

up-db:
	docker compose up db -d

migrate:
	@if [ `dbmate status | grep "Pending:" | awk '{print $$2}'` -gt 0 ]; then \
		echo "Dbmate: migrations pending. Migrating..."; \
		dbmate up; \
	else \
		echo "Dbmate: no pending migrations"; \
	fi

up-app:
	docker compose up app --build

start: up-db migrate up-app


stop:
	docker compose down --remove-orphans

clean:
	docker images prune

terminal:
	docker compose run --entrypoint /bin/sh app

deploy export_requirements:
	cd cdk && cdk deploy

diff:
	cd cdk && cdk diff