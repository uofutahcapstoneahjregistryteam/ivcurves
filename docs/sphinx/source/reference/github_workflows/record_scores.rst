Record Scores
=============

.. mermaid::

   flowchart
   PullRequestMerged(The Competitor's pull request is merged into ivcurves' main branch) --> StartWorkflow(GitHub begins running this workflow)

   StartWorkflow --> CheckoutIVCurvesBase(Checkout ivcurves' main branch)
   CheckoutIVCurvesBase --> InstallPython310(Install Python 3.10)
   InstallPython310 --> DownloadPRConfigFromPR(Download pr_config.json from the artifacts of the latest score-submission workflow that ran on the merged pull request)

