'''
param(
    [int]$Number
)
'''
[int]$Number = 177077
function IsPrime([int]$n) {
    if ($n -le 1) { return $false }
    for ($i = 2; $i -le [math]::Sqrt($n); $i++) {
        if ($n % $i -eq 0) { return $false }
    }
    return $true
}

if (IsPrime $Number) {
    Write-Output "prime"
} else {
    $lower = $Number - 1
    while (-not (IsPrime $lower)) {
        $lower--
    }
    Write-Output $lower

    $upper = $Number + 1
    while (-not (IsPrime $upper)) {
        $upper++
    }
    Write-Output $upper
}
