#%%
from llama_cpp import LlamaGrammar
from autonomus_social_media_avatar.fetcher.simulator.pydantic_models_to_grammar import generate_gbnf_grammar_and_documentation
from autonomus_social_media_avatar.fetcher.environment_objects import AvatarEnvironment


tools = [AvatarEnvironment]
gbnf_grammar, documentation = generate_gbnf_grammar_and_documentation(
        pydantic_model_list=tools, outer_object_name="function",
        outer_object_content="function_parameters", model_prefix="Function", fields_prefix="Parameters")
# %%
LlamaGrammar.from_string(gbnf_grammar)
# %%
