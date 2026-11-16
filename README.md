# Kermodes examples

Projects built on [Kermodes](https://github.com/reecetec/kermodes), each as a team would keep its
own: Python resources, apps with their pages, and the published `@kermodes/*` packages they pin.

| Project | What it is |
|---|---|
| [`ticker`](ticker) | A random-walk ticker feeding `md.ticks`, and `market`: a dashboard of the board, a tape, movers, and live charts |

Run one locally, with Kermodes installed (`pip install kermodes`, or a Kermodes checkout):

```sh
kermodes dev --project ticker
```

It prints the web UI's address; an app is at `/apps/<project>/<app>/`
(`http://127.0.0.1:8730/apps/ticker/market/`). Edits to an app's page reload it; edits to its
Python roll its process.

In a cluster, the controller syncs a project from git and runs its resources (the chart's
`control.projects`, with `path: ticker`). Only commits whose checks pass deploy: CI runs each
app's typecheck and tests against the packages it pins, and Ruff over the Python.
