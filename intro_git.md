# Short introduction to basic git commands

## General terms

Term | Description
--- | ---
`git` | Versioning system, mostly used on the command line
`command line` | Terminal window to run commands or applications like python or git
`GitHub` | The most frequent website that hosts git-repositories. Managed by Microsoft. Free alternative: GitLab
`repository` | Complex folder structure where data is stored via git
`clone` | Download a git-repository and store it on your computer
`commit` | Store changes made loaclly
`push` | Upload changes
`pull` | Update from server
`branch` | Working copy of repository
`pull request` | Request merge of branch to main branch
`merge` | combine changes from different branches

Generally, we run git from the command line instead of using graphical interfaces. The structure of a git command is generally `git %command% %argument%`, where `%command%` is replaced by pull/clone/push/commit etc. We will see examples later.

## The structure of a repository

In a first step, open your terminal (Windows: PowerShell), clone the repository that you want to work with, and switch into the folder.

```shell
git clone https://github.com/FredericBlum/workshop_template
cd workshop_template
```

In general, we work on so-called 'branches', with one branch being the `main` branch. This is where we store all reviewed changes. We avoid working on the main-branch directly, so that we can directly review all changes through Pull Requests. We can create a new branch with the following command:

```shell
git checkout -b new-working-branch
```

The `-b` flag tells git to create a new branch in case it does not yet exist. The following argument is the name of the branch that we want to work on.

## Making changes to a repository

We can verify all the changes in the repository through `git status`. This way, we get a list of all additions/delitions that we have made. In order to prepare any change for comitting, you should always check what changes you have made in order to avoid problems.

Once you have verified that you are happy with your changes, you have to `git add` them to the list of changes you want to commit. Running `git add .` adds all changes, but should be used carefully in complex repositories.

In the next step, you `commit` your changes:

```shell
git commit -m 'upload annotated data'
```

Within the quotation marks you set a descriptive commit message, so that other people can quickly grasp what kind of changes you have made.

As a last step, `git push` your changes to the server and open a Pull Request so that other people can review your changes.
