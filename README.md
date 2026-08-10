# Railway Reliability Community Templates

Three unofficial, reliability-focused Railway templates built from pinned public
open-source releases:

- `nanobot/`: authenticated WebUI, generated secret, persistent state, health check.
- `redbot/`: persistent Red Discord Bot, non-interactive boot, supervised readiness.
- `laravel/`: Laravel web, queue worker, scheduler, MySQL, and Redis roles.

These community templates are not endorsed by HKUDS, Cog Creators, Laravel, or
Railway. Upstream names identify compatibility only.

## Provenance

| Cell | Release | Licence | Source |
| --- | --- | --- | --- |
| nanobot | `nanobot-ai 0.2.2` | MIT | https://github.com/HKUDS/nanobot/tree/v0.2.2 |
| Red Discord Bot | `3.5.24` | GPL-3.0-only | https://github.com/Cog-Creators/Red-DiscordBot/tree/3.5.24 |
| Laravel | skeleton `v13.8.0`, framework `13.23.0` | MIT | https://github.com/laravel/laravel/tree/v13.8.0 |

Package/archive checksums are pinned in each Dockerfile. Runtime credentials are
never included in this repository. Railway-generated secrets or deployer-supplied
credentials are used at deployment time.

## Local checks

The deterministic source checks live in the experiment repository. Container
builds are also exercised by `.github/workflows/container-smoke.yml` after each
public-source change.

## Licence

Original wrapper and deployment files are MIT licensed; see `LICENSE`. Downloaded
upstream packages keep their respective licences. The Red Discord Bot image
downloads GPL-3.0-only software from its corresponding public source release.

