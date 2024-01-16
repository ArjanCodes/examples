from enum import StrEnum

class OpenAIModels(StrEnum):
    GPT3_TURBO = "gpt-3.5-turbo-1106"
    GPT4 = "gpt-4"
    GPT4_TURBO_VISION = "gpt-4-vision-preview"
    GPT4_TURBO = "gpt-4-1106-preview"

MODEL_TOKEN_LIMITS = {
    OpenAIModels.GPT3_TURBO: 4096,  # Assuming token limit for GPT-3.5 Turbo
    OpenAIModels.GPT4: 8192,        # Assuming token limit for GPT-4
    OpenAIModels.GPT4_TURBO_VISION: 128000,  # Assuming token limit for GPT-4 Turbo Vision
    OpenAIModels.GPT4_TURBO: 128000,  # Assuming token limit for GPT-4 Turbo
}
