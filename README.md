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
├── bitwigMain      # TDBitwig メイン接続コンポーネント
├── bitwigTrack0–8  # トラックごとの状態管理（color, volume, mute 等）
├── container1/     # UI コンテナ（トラック × 8）
├── oscin2          # OSC 受信（TouchOSC から）
├── oscout1         # OSC 送信（localhost）
└── oscout2         # OSC 送信（リモートデバイス）
```

## 使い方

1. `TouchOscToBitwig.toe` を TouchDesigner で開く
2. `bitwigMain` の接続パラメータを環境に合わせて調整
3. `oscout2` の送信先 IP アドレスを TouchOSC デバイスの IP に変更
4. TouchOSC のレイアウトを上記 OSC フォーマットに合わせて設定

## ライセンス

MIT
