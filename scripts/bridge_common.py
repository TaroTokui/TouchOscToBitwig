"""
bridge_common
=============

TouchOSC <-> TouchDesigner <-> Bitwig ブリッジの共通ロジック。

このファイルは TouchDesigner 内の Text DAT `bridgeCommon` に
Sync to File で読み込まれ、各コールバック DAT から

    common = mod('bridgeCommon')

として参照される。パラメータの対応表とヘルパーをここに一元化し、
oscin_ipad_callbacks / oscin_bitwig_callbacks / chopexec1 / chopexec2 は薄いディスパッチだけを持つ。

設計方針:
- TDBitwig パッケージのコード (BitwigTrackExt 等) は変更しない。
- 送信の実体は各トラック COMP が既に持つ拡張メソッド
  `onOutParValueChange` を再利用する。
- 関数は解決済みの Operator を受け取り、自身では op() を呼ばない
  (呼び出し側の文脈で解決させることで、ネットワーク移動に強くする)。
"""

# OSC パラメータ名 -> TD カスタムパラメータ名
# iPad (TouchOSC) から届く /{track}/{param} の param 部分をキーにする。
PARAM_TO_PAR = {
    'volume':      'Volume',
    'pan':         'Pan',
    'mute':        'Mute',
    'solo':        'Solo',
    'arm':         'Arm',
    'active':      'Active',
    'playState':   'Playstate',
    'loopEnabled': 'Loopenabled',
}


def _bitwig_ext(track_op):
    """トラック/ソング COMP から onOutParValueChange を持つ拡張を返す。

    Track は BitwigTrackExt、master (Song) は別名の拡張だが、
    送信メソッドは基底 (BitwigBaseExt) 由来で共通。拡張のクラス名に
    依存せず走査することで両方に対応する。
    """
    for ext in track_op.extensions:
        if hasattr(ext, 'onOutParValueChange'):
            return ext
    return None


def apply_incoming(track_op, param_name, value):
    """iPad から受信した 1 メッセージを TD パラメータへ反映し、Bitwig へ転送する。

    Args:
        track_op:   対象の bitwigTrack{N} COMP (呼び出し側で op() 解決済み)
        param_name: OSC パラメータ名 (例 'volume')
        value:      受信値
    """
    if track_op is None:
        return

    par_name = PARAM_TO_PAR.get(param_name)
    if par_name is None:
        # 未知のパラメータは無視 (protocol 外)
        return

    par = track_op.par[par_name]
    if par is None:
        return

    # 1) TD 側のパラメータを更新
    prev = par.eval()
    par.val = value

    # 2) 既存の送信経路を使って Bitwig へ転送
    #    (OutPar として登録済みのものだけを送る)
    ext = _bitwig_ext(track_op)
    if ext is not None and par.name in getattr(ext, 'OutParNames', ()):
        ext.onOutParValueChange(par, prev)


def send_param_out(osc_outs, address, value):
    """iPad フィードバック用に 1 パラメータを複数の OSC Out DAT へ送信する。

    Args:
        osc_outs: oscoutDAT のリスト (None は無視)
        address:  OSC アドレス (例 '/1/volume')
        value:    送信値
    """
    for out in osc_outs:
        if out is not None:
            out.sendOSC(address, [value])
