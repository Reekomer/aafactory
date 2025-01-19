from autonomus_social_media_avatar.src.avatar.acting import run_avatar
from autonomus_social_media_avatar.src.fetcher.fetching import run_fetcher
from autonomus_social_media_avatar.src.narrator.narration import run_narration

def main():
    current_environment = run_fetcher(simulation=True)
    current_situation = run_narration(current_environment)
    avatar_taken_actions = run_avatar(current_situation)
    

if __name__ == "__main__":
    main()