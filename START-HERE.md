# Your advanced GitHub dashboard

This package provides two views of the same real activity data:

1. A dashboard overview and animated 3D contribution image inside your GitHub README.
2. A separate interactive dashboard with date filtering, contribution trends, a language breakdown, daily inspection, 3D rotation and CSV export.

The interactive dashboard is a custom Tableau-style design, not an embedded Tableau workbook. GitHub READMEs cannot run its interactive controls.

## Preview immediately

Open dashboard/index.html in a browser. It is self-contained and includes the real data snapshot, so you do not need a server or API key to view it. The generated images are already included for the README too.

## Install on GitHub

1. Extract the ZIP.
2. Open your profile repository: https://github.com/naveenvarma999/naveenvarma999.
3. Upload the contents of this package to the repository root, replacing README.md and matching older analytics files. Preserve the analytics, scripts, dashboard and .github folders. Do not upload an extra enclosing folder.
4. The workflow must be at .github/workflows/profile-analytics.yml. If your file picker hides .github, use Add file → Create new file on GitHub, enter that full filename, and paste the YAML contents.
5. Open repository Settings → Pages. Under Build and deployment, select GitHub Actions as the source. The supplied workflow publishes this dashboard as the Pages site for THIS repository; if that repository already hosts a different Pages site, use a separate repository instead and adjust the README dashboard URL.
6. Open Actions → Update GitHub Analytics → Run workflow. This refreshes data, commits the generated images and publishes the dashboard. The charts in the uploaded README are visible even before this first run.
7. After the deployment succeeds, use the live URL reported by GitHub Pages. With the default GitHub domain and this repository name, the expected URL is https://naveenvarma999.github.io/naveenvarma999/. The README is configured for that address. It is not live merely because the files were downloaded.

Expected files:

    README.md
    neural-banner.gif
    neural-banner.png
    analytics/
      activity.json
      repositories.json
      dashboard-overview.png
      contributions-3d.gif
      contributions-3d.png
      activity-summary.png
    dashboard/
      index.html
      template.html
    scripts/
      update_analytics.py
      build_dashboard.py
    .github/workflows/profile-analytics.yml

Replace the earlier profile-analytics.yml with this version. Do not create a second competing daily update workflow.

## Data definitions

- Contributions, active days and longest streak come from the public contribution calendar. The bundled snapshot covers 367 displayed days, 329 contributions and 118 active days.
- Public repositories: 29 at the repository snapshot. This is an account figure and does not change with contribution date filters.
- Language mix counts repositories by the primary language GitHub reports, including forks. Unclassified repositories remain visible. It is not a percentage of source-code bytes or language proficiency.
- Date filters change contribution KPIs, streak, trend, weekday totals, daily table and 3D landscape. The calendar shows the full period and dims days outside the filter.
- Bar heights represent actual counts. The optional moving camera and README highlight do not alter the data.
- The table lists the ten highest-count days in the selected range. CSV export includes every selected day, including zeros.
- Weekly trends use consecutive seven-day buckets within the selected period, not ISO calendar weeks.
- A streak is measured only within the selected range. Prior-period comparisons appear only if a complete previous range of equal length exists in the snapshot.

## Refresh behavior

Once installed, the workflow requests public data around 06:23 UTC daily, renders updated charts, commits the explicit generated files and deploys the dashboard. Scheduled runs may be delayed. Opening the website does not call GitHub APIs; it reads the embedded snapshot.

No personal access token is required. GitHub's built-in temporary token is used for API rate limits and committing generated files. The workflow declares contents:write, pages:write and id-token:write for those operations and Pages deployment. It does not read private repository contents. Hosting/account settings may prevent a workflow from committing or deploying; check the Actions result.

If GitHub blocks retrieval or changes its contribution-calendar HTML, refresh fails and the last committed snapshot remains available. The snapshot date makes stale data visible. Automation commits may themselves count toward GitHub activity.

## Verification

The overview image was visually inspected. The renderer ran successfully on the fetched public data. JavaScript initialization, real totals, preset and custom date ranges, invalid-range handling, calendar selection, motion controls, narrow-canvas calculations and CSV output passed automated checks using a DOM test double. A real browser session could not be connected, so browser visual/responsive verification and the first hosted GitHub Actions run remain unverified.

## Sources

- Public calendar: https://github.com/users/naveenvarma999/contributions
- Repository metadata: https://api.github.com/users/naveenvarma999/repos
- Pages workflow documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

Projects remain removed. The README retains Tableau, Docker, Django and your existing profile animation.
