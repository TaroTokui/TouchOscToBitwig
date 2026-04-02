# TouchOscToBitwig

A TouchDesigner project that bridges **TouchOSC** and **Bitwig Studio** via OSC. Receives track information (volume, mute, solo, arm, color, etc.) from Bitwig and controls it from a TouchOSC device.

TouchOSC と Bitwig Studio を OSC でつなぐ TouchDesigner プロジェクトです。Bitwig のトラック情報（ボリューム、ミュート、ソロ、アーム、カラーなど）を TouchDesigner で受け取り、TouchOSC デバイスから操作できるようにします。

---

## English

### Overview

```
TouchOSC (iOS/Android)
    ↕ OSC
TouchDesigner (this project)
    ↕ OSC (TDBitwig)
Bitwig Studio
```

### Requirements

- [TouchDesigner](https://derivative.ca/) 2023.12206 or later
- [Bitwig Studio](https://www.bitwig.com/)
- TouchOSC or any OSC-capable device

### OSC Ports

| Direction | Host | Port | Description |
|-----------|------|------|-------------|
| IN | localhost | 10001 | TouchOSC → TouchDesigner |
| OUT (local) | localhost | 10002 | TouchDesigner → TouchOSC (same PC) |
| OUT (remote) | your device IP | 10002 | TouchDesigner → TouchOSC (remote device) |
| Bitwig IN | 127.0.0.1 | 9099 | TDBitwig → TouchDesigner |
| Bitwig OUT | 127.0.0.1 | 8088 | TouchDesigner → Bitwig |

### OSC Message Format

Messages sent from TouchOSC to TouchDesigner:

```
/{track_index}/{param_name}  value
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `volume` | float (0.0–1.0) | Track volume |
| `mute` | bool | Mute |
| `solo` | bool | Solo |
| `arm` | bool | Record arm |
| `playState` | bool | Play state |
| `loopEnabled` | bool | Loop enabled |

### Setup

1. Open `TouchOscToBitwig.toe` in TouchDesigner
2. Adjust connection parameters in `bitwigMain`
3. Set the destination IP in `oscout2` to your TouchOSC device's IP
4. Configure your TouchOSC layout to match the OSC message format above

---

## 日本語

### 概要

```
TouchOSC (iOS/Android)
    ↕ OSC
TouchDesigner (このプロジェクト)
    ↕ OSC (TDBitwig)
Bitwig Studio
```

### 必要なもの

- [TouchDesigner](https://derivative.ca/) 2023.12206 以降
- [Bitwig Studio](https://www.bitwig.com/)
- TouchOSC または OSC 送信可能なデバイス

### OSC ポート設定

| 方向 | ホスト | ポート | 用途 |
|------|--------|--------|------|
| IN | localhost | 10001 | TouchOSC → TouchDesigner |
| OUT (localhost) | localhost | 10002 | 通信テスト用 |
| OUT (リモート) | デバイスの IP | 10002 | TouchDesigner → TouchOSC (別デバイス) |
| Bitwig IN | 127.0.0.1 | 9099 | TDBitwig → TouchDesigner |
| Bitwig OUT | 127.0.0.1 | 8088 | TouchDesigner → Bitwig |

### OSC メッセージフォーマット

TouchOSC から TouchDesigner へ送信するアドレス形式：

```
/{track_index}/{param_name}  value
```

| パラメータ名 | 値の型 | 説明 |
|-------------|--------|------|
| `volume` | float (0.0–1.0) | トラックボリューム |
| `mute` | bool | ミュート |
| `solo` | bool | ソロ |
| `arm` | bool | アーム（録音待機） |
| `playState` | bool | 再生状態 |
| `loopEnabled` | bool | ループ有効 |

### 使い方

1. `TouchOscToBitwig.toe` を TouchDesigner で開く
2. `bitwigMain` の接続パラメータを環境に合わせて調整
3. `oscout2` の送信先 IP アドレスを TouchOSC デバイスの IP に変更
4. TouchOSC のレイアウトを上記 OSC フォーマットに合わせて設定

---

## License

MIT
