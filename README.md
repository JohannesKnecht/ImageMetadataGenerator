# ImageMetadataGenerator
ImageMetadataGenerator

# Requirements
- python 3.14
- uv
- docker (as alternative to non docker setup)
- Taskfile (optional)

# Setup (non docker)
- install uv depedencies
- place .env in backend/ImageMetadataGeneratorBackend conating openai api key in the form
OPENAI_API_KEY="key here"
- "task run-backend"

# Setup (docker)
- "run-backend-docker"