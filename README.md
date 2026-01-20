# netrach

## Install with pip

```bash
pip install git+https://github.com/Milansuman/netrach-agent.git
```

## Usage

Ensure the following environment variables are set:
```env
GROQ_API_KEY=
GITHUB_TOKEN=
NETRA_API_KEY=
NETRA_OTLP_ENDPOINT=
```
then run `netrach` to use the utility.

```bash
$ netrach # Starts the agent in interactive mode and maintains a chat log that ends when the session is exited
$ netrach --auto # Automatically generates a CHANGELOG.md based on the commits for the latest release
$ netrach --auto -f path/to/changelog.md # Asks the agent to save the changelog at the specified path
$ netrach --auto -r v1.2.3 # Generates a changelog for a specific release version
$ netrach --auto --repo owner/repo # Generates a changelog for a specific repository
$ netrach --auto -r v1.2.3 --repo owner/repo -f CHANGELOG.md # Combine all options
```

## Repo Setup 

Clone the repo and create a python venv
```bash
python3 -m venv .venv
source .venv/bin/activate
```
(If you're creating a venv with a different name, add it to the .gitignore)

Install the dependencies
```bash
pip install -r requirements.txt
```

set up the env based on .env.example and run!
```bash
python3 src/agent.py
```