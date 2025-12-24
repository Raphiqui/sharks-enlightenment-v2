clean:
	@echo "Stopping containers..."
	-docker compose down
	@echo "Removing images..."
	-docker rmi sharks-enlightenment-v2-front sharks-enlightenment-v2-back
	@echo "Removing specific volumes..."
	-docker volume rm sharks-enlightenment-v2_media_volume sharks-enlightenment-v2_static_volume
	@echo "Listing remaining dangling volumes (NOT removing)..."
	@docker volume ls -qf dangling=true
	@echo "Cleanup complete! Database and other volumes preserved."

clean-dangling:
	@echo "This will remove dangling volumes (random hash names)."
	@echo "Your postgres_data and eburydata volumes are safe if in use."
	@docker volume ls -qf dangling=true
	@read -p "Remove these dangling volumes? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker volume prune -f; \
		echo "Dangling volumes removed!"; \
	fi
