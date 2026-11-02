# Image to Editable PPT

[English](#english) | [中文](#中文)

## English

An agent skill for reconstructing reference images, screenshots, posters, diagrams, and infographics as editable PowerPoint slides while preserving their composition and visual direction.

### What it does

- Rebuilds text, headings, badges, arrows, platforms, lines, and simple geometry as native PowerPoint objects.
- Keeps complex products, people, 3D renders, and detailed illustrations as separate image layers, with transparent backgrounds where practical.
- Preserves the reference aspect ratio and names meaningful objects for the Selection Pane.
- Requires inspection of both the authoring preview and the rendered final PPTX, plus overflow checks.
- Translates image text only when requested.

**Editability is a hybrid:** native text and geometry are editable internally; raster layers can be moved, resized, cropped, or replaced, but their internal parts are not vector-editable. Reconstruction may be approximate when fonts or source design files are unavailable.

### Requirements

- An agent environment that supports `SKILL.md` skills, image inspection, and running local scripts.
- A separate presentation/PPT authoring skill with its supported library, final-PPTX renderer, and overflow checker. This repository does **not** bundle that companion skill or a PowerPoint generation engine. If no suitable companion is available, the workflow must report the limitation.
- Python 3.10+ and Pillow for the optional region-extraction helper.

### Download and install

[Download ZIP](https://github.com/NoahYUYE/image-to-editable-ppt/archive/refs/heads/main.zip), extract it, and copy the repository folder to your agent's skills directory as `image-to-editable-ppt`.

Or clone directly to the usual Codex skills location (only if that destination does not already exist):

```bash
git clone https://github.com/NoahYUYE/image-to-editable-ppt.git ~/.codex/skills/image-to-editable-ppt
```

For Codex, a typical user skills location is:

```text
~/.codex/skills/image-to-editable-ppt/
```

The installed directory must directly contain `SKILL.md`, `agents/`, `references/`, and `scripts/`. Review the files before installation. If this skill is already installed, back it up before replacing it. Start a new agent session if needed for discovery.

Install the helper dependency in a virtual environment:

```bash
cd /path/to/image-to-editable-ppt
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Use

Attach a reference image and ask:

```text
Use $image-to-editable-ppt to reconstruct this image as an editable PowerPoint slide.
Preserve the layout and aspect ratio. Keep text and simple shapes editable, and
keep complex artwork as separate image layers.
```

By default, the skill produces one slide per image and delivers the final PPTX. It is an agent workflow, not a standalone image-to-PPT command or a guarantee of pixel-perfect output.

### Region-extraction helper

After inspecting the image, create a region specification:

```json
{
  "regions": [
    {"name": "product", "box": [20, 30, 220, 230], "mode": "near-white"},
    {"name": "logo", "box": [240, 20, 340, 100], "mode": "preserve"}
  ]
}
```

Coordinates are `[left, top, right, bottom]` in source pixels; right and bottom are exclusive. Region names may contain only letters, digits, hyphens, and underscores.

```bash
python scripts/extract_regions.py \
  --input reference.png \
  --regions regions.json \
  --out extracted-assets
```

Use `near-white` only for crops with a white or nearly white background. It applies a color-based transparency mask and can remove white details inside an object; it is not semantic segmentation. Use `preserve` when masking would damage the image. Fully transparent borders are trimmed by default; pass `--no-trim` to retain the crop dimensions. Inspect each result before placing it on a slide.

### Repository contents

| File | Purpose |
| --- | --- |
| `SKILL.md` | Agent instructions and reconstruction workflow |
| `agents/openai.yaml` | Display name and suggested invocation |
| `references/reconstruction-playbook.md` | Layer strategy, fidelity tradeoffs, region format, and QA checklist |
| `scripts/extract_regions.py` | Cropping and optional near-white transparency masking |
| `requirements.txt` | Python helper dependency |

## 中文

把图片、截图、海报、流程图或信息图重建成可编辑 PowerPoint 的 agent skill。

### 能力与边界

- 文字、标题、标签、箭头、平台、线条和简单几何图形尽量使用 PPT 原生对象重建。
- 产品照片、人物、3D 渲染和复杂插画保留为独立图片元素，适合时使用透明背景。
- 默认保留原图比例，每张参考图对应一页幻灯片，并为对象设置有意义的名称。
- 要求检查制作预览和最终 PPTX 渲染结果，并执行溢出检查。
- 仅在用户要求时翻译图中文字。

原生文字和形状可以编辑内部内容；图片元素可以独立移动、缩放、裁剪或替换，但不等于内部矢量可编辑。缺少原字体、矢量素材或分层设计文件时，重建效果可能存在差异。

### 安装

1. [下载 ZIP](https://github.com/NoahYUYE/image-to-editable-ppt/archive/refs/heads/main.zip) 并解压，也可以通过上方 `git clone` 命令安装到尚不存在的目标目录。
2. 将仓库文件夹复制到 agent 的 skills 目录，文件夹命名为 `image-to-editable-ppt`。Codex 的常见位置为 `~/.codex/skills/image-to-editable-ppt/`。
3. 确保该目录下直接包含 `SKILL.md`、`agents/`、`references/` 和 `scripts/`。安装前可先检查文件；已有同名 skill 时先备份，再替换。
4. 如需使用裁图脚本，按上方命令创建 Python 虚拟环境并安装 `requirements.txt`。
5. 如未识别新技能，开启新的 agent 会话后再使用。

**还需要配套 PPT 技能**：运行环境必须具备支持的 PPT 制作库、最终文件渲染工具和溢出检查能力。本仓库不包含该配套技能，也不是独立的自动转换程序；缺少配套能力时应明确报告限制。

### 使用示例

上传参考图片后输入：

```text
使用 $image-to-editable-ppt，把这张图片重建成可编辑的 PPT。
保留当前布局、配色和原图比例；文字和简单图形使用原生可编辑对象，
复杂产品和插画拆成独立图片元素。检查最终 PPTX 渲染和溢出后，只交付 PPTX。
```

裁图脚本的 `near-white` 模式只适合白色或近白色背景，可能影响物体内部的白色细节，不是智能抠图；有此风险时用 `preserve`。区域坐标和调用方法见上方英文示例及 [重建指南](references/reconstruction-playbook.md)。

## License / 许可证

[MIT License](LICENSE). You may download, use, modify, and redistribute this skill under the license terms. The license applies to this repository's files; it does not grant rights to third-party reference images, fonts, logos, presentation tools, or generated materials.

可按 MIT 许可证下载、使用、修改和再分发本仓库内容。第三方参考图、字体、标志、PPT 工具及生成材料的权利不因本仓库许可证而自动授予。
