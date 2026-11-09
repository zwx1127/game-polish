"""Static per-round reports. Recorded observations are not independent verification."""
from html import escape
import json
from pathlib import Path


def _text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def sections(manifest, observations=None):
    obs = {} if observations is None else observations
    if not isinstance(obs, dict):
        raise ValueError("observations.json must be an object")
    result = [
        ("本轮概况", [f"项目：{manifest['project']}", f"轮次：{manifest['id']} / {manifest['phase']}",
                      f"时间：{manifest['created_at']}", f"命令检查：{manifest['status']}",
                      f"观察记录结论（未经独立认证）：{obs.get('decision', 'pending')}",
                      "This report records command results, not proof of visual quality or gameplay improvement."]),
        ("目标与问题", [_text(obs.get('hypothesis') or '尚未填写问题假设')] + [_text(x) for x in manifest.get('goals', [])]),
    ]
    for title, key in [("具体修改", "changes"), ("前后视觉证据与观看位置", "evidence"),
                       ("观察结果", "observations"), ("回归与已知旧错", "regressions"),
                       ("限制与未验证项", "limitations"), ("回退方式", "rollback")]:
        values = obs.get(key, [])
        if isinstance(values, str):
            values = [values]
        if not isinstance(values, list):
            raise ValueError(f"observations.{key} must be a list or string")
        result.append((title, [_text(x) for x in values] or ["尚未记录；不能据此视为已验证或无问题。 "]))
    result += [("命令检查明细", [f"{name}: {c['status']} / exit={c.get('exit_code')} / log={c.get('log', 'not executed')} / stderr={c.get('stderr_log', 'not recorded')} / json_ok={c.get('json_ok', 'not requested')} / error={c.get('error', 'none recorded')}" for name, c in manifest['checks'].items()]),
               ("验收要求（需人工或 dot 核对）", manifest['review']['acceptance']),
               ("要求的证据", manifest['review']['required_evidence']),
               ("源版本与比较范围", [_text(manifest.get('source', {})), _text(manifest.get('source_after', {})),
                               _text(manifest.get('comparison', {})), f"基线：{manifest.get('baseline') or '未关联'}",
                               f"客观检查回归：{_text(manifest.get('regression', {}))}"]),
               ("周期与预算", [f"请求：{_text(manifest.get('cycle', {}))}", f"预算记录：{_text(manifest.get('budget', {}))}",
                             "CLI 不创建调度，不统计或强制模型 token 预算；需现有宿主提供。"])]
    return result


def render_report(manifest, observations=None):
    return '\n\n'.join('## ' + title + '\n\n' + '\n'.join('- ' + _text(v).replace('\n', '\n  ') for v in values)
                         for title, values in sections(manifest, observations)) + '\n'


def render_html(manifest, observations=None):
    body = ''.join('<section><h2>' + escape(title) + '</h2><ul>' +
                   ''.join('<li>' + escape(_text(v)) + '</li>' for v in values) + '</ul></section>'
                   for title, values in sections(manifest, observations))
    return ('<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Game Polish 本轮报告</title><style>body{max-width:900px;margin:36px auto;padding:0 20px;'
            'font:16px/1.7 system-ui,sans-serif;color:#24332e;background:#faf9f5}h1,h2{line-height:1.3}'
            'section{margin:28px 0}li{overflow-wrap:anywhere;white-space:pre-wrap}h2{font-size:21px}</style>'
            '<h1>Game Polish 本轮报告</h1>' + body + '</html>')


def write_reports(directory: Path, manifest):
    path = directory / 'observations.json'
    obs = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    if not isinstance(obs, dict):
        raise ValueError('observations.json must be an object')
    # Validate and render both before touching any previous report.
    markdown, html = render_report(manifest, obs), render_html(manifest, obs)
    for name in ('report.md', 'report.html'):
        if (directory / name).is_symlink():
            raise ValueError(f'{name} must not be a symlink')
    (directory / 'report.md').write_text(markdown, encoding='utf-8')
    (directory / 'report.html').write_text(html, encoding='utf-8')
