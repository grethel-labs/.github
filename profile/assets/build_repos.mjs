#!/usr/bin/env node
/**
 * Builds the dynamic part of the Grethel Labs profile from the organization's public repositories:
 *   - lab-map-{dark,light}.svg  organization map, rendered by excaliplant
 *   - the repository table and lab map block between <!-- repos:start --> and <!-- repos:end --> in profile/README.md
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

const THEMES = { dark: {}, light: {} }; // modes the lab map is rendered in

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
  const picture = (name, alt) => `<picture>
  <source media="(prefers-color-scheme: dark)" srcset="${RAW}/${name}-dark.svg">
  <img src="${RAW}/${name}-light.svg" alt="${alt}" width="100%">
</picture>`;
  const table = ["| Repository | Description | Status |", "|---|---|---|",
    ...repos.map((r) => `| [${r.name}](${r.url}) | ${r.desc.replace(/\|/g, "\\|")} | ${r.status} |`)].join("\n");
  const block = `<!-- repos:start -->
${table}

<details>
<summary>Lab map</summary>

${picture("lab-map", "Map of the Grethel Labs repositories, rendered with excaliplant")}

<sub>Generated from the repository list and rendered with <a href="https://github.com/${ORG}/excaliplant">excaliplant</a>.</sub>

</details>
<!-- repos:end -->`;
  const md = readFileSync(README, "utf8");
  const next = md.replace(/<!-- repos:start -->[\s\S]*?<!-- repos:end -->/, () => block);
  if (next === md && !md.includes("<!-- repos:start -->")) throw new Error("repos markers missing in README");
  writeFileSync(README, next);
}

const repos = await fetchRepos();
renderLabMap(repos);
updateReadme(repos);
console.log(`ok: ${repos.length} repositories`);
