.. _participating:

How to Participate
==================


Making a Submission
-------------------

Here are the steps to make your submission as a competitor.
You may as many submissions as you like, and each will be a separate entry on the leaderboard.

#. Create a fork of the ivcurves repository.
#. Create a new folder ``submissions/<your_GitHub_username>``.
   This folder will store all of the files you create.
#. Write or copy your submission's code inside this folder.
#. Create a file ``pr_config.json`` with three entries:
   
   .. code-block:: json

      {
          "RUN_SCORER": true,
          "REQUIREMENTS": "<path_to_requirements.txt>",
          "SUBMISSION_MAIN": "<path_to_submission_entrypoint.py>"
      }

   The paths of ``REQUIREMENTS`` and ``SUBMISSION_MAIN`` must be relative to your ``submissions/<your_GitHub_username>`` folder.
   For example, for a Pip requirements file located at ``submissions/<your_GitHub_username>/requirements.txt``, the path of ``REQUIREMENTS`` should be ``./requirements.txt``.
#. Push your changes to your fork.
   GitHub will automatically run your code and provide a CSV file containing your scores.
   You will see either a green check mark or red x next to your commit.
   Click on it to see your results.
#. When you are ready, and see a green check mark next to your commit, create a pull request into ``cwhanse/ivcurves/main``.
   GitHub will again automatically run and score your code.
   An ivcurves maintainer will be notified of your pull request.
#. After an ivcurves maintainer reviews and approves your pull request, it will be merged.
   GitHub will record your score in its database, and post it to the leaderboard.

Submission Workflow Diagram
---------------------------

.. mermaid::

   sequenceDiagram
       participant Competitor
       participant GitHub Actions
       participant ivcurves Maintainer

       activate Competitor
       Note over Competitor: Forks ivcurves repository.
       Note over Competitor: Creates folder submissions/<your_GitHub_username> to put their files into.
       Note over Competitor: Creates pr_config.json.
       Note over Competitor: Writes code for submission.

       Competitor->>GitHub Actions: Pushes code to fork on GitHub
       deactivate Competitor
       activate GitHub Actions
       Note over GitHub Actions: Reads pr_config.json and scores submission.
       GitHub Actions->>Competitor: Reports results with CSV of scores
       deactivate GitHub Actions

       Competitor->>GitHub Actions: Creates pull request
       activate GitHub Actions
       GitHub Actions->>ivcurves Maintainer: Notifies of pull request
       activate ivcurves Maintainer
       Note over GitHub Actions: Reads pr_config.json and scores submission code.
       GitHub Actions->>Competitor: Reports results with CSV of scores
       Note over ivcurves Maintainer: Reviews pull request.
       ivcurves Maintainer->>GitHub Actions: Merges competitor's pull request
       deactivate ivcurves Maintainer
       GitHub Actions->>Competitor: Notifies of pull request merge
       Note over GitHub Actions: Records submission's score in database.
       Note over GitHub Actions: Updates Sphinx webiste with new data.
       deactivate GitHub Actions

