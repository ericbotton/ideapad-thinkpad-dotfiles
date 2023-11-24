function which($name) {
    $path = ($env:Path).Split(';') | ForEach-Object { $_ + '\' + $name } | Where-Object { Test-Path $_ }
    if ($path) {
        return $path
    } else {
        return "Could not find $name in PATH"
    }
}