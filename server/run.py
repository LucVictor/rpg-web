from watchfiles import run_process
import asyncio

def start():
    from main import main
    asyncio.run(main())

if __name__ == "__main__":
    run_process(".", target=start)