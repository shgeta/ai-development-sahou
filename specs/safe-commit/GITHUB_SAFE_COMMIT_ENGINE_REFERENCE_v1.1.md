# GitHub Safe Commit Engine Reference v1.1

## 目的

AI作業で大きい既存text fileをGitHub connectorへ丸ごと再送する時間・truncation・SHA不一致リスクを減らす。

基本形:

```text
parallel prepare
  -> verified patch bundle
  -> exact HEAD guard
  -> temporary-worktree verify
  -> remote long-running validation
  -> single commit
  -> push
```

## なぜcommitそのものを並列化しないか

fileごとのdiff/hash生成は独立しているため並列化できる。一方、branch refを動かすcommit transactionは競合を避けるため直列化する。したがって高速化対象はprepare/validationであり、ref updateではない。

## CLI

### 1. Prepare

```bash
python -m common_modules.safe_commit_engine prepare \
  --repo . \
  --bundle .safe-commit/bundle \
  --issue 123 \
  --max-workers 8
```

生成物:

```text
.safe-commit/bundle/
├── manifest.json
└── patches/
    ├── 0001-....patch
    └── 0002-....patch
```

manifestは少なくとも以下を保持する。
- expected HEAD
- branch
- issue
- allowed paths
- before SHA256
- after SHA256
- patch path
- prepare executor / process start method
- prepare worker count

### 2. Verify

```bash
python -m common_modules.safe_commit_engine verify \
  --repo . \
  --bundle .safe-commit/bundle
```

temporary detached git worktreeを使うため、target checkoutを変更せずにpatch適用後のhashまで検証する。path allowlistはNUL区切りのGit statusで判定し、空白を含むpathでもquote依存を避ける。rename/copyはv0.1ではfail closedする。

### 3. Apply

```bash
python -m common_modules.safe_commit_engine apply \
  --repo . \
  --bundle .safe-commit/bundle \
  --message 'fix: example (#123)' \
  --validate 'PYTHONPATH=. python -m pytest -q tests/test_target.py'
```

複数validationは `--validate` を繰り返すか、1行1commandの `--validation-file` を使う。 pytestをvalidationへ含める場合は、`GITHUB_AI作業運用共通仕様` のpytest規約に従い、project固有の `PYTHONPATH` をcommand内で必ず明示する。

`apply`はtarget checkoutへ直接patchしてから検証しない。temporary worktree内でpatch適用・hash/allowlist/diff check・validation・candidate commit作成まで完了し、全gate成功後にだけtarget checkoutをcandidate commitへfast-forwardする。validation失敗時のtarget checkoutはHEAD/working treeとも変更しない。

## GitHub Actions backend

`.github/workflows/safe-commit-engine.yml` を利用する。

推奨運用:
1. staging branchにbundleだけを置く。
2. `target_branch` と `expected_head` を指定してworkflowを起動する。
3. workflowはbundleを一時退避する。
4. target branchのremote HEADがexpected HEADと一致することを確認する。
5. exact HEADへ切り替える。
6. bundle verifyを実行する。
7. validation commandsをresult treeに対して実行する。
8. 1 commitだけ作る。
9. target branchへpushする。

`GITHUB_TOKEN`で作られたpushが別のpush workflowを再発火しないことがあるため、安全性を後続workflowの自動発火へ依存させない。canonical validationを必要とする場合、そのcommandをSafe Commit workflow内のvalidationへ含める。

## Prepare executor

`--executor auto|process|thread` を選べる。標準 `auto` は、import可能な通常CLI/スクリプト上のPOSIX環境で複数workerを使う場合にProcessPoolを選ぶ。`forkserver` が利用できる場合は明示的に使用し、multi-threaded parentからのraw `fork()`依存を避ける。

interactive/stdinのように子processが`__main__`を再importできない実行形態では、`auto` はThreadPoolへfail-safe fallbackする。明示的に `--executor process` を指定した場合は、曖昧にfallbackせず理由付きで停止する。

観測例（非規範、同一環境の8 large text files）:
- ThreadPool: 1 worker 約0.91s / 8 workers 約0.87s
- ProcessPool(forkserver): 1 worker相当 約0.87s / 4 workers 約0.39s / 8 workers 約0.29s

したがってpatch生成のCPU負荷が支配的なlarge textではProcessPoolを第一候補とする。実速度はrunner CPU/IO/file内容に依存する。

## 並列化の境界

並列化してよい:
- before/after read
- SHA256計算
- unified patch生成
- file単位のprepare
- 互いに独立したread-only analysis

直列化する:
- expected HEAD最終確認
- target checkoutへのpatch適用transaction
- git add
- git commit
- branch ref push/update

## Timeout方針

container/tool command内でthread/processを利用してprepareを高速化してよい。ただし親tool timeout後もdetached child processが確実に存続することを前提にしない。

長時間処理はremote runnerへ委譲し、bundleをcheckpointとして再実行可能にする。

## v0.1 limitation

- UTF-8 text fileのみ。
- binary / non-UTF8はfail closed。
- rename/copyの専用transaction表現は未実装。検出時はfail closed。
- remote backendはGitHub Actions template。各repoへ導入して使う。