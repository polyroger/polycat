#!/usr/bin/env pwsh

$transcoder = "\\YARN\projects\pipeline\development\pipeline_utilities\dalies_submitter\pc_dailies_ui.py"
$conaenv = "\\YARN\projects\pipeline\utilities\conda_envs\polycat_3_production"

Unblock-File -Path $transcoder

conda activate $conaenv

python $transcoder
