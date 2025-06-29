# Virginia Tech RockSat-X 2026 Project.

- Etiquette.
  - [_**Don't Track Junk Files.**_](#dont-track-junk-files)
  - [_**Don't Track Chunky Files.**_](#dont-track-chunky-files)
- [Action Items](#action-items).
- Git Workflow.
  - [Onboarding the Git Workflow](#onboarding-the-git-workflow).
  - [Creating Tickets](#creating-tickets).
  - [Git Conflicts](#git-conflicts).

# Action Items.

- [ ] Design.
  - [ ] Aluminium/plywood mock-up of deck plate and experiment.
  - [ ] Design for easy access remove before flight (RBF) pins.
  - [ ] Design for function indicators for power functions.
  - [ ] Main material list (one system of measurement).
  - [ ] Full 3D printed payload.
  - [ ] Desgin mechanial test beds for each main actuation.
  - [ ] Finite element analysis.

- [ ] Build.
  - [ ] Integration of function indicators (lights, buzzers, etc.).
  - [ ] Install RBF inhibits and tags.
  - [ ] Locktight/hotglue/secure fasteners.

- [ ] Test.
  - [ ] Build test beds and run actuation testing.
  - [ ] Full sequence test.
  - [ ] Vibration test.
  - [ ] Summer testing preparations.
    - [ ] Full walk around inspection.
    - [ ] Procedures checksheets.
    - [ ] Personel briefing.

# Don't Track Junk Files.

When you add files for Git to track,
it will mean that other people will have access to those files when you push your work to GitHub,

_**BUT NOT ALL FILES SHOULD BE TREATED EQUAL**_.

This means you _SHOULD NOT BE PUSHING FILES OF THE FOLLOWING_:
  - ❌ Backup files.
  - ❌ Cache files.
  - ❌ Auto-generated temporary files.
  - ❌ Build artifacts.
  - ❌ Debug info.
  - ❌ Personal settings/configurations.
  - ❌ Any binary data that you do not understand.

Some examples of things that might be _OK_ to track through version control:

- ✅ Source code.
- ✅ CAD parts, assemblies, materials, and such.
- ✅ 3D models like STEP, STL, etc.

Remember,
Kind engineers are the most productive engineers.
Take some time to look at the files you are going to be pushing to GitHub.

> [!TIP]
> Let's say you opened SolidWorks and started to make a thingmajig.
> After you feel like you have reached a good checkpoint,
> you decide to save your progress so far with the GitHub Desktop GUI.
> The GUI lists all the files that it sees that aren't currently being tracked;
> things like `my_new_part.sldprt`, `my_new_thing.sldasm`, `.workspace_settings`.
>
> The first two files are obviously the thing you've been working on,
> so you should be tracking those with version control,
> but what about `.workspace_settings`?
> You opened the file in NotePad and see that it seems to keep track of stuff like your window layout and what theme you're currently using.
> Should this file be tracked with version control?
> 
> **NO!**
> This file is an example of a _user configuration_ file.
> This file is so that
> when you reopen SolidWorks again,
> it looks exactly like where you left it.
> But other people shouldn't have to care about how you like your windows and panels to be laid out in SolidWorks!
>
> The bare minimum that is needed for other people to contribute to your SolidWorks part/assembly should just be the necessary ones;
> nothing more, nothing less.

> [!IMPORTANT]
> If you're unsure whether or not something should be tracked through Git or not,
> just ask!
> 
> In the event that a junk file is accidentally added to the repository,
> this can always be cleaned up later on.
> If a file was mistaken for junk but was actually critical,
> the file can always be added later on.
>
> Remember,
> the point of this etiquette is so that we can be kind to each other and not clutter the project repository,
> very much like you wouldn't want to clutter up a guest's house.

# Don't Track Chunky Files.

When you track a file with Git,
be wary of its file size.
This doesn't really matter for certain things like source code,
where even if there were a hundred thousand lines of code in this whole project,
this would only roughly amount to `100,000 * 100 bytes = 10 megabytes` of space, assuming 100 bytes per line.
However, for things like 3D models,
especially uncompressed formats like STEP and STL,
a complicated model might be on the order of 50 megabytes or larger.
If this is the case,
see if there's a way to trim down the fat
(e.g., reducing the complexity of the STEP model by opening your favorite CAD program and hide components and then re-export).

Why?
Because you should be kind to the other people here.
When you upload chunky files,
this means when they perform a fetch on the repository,
they'll be forced to download all your chunky files.
Don't waste their time and storage if you can.

# Onboarding the Git Workflow.

First download the [GitHub Desktop GUI client](https://desktop.github.com/download/).
Go through the installation process and create your GitHub account (if needed) and sign into the GUI with it.

<p align="center"><kbd><img src="./misc/GUI_Lets_Get_Started.jpg" width="80%"></kbd></p>

Next,
clone the RSXVT2026 project using its [GitHub URL](https://github.com/RockSat-X/RSXVT2026/).

<p align="center"><kbd><img src="./misc/GUI_Cloning_Repo.jpg" width="80%"></kbd></p>

"Clone" is just Git-jargon for downloading a repository.
After Git is done downloading,
you should be greeted with the following page:

<p align="center"><kbd><img src="./misc/GUI_Fresh_Clone.jpg" width="80%"></kbd></p>

Create a text file of the form `{yourname}.md` in the `people` folder that's at the root of the project.
Go ahead and introduce yourself here to your fellow engineers.
Examples of things you can tell about yourself:

- Name (and if it's typical that people mispronunce your name, help them out here).
- Major.
- Past experience.
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

We're now almost ready to make a "commit".

> [!IMPORTANT]
> But before you make a "commit",
> it's best to make sure your copy of the repository is up-to-date.
> This is done by "fetching".
>
> <p align="center"><kbd><img src="./misc/GUI_Fetch.jpg" width="80%"></kbd></p>
>
> If there were new commits made on the RSX2026 repository since you cloned it,
> you can "pull" them to be downloaded.
>
> <p align="center"><kbd><img src="./misc/GUI_Pull.jpg" width="80%"></kbd></p>
>
> There shouldn't be any conflict between the new commits
> and the changes you've made so far,
> but if there is one,
> see [Git Conflicts](#git-conflicts).

Go ahead and press the big blue "commit" button.

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

> [!CAUTION]
> If you instead get the following warning:
>
> <p align="center"><kbd><img src="./misc/GUI_New_Commits_On_Remote.jpg" width="80%"></kbd></p>
>
> This means there were updates to the RSX2026 repository on the `main` branch
> since the time you clone the repository to your local machine
> (see [Git Conflicts](#git-conflicts)).
>
> You can learn how to resolve this conflict,
> but for the sake of onboarding,
> you can just start over by recloning the repository again
> and this time have better luck.

To get around this pull request,
we first undo our commit that we just did;
don't worry, this will not delete your work.

<p align="center"><kbd><img src="./misc/GUI_Undoing_Commit.jpg" width="80%"></kbd></p>

We then make a new branch;
this is where we'll put our commit instead.

<p align="center"><kbd><img src="./misc/GUI_Creating_New_Branch.jpg" width="80%"></kbd></p>

Give your new branch a name;
what it is doesn't really matter just as long it's unique (e.g. `{yourname}-main`).

<p align="center"><kbd><img src="./misc/GUI_Naming_New_Branch.jpg" width="80%"></kbd></p>

Select "Bring my changes to `{yournewbranch}`".

<p align="center"><kbd><img src="./misc/GUI_How_New_Branch_Is_Used.jpg" width="80%"></kbd></p>

You can now redo the commit and this time it'll be on the new branch instead of the default `main` branch.

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
Go to the "Pull requests" page of the RSX2026 repository.

<p align="center"><kbd><img src="./misc/GitHub_PR_Page.jpg" width="80%"></kbd></p>

When making a new pull request,
the difference between two branches will be shown.
Since we want to merge the branch you made into `main`,
make sure to indicate so.

<p align="center"><kbd><img src="./misc/GitHub_Creating_PR.jpg" width="80%"></kbd></p>

Once you look over the changes and it all seems like what it should be,
go ahead and give your pull request a title and, if needed, a detailed description.

<p align="center"><kbd><img src="./misc/GitHub_Describing_PR.jpg" width="80%"></kbd></p>

Once you published your pull request,
a thread is created where anyone can comment on it to create a discussion.
Additional things to be done for the pull request to help better categorize it
like labels (e.g. "bug", "documentation", etc.)
and assignees (e.g. anyone who'd be responsible for answering questions on the thread).

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
"Can you document somewhere the manufacturer number of the electronics box you used?").
If all goes well,
your reviewers will approve your commits and have them merged into `main`.

<p align="center"><kbd><img src="./misc/GitHub_PR_Merged.jpg" width="80%"></kbd></p>

The new branch you created can also be deleted if its whole purpose was for the work you just did,
but you really don't need to do this.

Your introduction file can be found in its expected location on the `main` branch now.

<p align="center"><kbd><img src="./misc/GitHub_Introduction_On_Main_Branch.jpg" width="80%"></kbd></p>

# Creating Tickets.

If you have questions about the project or things you'd like to see improved upon,
it's best to create a ticket on GitHub.
This is done through the "Issues" tab on the page of the RSX2026 repository.

<p align="center"><kbd><img src="./misc/GitHub_Issue_Page.jpg" width="80%"></kbd></p>

Give a summary of your ticket in the title field
and expand it further (if needed) in the description box.

<p align="center"><kbd><img src="./misc/GitHub_Making_Issue.jpg" width="80%"></kbd></p>

A thread will be created where anyone can contribute to the discussion.
The ticket can be assigned people and labels to better help categorize it.

<p align="center"><kbd><img src="./misc/GitHub_Issue_Thread.jpg" width="80%"></kbd></p>

When you feel like you got the answer you wanted,
you can close the ticket;
if needed,
the ticket can always be reopened later on.

<p align="center"><kbd><img src="./misc/GitHub_Closed_Issue.jpg" width="80%"></kbd></p>

You'll be able to see the tickets you've made and anyone else's for future prosperity 
on the issue page of the base repository.

<p align="center"><kbd><img src="./misc/GitHub_Issue_List.jpg" width="80%"></kbd></p>

That's pretty much the gist of using issues on GitHub.

> [!TIP]
> Discord is best reserved for virtual meetings or miscellaneous conversations.
> If you want the quickest response time,
> use Discord,
> but for the sake of bookkeeping,
> create a ticket on GitHub whenever possible.
> Over time,
> the issue tab will serve as a great reference to look back upon for your fellow engineers.

# Git Conflicts.

As you work,
you might encounter certain conflicts with other people's work.
This will happen whenever you make several commits on a branch
and so does another person independently.
As a result,
there ends up being a "divergence" between you two.

One of you will push their commits to GitHub first,
and as a result,
the other person will be the one that has an out-of-date repository.

If the files that were changed by the two of you are completely independent,
then this is often pretty easy to fix;
it is just a simple merge.

But if the two of you modified the same file
(e.g. edited the same code or tweaked the same CAD model)
then the situtation is a bit trickier.

If this situation describes you,
feel free to create a [ticket](#creating-tickets) to see how we can resolve it.
I'd put in time to explain how to do it here,
but there's a lot of things to look out for,
and besides there's plenty of resources online.

> [!TIP]
> The usage of AI in this scenario is probably good,
> since Git version control is littered with lots of weird technical terms and edge cases.
> Maybe try out GitHub's Copilot?
