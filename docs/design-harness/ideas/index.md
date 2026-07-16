# ideas — human-created, two states (live / archived)

## topic-design: content and style judgment for topics
- [X topic style: substance — share+@author or original reflection/insight](x-topic-style-ganhuo-at-creators.md) — two content types; entity extraction→@handle, insight extraction, value gate skips the ones with no substance
- [ordering for identifying who to @](at-ordering.md) — share-type in-session first, reflection-type searches X after the topic is set (decided)
- [hotspot and session have no necessary before/after relationship](topic-source-independence.md) — a topic can come from hotspot only / session only / overlap

## session-input: what to read, how much to read
- [read range: default last 24h, only supports Claude Code](session-read-range-timewindow.md) — script reads conversation and filters out tool results (saves tokens); AI adapts the script if CC's format changes

## external-signal: where hotspots come from
- [hotspots via external tools](hotspot-via-external-tools.md) — soft-enhance: still produces topics if not installed+prompt to install

## trigger: when to run
- [trigger timing: human manual trigger](trigger-manual.md) — no automatic trigger; deliberately the opposite of content-collector's proactive trigger

## post-confirm: after the human picks a topic
- [learn the tone from hot posts and comments after topic confirmation](tone-learning-after-confirm.md) — only for the confirmed topic; agent-reach/last30days, soft-enhance; outputs tone notes + exemplars, still no body writing — ⚠ pending: [voice-from-static-exemplars](voice-from-static-exemplars.md) contests the live-retrieval mechanism
- [voice from a maintained static exemplar file, not live retrieval](voice-from-static-exemplars.md) — ⚠ conflicts with tone-learning-after-confirm on mechanism (shared "after confirm" timing); awaiting human adjudication

## downstream-publish: after the body exists (out of this skill's scope)
- [auto-publish Markdown posts to X](auto-publish-markdown-to-x.md) — downstream extension of the chain; x-article-publisher-skill proves it works for X Articles; posts/threads + build-vs-adopt open
