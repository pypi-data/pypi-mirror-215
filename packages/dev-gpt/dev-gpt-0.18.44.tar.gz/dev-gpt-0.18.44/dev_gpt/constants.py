DOCKER_BASE_IMAGE_VERSION = '0.0.8'

EXECUTOR_FILE_NAME = '__init__.py'
IMPLEMENTATION_FILE_NAME = 'microservice.py'
TEST_EXECUTOR_FILE_NAME = 'test_microservice.py'
REQUIREMENTS_FILE_NAME = 'requirements.txt'
DOCKER_FILE_NAME = 'Dockerfile'
CLIENT_FILE_NAME = 'client.py'
STREAMLIT_FILE_NAME = 'streamlit.py'

EXECUTOR_FILE_TAG = 'python'
IMPLEMENTATION_FILE_TAG = 'python'
TEST_EXECUTOR_FILE_TAG = 'python'
REQUIREMENTS_FILE_TAG = ''
DOCKER_FILE_TAG = 'dockerfile'
CLIENT_FILE_TAG = 'python'
STREAMLIT_FILE_TAG = 'python'

FILE_AND_TAG_PAIRS = [
    (EXECUTOR_FILE_NAME, EXECUTOR_FILE_TAG),
    (IMPLEMENTATION_FILE_NAME, IMPLEMENTATION_FILE_TAG),
    (TEST_EXECUTOR_FILE_NAME, TEST_EXECUTOR_FILE_TAG),
    (REQUIREMENTS_FILE_NAME, REQUIREMENTS_FILE_TAG),
    (DOCKER_FILE_NAME, DOCKER_FILE_TAG),
    (CLIENT_FILE_NAME, CLIENT_FILE_TAG),
    (STREAMLIT_FILE_NAME, STREAMLIT_FILE_TAG)
]

INDICATOR_TO_IMPORT_STATEMENT = {
    'io.BytesIO': 'import io',
    'BeautifulSoup': 'from bs4 import BeautifulSoup',
    'BytesIO': 'from io import BytesIO',
    'base64': 'import base64',
}

FLOW_URL_PLACEHOLDER = 'jcloud.jina.ai'

PRICING_GPT4_PROMPT = 0.03
PRICING_GPT4_GENERATION = 0.06
PRICING_GPT3_5_TURBO_PROMPT = 0.002
PRICING_GPT3_5_TURBO_GENERATION = 0.002

CHARS_PER_TOKEN = 3.4

NUM_IMPLEMENTATION_STRATEGIES = 5
MAX_DEBUGGING_ITERATIONS = 10

DEMO_TOKEN = '45372338e04f5a41af949024db929d46'

BLACKLISTED_PACKAGES = [
    'moderngl', 'pyopengl', 'pyglet', 'pythreejs', 'panda3d',  # because they need a screen,
    'tika',  # because it needs java
    'clearbit',  # because of installation issues on latest version
    'pyttsx3',  # after engine.save_to_file(summarized_text, "summarized_audio.wav"); engine.runAndWait() "summarized_audio.wav" does not exist
]

UNNECESSARY_PACKAGES = [
    'jinja2', 'werkzeug', 'flask', 'flask_restful', 'http.server', 'flask_json', 'flask_cors', 'fastapi', 'uvicorn', 'starlette',  # because the wrappers are used instead
    'pypng', # if we provide access to the documentation all should be fine but for now it is too hard to use since the import is png

]

LANGUAGE_PACKAGES = [
    'allennlp', 'bert-for-tf2', 'bertopic', 'gpt-3', 'fasttext', 'flair', 'gensim', 'nltk', 'openai',
    'pattern', 'polyglot', 'pytorch-transformers', 'rasa', 'sentence-transformers',
    'spacy', 'stanza', 'summarizer', 'sumy', 'textblob', 'textstat', 'transformers',
    'vadersentiment', 'language-tool-python'
]

SEARCH_PACKAGES = [
    'googlesearch-python', 'google', 'googlesearch', 'google-api-python-client', 'pygooglenews', 'google-cloud'
]

TOOL_TO_ALIASES = {
    'gpt_3_5_turbo': ['gpt-3', 'GPT-3'],
    'google_custom_search': ['Google Custom Search API']
}

