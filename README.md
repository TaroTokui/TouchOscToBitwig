# TouchOscToBitwig

TouchDesigner project that bridges **TouchOSC** and **Bitwig Studio** via OSC.  
Bitwig のトラック情報（ボリューム、ミュート、ソロ、アーム、カラーなど）を TouchDesigner で受け取り、TouchOSC デバイスから操作できるようにします。

## 概要

```
TouchOSC (iOS/Android)
    ↕ OSC
TouchDesigner (このプロジェクト)
    ↕ OSC (TDBitwig)
Bitwig Studio
```

## 必要なもの

- [TouchDesigner](https://derivative.ca/) 2023.12206 以降
- [Bitwig Studio](https://www.bitwig.com/)
- TouchOSC または OSC 送信可能なデバイス

## OSC ポート設定

| 方向 | ホスト | ポート | 用途 |
|------|--------|--------|------|
| IN | localhost | 10001 | TouchOSC → TouchDesigner |
| OUT (localhost) | localhost | 10002 | 通信テスト用 |
| OUT (リモート) | "your iPad address" | 10002 | TouchDesigner → TouchOSC (別デバイス) |
| Bitwig IN | 127.0.0.1 | 9099 | TDBitwig → TouchDesigner |
| Bitwig OUT | 127.0.0.1 | 8088 | TouchDesigner → Bitwig |

## OSC メッセージフォーマット

TouchOSC から TouchDesigner へ送信するアドレス形式：

```
/{track_index}/{param_name}  value
```

### 対応パラメータ

| パラメータ名 | 値の型 | 説明 |
|-------------|--------|------|
| `volume` | float (0.0–1.0) | トラックボリューム |
| `mute` | bool | ミュート |
| `solo` | bool | ソロ |
| `arm` | bool | アーム（録音待機） |
| `playState` | bool | 再生状態 |
| `loopEnabled` | bool | ループ有効 |

### 例

```
/1/volume  0.8    → bitwigTrack1 のボリュームを 0.8 に設定
/2/mute    1      → bitwigTrack2 をミュート
/3/arm     1      → bitwigTrack3 をアーム
```

## プロジェクト構成

```
project1/
├── bitwigMain              # TDBitwig メイン接続コンポーネント
├── bitwigTrack0–8          # トラックごとの状態管理（color, volume, mute 等）
├── trackControlUI/         # UI コンテナ（トラック × 8）
│   ├── container1–8/       # 各トラックの UI（Index パラメータでトラック番号を指定）
│   │   ├── button1         # 前のトラックを選択
│   │   ├── button2         # 次のトラックを選択
│   │   └── button3         # ON ボタン（bitwigTrack のカラーを反映）
├── selectTrack1–8          # bitwigTrack1–8 の CHOP チャンネル取得
├── selectTransport         # トランスポート情報（playState, loopEnabled）取得
├── mergeTrackParams        # 全トラックの CHOP チャンネルをマージ
├── params                  # マージされた全トラックパラメータ
├── fromUI                  # UI からの出力受け取り
├── selectUITrigger         # UI 操作トリガー信号の取得
├── uiTrigger               # UI 操作トリガー
├── sendOnChange            # params 変化時に OSC 送信
├── sendAllOnTrigger        # UI 操作時に params 全チャンネルを OSC 送信
├── oscFromTouchOSC         # OSC 受信（TouchOSC から）
├── oscToLocalhost          # OSC 送信（localhost、通信テスト用）
├── oscToDevice             # OSC 送信（リモートの TouchOSC デバイス）
├── oscInCallbacks          # OSC 受信コールバック
└── bitwigSongCallbacks     # ソングレベルのコールバック
```

## 使い方

1. `TouchOscToBitwig.toe` を TouchDesigner で開く
2. `bitwigMain` の接続パラメータを環境に合わせて調整
3. `oscout2` の送信先 IP アドレスを TouchOSC デバイスの IP に変更
4. TouchOSC のレイアウトを上記 OSC フォーマットに合わせて設定

## ライセンス

MIT
