Record Scores
=============

.. mermaid::

   flowchart
   PullRequestMerged(The Competitor's pull request is merged into ivcurves' main branch) --> StartWorkflow(GitHub begins running this workflow)

   StartWorkflow --> StartReadPRConfigJob(Github begins the read-pr-config job)
   StartReadPRConfigJob --> CheckoutReadPRConfig(Checkout ivcurves' main branch)
   CheckoutReadPRConfig --> InstallPython310(Install Python 3.10)
   InstallPython310 --> DownloadPRConfigFromPR(Download pr_config.json from the the score-submission workflow)
   DownloadPRConfigFromPR --> ReadPRConfig(Read and validate the Competitor's pr_config.json)

   ReadPRConfig -->|RUN_SCORER is true| StartRecordScoresJob(GitHub begins the record-scores job)
   ReadPRConfig -->|RUN_SCORER is false| TerminateWorkflow(End the workflow)

   StartRecordScoresJob --> CheckoutRecordScores(Checkout ivcurves' main branch)
   CheckoutRecordScores --> InstallPython310RecordScores(Install Python 3.10)
   InstallPython310RecordScores --> DownloadOverallScores(Download overall scores from the score-submission workflow)
   DownloadOverallScores --> ValidateAndRecordScores(Validate the overall scores CSV and record the scores to the database)

   ValidateAndRecordScores --> CommitModifiedDatabase(Commit and push updated database to GitHub)

   CommitModifiedDatabase -->|RUN_SCORER is true| StartBuildSphinxDocsWorkflow(GitHub begins the build-sphinx-docs workflow)
   CommitModifiedDatabase -->|RUN_SCORER is false| TerminateWorkflowRecordScores(End the workflow)

