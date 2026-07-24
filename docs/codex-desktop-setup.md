# Codex desktop app — auto-gtm install & setup

**This file is written for the Codex agent to read and act on.** A user may hand you only this file's URL and say "install it". Do every step below in order, top to bottom.

auto-gtm is a drafts-only GTM plugin: it drafts X/Reddit posts and replies, and must **never** post, comment, or perform any platform write. Its data layer shells out to `rdt` / `twitter` / `opencli`, which fail inside the desktop app's default `workspace-write` sandbox until the host is configured. Do not weaken the sandbox beyond the single `network_access` opt-in below.

## 0. Install the plugin

Run in the terminal:

```
codex plugin marketplace add tigerless-labs/auto-gtm
codex plugin add auto-gtm@tigerless-labs
```

Skills sync across the app, CLI, and IDE.

## 1. Enable outbound network (required)

The `workspace-write` sandbox blocks network by default, so every data fetch fails. Add to `~/.codex/config.toml`:

```toml
[sandbox_workspace_write]
network_access = true
```

Keep `workspace-write` and enable only the network. **Never** set `danger-full-access` — it also removes file protections. Ask the user to restart the app after editing `config.toml`.

## 2. Credential setup runs outside the sandbox

The sandbox blocks writes outside the project, so `rdt login` (it writes the reddit cookie under the user's home dir) fails from inside the app. **Do not run it yourself.** Tell the user to run these once in a plain system terminal:

```
pipx install 'git+https://github.com/public-clis/rdt-cli.git'
rdt login
rdt status
```

Each CLI's credential store is machine-global. At run time you can read it back — reads outside the workspace are allowed — so no further setup is needed for Reddit.

## 3. X higher-fidelity cookies (optional)

The app does not inherit shell env vars and strips `*TOKEN*` variables from subprocesses, so `export TWITTER_AUTH_TOKEN=…` never reaches `twitter`. Either add to `~/.codex/config.toml`:

```toml
[shell_environment_policy]
set = { TWITTER_AUTH_TOKEN = "…", TWITTER_CT0 = "…" }
```

or use OpenCLI's browser login (`opencli twitter …`), which needs no env vars. If neither is set, X still works keyless via the host's web search — lower fidelity, never blocked.

## Windows

The desktop sandbox has known bugs (`danger-full-access` can still run read-only; `elevated` can write outside the workspace). On Windows, tell the user to run the data CLIs from a system terminal or WSL rather than relying on the in-app sandbox.
