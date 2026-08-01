---
title: "Git (LFS): what is locking support? And should I enable it?"
source: "https://stackoverflow.com/questions/42597408/git-lfs-what-is-locking-support-and-should-i-enable-it"
author:
  - "[[Mike Williamson]]"
  - "[[huw]]"
  - "[[kennytm]]"
  - "[[Peter Krauss]]"
  - "[[Gandalf Saxe]]"
  - "[[Sorin Postelnicu]]"
  - "[[Bob Kerns]]"
published: 2017-03-04
created: 2026-07-31
description: "\"New\" Git Comment:Just today I ran across the following comment from Git for the first time (at least the first time I saw it):Mikes-Mac$ git pushLocking support detected on remote \"origin\"."
---
This question shows research effort; it is useful and clear

149

This question does not show any research effort; it is unclear or not useful

Save this question.

Show activity on this post.

## "New" Git Comment:

Just today I ran across the following comment from Git for the first time (at least the first time I saw it):

```
Mikes-Mac$ git push
Locking support detected on remote "origin". Consider enabling it with:
  $ git config 'lfs.https://github.com/<my_repo>.git/info/lfs.locksverify' true
Everything up-to-date
Mikes-Mac$
```

What is this `Locking support`? Is this some sort of [mutex locking](https://en.wikipedia.org/wiki/Mutual_exclusion) for the LFS (large file storage)? If so, isn't it absolutely essential to get anything on git to work? (Minimally, how else could the "ordering" of the log history be established? Worse case, couldn't I have a binary file corrupted by simultaneous writes?)

## My Actions

I didn't do anything differently to this repository recently, nor have I done anything differently with this repository compared to any others that I've established with LFS.

I'm therefore assuming this is a new comment being provided to "the world" to let us know of new features.

## No Obvious Documentation

However, neither a Google search nor a *quick* search through their documentation led me to anything to explain this. So, I'm left wondering:

- What is this locking?
	- Is it mutex? If so, how could my repo even function without it?
		- Is this limited to just LFS? How is it different from normal git file locking?
- What are the pros and cons of adding locking support for LFS?

[edited Jul 24, 2019 at 12:50](https://stackoverflow.com/posts/42597408/revisions "show all edits to this post")

[Kevin Chen](https://stackoverflow.com/users/1489823/kevin-chen)

1,026 9 silver badges24 bronze badges

asked Mar 4, 2017 at 14:56

[Mike Williamson](https://stackoverflow.com/users/534238/mike-williamson)

4,190 16 gold badges83 silver badges126 bronze badges

1

This answer is useful

140

This answer is not useful

Save this answer.

Loading when this answer was accepted…

Show activity on this post.

Locking support of Git LFS is documented here [https://github.com/git-lfs/git-lfs/wiki/File-Locking](https://github.com/git-lfs/git-lfs/wiki/File-Locking).

> Git LFS v2.0.0 includes an early release of File Locking. File Locking lets developers lock files they are updating to prevent other users from updating them at the same time. Concurrent edits in Git repositories will lead to merge conflicts, which are very difficult to resolve in large binary files.

> Once file patterns in `.gitattributes` are lockable, Git LFS will make them readonly on the local file system automatically. This prevents users from accidentally editing a file without locking it first.

> Git LFS will verify that you're not modifying a file locked by another user when pushing. Since File Locking is an early release, and few LFS servers implement the API, Git LFS won't halt your push if it cannot verify locked files. You'll see a message like this:
> 
> ```
> $ git lfs push origin master --all
> Remote "origin" does not support the LFS locking API. Consider disabling it with:
>   $ git config 'lfs.http://git-server.com/user/test.locksverify' false
> Git LFS: (0 of 0 files, 7 skipped) 0 B / 0 B, 879.11 KB skipped
> ```
> ```
> $ git lfs push origin master --all
> Locking support detected on remote "origin". Consider enabling it with:
>   $ git config 'lfs.http://git-server.com/user/repo.locksverify' true
> Git LFS: (0 of 0 files, 7 skipped) 0 B / 0 B, 879.11 KB skipped
> ```

So in some sense you may consider it an advisory mutex, because:

- If you don't "lock" the file, you can't edit it
- Once you "lock" the file with `git lfs lock`, you can edit it, and the repository server will recognize that you are editing it
- The server will not accept commits from other people that change the files you have locked.

It is mainly added to help team managing large files to prevent merge conflicts.

[edited Feb 6, 2021 at 0:25](https://stackoverflow.com/posts/42597577/revisions "show all edits to this post")

[prolyx](https://stackoverflow.com/users/6472660/prolyx)

501 1 gold badge3 silver badges15 bronze badges

answered Mar 4, 2017 at 15:11

[kennytm](https://stackoverflow.com/users/224671/kennytm)

527k 111 gold badges1.1k silver badges1k bronze badges