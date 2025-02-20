Update Scores
=============

.. mermaid::

   flowchart
   MaintainerCallsWorkflow(An ivcurves maintainer requests to update all submission scores) --> StartWorkflow(GitHub begins running this workflow)

   StartWorkflow --> StartGetPRDataJob(GitHub begins the get-pr-data job)
   StartGetPRDataJob --> CheckoutGetPRData(Checkout ivcurves' main branch)
   CheckoutGetPRData --> InstallPython310GetPRData(Install Python 3.10)
   InstallPython310GetPRData --> ReadScoresDatabasePullRequestData(Read scores_database.json and create a 2-D array with these columns: pr_number, username, and submission_datetime)

   ReadScoresDatabasePullRequestData --> StartCollectPRSubmissionsJob(For every pull request number in scores_database.json, GitHub begins the collect-pr-submissions job)
   StartCollectPRSubmissionsJob --> CheckoutCollectPRSubmissions(Checkout ivcurves' main branch with its entire commit history)
   CheckoutCollectPRSubmissions --> FindPRMergeCommit(Use GitHub CLI to find the merge commit of the pull request)
   FindPRMergeCommit --> CheckoutPRMergeCommit(Checkout the merge commit of the pull request)
   CheckoutPRMergeCommit --> RenameSubmissionFolder(Rename the pull request author's submission to pr_number--username)
   RenameSubmissionFolder --> UploadRenamedSubmissionFolder(Upload the renamed submission folder to GitHub artifacts)

   UploadRenamedSubmissionFolder -->|Every collect-pr-submissions job has completed| StartScoreAllSubmissionsJob(GitHub beings the score-all-submissions job)
   StartScoreAllSubmissionsJob --> CheckoutScoreAllSubmissions(Checkout ivcurves' main branch)
   CheckoutScoreAllSubmissions --> InstallPython310ScoreAllSubmissions(Install Python 3.10)
   InstallPython310ScoreAllSubmissions --> InstallIVCurvesDependencies(Install ivcurves Python dependencies)
   InstallIVCurvesDependencies --> DeleteAllSubmissions(Delete all submissions to make room for the ones uploaded by the collect-pr-submissions job)
   DeleteAllSubmissions --> DownloadGitHubArtifactsSubmissions(Download all submissions uploaded by the collect-pr-submissions job)
   DownloadGitHubArtifactsSubmissions --> BeginBashScriptToRunAllSubmissions(Begin a Bash script to run and score all submissions)
   BeginBashScriptToRunAllSubmissions -->|For every submission| BashCreateVirtualEnv(Bash creates a virtual environment for the submission)
   BashCreateVirtualEnv --> BashInstallSubmissionDependencies(Bash installs the submission's Python dependencies)
   BashInstallSubmissionDependencies --> BashRunSubmission(Bash runs the submission)
   BashRunSubmission --> BashScoreSubmission(Bash scores the submission)
   BashScoreSubmission --> BashValidateRecordScores(Bash validates and records the scores, marking the submission broken if validation fails)
   BashValidateRecordScores --> BashRemoveVirtualEnv(Bash removes the virtual environment for the submission)
   BashRemoveVirtualEnv --> CommitModifiedDatabase(Commit and push the udpated database to GitHub)
   CommitModifiedDatabase --> StartBuildSphinxDocksWorkflow(GitHub begins the build-sphinx-docs workflow)

