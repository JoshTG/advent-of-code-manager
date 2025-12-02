from shiny import run_app


def main() -> None:
  run_app('aoc_manager.app:app', reload=True)


if __name__ == '__main__':
  main()
