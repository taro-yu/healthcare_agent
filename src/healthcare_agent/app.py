import sys
from health_agent.core.agent import HealthAgent
from health_agent.config.settings import settings
from health_agent.core.logger import get_logger

log = get_logger(__name__)

def main():
    agent = HealthAgent()
    print("健康管理AIエージェントへようこそ。何を手伝いましょう？（'exit'で終了）")
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nまたお話ししましょう。")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("またお会いしましょう。")
            break

        reply = agent.handle_user_message(user_input, locale=settings.DEFAULT_LOCALE)
        print(reply)

if __name__ == "__main__":
    main()