#!/usr/bin/env node
/**
 * Builds the dynamic part of the Grethel Labs profile from the organization's public repositories:
 *   - repos-{dark,light}.svg    repository table
 *   - lab-map-{dark,light}.svg  organization map, rendered by excaliplant
 *   - the block between <!-- repos:start --> and <!-- repos:end --> in profile/README.md
 *
 * Usage: node build_repos.mjs   (run from the repository root; GITHUB_TOKEN is optional)
 * Needs Node 18+ and network access (GitHub API, npm for excaliplant).
 *
 * A repository counts as an experiment when it has the topic "experiment", otherwise as a tool.
 */
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ORG = "grethel-labs";
const OUT = "profile/assets";
const README = "profile/README.md";
const RAW = `https://raw.githubusercontent.com/${ORG}/.github/main/${OUT}`;
const EXCLUDE = new Set([".github", "excaliplant-obsidian"]); // profile repo, release mirror

const THEMES = {
  dark: { canvas: "#111827", surface: "#192231", border: "#334155", text: "#F7F8FA", text2: "#B6C2D1", muted: "#8DA0B8",
          brand: "#2DB8A8", accent: "#5CE0CC", accentSubtle: "#143A3B", warn: "#FFCA16", warnSubtle: "#3A2E0F" },
  light: { canvas: "#F7F8FA", surface: "#FFFFFF", border: "#D4DAE2", text: "#111827", text2: "#526173", muted: "#526173",
           brand: "#2DB8A8", accent: "#0B6E63", accentSubtle: "#E5F6F2", warn: "#915500", warnSubtle: "#FFF3D6" },
};
const LANG_COLORS = { JavaScript: "#F1E05A", TypeScript: "#3178C6", Python: "#3572A5", Go: "#00ADD8", Rust: "#DEA584",
                      Shell: "#89E051", HTML: "#E34C26", CSS: "#9B6BDF", Java: "#B07219", "C#": "#178600" };
const SANS = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif";
const MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace";

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

function wrap(text, width, maxLines) {
  const lines = [];
  let line = "";
  for (const word of text.split(/\s+/).filter(Boolean)) {
    if (line && (line + " " + word).length > width) { lines.push(line); line = word; }
    else line = line ? line + " " + word : word;
  }
  if (line) lines.push(line);
  if (lines.length > maxLines) {
    lines.length = maxLines;
    lines[maxLines - 1] = lines[maxLines - 1].replace(/[\s.,;:]*$/, "").slice(0, width - 1) + "…";
  }
  return lines;
}

async function fetchRepos() {
  const headers = { Accept: "application/vnd.github+json" };
  if (process.env.GITHUB_TOKEN) headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  const res = await fetch(`https://api.github.com/orgs/${ORG}/repos?type=public&per_page=100`, { headers });
  if (!res.ok) throw new Error(`GitHub API ${res.status}: ${await res.text()}`);
  return (await res.json())
    .filter((r) => !r.fork && !r.archived && !r.private && !EXCLUDE.has(r.name))
    .map((r) => ({
      name: r.name, url: r.html_url, desc: r.description || "", lang: r.language || "", stars: r.stargazers_count,
      status: (r.topics || []).includes("experiment") ? "Experiment" : "Tool",
    }))
    .sort((a, b) => (a.status === b.status ? b.stars - a.stars || a.name.localeCompare(b.name) : a.status === "Tool" ? -1 : 1));
}

function tableSvg(repos, mode) {
  const t = THEMES[mode];
  const W = 1280, HEAD = 56, ROW = 92, PAD = 28;
  const H = HEAD + ROW * repos.length + 12;
  let body = `<rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="20" fill="${t.surface}" stroke="${t.border}"/>`;
  const col = { name: PAD, desc: 400, lang: 940, stars: 1110, status: 1170 };
  body += `<g font-size="13" font-weight="600" letter-spacing="1.2" fill="${t.muted}">`
    + `<text x="${col.name}" y="35">REPOSITORY</text><text x="${col.desc}" y="35">DESCRIPTION</text>`
    + `<text x="${col.lang}" y="35">LANGUAGE</text><text x="${col.stars}" y="35">STARS</text><text x="${col.status}" y="35">STATUS</text></g>`;
  repos.forEach((r, i) => {
    const y = HEAD + i * ROW, mid = y + ROW / 2;
    const exp = r.status === "Experiment";
    body += `<path d="M ${PAD} ${y} H ${W - PAD}" stroke="${t.border}"/>`;
    body += `<a href="${esc(r.url)}"><text class="mono" x="${col.name}" y="${mid + 6}" font-size="20" font-weight="700" fill="${t.text}">${esc(r.name)}</text></a>`;
    const lines = wrap(r.desc || "No description yet.", 62, 3);
    const top = mid - ((lines.length - 1) * 11) + 5;
    lines.forEach((l, j) => { body += `<text x="${col.desc}" y="${top + j * 22}" font-size="15" fill="${t.text2}">${esc(l)}</text>`; });
    if (r.lang) body += `<circle cx="${col.lang + 6}" cy="${mid}" r="6" fill="${LANG_COLORS[r.lang] || t.muted}"/><text x="${col.lang + 20}" y="${mid + 5}" font-size="15" fill="${t.text2}">${esc(r.lang)}</text>`;
    else body += `<text x="${col.lang}" y="${mid + 5}" font-size="15" fill="${t.muted}">–</text>`;
    body += `<text x="${col.stars}" y="${mid + 5}" font-size="15" fill="${t.text2}">★ ${r.stars}</text>`;
    const pw = exp ? 96 : 56;
    body += `<rect x="${col.status}" y="${mid - 14}" width="${pw}" height="28" rx="14" fill="${exp ? t.warnSubtle : t.accentSubtle}"/>`
      + `<text x="${col.status + pw / 2}" y="${mid + 5}" text-anchor="middle" font-size="13" font-weight="700" fill="${exp ? t.warn : t.accent}">${r.status}</text>`;
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-labelledby="t">
<title id="t">Grethel Labs repositories</title>
<style>text { font-family: ${SANS}; } .mono { font-family: ${MONO}; }</style>
${body}
</svg>
`;
}

function labMapSource(repos) {
  const branch = (status) => {
    const items = repos.filter((r) => r.status === status);
    return items.length ? `** ${status}s\n${items.map((r) => `*** ${r.name}`).join("\n")}\n` : "";
  };
  return `@startmindmap\n* Grethel Labs\n${branch("Tool")}${branch("Experiment")}@endmindmap\n`;
}

function renderLabMap(repos) {
  const dir = mkdtempSync(join(tmpdir(), "labmap-"));
  const src = join(dir, "lab-map.puml");
  writeFileSync(src, labMapSource(repos));
  for (const mode of Object.keys(THEMES)) {
    execFileSync("npx", ["--yes", "@grethel-labs/excaliplant", src, "-o", join(OUT, `lab-map-${mode}.svg`), "--theme", mode],
      { stdio: "inherit" });
  }
}

function updateReadme(repos) {
  const img = (name, alt, mode) => `<img src="${RAW}/${name}-${mode}.svg#gh-${mode}-mode-only" alt="${alt}" width="100%">`;
  const links = repos.map((r) => `[${r.name}](${r.url})`).join(" · ");
  const block = `<!-- repos:start -->
${img("repos", "Table of Grethel Labs repositories", "dark")}
${img("repos", "Table of Grethel Labs repositories", "light")}

${links}

<details>
<summary>Lab map</summary>

${img("lab-map", "Map of the Grethel Labs repositories, rendered with excaliplant", "dark")}
${img("lab-map", "Map of the Grethel Labs repositories, rendered with excaliplant", "light")}

<sub>Generated from the repository list and rendered with <a href="https://github.com/${ORG}/excaliplant">excaliplant</a>.</sub>

</details>
<!-- repos:end -->`;
  const md = readFileSync(README, "utf8");
  const next = md.replace(/<!-- repos:start -->[\s\S]*?<!-- repos:end -->/, () => block);
  if (next === md && !md.includes("<!-- repos:start -->")) throw new Error("repos markers missing in README");
  writeFileSync(README, next);
}

const repos = await fetchRepos();
for (const mode of Object.keys(THEMES)) writeFileSync(join(OUT, `repos-${mode}.svg`), tableSvg(repos, mode));
renderLabMap(repos);
updateReadme(repos);
console.log(`ok: ${repos.length} repositories`);
