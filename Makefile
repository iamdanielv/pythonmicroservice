# The help comments are based on https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

# Color Definitions
C_RED := \033[31m
C_GREEN := \033[32m
C_YELLOW := \033[33m
C_BLUE := \033[34m
C_MAGENTA := \033[35m
C_CYAN := \033[36m
C_WHITE := \033[37m

T_RESET := \033[0m
T_BOLD := \033[1m
# Helpful Icons
T_OK_ICON := [${T_BOLD}${C_GREEN}✓${T_RESET}]
T_ERR_ICON := [${T_BOLD}${C_RED}✗${T_RESET}]
T_INFO_ICON := [${T_BOLD}${C_YELLOW}i${T_RESET}]

# run commands in a single shell, otherwise venv may not work
.ONESHELL:

# set some environment variables
CURRENT_PYTHON = which python3
VENV := $(notdir $(CURDIR)).venv
VENV_PYTHON := $(VENV)/bin/python
QUIET_PIP := pip -q --exists-action i

.DEFAULT_GOAL := help
.PHONY: help env show-env clean test run

define check_venv
	printf "$(C_BLUE)$(VENV)$(T_RESET)"
	if [ -d "$(VENV)" ]; then \
		printf " exists $(T_OK_ICON)\n"; \
		if [ -f "$(VENV)/bin/activate" ]; then \
			printf "$(C_BLUE)$(VENV)$(T_RESET) activate exists $(T_OK_ICON)\n"; \
		else \
			printf "$(C_BLUE)$(VENV)$(T_RESET) activate NOT found $(T_ERR_ICON)\n"; \
			printf "Maybe run:\n    make clean && make dev-env\n\n" ; \
			exit 1;\
		fi;
	else
		printf " does not exist $(T_ERR_ICON)\n"; \
		printf " \n$(T_INFO_ICON) Have you run?\n      make dev-env\n\n"; \
		exit 1; \
	fi
endef

help: ##@ show help contents
	@printf "$(C_BLUE)%-12s$(T_RESET) %s\n" "Target" "Description"
	@printf "%-12s %s\n" "------" "-----------"
	@grep -E '^[a-zA-Z_-]+:.*?##@ .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?##@ "}; {printf "\033[34m%-12s\033[0m %s\n", $$1, $$2}'

env: ##@ setup a virtual environment
	@printf "Setting up a $(C_YELLOW)Virtual Environment$(T_RESET) in $(C_BLUE)$(VENV)$(T_RESET)\n"
	@(
	if [ -d "$(VENV)" ]; then \
        printf "$(C_BLUE)$(VENV)$(T_RESET) exists, skipping $(T_OK_ICON)\n"; \
    else \
		printf "Creating $(C_BLUE)$(VENV)$(T_RESET) "; \
		python3 -m venv $(VENV); \
		if [ $$? -ne 0 ]; then \
        	printf "$(T_ERR_ICON) FAILED\n"; \
			exit 1; \
		else \
			printf "$(T_OK_ICON)\n"; \
    	fi; \
		echo "*" > $(VENV)/.gitignore ; \
	fi
	)
	@$(call check_venv)
	@printf "Activate $(C_BLUE)$(VENV)$(T_RESET) "
	@. $(VENV)/bin/activate
	if [ $$? -ne 0 ]; then \
        printf "$(T_ERR_ICON) FAILED\n"; \
	else \
		printf "$(T_OK_ICON)\n"; \
    fi
	@printf "Using python:\n  "
	@which python

	@printf "\nInstall pip "
	@$(VENV_PYTHON) -m $(QUIET_PIP) install --upgrade pip
	if [ $$? -ne 0 ]; then \
        printf "$(T_ERR_ICON) FAILED\n"; \
	else \
		printf "$(T_OK_ICON)\n"; \
    fi
	@printf "Install requirements "
	@$(QUIET_PIP) install -r requirements.txt
	if [ $$? -ne 0 ]; then \
        printf "$(T_ERR_ICON) FAILED\n"; \
	else \
		printf "$(T_OK_ICON)\n"; \
    fi

	printf "\n$(T_INFO_ICON) To $(C_GREEN)activate$(T_RESET) the virtual environment, type:\n"
	printf "  source $(VENV)/bin/activate \n\n"

show-env: ##@ Show paths used by python
	@(
	if [ -d "$(VENV)" ]; then \
        $(call check_venv); \
	else \
		printf "$(T_INFO_ICON) $(C_BLUE)$(VENV)$(T_RESET) Not Found\n"; \
    fi
	)
	@printf "current python:\n  "
	@which python3
	printf "\n$(T_INFO_ICON) To $(C_GREEN)activate$(T_RESET) the virtual environment, type:\n"
	printf "  source $(VENV)/bin/activate \n\n"

clean: ##@ delete the .venv environment
	@(if [ -d "$(VENV)" ]; then \
		printf "$(T_OK_ICON) $(C_BLUE)$(VENV)$(T_RESET) Found, $(C_RED)Removing$(T_RESET) Dev Environment\n"
		rm -rf "$(VENV)"; \
    else \
		printf "$(T_INFO_ICON) $(C_BLUE)$(VENV)$(T_RESET) Not Found, nothing to do\n"; \
	fi)

test: ##@ Run unit tests
	@printf "Running $(C_YELLOW)unit tests$(T_RESET)...\n"
	@pytest -v tests/
 

run: ##@ Run the application
	@printf "$(C_BLUE)Running the application$(T_RESET)...\n"
	@uvicorn src.main:app --reload
