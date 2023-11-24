$dir1 = "C:\Users\Owner\Videos\VideoDownloader"
$dir2 = "C:\Users\Owner\dwhelper"

$dir1Files = Get-ChildItem $dir1 -Recurse | Where-Object {!$_.PSIsContainer}
$dir2Files = Get-ChildItem $dir2 -Recurse | Where-Object {!$_.PSIsContainer}

$duplicates = @()

foreach ($file1 in $dir1Files) {
    foreach ($file2 in $dir2Files) {
        if ($file1.Name -eq $file2.Name -and $file1.Length -eq $file2.Length) {
            $duplicates += $file1.FullName
        }
    }
}

$duplicates