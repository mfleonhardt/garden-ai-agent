FROM python:3.12

# Set working directory
WORKDIR /workspace

# Install basic system dependencies
RUN apt-get update && apt-get install -y \
    git curl sqlite3 gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m vscode

# Add local bin to PATH for the vscode user
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Switch to the non-root user
USER vscode

# Set up the command to run when the container starts
CMD ["bash"]
