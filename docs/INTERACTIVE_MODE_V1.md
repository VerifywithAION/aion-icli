# AION ICLI Interactive Mode V1

## Purpose

Interactive Mode V1 lets users run AION ICLI as a persistent local session instead of only a one-shot command.

One-shot mode:

    .\bin\aion.cmd "Who are you, AION?"

Interactive mode:

    .\bin\aion.cmd

Then:

    Operator > help
    Operator > who are you
    Operator > can I connect an API?
    Operator > receipt
    Operator > boundary
    Operator > exit

## Behavior

Interactive Mode V1 remains:

- local-first
- no network by default
- no file mutation by default except local receipt writing
- no live execution by default
- receipt-bound
- non-destructive
- public-safe

## Built-in commands

- `help`
- `receipt`
- `boundary`
- `verify`
- `exit`

## Receipt behavior

Each prompt writes the latest local receipt:

    receipts\local\aion_cli_receipt_v1.json

The receipt records:

- mode
- prompt
- response
- boundary
- network
- mutation
- execution
- governance tone

## Expected markers

    AION_INTERACTIVE_MODE_V1_VERIFY_OK

## Status

LOCKED as AION ICLI Interactive Mode V1.
