Score Submission Workflow
=========================

.. mermaid:: 

   flowchart
   Push(A commit is pushed)
   PullRequest(Pull Request is opened, synchronized, or closed)

   Push --> ReadPRConfig(Read the Competitor's pr_config.json)
   PullRequest --> ReadPRConfig

