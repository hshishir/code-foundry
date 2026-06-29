import argparse

from app.db.database import Base, SessionLocal, engine
from orchestrator import workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="code-foundry",
        description="Run deterministic local workflow agents.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "run-once",
        help="Advance the oldest eligible feature by one workflow step.",
    )
    run_feature_parser = subparsers.add_parser(
        "run-feature",
        help="Advance a specific feature by one workflow step.",
    )
    run_feature_parser.add_argument("feature_id", type=int)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if args.command == "run-once":
            result = workflow.run_once(db)
        elif args.command == "run-feature":
            result = workflow.run_feature(db, args.feature_id)
        else:
            parser.error(f"Unsupported command: {args.command}")

    print(result.message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
