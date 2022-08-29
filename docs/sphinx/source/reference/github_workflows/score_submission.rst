Score Submission
================

.. mermaid:: 

   flowchart
   Push(A commit is pushed)
   PullRequest(A pull request is opened, synchronized, or closed)

   Push --> StartWorkflow(GitHub begins running this workflow)
   PullRequest --> StartWorkflow

   StartWorkflow --> StartReadPRConfigJob(GitHub begins the read-pr-config job)

   StartReadPRConfigJob --> CheckoutReadPRConfig(Checkout Competitor's pull request branch)
   CheckoutReadPRConfig --> InstallPython310ReadPRConfig(Install Python 3.10)

   InstallPython310ReadPRConfig --> ReadPRConfig(Read and validate the Competitor's pr_config.json)

   ReadPRConfig --> UploadPRConfig(Upload pr_config.json to the workflow's artifacts)
   
   UploadPRConfig -->|RUN_SCORER is true| StartScoreSubmissionJob(GitHub begins the score-submission job)
   UploadPRConfig -->|RUN_SCORER is false| TerminateWorkflow(End the workflow)

   StartScoreSubmissionJob --> CheckoutScoreSubmission(Checkout Competitor's pull request branch)
   CheckoutScoreSubmission --> InstallPython310ScoreSubmission(Install Python 3.10)
   InstallPython310ScoreSubmission --> InstallIVCurvesDependencies(Install ivcurves Python dependencies)
   InstallIVCurvesDependencies --> InstallCompetitorDependencies(Install Competitor's Python dependencies)

   InstallCompetitorDependencies --> RunCompetitorSubmission(Run the Competitor's submission)
   RunCompetitorSubmission --> ScoreCompetitorOutput(Run ivcurve's compare_curves.py to score competitor's CSV output)

   ScoreCompetitorOutput --> UploadOverallScores(Upload compare_curves.py's output to workflow's artifacts)

