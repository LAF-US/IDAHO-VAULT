---
date: 2026-08-11
doc_class: provenance
subject: "Vendored community-plugin executables — source, version, and integrity record"
authority: LOGAN (policy); session-generated (evidence)
---

# Vendored Plugin Provenance

Integrity record for the plugin executables restored by PR #956. Each file was
fetched from its plugin's official GitHub release at exactly the version pinned
by the plugin's tracked `manifest.json`, with the id→repository mapping resolved
through Obsidian's community-plugins registry
(`obsidianmd/obsidian-releases:community-plugins.json`). Fetched 2026-08-11 by
session `01Fipj4vEJ5ADPuunn9ed5Hd`.

Verify any file against this record:

    sha256sum .obsidian/plugins/<id>/main.js

Not vendored, and why:

- `roygbiv-day-accent` — locally authored; its `main.js` was already tracked.
- `nldates-obsidian` 0.6.2 — no release asset exists at the pinned tag; manual
  one-time reinstall via Settings → Community plugins on a fresh checkout.
- `mcp-tools`, `phone-to-roam-to-obsidian` — side-loaded, not in the community
  registry; vendoring them is a separate trust decision, held for Logan.

Proposed vault policy (Logan inscribes it wherever doctrine of this kind
belongs, if anywhere — no destination is presumed):
*Community-plugin executables are tracked, vendored verbatim from official
registry-resolved releases at manifest-pinned versions, with integrity recorded
in this file. Upstream bugs in vendored artifacts are reported upstream, never
patched locally.*

| plugin | source repo | version | release tag | file | bytes | sha256 |
| --- | --- | --- | --- | --- | ---: | --- |
| breadcrumbs | michaelpporter/breadcrumbs | 4.4.4 | 4.4.4 | main.js | 901461 | `da7c667edc5a6c5cdf7ca67a28d17c083d3ec9669e324a0dbc82cb34a042a06d` |
| breadcrumbs | michaelpporter/breadcrumbs | 4.4.4 | 4.4.4 | styles.css | 2639 | `ac888704c3beea819fa4a54615b48dde465d26bd91fce280cb237969b7959654` |
| calendar | liamcain/obsidian-calendar-plugin | 1.5.10 | 1.5.10 | main.js | 141498 | `7fb339e9cf9fdbe5a801fa2b8ab85b366b5b3777fbd193cbc8728bc27711d125` |
| dataview | blacksmithgu/obsidian-dataview | 0.5.68 | 0.5.68 | main.js | 2377639 | `794e9eaede73920bb8d54b0eda4f5de2182d698cc638774500f24f14bcd4da0b` |
| dataview | blacksmithgu/obsidian-dataview | 0.5.68 | 0.5.68 | styles.css | 2965 | `3306dd9032e00f989ba7233a37fd255bc4d3f4340cee661762e952f3f6aa1de9` |
| habit-calendar | hedonihilist/obsidian-habit-calendar | 1.2.0 | 1.2.0 | main.js | 15180 | `efa59ca200313d334a5639e8a9febd0ed28dcb23e45bfb2f33bfb273b070bab7` |
| habit-calendar | hedonihilist/obsidian-habit-calendar | 1.2.0 | 1.2.0 | styles.css | 1065 | `c98b059365964efff0110157f59539c20525a322a33e9e7d903ae186aced8fc6` |
| handwritten-notes | fbarrca/obsidian-handwritten-notes | 1.4.0 | 1.4.0 | main.js | 307388 | `ca267f18b2cc152740e560c3a1eeab64e3688567e2a6961515c02ac46b4353d3` |
| heatmap-calendar | richardsl/heatmap-calendar-obsidian | 0.7.1 | 0.7.1 | main.js | 15945 | `68763a711b23284ff1551bfe685837451a4059b74d39c7bd121659c9e6a259ba` |
| heatmap-calendar | richardsl/heatmap-calendar-obsidian | 0.7.1 | 0.7.1 | styles.css | 3415 | `5fbfab61956802286c4fc6504c796356087a8b14f2e3c9613fa8c036c83ed0bd` |
| home-tab | olrenso/obsidian-home-tab | 1.2.2 | 1.2.2 | main.js | 374793 | `231992ba669102b56b006553c4e08dd8d0049aaa5c1d4f6540c288c4a3a5e55b` |
| home-tab | olrenso/obsidian-home-tab | 1.2.2 | 1.2.2 | styles.css | 2481 | `8cdc2b47c959d51fdf08002b730927f6663db078c3205486675287fb8f1d963a` |
| letterboxd-rss-sync | fleker/letterboxd-for-obsidian | 1.3.0 | 1.3.0 | main.js | 45794 | `c6fa66b2422637c1241b7777ba01a7a2da46cf7c85ad024850d6cbe4353f79b9` |
| letterboxd-rss-sync | fleker/letterboxd-for-obsidian | 1.3.0 | 1.3.0 | styles.css | 1418 | `82f5e043f273bb2705b499358c868d0f9b2f1619b8be5b56d7ebc2e276eb675b` |
| map-of-content | robin-haupt-1/Obsidian-Map-of-Content | 1.4.0 | 1.4.0 | main.js | 226091 | `32757152704c1e9f4565f1712459758be24a1270f02084cb2b69fb85e8121299` |
| metadata-menu | mdelobelle/metadatamenu | 0.8.12 | 0.8.12 | main.js | 1003040 | `a4c37d9f3931a72a8115c34ca226121f8d6f3d1c1d1feaef1179f05113cf3c6d` |
| metadata-menu | mdelobelle/metadatamenu | 0.8.12 | 0.8.12 | styles.css | 82452 | `b08f764bb08ae8ea06c1def27f97a2da16b4cc1920bbb618aaae2dcc7cf4f3cf` |
| move-cursor-on-startup | treadder/move-cursor-on-startup | 1.0.0 | 1.0.0 | main.js | 3435 | `f9387d6264d6f4073719e3887af044e10203d9bfd69f5cedb9072bc0a39c8334` |
| moviegrabber | superschnizel/Obsidian-Moviegrabber | 1.1.23 | 1.1.23 | main.js | 88527 | `8aed71d001533948144d7cb8d241341bb6ba533c573838068266a6f66e25dc11` |
| moviegrabber | superschnizel/Obsidian-Moviegrabber | 1.1.23 | 1.1.23 | styles.css | 3135 | `7c73a08e2a23023c9f3cb0336a22828ff9625071b2711903c8a4ac2287169e95` |
| msg-handler | ozntel/obsidian-msg-handler | 0.0.6 | 0.0.6 | main.js | 1040788 | `d77817cd140d1451dea95d428a6c9fcb2bb1d39e0f3fcdc32fd73a96ce83bfa2` |
| nostr-writer | jamesmagoo/nostr-writer | 2.2.0 | 2.2.0 | main.js | 1463755 | `f81c7d8381f96043a871317fa11770b83c810c3e7df79abb25396abbfb5a4806` |
| nostr-writer | jamesmagoo/nostr-writer | 2.2.0 | 2.2.0 | styles.css | 4118 | `9df84843cf4f326d85269da8588efb5157cecd0211fbc320982faff5e04222b7` |
| notebook-navigator | johansan/notebook-navigator | 2.5.6 | 2.5.6 | main.js | 4606387 | `a962630c743c25e6795e458b3d16cde36ea32ca098ceb8d0a058f835c9fd6a40` |
| notebook-navigator | johansan/notebook-navigator | 2.5.6 | 2.5.6 | styles.css | 282226 | `d1a0a9dbfa8e13ed544c39b0d4c153addcc6ce997b34454c1f9a2b5e239c7e11` |
| obsidian-day-planner | ivan-lednev/obsidian-day-planner | 0.28.0 | 0.28.0 | main.js | 1529879 | `5648366c6fe2cc9b87a0e183e125e2ea659fedb6868333925f6bd5df87b0630b` |
| obsidian-day-planner | ivan-lednev/obsidian-day-planner | 0.28.0 | 0.28.0 | styles.css | 38402 | `dcd0aa818f32492054c8267a30d59bc4a57458410082215827275f225cfc5ae5` |
| obsidian-folder-index | turulix/obsidian-folder-index | 1.0.30 | 1.0.30 | main.js | 43283 | `fc8f918a0dff1f458c2b32fc5205a4b6a02a1456eb1f1db4d21212898c9ca3ff` |
| obsidian-folder-index | turulix/obsidian-folder-index | 1.0.30 | 1.0.30 | styles.css | 76 | `ca8110476ff04163e03b65cd3a2d5e887d005c512f9915cba91ba0392e608dfa` |
| obsidian-footnotes | michabrugger/obsidian-footnotes | 0.1.3 | 0.1.3 | main.js | 96689 | `fb39a9469ffaef01911fb4befff0cbaf9fbd61fc9ab629881417f91b1f505953` |
| obsidian-icon-folder | florianwoelki/obsidian-iconize | 2.14.7 | 2.14.7 | main.js | 1003719 | `b0e6dfaf820b12cd3570a80938f7bd19307b442426db78fe32a488fe1d7c7e66` |
| obsidian-icon-folder | florianwoelki/obsidian-iconize | 2.14.7 | 2.14.7 | styles.css | 2216 | `56ffeb8349f4af97dab8a14fcadcb0019d3b37b116d7a34aa21e958e98455a89` |
| obsidian-icon-shortcodes | aidenlx/obsidian-icon-shortcodes | 0.9.7 | 0.9.7 | main.js | 1635210 | `d816fddaa0079e8de87841f86e4fbab08948e7824851ffb7ed5f76921bb129ad` |
| obsidian-icon-shortcodes | aidenlx/obsidian-icon-shortcodes | 0.9.7 | 0.9.7 | styles.css | 19755 | `c43e5af88fe2c640a788631be6dd96008e409e0eace6c817ffba28c6ae96ae25` |
| obsidian-linter | platers/obsidian-linter | 1.31.2 | 1.31.2 | main.js | 898635 | `3117c05752606d5d26559e11fc0c2d8e12ef6f5a72f05c3649509191174b8750` |
| obsidian-local-rest-api | coddingtonbear/obsidian-local-rest-api | 3.5.0 | 3.5.0 | main.js | 2527134 | `189794b5461df4a35da5ab27c4f10d47e277da0a59ca1d9e0fd91513adadd61f` |
| obsidian-tasks-plugin | obsidian-tasks-group/obsidian-tasks | 7.23.1 | 7.23.1 | main.js | 830432 | `7c8df16eafe2317fa61d6dda247b4e8bc450f05de9a7cf215e955a03188f884f` |
| obsidian-tasks-plugin | obsidian-tasks-group/obsidian-tasks | 7.23.1 | 7.23.1 | styles.css | 27067 | `b4a955fce5f7cf953348e56a94e9aecaee37171bd983379aabbf40c8f58b2eae` |
| obsidian-tidy-footnotes | charliecm/obsidian-tidy-footnotes | 0.1.2 | 0.1.2 | main.js | 5435 | `d940a8aec3dabe11f7a62b7b9f813fa4d46f01d743d168d8a80529c62389d32d` |
| obsidian42-strange-new-worlds | tfthacker/obsidian42-strange-new-worlds | 2.3.7 | 2.3.7 | main.js | 102703 | `2347c6313449e30a591bed34082667a1bbc662a325b7752ffc74c3f20201f6af` |
| obsidian42-strange-new-worlds | tfthacker/obsidian42-strange-new-worlds | 2.3.7 | 2.3.7 | styles.css | 6543 | `00ad03e6b40954207c9e874994d63bf27881c762a69996e885bf8ca4de108c27` |
| omnisearch | scambier/obsidian-omnisearch | 1.28.2 | 1.28.2 | main.js | 616523 | `787e80d61a7f482ae4a69940c8e34f972f9eb264c5c69dd83c50ddde9458a958` |
| oz-image-plugin | ozntel/oz-image-in-editor-obsidian | 2.2.6 | 2.2.6 | main.js | 155627 | `1fa35510731a9fd5ba0d4ee49e26b1766f9d8baade98492061c6b74f6ca0cb31` |
| periodic-notes | liamcain/obsidian-periodic-notes | 0.0.17 | 0.0.17 | main.js | 180567 | `ccf1a18673693d1036fc7614c3af9d23e5edfe425d1053df81dddcc29b1f8b0e` |
| periodic-notes | liamcain/obsidian-periodic-notes | 0.0.17 | 0.0.17 | styles.css | 488 | `613f3985d4c84900ed2e25d8a46efb7b3ace6889fb71217055084084eb146238` |
| quickadd | chhoumann/quickadd | 2.12.0 | 2.12.0 | main.js | 4265284 | `e09403bd9e20fe97affd1d53225ba09fbeada7f5e024dde8b64c5890529bffbe` |
| quickadd | chhoumann/quickadd | 2.12.0 | 2.12.0 | styles.css | 10952 | `e820f28cbb62f604727a07a7dee614386e765ef3d98bc541ac863ce5961bcba2` |
| recent-files-obsidian | tgrosinger/recent-files-obsidian | 1.7.6 | 1.7.6 | main.js | 54495 | `542aa5f7f447b967c6f5df63a11e43edd96b892679356ec80ff4aa504836962b` |
| settings-search | javalent/settings-search | 1.3.10 | 1.3.10 | main.js | 18531 | `df7ee3df3fd6ed21495a8180abb560c687f0c9bd415df3a27a345ce64c029489` |
| settings-search | javalent/settings-search | 1.3.10 | 1.3.10 | styles.css | 589 | `026384fbd28cdc029c4a012a9d5407cc644974fd2fe2492bf4883ce48f318a85` |
| smart-connections-visualizer | mossy1022/Smart-Connections-Visualizer | 1.0.27 | 1.0.27 | main.js | 809377 | `625554f8eb75c029d9fbdeaa042bce865f1fe5c3988a32d336ba1029216228a6` |
| smart-connections | brianpetro/obsidian-smart-connections | 4.1.8 | 4.1.8 | main.js | 955939 | `91fee76be870926530e7136797e5aa3888c3e826cf7136e795d7f83e7cb6f420` |
| tag-wrangler | pjeby/tag-wrangler | 0.6.4 | 0.6.4 | main.js | 133503 | `94ad72ea45e60629d7a628686f8cf7956a7ad963f43d39f201ab8016d2ee64a2` |
| templater-obsidian | silentvoid13/Templater | 2.18.1 | 2.18.1 | main.js | 339546 | `390be01a6e5b78ffb21b79dce296564c126972c32a4ef94deff81fe2c43ec5c6` |
| time-ruler | j-palindrome/obsidian-time-ruler | 2.7.1 | 2.7.1 | main.js | 10153919 | `d8bbb918925e06f39edc4d55fc03871768820fe3c0d3515548341307c7587233` |
| time-ruler | j-palindrome/obsidian-time-ruler | 2.7.1 | 2.7.1 | styles.css | 71965 | `d916ac547015d3fcbebd18fb57afb9efd85ba8ca43155b33aa8a2c712632d329` |
| tipa-support | akdemirdeniz/obsidian-tipa | 1.0.1 | 1.0.1 | main.js | 11387 | `b40ae166fe4a85171de554b785da9f53a1e84bdfda3eb4e9298a12b74a552388` |
| tipa-support | akdemirdeniz/obsidian-tipa | 1.0.1 | 1.0.1 | styles.css | 2159 | `56c769f28599b6b1fc4943190df80ab88d84321ace5bd523e04e0915c3757938` |
| todoist-context-bridge | wenlzhang/obsidian-todoist-context-bridge | 1.1.1 | 1.1.1 | main.js | 818770 | `4f1d05c9a64770dbfa19e39a1ed4f68b581bd534e92d11478fc7dfe4624f4691` |
| todoist-context-bridge | wenlzhang/obsidian-todoist-context-bridge | 1.1.1 | 1.1.1 | styles.css | 163 | `dd4d54d00724d846faa99e129ffffa3d722009ac865c65fbcd11a43162e52da3` |
| translate | fevol/obsidian-translate | 1.4.9 | 1.4.9 | main.js | 1204521 | `668cb58fd66dbcd515066c9441b27900a41cd3e2bbd31436672bcf0cf97338a8` |
| translate | fevol/obsidian-translate | 1.4.9 | 1.4.9 | styles.css | 13599 | `8bd826709696e0efc160e663cbcdc27409c7c2f4d6c8564ab4d2971ce03b76f0` |
| wikipedia-search | strangegirlmurph/obsidian-wikipedia-helper | 2.7.0 | 2.7.0 | main.js | 111646 | `2a0507a586c26962e5306cb18ebc7068932f758462a5e9fb2a5f38a6eb5e3b8f` |
