# 合成ケーステスト・判定行列

Status: SYNTHETIC TEST ONLY. **自動検証**は `validate_examples.py` に含まれる項目のみ。その他は適用時のacceptance test候補。

| ケース | 期待動作 | 今回の自動検証 |
|---|---|---|
| 同一ID・同一内容の再書込 | 冪等として無害 | cross-reference/unique ID部分のみ |
| 同一ID・内容違い | integrity error / 適用禁止 | 未実装 |
| 同じscopeの方式A/B | `CONFLICT_DETECTED`、未解決を保持 | **済** |
| 同じscopeで承認済みresolution | 競合解決、両方の元判断を保持 | **済** |
| decision保存、正本未反映 | `DECIDED_NOT_APPLIED` / CURRENTではない | **済** |
| 正本反映成功、APPLIED追記失敗 | `UNKNOWN_APPLY` / 正本再照合 | 未実装 |
| APPLIEDでexact revision・evidence不足 | schema validationで拒否 | **済** |
| QAとproductionなどscopeが非重複 | 両立可能 | 未実装 |
| 全scopeルールとQA限定ルール | scope overlapとして評価 | 未実装 |
| 異なるauthorityに矛盾 | 勝手なlast-write-winsをしない | 未実装 |
| 3件以上の競合 | 参加決定をすべて検出・統合する | 未実装 |
| 決定訂正 | 元eventを保存、新eventで追記 | 未実装 |
| `DEFER`による競合保留 | blocked継続 | 未実装 |
| full replayとsnapshot+delta replay | 同一結果 | fixture整合性のみ |
| snapshot改ざん | digest不一致、破棄対象 | **済** |
| event順が異なる | 固定fixtureでprojectionが同じ | **済** |
| 追加eventで旧snapshotがstale | 差分を再生 | 未実装 |
| 失効した仕様とIssue判断 | project authorityに従って再検証 | 未実装 |
| write lock中のDecision | canonical storeへ無断書込みなし | 設計検証のみ |

## 合成サンプルの流れ

1. `evt-a01`: QAに方式Aを採用
2. `evt-a02`: 同じ条件で方式Bを採用
3. `evt-a03`: AとBの矛盾を記録
4. `evt-a04`: 適切なauthorityがAを選択し、A/Bを置き換える統合決定
5. `evt-a05`: 統合決定を正本へ反映し、revision/evidenceを記録

`evt-a04`までで止めれば決定済み・未反映。`evt-a03`までなら未解決競合。
スナップショットは`evt-a05`まで含み、未解決競合なし、現在有効な統合決定は`evt-a04`とする。

## 試験方法

```sh
python examples/validate_examples.py
```

`jsonschema` パッケージが必要。実行結果がPASSでも、汎用Conflict Resolverや実データwriterを実装済みとは意味しない。