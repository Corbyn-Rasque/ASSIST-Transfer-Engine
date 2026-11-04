# ASSIST Transfer Engine

The ASSIST Transfer Engine is a project aimed at helping transfer students in California plan for and make decisions around transferring to California four-year colleges. While tools like [ASSIST](https://assist.org) allow for building plans from static agreements by hand, the process can be incredibly cumbersome and scales poorly when multiple community colleges and multiple four-year universities are in the mix.

This tool started as my senior project at Cal Poly and aims to allow prospective transfer students to enter in class information from classes they've taken across multiple community colleges (along with information about the schools and degrees they're pursuing) to generate progress reports for every prospective university at once. The plan is, ideally, to allow for updating this information as courses are taken to allow for planning and progress to be updated quickly and seamlessly.

## Where things stand

| Part | Status |
| --- | --- |
| API models | Working: typed Pydantic models for ASSIST's published API schema, tested against real payloads |
| Web client | Working: pulls agreements from the ASSIST website, caches responses on disk, and validates them against the API models |
| Database | In progress: PostgreSQL schema that stores requirements as AND/OR trees, plus loaders |
| Progress reports | Not started: entering completed courses and seeing where you stand for each school |

## How it works

```
ASSIST website  ->  web client (cached)  ->  Pydantic models  ->  expression trees  ->  PostgreSQL
```

ASSIST publishes documentation for an API, but I never got access to it. So I modeled the documented API schema anyway, then adapted the data coming from the website's own endpoints to fit it. If API access ever comes through, switching over should mostly mean swapping out the source.

### Polymorphic data

A lot of ASSIST's JSON is polymorphic: one field can hold any of several kinds of objects, told apart by a `type` field, and they nest. Each kind gets its own model, and the models register themselves into discriminated unions, so Pydantic picks the right class while parsing.

### AND/OR requirements

The hardest part is the course requirements. A university course might be satisfied by `(FR 2 AND FR 1) OR (FR 2 AND FR 1H)` at a community college, and ASSIST describes that in two flattened layers: groups of courses joined by AND or OR, plus position ranges saying which groups are joined how.

The loader turns both layers into a proper tree, which is stored in Postgres as nodes with parent pointers:

```
(CS 36 AND CS 38) OR CS 40

expressions:         e1  OR   (root)
                     e2  AND  parent = e1
expression_courses:  e2 -> CS 36,  e2 -> CS 38,  e1 -> CS 40
```

From there, checking whether a set of completed courses satisfies a requirement is a recursive walk down the tree, which the schema includes as a SQL function (`expression_satisfied`).

## Setup

Requires Python 3.12 or newer.

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[web,database,dev]"
```

The database code reads its connection settings from a `.env` file: `PROJECT` (user), `PASSWORD`, `HOST`, `PORT`, and `DB`.

## Tests

```bash
python -m pytest
```

The tests run against real ASSIST payloads saved in `tests/fixtures/`, and check that each kind of object parses into its specific model rather than a base type.

## Layout

```
sources/api/    models for ASSIST's API schema
sources/web/    client for the ASSIST website
database/       PostgreSQL schema and loaders (in progress)
tests/          tests and saved ASSIST payloads
```

*Not affiliated with or endorsed by ASSIST.*