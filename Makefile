clean-all:
	@echo "Stopping containers..."
	-docker compose down
	@echo "Removing images..."
	-docker rmi sharks-enlightenment-v2-front sharks-enlightenment-v2-back
	@echo "Removing specific volumes..."
	-docker volume rm sharks-enlightenment-v2_media_volume sharks-enlightenment-v2_static_volume
	@echo "Removing dangling volumes..."
	-docker volume prune -f

clean:
	@echo "Stopping containers..."
	-docker compose down
	@echo "Removing images..."
	-docker rmi sharks-enlightenment-v2-front sharks-enlightenment-v2-back
	@echo "Removing specific volumes..."
	-docker volume rm sharks-enlightenment-v2_static_volume
	@echo "Removing dangling volumes..."
	-docker volume prune -f

restart:
	@echo "Stopping containers..."
	-docker compose down
	@echo "Removing images..."
	-docker rmi sharks-enlightenment-v2-front sharks-enlightenment-v2-back
	@echo "Removing specific volumes..."
	-docker volume rm sharks-enlightenment-v2_static_volume
	@echo "Removing dangling volumes..."
	-docker volume prune -f
	@echo "Restarting..."
	-docker compose up

migrate:
	@echo "Applying migrations..."
	-docker exec -it sharks-enlightenment-v2-back-1 sh -c "./manage.py makemigrations && ./manage.py migrate"
