***

# Onboarding.

First download the [GitHub Desktop GUI client](https://desktop.github.com/download/).
Go through the installation process and create your GitHub account (if needed) and sign into the GUI with it.

<p align="center"><kbd><img src="./misc/GUI_Lets_Get_Started.jpg" width="80%"></kbd></p>

Next,
clone the RSXVT2026 project using the [GitHub URL](https://github.com/RockSat-X/RSXVT2026/).

<p align="center"><kbd><img src="./misc/GUI_Cloning_Repo.jpg" width="80%"></kbd></p>

"Clone" is just Git-jargon for downloading a repository.
After Git is done downloading,
you should be greeted with the following page:

<p align="center"><kbd><img src="./misc/GUI_Fresh_Clone.jpg" width="80%"></kbd></p>

For your onboarding,
create a text file of the form `{yourname}.md` in the `people` folder that's at the root of the project.
Go ahead and introduce yourself here to your fellow engineers.
Examples of things you can tell about yourself:

- Name (and if it's typical that people mispronunce your name, help them out here).
- Pets.
- Spice tolerance.
- Blood type.
- Siblings.
- Etc.

When doing this,
the GUI will detect that a new file was created.
After you're done writing,
go ahead and describe what you've done in the summary box.
You can optionally go into more details with the description box.
Once you feel ready,
you can press the big blue "commit" button.

<p align="center"><kbd><img src="./misc/GUI_New_Introduction.jpg" width="80%"></kbd></p>

> [!CAUTION]
> If you see a warning about not having write access,
> then this means you are not currently added as a collaborator of the RSX2026 repository.
> Contact a team lead to have you be added.
> <p align="center"><kbd><img src="./misc/GUI_No_Write_Access.jpg" width="80%"></kbd></p>

A "commit" is another bit of Git-jargon for a checkpoint in your work.
Everything is still locally stored on your machine,
however,
so no one can see the new file you've created yet.
To upload it to GitHub for others to have access,
we "push" the commits.

<p align="center"><kbd><img src="./misc/GUI_Commiting_Directly_On_Main.jpg" width="80%"></kbd></p>

However,
if you try to do so,
you'll get an error message about how "changes must be made through a pull request".

<p align="center"><kbd><img src="./misc/GUI_Need_To_Do_PR.jpg" width="80%"></kbd></p>

This is intentional.
The default branch of the repository,
called `main`,
is protected with the rule that no one can modify it
willy-nilly without first creating a "pull request";
what a pull request is will be explained later,
but for now,
know that it is just a barrier for quality control.

What we should be doing instead is not make commits on the `main` branch which has this rule,
so we first undo our commit (this will not delete your work).

<p align="center"><kbd><img src="./misc/GUI_Undoing_Commit.jpg" width="80%"></kbd></p>

Then make a new branch.

<p align="center"><kbd><img src="./misc/GUI_Creating_New_Branch.jpg" width="80%"></kbd></p>

Give this branch a name;
what it is doesn't really matter just as long it's unique (e.g. `{yourname}-main`).

<p align="center"><kbd><img src="./misc/GUI_Naming_New_Branch.jpg" width="80%"></kbd></p>

Select "Bring my changes to `{yournewbranch}`".

<p align="center"><kbd><img src="./misc/GUI_How_New_Branch_Is_Used.jpg" width="80%"></kbd></p>

You can now redo the commit and this time it'll be on the new branch.

<p align="center"><kbd><img src="./misc/GUI_On_New_Branch.jpg" width="80%"></kbd></p>

Now you can finally upload your work online to GitHub;
since you made a new branch,
this is phrased as "publish branch",
but otherwise,
this is equivalent to the pushing operation we tried to do earlier.

<p align="center"><kbd><img src="./misc/GUI_Publishing_New_Branch.jpg" width="80%"></kbd></p>

This time,
we shouldn't be getting any error about pull requests being required,
since the newly created branch you made wouldn't have the rule that `main` does.

You can see on GitHub
(and so do other people)
the introduction file you made.

<p align="center"><kbd><img src="./misc/GitHub_Introduction_On_New_Branch.jpg" width="80%"></kbd></p>

But remember,
this file is only on the branch you made but not on the default `main` branch (yet).

<p align="center"><kbd><img src="./misc/GitHub_No_Introduction_On_Main.jpg" width="80%"></kbd></p>

To get it be on the `main` branch,
we perform a pull request.
There are several ways to do this;
one is to go to the "Pull requests" page of the RSX2026 repository.

<p align="center"><kbd><img src="./misc/GitHub_PR_Page.jpg" width="80%"></kbd></p>

When making a new pull request,
the difference between `main` and `{yournewbranch}` will be summarized with the commits you've made.

<p align="center"><kbd><img src="./misc/GitHub_Creating_PR.jpg" width="80%"></kbd></p>

Once you look over the changes and it all seems like what it should be,
go ahead and give your pull request a title and, if needed, a detailed description.

<p align="center"><kbd><img src="./misc/GitHub_Describing_PR.jpg" width="80%"></kbd></p>

Once you published your pull request,
a thread is created where anyone can comment on it to create a discussion.
Additional things to be done for the pull request to help better categorize it,
like labels (e.g. "bug", "documentation", etc.) and assignees.

<p align="center"><kbd><img src="./misc/GitHub_Published_New_PR.jpg" width="80%"></kbd></p>

The one you'd care most about are the reviewers you (or someone else) assign to the pull request.
They'll be the person that can offically approve your pull request
so your commits can be merged into the `main` branch of the RSX2026 repository.
The reviewers will typically be your team lead,
but need not be;
any of your fellow engineers can approve your pull request.

> [!CAUTION]
> That being said,
> you can also always sidestep the whole pull request procedure and merge directly into `main`. 
>
> <p align="center"><kbd><img src="./misc/GitHub_PR_Bypass.jpg" width="80%"></kbd></p>
>
> _**Do not do this unless you know what you are doing.**_
>
> Remember,
> the whole point of having a rule to enforce pull requests on the `main` branch
> is so your team leads can be kept-up-to-date with what has been done so far
> and ensure quality control.
> You don't want to be dealing with people's disorganized mess,
> do you?

Your reviewers might provide feedback
(e.g. "The code doesn't seem to execute at the right timer event...",
"Can you document somewhere the manufacturer number on the electronics box?").
If all goes well,
your reviewers will approve your commits and have them merged into `main`.

<p align="center"><kbd><img src="./misc/GitHub_PR_Merged.jpg" width="80%"></kbd></p>

The new branch you created can also be deleted if its whole purpose was for the work you just did,
but you really don't need to do this.

Your introduction file can be found in its expected location on the `main` branch now.

<p align="center"><kbd><img src="./misc/GitHub_Introduction_On_Main_Branch.jpg" width="80%"></kbd></p>

# Creating tickets.

If you have questions about the project or things you'd like to see improved upon,
it's best to create a ticket on GitHub.
This is done through the "Issues" tab on the page of the base repository.

<p align="center"><kbd><img src="./misc/GitHubIssueTab.jpg" width="80%"></kbd></p>

Give a summary of your ticket in the title field
and expand it further (if needed) in the description box.

<p align="center"><kbd><img src="./misc/GitHubExampleIssue.jpg" width="80%"></kbd></p>

A thread will be created where anyone can contribute to the discussion.

<p align="center"><kbd><img src="./misc/GitHubIssueAnswered.jpg" width="80%"></kbd></p>

When you feel like you got what you wanted,
you can close the ticket.

<p align="center"><kbd><img src="./misc/GitHubIssueBye.jpg" width="80%"></kbd></p>

Even if the ticket is closed,
the discussion thread can still be commented on or the ticket as a whole be reopened
(which is to make it more obvious that we still need to talk about the subject more).

<p align="center"><kbd><img src="./misc/GitHubIssueClosed.jpg" width="80%"></kbd></p>

You'll be able to see the tickets you've made and anyone else's for future prosperity 
on the issue page of the base repository.

<p align="center"><kbd><img src="./misc/GitHubIssueList.jpg" width="80%"></kbd></p>

That's pretty the gist of using issue tickets on GitHub.

> [!TIP]
> Discord is best reserved for virtual meetings or miscellaneous conversations.
> If you want the quickest response time,
> use Discord,
> but for the sake of bookkeeping,
> create a ticket on GitHub whenever possible.
> Over time,
> the issue tab will serve as a great reference to look back upon for your fellow engineers.

> [!IMPORTANT]
> GitHub Issues can be assigned to specific people and be labled
> (e.g. "bug", "help wanted", "question", etc.)
> as a way to categorize multiple tickets.
>
> <p align="center"><kbd><img src="./misc/GitHubIssueCategorizingAccess.jpg" width="30%"></kbd></p>
>
> However due to GitHub's implementation quirks,
> you will not be able to set the assignees or labels for any ticket you create
> unless you have write permissions to the base repository
> (which only your team leads will have).
> What you will see instead are some unconfigurable settings:
>
> <p align="center"><kbd><img src="./misc/GitHubIssueCategorizingNoAccess.jpg" width="30%"></kbd></p>
>
> This is just an unfortunate "issue" of the GitHub Issue ticketing system.
> Your team leads will do their best to organize and address every ticket.

***

# What's Git?

Git is a version control program that keeps track of a project's files throughout its development.
It helps keep track of what files are in the project,
what changes were made to files,
who did those changes,
when they did it,
why they did it,
and so on.

# But why use version control?

Because the old way of dumping files onto Google Drive is unmanagable.
Google Drive is not designed for large, complicated projects where there can be a dozen people making all sorts of changes here and there.
It's good for storing things like presentation slides, pictures, or whatever,
but not critical things like code or CAD files.

# How can I start doing version control?

Start off by downloading the [GitHub Desktop GUI](https://desktop.github.com/download/) application.

Once you go through the installation process,
sign into your GitHub account (make one if you don't already have one).

Once you do that,
go ahead and "clone" the RockSat-X 2026 repository.
To do this,
just copy the URL of the repository `https://github.com/RockSat-X/RockSatX_2026` and pass it to the GUI program.

When you clone the repository,
you now have a local copy of the project on your machine.

Go ahead and create a text file in the folder `people` with the file name of something like `{firstname}{lastname}.md` using your text editor of choice
(e.g. Notepad, Visual Studio Code, Vim, etc.).
In this file,
go ahead give an introduction to who you are!
Do you have any pets?
Do you have an arch nemesis?
Do you faint at the sight of blood?

Once you're done,
save the file and go back to the GUI client.

To show you what it should look like,
I went ahead and created the text file `PhucDoan.md` where I introduced myself.
After I did that,
my GitHub GUI client looks something like this:

TODO

Git detects that I have created a new file that's currently not being tracked.
To start tracking the file,
I go ahead write a summary of what I did (the commit message) and press the big blue commit button.

Once I do that,
Git is now tracking my introduction file!
To see what that means,
let's say I continue to edit the text file even further,
adding some details and fixing typos.

Going back to the GUI client,
I can see the modifications that were made ("diff" is the jargon for this).

Once again,
I can summarize my changes and then press the big blue commit button.

But what does "commiting" actually mean?
You can think of a commit as essentially as a checkpoint on your work so far.
Ideally, a commit should be small and succinct so that your fellow team members can follow along easily.

When you make commits,
however,
they do not appear to everyone on GitHub immediately.
That is,
all the work you've been doing so far is still on your local machine.
To actually push it online,
simply press the "push" button in the GitHub GUI client.

> [!TIP]
> Let's be clear on some vocab:
> - _**Git**_ is the command line program that actually tracks the project files.
> - _**GitHub**_ is a website that can host Git repositories (jargon for "project") so that people can download them from the cloud.
> - _**The GitHub Desktop GUI**_ is a wrapper around the Git program to make it easier for people to use Git (without having to use a terminal)
and also be able to work with the GitHub website easily.
