#!/usr/bin/env pwsh

$transcoder = "\\YARN\projects\pipeline\development\pipeline_utilities\dalies_submitter\pc_dailies_ui.py"
$conaenv = "\\YARN\projects\pipeline\environments\polycat3"

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -NoExit -Command "& 'C:\ProgramData\Anaconda3\shell\condabin\conda-hook.ps1' ; conda activate $conaenv ; python $transcoder "
