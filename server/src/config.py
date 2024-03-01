
import os

OPENAI_MODEL = "gpt-3.5-turbo-1106"
# EMBED_MODEL = "text-embedding-ada-002"
EMBED_MODEL = "text-embedding-3-small"

QUESTION_SIMILARITY_THRESHOLD = 0.92
IS_ANSWERED_THRESHOLD = 0.85

# Check a directory in src/promps exists if not create it
if not os.path.exists('src/prompts'):
    os.makedirs('src/prompts')

PROMPTS_JSON_PATH = 'src/prompts/prompts.json'
COMPLETION_JSON_PATH = 'src/prompts/completion.json'
KEYNOTES_PROMPT_JSON_PATH = 'src/prompts/generated_keynotes_prompt.json'
QUESTIONS_PROMPT_JSON_PATH = 'src/prompts/generated_questions_prompt.json'
ANS_QUESTIONS_PROMPT_JSON_PATH = 'src/prompts/answered_questions_prompt.json'
SUMMARY_PROMPT_JSON_PATH = 'src/prompts/meeting_summary_prompt.json'
KEYNOTES_PROMPT_PATH = 'src/prompts/keynotes.txt'
QUESTIONS_PROMPT_PATH = 'src/prompts/keynotes.txt'
KEYNOTES_PATH = 'src/prompts/keynotes_generated.txt'
QUESTIONS_PATH = 'src/prompts/questions_generated.txt'
ANSWERED_QUESTIONS_PATH = 'src/prompts/answered_questions_generated.txt'

PHRASE_TO_REMOVE = 'key points discussed:'


MEETING_OBJECTIVES = ["kickoff", "head of department interview", "management interview", "on the ground interview", "status update"]

