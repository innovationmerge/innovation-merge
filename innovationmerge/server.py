import argparse
import sys
import traceback
import uvicorn
import os


def cmdline_args():
    parser = argparse.ArgumentParser(description="Parse arguments")
    parser.add_argument(
        "ENVIRONMENT", type=str, default=sys.stdout,
        help="production/development/test"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = cmdline_args()

    try:
        if not os.getenv("ENVIRONMENT"):
            os.environ["ENVIRONMENT"] = args.ENVIRONMENT

        # custom imports
        from innovationmerge.config import configs
        from innovationmerge.app import create_app
        from innovationmerge.app.exceptions import innovationmergeMethodException

        HOST = configs.HOST
        PORT = configs.PORT
        print(HOST, PORT)
        app = create_app()
        uvicorn.run(app, host=HOST, port=PORT)
    except Exception as e:
        raise innovationmergeMethodException(str(e))
        print("Exeception: ", traceback.format_exc())
