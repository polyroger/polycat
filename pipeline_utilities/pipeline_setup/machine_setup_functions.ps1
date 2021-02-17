# sets the ocio variable
function set_ocio {

    $ocio_path = "\\YARN\projects\pipeline\utilities\ocio\aces\OpenColorIO-Configs\aces_1.1\config.ocio"
    [Environment]::SetEnvironmentVariable("OCIO", $ocio_path, 'Machine')

}

function set_remote_signed {

    Set-ExecutionPolicy RemoteSigned
    
}

set_remote_signed
set_ocio