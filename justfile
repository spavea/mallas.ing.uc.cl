# This is the [INFO] prefix in bold cyan

info_prefix := `echo "\e[1;36m[Info]\e[0m"`

default:
    @just --list

deps-front:
    @echo "{{ info_prefix }} \e[1mInstalling front-end dependencies...\e[0m"
    cd frontend && npm install

generate-client:
    @echo "{{ info_prefix }} \e[1mGenerating OpenAPI client...\e[0m"
    cd frontend && npm run generate

wait-backend-start:
    #!/usr/bin/env bash
    set -euo pipefail
    echo -e "{{ info_prefix }} \e[1mWaiting for back-end to start...\e[0m"
    # Activate poetry virtualenv
    source /workspaces/planner/backend/.venv/bin/activate
    cd frontend
    # Wait till localhost:8000 is available
    while ! http --check-status :8000/health 2> /dev/null; do
        sleep 1
    done
    echo -e "{{ info_prefix }} \e[1mBack-end started.\e[0m"

generate-client-watch: wait-backend-start
    @echo "{{ info_prefix }} \e[1mStarting watcher to generate OpenAPI client when needed...\e[0m"
    # Use nodemon to track changes
    cd frontend && npx --yes nodemon -e py --watch ../backend/ --exec "npm run generate" --signal SIGTERM

generate-client-on-start: wait-backend-start generate-client
    
deps-back:
    @echo "{{ info_prefix }} \e[1mInstalling back-end dependencies...\e[0m"
    cd backend && poetry config virtualenvs.in-project true
    cd backend && poetry install

deps: deps-front deps-back

lint-front:
    @echo "{{ info_prefix }} \e[1mLinting front-end...\e[0m"
    cd frontend && npm run lint

lint-back:
    @echo "{{ info_prefix }} \e[1mLinting back-end...\e[0m"
    cd backend && poetry run black --diff .
    cd backend && poetry run ruff check .
    cd backend && poetry run pyright

lint: lint-front lint-back

format-front:
    @echo "{{ info_prefix }} \e[1mFormatting front-end...\e[0m"
    cd frontend && npm run format

format-back:
    @echo "{{ info_prefix }} \e[1mFormatting back-end...\e[0m"
    cd backend && poetry run black .

format: format-front format-back

init: deps
    @echo "{{ info_prefix }} \e[1mInitializing developer environment...\e[0m"
    @echo "{{ info_prefix }} \e[1mCreating default files...\e[0m"
    cd backend && cp -n .env.development.example .env
    cd backend/mock-data && cp -n cas-mock-users.json.example cas-mock-users.json
    cd frontend && cp -n .env.development .env
    @echo "{{ info_prefix }} \e[1mSetting up database...\e[0m"
    @just db-reset
    @echo "{{ info_prefix }} \e[1mInitialized developer environment successfully 🚀.\e[0m"

db-studio:
    @echo "{{ info_prefix }} \e[1mStarting Prisma Studio...\e[0m"
    cd backend && poetry run prisma studio

db-migrate:
    @echo "{{ info_prefix }} \e[1mRunning and generating database migrations...\e[0m"
    cd backend && poetry run prisma migrate dev

db-reset:
    @echo "{{ info_prefix }} \e[1mResetting and initializing database...\e[0m"
    cd backend && poetry run prisma migrate reset --force

db-generate:
    @echo "{{ info_prefix }} \e[1mGenerating Prisma client...\e[0m"
    cd backend && poetry run prisma generate
