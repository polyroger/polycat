#!/usr/bin/env pwsh

$myvar = $Env:OCIO
$on = "\\YARN\projects\pipeline\utilities\ocio\aces\OpenColorIO-Configs\aces_1.1\config.ocio"
$off = ""


if ($myvar) {
    $myvar = $off
} 
else {
    $myvar = $on
}

[System.Environment]::SetEnvironmentVariable("OCIO",$myvar,[System.EnvironmentVariableTarget]::User)


$myvar
$on
$off

Clear-Variable -Name "myvar"
Clear-Variable -Name "on"
Clear-Variable -Name "off"

$myvar
$on
$off

$env:OCIO
