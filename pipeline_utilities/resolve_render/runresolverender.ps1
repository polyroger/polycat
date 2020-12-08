#!/usr/bin/env pwsh

$transcoder = "C:\Users\Administrator\Documents\0_LOCAL_DEV\pipeline\polycat\pipeline_utilities\resolve_render\pc_previs_from_resolve_ui.py"
# $transcoder = "\\YARN\projects\pipeline\development\pipeline_utilities\dalies_submitter\pc_dailies_ui.py"
$conaenv = "\\YARN\projects\pipeline\environments\polycat3.6"

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -Command "& 'C:\ProgramData\Anaconda3\shell\condabin\conda-hook.ps1' ; conda activate $conaenv ; python $transcoder "
