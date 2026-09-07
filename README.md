# CrewAI Market Research & GTM Generator

Streamlit app that runs a hierarchical CrewAI multi-agent workflow to turn a single
research topic into a market research report, business analysis, and go-to-market
(GTM) strategy — grounded in live web search/scrape data and a custom MCP tool server.

## Architecture

Two processes, run separately, talk to each other over MCP (SSE):

```
┌─────────────────────────────┐        SSE (MCP)        ┌──────────────────────────────┐
│   Azure-test.py (Streamlit)  │ <──────────────────────>│   server.py (FastMCP server)  │
│                               │   http://127.0.0.1:8005 │                               │
│  - Chat UI, progress/status  │          /sse           │  - company_overview           │
│  - Builds CrewAI Crew        │                          │  - list_competitors           │
│  - Connects MCPServerAdapter │                          │  - product_portfolio          │
└──────────────┬────────────────┘                          │  - pricing_snapshot           │
               │                                            │  - recent_news_pulse          │
               │ LLM calls                                  │  (all backed by SerpAPI)      │
               ▼                                            └──────────────────────────────┘
     Anthropic API (Claude)
   via crewai.llm.LLM / LiteLLM
```

**Crew (hierarchical process, `Process.hierarchical`)** — defined in `Azure-test.py`:

| Agent | Role | Tools |
|---|---|---|
| Head Manager | Delegates work to the other three agents; also assembles the final synthesis report | none directly — delegation only |
| Researcher | Runs market research | SerpAPI search, web scraper, + all MCP tools |
| Business Analyst | Builds TAM/SAM/SOM sizing, competitive matrix, trends | SerpAPI search, web scraper |
| GTM Strategist | Builds ICP, positioning, messaging, channel plan, roadmap | SerpAPI search, web scraper |

Tasks run in order: `research_task → analysis_task → gtm_task → synthesis_task` (the
last is explicitly assigned to the Head Manager, who compiles everything into one
markdown report). `planning=True` is enabled, so CrewAI also runs a planning pass
before execution using the same Claude model.

**LLM provider**: all agents use `crewai.llm.LLM` pointed at
`anthropic/claude-sonnet-4-5` (Anthropic's Messages API, routed through LiteLLM).
`MODEL_PROVIDER` in `Azure-test.py` is a display-only label for the UI — actually
switching providers requires wiring up a different `LLM(...)` instance (an OpenAI
config block exists in the file, commented out, from an earlier iteration).

**Other files:**

- `main.py` — the default `uv init` entry point (`Hello from capstone!`). Not part of
  the running app; harmless placeholder.
- `pyproject.toml` / `uv.lock` — dependency manifest, managed by `uv`.
- `CREWAI_SETUP.md` — the original lab handout. It predates the Anthropic switch and
  still describes an OpenAI-only setup (different `.env` keys, no mention of
  `CLAUDE_API_KEY`); treat the **Setup** section below as the current instructions.

## Setup

### Prerequisites

- Python >= 3.13
- [`uv`](https://docs.astral.sh/uv/) package manager
- An Anthropic API key (Claude) and a SerpAPI key

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables

Create a `.env` file in the project root with the following keys (see the code for
where each is read — `Azure-test.py` and `server.py`):

```env
CLAUDE_API_KEY=<your-anthropic-api-key>
SERPAPI_API_KEY=<your-serpapi-api-key>
```

`.env` is already covered by `.gitignore` via the virtualenv rule pattern used in this
project — double check it's excluded before committing, and never paste real keys into
this README or any other tracked file.

### 3. Start the MCP server (terminal 1)

```bash
uv run server.py
```

Serves on `http://127.0.0.1:8005/sse`. Keep this terminal running — the Streamlit app
connects to it on every research run and falls back to base tools only (no MCP tools)
if the connection fails.

### 4. Start the Streamlit app (terminal 2)

```bash
uv run streamlit run Azure-test.py
```

Open `http://localhost:8501`, enter a research topic (e.g. "OpenAI competitors"), and
submit. A full run exercises planning + 4 agents + real web search/scrape calls, so
expect several minutes end to end.

## Test notes

There is no automated test suite in this repository (no `tests/` directory, no
pytest/unit tests configured) — verification so far has been manual, end-to-end
through the Streamlit UI with both processes running. Recommended manual checklist:

- [ ] MCP server starts cleanly and logs `Application startup complete.`
- [ ] Streamlit sidebar shows `SerpAPI: ✅` and `Scraping: ✅` under Tool Status
- [ ] Sidebar shows `🔗 MCP Connection: ✅ Connected (N tools)` after submitting a topic
- [ ] A full run completes and renders a markdown report with all four sections
      (executive summary, research findings, business analysis, GTM strategy)
- [ ] The success banner's latency metric (`crew.kickoff` is timed in-app via
      `time.time()`) reports a sane duration for the run

### Known issues found during manual testing (and their fixes)

| Issue | Root cause | Fix applied |
|---|---|---|
| `Error code: 400 … This model does not support assistant message prefill` | `claude-sonnet-4-6` and the whole 4.6+/5 Claude family reject requests where CrewAI's executor ends the conversation on an `assistant`-role message (prefill), which CrewAI's agentic loop relies on | Switched `CLAUDE_MODEL` to `anthropic/claude-sonnet-4-5` (Azure-test.py:25), the newest Claude model that still supports prefill |
| `TimeoutError: Task '...' execution timed out` from `agent/core.py:_execute_with_timeout` | In `Process.hierarchical`, the Head Manager wraps and waits on all delegated agent work, but its `max_execution_time` (600s) was the *smallest* budget in the crew — smaller than the Researcher's own (800s) — even though it's on the hook for the cumulative time of research + analysis + GTM delegation | Raised Head Manager's `max_execution_time` to 2500 and Researcher's to 1200 (Azure-test.py:146, :158), both under the Crew-level ceiling of 2400s... *(note: Head Manager's 2500 currently exceeds the Crew's own `max_execution_time=2400` — worth revisiting so the manager's budget doesn't outlive the crew's)* |

No regression run has been done yet to confirm the timeout fix resolves the failure
under real network conditions (SerpAPI + scraping latency is variable) — next manual
test should be a full run on a broad topic (e.g. "AI market analysis") to confirm no
timeout recurs.

## Comparison results

The model/provider choice went through three iterations before settling on the
current configuration. This is a qualitative summary from development history and
code comments, **not a benchmarked A/B test** — no controlled side-by-side runs with
matched topics/latency/output-quality scoring have been recorded yet.

| Provider / Model | Outcome | Notes |
|---|---|---|
| DeepSeek | ❌ Dropped | Caused a `400` error against this stack (per in-code comment); not investigated further |
| OpenAI (`gpt-4o-mini`) | ⚪ Working, but superseded | Original lab's default provider (see `CREWAI_SETUP.md`); code for it is still present but commented out in `Azure-test.py` |
| Anthropic Claude (`claude-sonnet-4-6`) | ❌ Dropped | Rejected by CrewAI's prefill-based agent loop (see Known Issues above) |
| Anthropic Claude (`claude-sonnet-4-5`) | ✅ Current | Compatible with CrewAI's prefill usage; in active use |

**Suggested next step**: since the app already measures and displays per-run latency
(`st.metric("Total Latency", ...)`), the most useful comparison data would be a small
table of actual runs — same topic, same tool availability, provider/model varied —
recording latency, whether all 4 tasks completed, and a subjective quality read of the
final report. That data doesn't exist yet in this repo; add it here once you've run a
few trials, e.g.:

| Run | Provider/Model | Topic | Latency (s) | Tasks completed | Notes |
|---|---|---|---|---|---|
| 1 | `claude-sonnet-4-5` | Business Aviation market analysis | 2029.49s| 4/4| |
| 2 | `gpt-4o-mini` | | | | |
