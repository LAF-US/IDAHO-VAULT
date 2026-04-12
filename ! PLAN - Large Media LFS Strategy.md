# Resolve Obsidian Sync and Git LFS Limits for Massive Vault Media

You've accumulated over 100GB of large `.mxf` and `.mp4` video files directly at the root of `IDAHO-VAULT` (some exceeding 20GB each). 

This presents two major blocking issues:
1. **Obsidian Sync Constraints**: Obsidian Sync imposes per-file limits (typically hard rejected around 100MB-200MB or capped by total vault tier size).
2. **Git LFS Constraints**: While `.gitattributes` tracks files like `.mp4` via LFS, GitHub's free tier imposes a strict 1GB storage/bandwidth limit. Pushing a single 20GB file will immediately fail and block all `git push` operations.

To create an "LFS-like" solution specialized for a Markdown/Obsidian ecosystem, we need to decouple these massive binary assets from both Obsidian Sync and Git, while keeping them contextually accessible in your workspace.

## Proposed Solutions

### Option A: The "Media Stub" Pattern (Recommended for Sync Portability)
Instead of keeping the actual media file inside the vault, we treat the vault strictly as a knowledge graph.
- **Workflow**: Move all large media to a local external SSD or Google Drive folder (e.g., `G:\My Drive\IDAHO-MEDIA`).
- **LFS-Like Link**: For each video, we create a tiny Markdown "stub" file in the vault (e.g., `XD4_6602.md`). 
- **Structure**: The stub contains metadata tags, your notes on the video, and an external local file link (`[Play XD4_6602.mxf](file:///G:/My%20Drive/IDAHO-MEDIA/XD4_6602.MXF)`).
- **Pros**: Zero sync issues, tiny vault size, keeps your notes perfectly interwoven with the video identities.
- **Cons**: You cannot stream the video directly inside an Obsidian note embed; clicking the link opens it in your default media player.

### Option B: The "Symlinked & Ignored" Drive (Recommended for In-App Viewing)
If you *must* have the files accessible to Obsidian directly (e.g., to embed `<video>` or `![[Clip0001.mp4]]`), we create a "black hole" folder inside the vault.
- **Workflow**: 
  1. Move all massive files to Google Drive (which you have via Google Workspace).
  2. Create a junction/symlink in Windows from `C:\Users\loganf\Documents\IDAHO-VAULT\LargeMedia` pointing to the Google Drive folder.
  3. Add `LargeMedia/` to `.gitignore`.
  4. Add `LargeMedia/` to the **Obsidian Sync Excluded Folders** list in the Obsidian app settings.
- **Pros**: Obsidian can natively embed the videos, but Obsidian Sync and Git both completely ignore them. The heavy lifting of syncing 20GB files is offloaded entirely to Google Drive Desktop.
- **Cons**: Might significantly slow down Obsidian's local indexing performance on startup due to the sheer size of the files it scans in the local symlinked path. 

### Option C: Self-Hosted Git LFS with a Custom Remote
This is the literal "LFS" solution, but it only solves the Git side of the problem, not Obsidian Sync. 
- **Workflow**: Change your Git LFS backend to point to a custom server (like an S3 bucket, or a Google Drive remote integration like `git-annex` / `dvc`). 
- **Pros**: True version control for giant binary files.
- **Cons**: High technical overhead. Doesn't stop Obsidian Sync from trying to upload them unless you explicitly exclude `.mxf` and `.mp4` inside Obsidian Sync's settings.

## Decision Needed
Which option aligns best with your workflow? 

If you choose **Option A** or **Option B**, I can act immediately: I will construct the `.gitignore` rules, provide the exact commands to migrate your 100GB+ of files to a new directory, and (if applicable) help build the Markdown stub files.

## Next Steps upon Approval
1. Add `*.mxf` and the chosen media directory to `.gitignore` to unblock `git` operations.
2. (If doing Option A): Script the generation of stub `.md` files for all major video assets in the vault root.
3. Migrate the massive files out of the vault root to clear up Obsidian Sync bottlenecks.
4. Update standard Vault Conventions to reflect this new LFS-like media policy.
