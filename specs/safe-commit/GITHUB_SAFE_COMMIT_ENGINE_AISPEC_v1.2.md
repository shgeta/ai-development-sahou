# GITHUB SAFE COMMIT ENGINE — AISPEC v1.2

- Updated: 2026-09-24
- Status: PROPOSED
- Scope: AI/人間によるGitHub repositoryへの安全な大規模text変更commit
- Relation: `AISPEC_AI仕様記述共通仕様_v1.2.md` / `GITHUB_AI作業運用共通仕様_v1.15.md` の実行系兄弟仕様

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | CLOSURE | WHEN | UNLESS | TARGET | GROUP | ORDER | DEPENDS_ON | STATUS | SOURCE | NOTE |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|
| GIT.SAFE.010 | Freeze target HEAD | REQUIREMENT | bundle作成時のtarget HEADを固定し、remote apply時に同一SHAであることを要求する | commit transaction | prepare HEAD -> remote target HEAD | always | なし | target branch | SAFE_COMMIT | 10 |  | APPROVED | v0.1 design decision | HEAD移動時はfail closed |
| GIT.SAFE.020 | Parallel file preparation | PROCESS | changed fileごとのbefore/after hash・patch生成を独立タスクとして並列処理する。通常CLIのPOSIXではCPU-bound diff生成をProcessPoolで並列化し、interactive/stdin等のprocess再import不可能環境ではauto時のみThreadPoolへfallbackする | prepare | all selected changed paths | changed path count >= 1 | binary/non-UTF8 | changed text files | SAFE_COMMIT | 20 | GIT.SAFE.010 | APPROVED | v0.1 implementation | commit/ref update自体は並列化しない。ProcessPoolはforkserver優先 |
| GIT.SAFE.025 | Process executor safety | SAFETY | ProcessPoolはimport可能な`__main__`を必要とし、forkserver利用可能時はそれを明示使用する。明示process指定で条件不成立ならsilent fallbackせず停止する | prepare executor selection | executor=process | executor=auto in interactive/stdin | prepare runtime | SAFE_COMMIT | 25 | GIT.SAFE.020 | APPROVED | v0.1 implementation | autoのみthread fallback可 |
| GIT.SAFE.030 | Verified bundle manifest | REQUIREMENT | bundleはexpected HEAD、allowlist、各fileのbefore/after SHA256、patch pathを保持する | prepare output | all selected paths | prepare success | なし | manifest.json | SAFE_COMMIT | 30 | GIT.SAFE.020 | APPROVED | v0.1 implementation | schema `GITHUB_SAFE_COMMIT_BUNDLE_v0.1` |
| GIT.SAFE.040 | Temporary worktree verification | GATE | patchをtemporary detached worktreeへ適用し、after hash・allowlist・diff checkを検証する | local/remote verify | every bundle patch | before mutation | verification failure | bundle | SAFE_COMMIT | 40 | GIT.SAFE.030 | APPROVED | v0.1 implementation | target checkoutを汚さずverifyする |
| GIT.SAFE.050 | Result hash authority | SAFETY | patch適用後file SHA256がmanifestのafter SHA256と一致しなければcommitしない | verify/apply | all bundle files | patch apply success | なし | changed files | SAFE_COMMIT | 50 | GIT.SAFE.040 | APPROVED | v0.1 implementation | connector truncation等を検出する |
| GIT.SAFE.060 | Changed-path allowlist | SAFETY | manifestにないpathが変更された場合commitしない | verify/apply | git status changed set | after patch apply | なし | repository worktree | SAFE_COMMIT | 60 | GIT.SAFE.040 | APPROVED | v0.1 implementation | accidental side effectを禁止 |
| GIT.SAFE.065 | Path parsing and rename safety | SAFETY | changed path集合はNUL区切りstatusで取得し、空白等のquote差を排除する。rename/copyはv0.1では解釈せずfail closedする | verify/apply | changed path allowlist | rename/copy status | なし | repository worktree | SAFE_COMMIT | 65 | GIT.SAFE.060 | APPROVED | v0.1 implementation | rename supportは将来scope |
| GIT.SAFE.070 | Remote long-run delegation | POLICY | local tool実行枠を超え得るvalidationはGitHub Actions等のremote runnerへ委譲する | execution | verify -> validation -> commit | long-running/CI suitable | remote unavailable | validation commands | SAFE_COMMIT | 70 | GIT.SAFE.040 | APPROVED | v0.1 design decision | detached child processによるtimeout回避をauthorityにしない |
| GIT.SAFE.080 | Validate before finalization | GATE | requested validation commandsをisolated candidate worktreeで実行し、全て成功するまでtarget checkout/refを動かさない | remote/local apply | all validation commands | commands supplied | command failure | candidate result tree | SAFE_COMMIT | 80 | GIT.SAFE.050,GIT.SAFE.060 | APPROVED | v0.1 implementation | validation failure時target checkoutは無変更 |
| GIT.SAFE.090 | Single commit transaction | REQUIREMENT | candidate commitはisolated worktreeで作り、全gate完了後にtargetをその1 commitへfast-forwardして直列確定する | finalization | verified candidate tree -> one commit -> target fast-forward | all gates pass | target HEAD/worktree changed | target branch | SAFE_COMMIT | 90 | GIT.SAFE.080 | APPROVED | v0.1 implementation | prepare並列・final ref movement直列 |
| GIT.SAFE.100 | Bot-push CI independence | POLICY | `GITHUB_TOKEN` pushで通常workflowが再発火しない場合でも、同一result treeのcanonical validationをcommit前に完了できるようにする | GitHub Actions backend | exact target tree + bundle result | bot token push | external CI required by policy | CI/validation | SAFE_COMMIT | 100 | GIT.SAFE.080 | APPROVED | v0.1 design decision | 必要ならGitHub App token等で通常CIを別途発火 |
| GIT.SAFE.110 | Binary fail closed in v0.1 | LIMITATION | v0.1 patch backendはUTF-8 textのみを対象としbinary/non-UTF8は処理しない | prepare | each selected file | binary or non-UTF8 | なし | changed file | SAFE_COMMIT | 110 |  | APPROVED | v0.1 implementation | binary backendは将来scope |

## Validation

AISPEC準拠確認:
- `RULE_ID / TITLE / TYPE / MEANING / SCOPE / TARGET` を全行で明示する。
- 順序依存は `ORDER / DEPENDS_ON` で表す。
- 安全停止条件を `WHEN / UNLESS / TYPE=SAFETY|GATE|LIMITATION` に明示する。
- 実装が本表と矛盾する場合、実装を勝手に正とせずIssueで差分を解決する。