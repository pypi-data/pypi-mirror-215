from enum import Enum

from mindflow.core.types.definitions.model_type import ModelType


class ModelID(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"

    CLAUDE_V1 = "claude-v1"
    CLAUDE_V1_2 = "claude-v1.2"
    CLAUDE_INSTANT_V1 = "claude-instant-v1"

    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


class ModelParameterKey(Enum):
    ID = "id"
    NAME = "name"
    SERVICE = "service"
    MODEL_TYPE = "model_type"
    SOFT_TOKEN_LIMIT = "soft_token_limit"
    HARD_TOKEN_LIMIT = "hard_token_limit"
    TOKEN_COST = "token_cost"
    TOKEN_COST_UNIT = "token_cost_unit"
    DESCRIPTION = "description"
    CONFIG_DESCRIPTION = "config_description"


class ModelService(Enum):
    GPT_3_5_TURBO = "openai"
    GPT_3_5_TURBO_0301 = "openai"

    GPT_4 = "openai"
    GPT_4_0314 = "openai"
    GPT_4_32K = "openai"
    GPT_4_32K_0314 = "openai"

    TEXT_EMBEDDING_ADA_002 = "openai"

    CLAUDE_V1 = "anthropic"
    CLAUDE_V1_2 = "anthropic"
    CLAUDE_INSTANT_V1 = "anthropic"


class ModelConfigParameterKey(Enum):
    SOFT_TOKEN_LIMIT = "soft_token_limit"


class ModelConfigParameterName(Enum):
    SOFT_TOKEN_LIMIT = "Soft Token Limit"


class ModelName(Enum):
    GPT_3_5_TURBO = "GPT 3.5 Turbo"
    GPT_3_5_TURBO_0301 = "GPT 3.5 Turbo March 1st"

    GPT_4 = "GPT 4"
    GPT_4_0314 = "GPT 4 March 14th"
    GPT_4_32K = "GPT 4 32K"
    GPT_4_32K_0314 = "GPT 4 32K March 14th"

    TEXT_EMBEDDING_ADA_002 = "Text Embedding Ada 002"

    CLAUDE_V1 = "Claude V1"
    CLAUDE_V1_2 = "Claude V1.2"
    CLAUDE_INSTANT_V1 = "Claude Instant V1"


class ModelSoftTokenLimit(Enum):
    GPT_3_5_TURBO = 500
    GPT_3_5_TURBO_0301 = 500

    GPT_4 = 500
    GPT_4_0314 = 500
    GPT_4_32K = 500
    GPT_4_32K_0314 = 500

    TEXT_EMBEDDING_ADA_002 = 8191

    CLAUDE_V1 = 500
    CLAUDE_V1_2 = 500
    CLAUDE_INSTANT_V1 = 500


class ModelHardTokenLimit(Enum):
    GPT_3_5_TURBO = 4000
    GPT_3_5_TURBO_0301 = 4000

    GPT_4 = 8192
    GPT_4_0314 = 8192
    GPT_4_32K = 32_768
    GPT_4_32K_0314 = 32_768

    TEXT_EMBEDDING_ADA_002 = 8191

    CLAUDE_V1 = 9000
    CLAUDE_INSTANT_V1 = 9000


class ModelTokenCost(Enum):
    GPT_3_5_TURBO = 0.002
    GPT_3_5_TURBO_0301 = 0.002

    GPT_4 = 0.002
    GPT_4_0314 = 0.002
    GPT_4_32K = 0.002
    GPT_4_32K_0314 = 0.002

    CLAUDE_V1 = 2.90
    CLAUDE_INSTANT_V1 = 0.43

    TEXT_EMBEDDING_ADA_002 = 0.0004


class ModelTokenCostUnit(Enum):
    THOUSAND = 1000
    MILLION = 1_000_000


class ModelDescription(Enum):
    GPT_3_5_TURBO = f"GPT 3.5 Turbo: {str(ModelHardTokenLimit.GPT_3_5_TURBO.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_3_5_TURBO_0301 = f"GPT 3.5 Turbo March 1st: {str(ModelHardTokenLimit.GPT_3_5_TURBO_0301.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO_0301.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."

    GPT_4 = f"GPT 4: {str(ModelHardTokenLimit.GPT_4.value)} token Limit. ${str(ModelTokenCost.GPT_4.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_0314 = f"GPT 4 March 14th: {str(ModelHardTokenLimit.GPT_4_0314.value)} token Limit. ${str(ModelTokenCost.GPT_4_0314.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_32K = f"GPT 4 32K: {str(ModelHardTokenLimit.GPT_4_32K.value)} token Limit. ${str(ModelTokenCost.GPT_4_32K.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_32K_0314 = f"GPT 4 32K March 14th: {str(ModelHardTokenLimit.GPT_4_32K_0314.value)} token Limit. ${str(ModelTokenCost.GPT_4_32K_0314.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."

    CLAUDE_V1 = f"Claude V1: {str(ModelHardTokenLimit.CLAUDE_V1.value)} token Limit. ${str(ModelTokenCost.CLAUDE_V1.value)} per {str(ModelTokenCostUnit.MILLION.value)} tokens. Anthropic's largest and most powerful model"
    CLAUDE_INSTANT_V1 = f"Claude Instant V1: {str(ModelHardTokenLimit.CLAUDE_INSTANT_V1.value)} token Limit. ${str(ModelTokenCost.CLAUDE_INSTANT_V1.value)} per {str(ModelTokenCostUnit.MILLION.value)} tokens. Anthropic's smaller, faster, and cheaper model."

    TEXT_EMBEDDING_ADA_002 = f"Text Embedding Ada 002: {str(ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002)} token Limit. ${str(ModelTokenCost.TEXT_EMBEDDING_ADA_002)} per {str(ModelTokenCostUnit.THOUSAND)} tokens.   OpenAI's best advertised embedding model. Fast and cheap! Recommended for generating deep and shallow indexes"


class ModelConfigDescription(Enum):
    GPT_3_5_TURBO = f"{ModelName.GPT_3_5_TURBO.value}:       OpenAI's Fast, cheap, and still powerful model.       Token Limit: {str(ModelHardTokenLimit.GPT_3_5_TURBO.value)}."
    GPT_4 = f"{ModelName.GPT_4.value}:               OpenAI's most powerful model (slower + expensive).    Token Limit: {str(ModelHardTokenLimit.GPT_4.value)}. Get access -> https://openai.com/waitlist/gpt-4-api."
    TEXT_EMBEDDING_ADA_002 = f"{ModelName.TEXT_EMBEDDING_ADA_002.value}:   OpenAI's best and cheapest embedding model.    Token Limit: {str(ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002.value)}"

    CLAUDE_INSTANT_V1 = f"{ModelName.CLAUDE_INSTANT_V1.value}:   Anthropic's Fast, cheap, and still powerful model.    Token Limit: {str(ModelHardTokenLimit.CLAUDE_INSTANT_V1.value)}. Get access -> https://www.anthropic.com/earlyaccess"
    CLAUDE_V1 = f"{ModelName.CLAUDE_V1.value}:           Anthropic's most powerful model (slower + expensive). Token Limit: {str(ModelHardTokenLimit.CLAUDE_V1.value)}. Get access -> https://www.anthropic.com/earlyaccess"


## Service Models (By Type)
class ModelTextCompletionOpenAI(Enum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value


class ModelTextCompletionAnthropic(Enum):
    CLAUDE_V1 = ModelID.CLAUDE_V1.value
    CLAUDE_INSTANT_V1 = ModelID.CLAUDE_INSTANT_V1.value


class ModelTextEmbeddingOpenAI(Enum):
    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Models (ALL)
class ModelOpenAI(Enum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value

    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


class ModelAnthropic(Enum):
    CLAUDE_V1 = ModelID.CLAUDE_V1.value
    CLAUDE_INSTANT_V1 = ModelID.CLAUDE_INSTANT_V1.value


MODEL_STATIC: dict = {
    ModelID.GPT_3_5_TURBO.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_3_5_TURBO.value,
        ModelParameterKey.NAME.value: ModelName.GPT_3_5_TURBO.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_3_5_TURBO.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_3_5_TURBO.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_3_5_TURBO.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.GPT_3_5_TURBO.value,
    },
    ModelID.GPT_3_5_TURBO_0301.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.NAME.value: ModelName.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_4.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.GPT_4.value,
    },
    ModelID.CLAUDE_V1.value: {
        ModelParameterKey.ID.value: ModelID.CLAUDE_V1.value,
        ModelParameterKey.NAME.value: ModelName.CLAUDE_V1.value,
        ModelParameterKey.SERVICE.value: ModelService.CLAUDE_V1.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.CLAUDE_V1.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.CLAUDE_V1.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.CLAUDE_V1.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.MILLION.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.CLAUDE_V1.value,
    },
    ModelID.CLAUDE_INSTANT_V1.value: {
        ModelParameterKey.ID.value: ModelID.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.NAME.value: ModelName.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.SERVICE.value: ModelService.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.MILLION.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.CLAUDE_INSTANT_V1.value,
    },
    ModelID.GPT_4_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_0314.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_0314.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_0314.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_0314.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_0314.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_0314.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_4_32K.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_32K.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_32K.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_32K.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_32K.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_32K.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_4_32K_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K_0314.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_32K_0314.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_32K_0314.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_32K_0314.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_32K_0314.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_32K_0314.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.TEXT_EMBEDDING_ADA_002.value: {
        ModelParameterKey.ID.value: ModelID.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.SERVICE.value: ModelService.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_EMBEDDING.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.TEXT_EMBEDDING_ADA_002.value,
    },
}
