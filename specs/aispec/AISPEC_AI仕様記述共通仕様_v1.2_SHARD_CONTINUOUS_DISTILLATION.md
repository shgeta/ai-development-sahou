# AISPEC v1.2 SHARD — Continuous Conversation Distillation

- Updated: 2026-09-24
- Status: APPROVED
- Parent authority: `AISPEC_AI仕様記述共通仕様_v1.2.md`
- Semantic version: AISPEC v1.2
- Physical role: additional shard; this file does not create a separate specification version.
- GROUP: `AISPEC_CONTINUOUS_DISTILLATION`

## Purpose

AIとの会話・対話作業を一時的な会話ログだけに残さず、将来のchat / AI / sessionが再利用できる形へ継続的に蒸留する。

ここでいう蒸留は逐語ログ保存ではない。会話から、確定した仕様、採用した運用ルール、再利用価値のある検証済み事実、継続作業に必要な状態だけを抽出し、適切な永続authorityへ正規化する。

| RULE_ID | TITLE | TYPE | MEANING | SCOPE | CLOSURE | WHEN | UNLESS | TARGET | GROUP | ORDER | DEPENDS_ON | STATUS | NOTE |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|---|
| AISPEC.DISTILL.010 | Conversation is an input stream, not authority | RULE | chat / voice / interactive workは仕様候補やdecisionを生む入力streamとして扱い、長期authorityそのものにはしない | AISPEC継続作業 | stable information -> durable authority | always | なし | conversation-derived information | AISPEC_CONTINUOUS_DISTILLATION | 10 |  | APPROVED | raw transcriptを仕様として保存することを要求しない |
| AISPEC.DISTILL.020 | Proactive distillation | REQUIREMENT | AIは明示的な「記録して」「仕様へ書いて」という指示を待たず、会話中に安定したdecision / rule / reusable factが成立したら適切な永続記録へ反映する | AISPECを使用する継続project | recent interaction -> candidate -> existing authority comparison -> durable write | meaningful checkpoint or stable decision detected | user explicitly requests no persistence, or candidate is not stable | current specification / decision record / project state | AISPEC_CONTINUOUS_DISTILLATION | 20 | AISPEC.DISTILL.010 | APPROVED | routineなmachine-oriented note / shard / state更新を許可する |
| AISPEC.DISTILL.030 | Stability gate | REVIEW_GATE | brainstorming、未採用案、仮説、雑談、単なる質問、一時的進捗をcurrent specificationへ自動昇格させない | conversation distillation | candidate -> confirmed / evidence-backed / review-required | before durable semantic write | explicit adoption or sufficient evidence already establishes stability | candidate information | AISPEC_CONTINUOUS_DISTILLATION | 30 | AISPEC.DISTILL.020 | APPROVED | 不明ならREVIEW_REQUIREDまたはIssue/Current Stateへ置き、確定仕様にしない |
| AISPEC.DISTILL.040 | Destination routing | PROCESS | current semantic truthはAISPEC/current spec、decision reasonはIssue/DECISION_REF、一時状態はCurrent State、project固有観測はproject固有authorityへ振り分ける | durable write routing | candidate -> exactly appropriate authority class | candidate passed stability gate | destination is unknown | normalized durable record | AISPEC_CONTINUOUS_DISTILLATION | 40 | AISPEC.DISTILL.030 | APPROVED | 同じ内容を複数authorityへ無秩序に複製しない |
| AISPEC.DISTILL.050 | Machine notes are allowed | POLICY | 再開性・検索性・routing・validationのために必要なmachine-oriented note / manifest / shard / state recordは、人間向け文書化の明示依頼がなくても作成してよい | project operational metadata | note -> searchable/referenced durable record | note materially improves restartability or machine interpretation | it would become an untracked shadow authority or duplicate existing authority | machine-readable project records | AISPEC_CONTINUOUS_DISTILLATION | 50 | AISPEC.DISTILL.040 | APPROVED | machine noteはauthority種別と役割を明確にする |
| AISPEC.DISTILL.060 | Write using AISPEC physical strategy | PROCESS | 既存recordのUPDATE/DELETEは必要回数のPATCH、新規recordのまとまった追加はNEW SHARDを用い、routine full-file replacementを行わない | AISPEC durable writes | candidate write -> PATCH or NEW SHARD | durable AISPEC write required | semantic migration required | AISPEC physical shards | AISPEC_CONTINUOUS_DISTILLATION | 60 | AISPEC.DISTILL.040 | APPROVED | write methodの都合でsemantic versionを上げない |
| AISPEC.DISTILL.070 | Preserve retrieval closure | VALIDATION | 新しいmachine note / shard / ruleを追加した後、SEARCH + specification closureから必要recordへ到達でき、RULE_ID重複や孤立authorityがないことを確認する | post-write validation | seed -> search -> specification closure -> required set | durable write performed | なし | changed specification set | AISPEC_CONTINUOUS_DISTILLATION | 70 | AISPEC.DISTILL.060 | APPROVED | file名や物理順への依存で発見性を保証しない |
| AISPEC.DISTILL.080 | Checkpoint distillation pass | PROCESS | meaningful checkpoint、handoff、session終了前には直近の対話で新しく確定した事項がauthorityへ未反映でないか確認し、必要なものだけ同期する | ongoing project work | recent interaction -> unresolved durable candidates -> sync | checkpoint / handoff / end of work segment | no durable candidate exists | project authority set | AISPEC_CONTINUOUS_DISTILLATION | 80 | AISPEC.DISTILL.020,AISPEC.DISTILL.070 | APPROVED | 毎発言ごとの書込みは要求しない |
| AISPEC.DISTILL.090 | Common-spec public safety | SAFETY | common specificationへ会話から昇格する内容はproject固有identifierを除去して一般化し、実案件データを混入させない | common specification maintenance | project decision -> generalized rule | promoting a project-derived rule to common spec | source is intentionally public and provenance is explicit | common specification shards | AISPEC_CONTINUOUS_DISTILLATION | 90 | AISPEC.DISTILL.040 | APPROVED | project固有内容はproject側authorityへ残す |

## Operational interpretation

標準的な対話後処理は次とする。

```text
conversation / interactive work
  -> detect stable candidate
  -> compare with current authority
  -> classify destination
       semantic truth        -> AISPEC / current spec
       reason / decision     -> Issue / DECISION_REF
       temporary work state  -> Current State
       project observation   -> project-specific authority
  -> write by PATCH or NEW SHARD
  -> validate SEARCH + specification closure
```

AIは「ユーザーが明示的に記録を依頼しなかった」ことだけを理由に、確定した継続ルールを会話ログへ放置してはならない。

一方、会話を逐語的に永続化したり、未確定案を勝手にcurrent specificationへ昇格させたりしてはならない。