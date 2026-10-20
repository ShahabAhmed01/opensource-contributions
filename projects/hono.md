# Project notes — honojs/hono

Last verified: 2026-10-20

## Facts

- Web framework built on Web Standards, built on the Fetch API. TypeScript,
  MIT. Ships the `hono` package plus standalone adapter packages
  (`@hono/aws-lambda`, `@hono/lambda-edge`, `@hono/vercel`,
  `@hono/netlify`, `@hono/cloudflare-pages`, `@hono/service-worker`).
  32,608 stars / 1,416 forks / 91 watchers (live 2026-10-20T16:44:34Z).
- Default branch `main`; tip `5ca49b0720755c585c9a9835f0a479ceea36fb52`
  (pushed 2026-10-17T13:08:26Z). Releases: `v5.0.0-rc.1` (2026-10-10),
  `v5.0.0-rc.0` (2026-10-08). v5 is in release candidate; `main` still
  carries `version: 4.13.13`.
- Toolchain: **pnpm 12.6.0** (`packageManager` in `package.json`), Node
  `>=16.9.0`, `vite-plus` (`vp`) as the test/lint/format/pack driver
  (`vp test --run`, `vp lint`, `vp fmt --check`, `vp pack`), vitest 5.0.1,
  TypeScript 6.0.3. `pnpm run test` = `tsc -p tsconfig.spec.json && vp test
  --run`.
- **HARD GATE — `pull_request_creation_policy: collaborators_only`.** The
  repository object exposes this field; it is `all` on the other projects in
  this tracker (`backlot`, `starlette`, `uvicorn`, `markitdown`,
  `isomorphic-git`, `odysseus`) and `collaborators_only` here. Every attempt to
  create a PR against this repo fails, including from an unrelated fork and
  from a same-repo branch:
  - `POST /repos/honojs/hono/pulls` → `404 Not Found` for every head
  - `gh pr create --repo honojs/hono` → GraphQL `FORBIDDEN`
    ("ShahabAhmed01 does not have the correct permissions to execute
    `CreatePullRequest`"), with and without `headRepositoryId`
  - the same request against `honojs/middleware` (same org, policy `all`)
    returns `422 Validation Failed`, so the token and the account are fine —
    the block is repository-scoped
- `docs/CONTRIBUTING.md` states the policy in words, under the heading
  **"Issues instead of Pull Requests"**: *"Pull requests are limited to
  maintainers. If you find a bug or want a change, please create an issue
  instead. A clear issue with a minimal reproduction helps us more than a
  pull request. If you have already fixed it in your fork, you can link the
  branch in the issue. A maintainer may open a pull request from it, and your
  commits keep your name."*
- The same file carries an **AI Usage Policy**: AI may be used to contribute,
  but *"it must never waste a maintainer's time or make their work
  unpleasant. To enforce this, and regardless of whether AI was actually
  used, a maintainer may close your issue without notice and block your
  account."* Recent merged PRs disclose AI assistance in an "## AI disclosure"
  section, so disclosure is the house norm.
- Issue intake: blank issues are enabled; `.github/ISSUE_TEMPLATE/config.yml`
  routes questions to `honojs` Discussions and Discord. No PR template beyond
  a four-box checklist (`.github/pull_request_template.md`: add tests, run
  tests, `pnpm run check:fix` to format and lint, add TSDoc/JSDoc).
- Acceptance record measured 2026-10-20: **97 non-member, non-owner merges
  since 2026-06-20** in the fetched window (92 `CONTRIBUTOR` + 5 `NONE`
  associations out of 208 merges), e.g. `#5405` (uniho, 2026-10-17),
  `#5423` (Yahiro025, 2026-10-16), `#5498` (NgoQuocViet2001, 2026-10-16),
  `#5436` (otnc, 2026-10-16), `#5451`/`#5450` (breken-ai, 2026-10-16),
  `#5314` (adityajha77, 2026-10-16), `#5243` (Kjubikstronk, 2026-10-09),
  `#5233` (bndnsmth, 2026-10-09), `#5488` (RubenPari, 2026-10-02). The
  maintainers merge outside fixes constantly — but through the issue channel,
  and the contributors carry collaborator access.
- Maintainer activity is high: `usualoma` and `yusukebe` merge and review
  daily (11 merges in the 2026-10-02 → 2026-10-17 window alone), and the
  repo's own issue tracker is a swarm of agent-filed bug reports carrying a
  `<!-- software-factory:… -->` marker. Several of those issues had
  announced fork fixes from other contributors before this run started
  (see the duplicate notes in `contributions/hono/issue-5569.md`).
- House vocabulary: `EventProcessor.createResult()` /
  `createResult()`, `defaultIsContentTypeBinary()`,
  `isContentEncodingBinary()`, `isContentTypeBinary()`, `isBase64Encoded`,
  `bodyEncoding`, `APIGatewayProxyResult`, `CloudFrontResult`. The adapter
  sources are duplicated on purpose — `src/adapter/aws-lambda/handler.ts`
  (shipped as `hono/aws-lambda`, deprecated) and
  `adapters/aws-lambda/src/handler.ts` (shipped as `@hono/aws-lambda`) are
  the same file apart from import paths and `@deprecated` JSDoc. Any adapter
  change has to be applied to all four copies (`src/adapter/*` and
  `adapters/*/src/*` for aws-lambda and lambda-edge).

## Development / validation commands

```bash
pnpm install --frozen-lockfile
pnpm run test          # tsc -p tsconfig.spec.json && vp test --run
pnpm run lint          # vp lint src runtime-tests build perf-measures benchmarks adapters
pnpm run format        # vp fmt --check "src/**/*.{js,ts,tsx}" …
pnpm run build         # rm -rf dist && vp pack && … && publint
pnpm -r --filter "./adapters/aws-lambda" --filter "./adapters/lambda-edge" run test
```

- The `build/declaration-emit.test.ts` and `build/jsx-types.test.ts` suites
  need `dist/`, so they **fail on a fresh checkout** until `pnpm run build`
  has run. That is an environment artefact, not a code failure: after
  building, the whole suite is green.
- The adapter packages resolve `hono` through the workspace
  (`devDependencies: { hono: "workspace:*" }`) and take `hono` as a
  **peer dependency** (`>=4.13.9 || ^5.0.0-0`). A new `hono/utils/*` export
  cannot be imported from an adapter without breaking that peer range, so an
  adapter fix has to stay self-contained inside the adapter package.

## Contribution route for an outside contributor

File or use an issue; **do not** open a pull request (the API refuses it).
If the fix already exists in a fork, link the branch in the issue and let a
maintainer open the PR from it — the commit keeps the contributor's name.
This is the route used for the first hono contribution in this tracker:
`contributions/hono/issue-5569.md`.
